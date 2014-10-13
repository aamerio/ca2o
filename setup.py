# see http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
# https://github.com/audreyr/cookiecutter-pypackage
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import ca2o

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='ca2o',
    version=ca2o.__version__,
    url='http://github.com//aamerio/ca2o/',
    license='Apache Software License',
    author='Alberto Amerio',
    tests_require=['pytest'],
    install_requires=[
                    ],
    cmdclass={'test': PyTest},
    author_email='alberto.amerio@gmail.com',
    description='Code Generator',
    long_description=long_description,
    packages=['ca2o'],
    include_package_data=True,
    platforms='any',
    test_suite='ca2o.test.test_ca2o',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - start',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)