=================
taurus-legacy-cli
=================


.. image:: https://img.shields.io/pypi/v/taurus_legacy_cli.svg
        :target: https://pypi.python.org/pypi/taurus_legacy_cli

.. image:: https://img.shields.io/travis/taurus-org/taurus_legacy_cli.svg
        :target: https://travis-ci.org/taurus-org/taurus_legacy_cli



taurus-legacy-cli adds back the taurus* scripts removed in taurus_ 4.5.4


* Free software: LGPLv3+


Taurus v4.5.4 `replaced the old console-scripts`_ (`taurusform`, `taurusdemo`,...)
by subcommands to a new `taurus` command which provides the same functionality.

While the CLI scripts are not strictly considered API, this change may break 
some scripts that relly on them (e.g. some automation procedures, etc.).

This project re-adds the old scripts to provide backwards-compatibility in those cases.

.. attention:: This is just a plugin to smooth the transition, but the old scripts should
   be considered deprecated and be replaced ASAP by calls to the new taurus CLI



Credits
-------

This package was created with Cookiecutter_ and the `taurus-org/cookiecutter-tauruspackage`_ template
(based on `audreyr/cookiecutter-pypackage`_).

.. _taurus: https://taurus-scada.org
.. _`replaced the old console-scripts`: https://github.com/taurus-org/taurus/pull/856
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`taurus-org/cookiecutter-taurus`: https://github.com/taurus-org/cookiecutter-taurus
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
