#!/usr/bin/env python
""" Password strength and validation """

from setuptools import setup, find_packages

setup(
    name='password_strength',
    version='0.0.1-1',
    author='Mark Vartanyan',
    author_email='kolypto@gmail.com',

    url='https://github.com/kolypto/py-password-strength',
    license='BSD',
    description=__doc__,
    long_description=open('README.rst').read(),
    keywords=['password', 'strength', 'policy', 'security'],

    packages=find_packages(),
    scripts=[],
    entry_points={},

    install_requires=[
    ],
    extras_require={
        '_dev': ['wheel', 'nose', 'exdoc', 'j2cli' ],
    },
    include_package_data=True,
    test_suite='nose.collector',

    platforms='any',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
