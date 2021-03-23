=======
Usage
=======

Configuration
-----------------

| ``dep-checker`` can be configured via the ``[tool.dep_checker]`` table of ``pyproject.toml``.
| The configuration can also be placed in the ``[dep_checker]`` section of ``tox.ini`` or ``setup.cfg``.

|

.. versionchanged:: 0.5.0

	Added support for ``pyproject.toml``


.. confval:: allowed_unused

	List of requirements which are allowed to be unused in the source code.

	**Examples:**

	.. code-block:: TOML

		# pyproject.toml
		[tool.dep_checker]
		allowed_unused = ["pytest", "sphinx"]


	.. code-block:: ini

		# tox.ini / setup.cfg
		[dep_checker]
		allowed_unused = pytest, sphinx


.. confval:: name_mapping

	Mapping of requirement names (e.g. "biopython") to the names of packages they provide (e.g. "Bio").

	.. versionadded:: 0.4.1

	**Examples:**

	.. code-block:: TOML

		# pyproject.toml
		[tool.dep_checker.name_mapping]
		biopython = "Bio"


	.. code-block:: ini

		# tox.ini / setup.cfg
		[dep_checker]
		name_mapping =
			biopython = Bio


.. confval:: namespace_packages

	List of namespace packages, e.g. ``ruamel.yaml``.
	This currently only handles imports in the form
	``import namespace.package`` or
	``from namespace.package import object``,
	but not ``from namespace import package``.

	.. versionadded:: 0.4.1

	**Examples:**

	.. code-block:: TOML

		# pyproject.toml
		[tool.dep_checker]
		namespace_packages = ["ruamel.yaml", "jaraco.docker"]


	.. code-block:: ini

		# tox.ini / setup.cfg
		[dep_checker]
		namespace_packages = ruamel.yaml, jaraco.docker


Ignoring imports that aren't listed as requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To ignore lines where packages are imported, but aren't listed in ``requirements.txt``, use ``# nodep``.

E.g.:

.. code-block:: python

	import pytest  # nodep


.. versionadded:: 0.4.1


dep-checker
-----------------

.. click:: dep_checker.__main__:main
	:prog: dep-checker


As a ``pre-commit`` hook
----------------------------

``dep-checker`` can also be used as a `pre-commit <https://pre-commit.com/>`_ hook.
To do so, add the following to your
`.pre-commit-config.yaml <https://pre-commit.com/#2-add-a-pre-commit-configuration>`_ file:

.. pre-commit::
	:rev: 0.6.0
	:hooks: dep_checker
	:args: <PKG_NAME>

``<PKG_NAME>`` should be replaced with the name of the package to check, e.g. ``consolekit``:

.. pre-commit::
	:rev: 0.6.0
	:hooks: dep_checker
	:args: consolekit
