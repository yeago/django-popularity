#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-popularity',
    version="0.2.2",
    description='A generic view- and popularity tracking pluggable for Django.',
    long_description=README,
    author='Mathijs de Bruin',
    author_email='drbob@dokterbob.net',
    url='http://github.com/dokterbob/django-popularity',
    packages=['popularity', 'popularity.templatetags'],
    include_package_data=True,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU Affero General Public License v3',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
)
