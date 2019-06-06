#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Taurus Community",
    author_email='tauruslib-devel@lists.sourceforge.net',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="taurus-legacy-cli adds back the taurus* scripts removed in taurus 4.5",
    install_requires=requirements,
    license="LGPLv3+",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='taurus_legacy_cli',
    name='taurus_legacy_cli',
    packages=find_packages(include=['taurus_legacy_cli']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/taurus-org/taurus_legacy_cli',
    version='0.1.0',
    zip_safe=False,
)
