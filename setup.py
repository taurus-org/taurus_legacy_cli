#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ["taurus"]

setup_requirements = [ ]

test_requirements = [ ]

console_scripts = [
    'taurustestsuite = taurus.test.testsuite:testsuite_cmd',
    'taurusconfigbrowser = taurus_legacy_cli:taurusconfigeditor',
    'taurusplot = taurus_legacy_cli:taurusplot',
    'taurustrend = taurus_legacy_cli:taurustrend',
    'taurusform = taurus_legacy_cli:taurusFormMain',
    'tauruspanel = taurus_legacy_cli:TaurusPanelMain',
    'taurusdevicepanel = taurus_legacy_cli:TaurusDevicePanelMain',
    'taurusgui = taurus_legacy_cli:taurusgui',
    'taurusdesigner = taurus_legacy_cli:taurusdesigner',
    'taurusimage = taurus_legacy_cli:taurusImageDlgMain',
    'taurustrend2d = taurus_legacy_cli:taurusTrend2DMain',
    'taurusiconcatalog = taurus.qt.qtgui.icon.catalog:icons_cmd',
    'taurusdemo = taurus_legacy_cli:taurusdemo',
]

entry_points = {
    'console_scripts': console_scripts,
}

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
    description="taurus-legacy-cli adds back the taurus* scripts removed in taurus 4.5.4",
    install_requires=requirements,
    entry_points=entry_points,
    license="LGPLv3+",
    long_description=readme,
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
