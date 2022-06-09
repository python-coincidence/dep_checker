############
dep_checker
############

.. start short_desc

**Tool to check all requirements are actually required.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/dep_checker/latest?logo=read-the-docs
	:target: https://dep_checker.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/dep_checker/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/dep_checker/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/dep_checker/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/dep_checker/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/dep_checker/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/dep_checker/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.herokuapp.com/github/domdfcoding/dep_checker/badge.svg
	:target: https://dependency-dash.herokuapp.com/github/domdfcoding/dep_checker/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/dep_checker/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/dep_checker?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/dep_checker?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/dep_checker
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/dep_checker
	:target: https://pypi.org/project/dep_checker/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dep_checker?logo=python&logoColor=white
	:target: https://pypi.org/project/dep_checker/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dep_checker
	:target: https://pypi.org/project/dep_checker/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/dep_checker
	:target: https://pypi.org/project/dep_checker/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/dep_checker
	:target: https://github.com/domdfcoding/dep_checker/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/dep_checker
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/dep_checker/v0.6.2
	:target: https://github.com/domdfcoding/dep_checker/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/dep_checker
	:target: https://github.com/domdfcoding/dep_checker/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/dep_checker
	:target: https://pypi.org/project/dep_checker/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``dep_checker`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install dep_checker

.. end installation
