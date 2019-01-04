#!/usr/bin/env python
""" Password strength and validation """

from setuptools import setup, find_packages

setup(
    name='password_strength',
    version='0.0.3-2',
    author='Mark Vartanyan',
    author_email='kolypto@gmail.com',

    url='https://github.com/kolypto/py-password-strength',
    license='BSD',
    description=__doc__,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['password', 'strength', 'policy', 'security'],

    packages=find_packages(),
    scripts=[],
    entry_points={},

    install_requires=[
        'six',
    ],
    extras_require={
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
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
