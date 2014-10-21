#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'

import json, time


class Generator():

    def __init__(self, inputfile, template):
        self._inputfile = inputfile
        self._outputfile = "outputs/sample.txt"
        self._template = template

    def parseJSON(self):
        d = {}
        with open(self._inputfile) as json_data:
            d = json.loads(json_data.read())
        json_data.close()
        return d

    def readTemplate(self):
        with open (self._template, "r") as template_file:
            tmpl=template_file.read()
        return tmpl

    def generate(self, contents):
        with open(self._outputfile, "a+") as destination_file:
            destination_file.write('\n%s' % contents)

    def prepare_keys_values(self, partial, template, separator):
        prepare = []
        for l in partial:
            elements = ""
            for k in l:
                elements = "%s %s %s \"%s\"" % (elements, k, separator, l[k])
            prepare.append(template.replace("#", elements))
        return prepare

    def prepare_list(self, partial, template):
        prepare = []
        elements = ""
        for l in partial:
            prepare.append(template.replace("#", l))
        return prepare


class mysqlGenerator(Generator):
    def __init__(self, inputfile, template):
        Generator.__init__(self, inputfile, template)

    def do(self):
        data = self.parseJSON()
        tmpl = self.readTemplate()
        body = '/* CA2O %s script created %s */\n' % (self._outputfile, time.strftime("%Y-%m-%d %H:%M:%S"))
        for tables in data['tables']:
            for table in tables:
                prepare_string = tmpl.replace('[cur_table]', table)
                prepare_columns = []
                prepare_fields = []
                prepare_input = []
                prepare_sql_insert =[]
                primary = ""
                for fields in tables[table]:
                    for field in fields:
                        prepare_columns.append(self.field_gen(field, fields[field]))
                        prepare_fields.append(field)
                        prepare_input.append(self.field_gen(field, fields[field], 'IN '))
                        prepare_sql_insert.append('in_%s' % field) 
                        if 'identity' in fields[field]:
                            primary = 'PRIMARY KEY (%s)' % field
                prepare_columns.append(primary)
                prepare_string = prepare_string.replace('[List_of_attributes_as_input_params]', ',\n'.join(prepare_input))
                prepare_string = prepare_string.replace('[List_of_attributes_as_SQL_insert_params]', ',\n'.join(prepare_sql_insert))
                prepare_string = prepare_string.replace('[List_of_fields]', ',\n'.join(prepare_fields))
                prepare_string = prepare_string.replace('[List_of_columns]', ',\n'.join(prepare_columns))
                body = "%s\n%s" % (body, prepare_string)
        self.generate(body)

    def field_gen(self, fname, params, prefix=''):
        sql_line = ""
        if (params['type'] == "varchar"):
                sql_line = '%s%s %s(%s)' % (prefix, fname, params['type'], params['length'])
        else:
            sql_line = '%s%s %s' % (prefix, fname, params['type'])
        if 'identity' in params and prefix == '' :
            sql_line += ' AUTO_INCREMENT NOT NULL'
        return sql_line

class phpGenerator(Generator):
    def __init__(self, inputfile, template):
        Generator.__init__(self, inputfile, template)

    def do(self):
        data = self.parseJSON()
        tmpl = self.readTemplate()
        output = data["params"]["output"] if "output" in data["params"] else self._outputfile
        pathcss = data["params"]["path-css"] if "path-css" in data["params"] else ""
        body = "test php template (%s) %s\n" % (output, time.strftime("%Y-%m-%d %H:%M:%S"))
        tmpl = tmpl.replace("[HEAD-META]", "\n".join(self.prepare_keys_values(data["content"]["HEAD-META"], "    <meta #>", "=")))
        tmpl = tmpl.replace("[TITLE]", data["content"]["TITLE"])
        template_css = "    <link href=\"%s#\" rel=\"stylesheet\" type=\"text/css\">" % pathcss
        tmpl = tmpl.replace("[CSS]", "\n".join(self.prepare_list(data["content"]["CSS"]["list"], template_css)))
        template_js = "    <script type=\"text/javascript\" src=\"#\" ></script>"
        if data["content"]["CDN"]["default"] == "true":
            tmpl = tmpl.replace("[CDN]", "\n".join(self.prepare_list(data["content"]["CDN"]["list"], template_js)))
        else:
            tmpl = tmpl.replace("[CDN]", "")
        tmpl = tmpl.replace("[SCRIPT]", "\n".join(self.prepare_list(data["content"]["SCRIPT"]["list"], template_js)))
        tmpl = tmpl.replace("[BODY-HEADER]", "\n".join(self.prepare_keys_values(data["content"]["BODY-HEADER"], "#", "=")))
        self.generate(tmpl)

def main():
    objects = []
    """ sample sql """
    #example_in = 'templates/sql-tblstruct.json'
    #example_out = 'outputs/sql-tblstruct.sql'
    #template = 'templates/sql.tmpl'
    #dog = mysqlGenerator(example_in, example_out, template)
    """ sample php """
    example_in = 'templates/php-head.json'
    template = 'templates/php-head.tmpl'
    dog = phpGenerator(example_in, template)
   

    bone = dog.do()
    

if __name__ == "__main__":
    main()
