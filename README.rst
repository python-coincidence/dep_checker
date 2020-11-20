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
	  - |travis| |actions_windows| |actions_macos| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/dep_checker/latest?logo=read-the-docs
	:target: https://dep_checker.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/dep_checker/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://github.com/domdfcoding/dep_checker/workflows/Linux%20Tests/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22Linux+Tests%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/dep_checker/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/dep_checker/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/dep_checker/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Test Status

.. |requires| image:: https://requires.io/github/domdfcoding/dep_checker/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/dep_checker/requirements/?branch=master
	:alt: Requirements Status

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

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/dep_checker/v0.4.1
	:target: https://github.com/domdfcoding/dep_checker/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/dep_checker
	:target: https://github.com/domdfcoding/dep_checker/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/dep_checker/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/dep_checker/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``dep_checker`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install dep_checker

.. end installation
