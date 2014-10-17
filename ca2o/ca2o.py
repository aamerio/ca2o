#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'

import json, time

class Generator():

    def __init__(self, inputfile, outputfile, template):
        self._inputfile = inputfile
        self._outputfile = outputfile
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

class mysqlGenerator(Generator):
    def __init__(self, inputfile, outputfile, template):
        Generator.__init__(self, inputfile, outputfile, template)

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
    def __init__(self, inputfile, outputfile, template):
        Generator.__init__(self, inputfile, outputfile, template)

    def generate(self):
        pass

def main():
    objects = []
    example_in = 'templates/sql-tblstruct.json'
    example_out = 'outputs/sql-tblstruct.sql'
    template = 'templates/sql.tmpl'
    dog = mysqlGenerator(example_in, example_out, template)
    bone = dog.do()
    

if __name__ == "__main__":
    main()
