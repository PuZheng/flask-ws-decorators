# -*- coding: UTF-8 -*-

from distutils.core import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys

NAME = u"flask-ws-decorators"
PACKAGE = u"flask_ws_decorators"
DESCRIPTION = ""
AUTHOR = "xiechao"
AUTHOR_EMAIL = "xiechao06@gmail.com"
URL = "https://github.com/PuZheng/flask-ws-decorators"
DOC = "decorators for web services"
VERSION = '0.1'
LICENSE = 'MIT'


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)

install_requires = ['flask']

setup(
    name=NAME,
    version=VERSION,
    long_description=DOC,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    install_requires=install_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framwork :: Flask',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
