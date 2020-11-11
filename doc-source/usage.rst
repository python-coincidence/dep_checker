=======
Usage
=======

Configuration
-----------------

``dep-checker`` can be configured via ``tox.ini`` or ``setup.cfg``
In either case options must be placed in the ``[dep_checker]`` section.

.. confval:: allowed_unused

	List of requirements which are allowed to be unused in the source code.


.. confval:: name_mapping

	Mapping of requirement names (e.g. "biopython") to the names of packages they provide (e.g. "Bio").

	.. versionadded:: 0.2.0

	**Example:**

	.. code-block:: ini

		[dep_checker]
		name_mapping =
			biopython = Bio


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
	:rev: 0.1.2
	:hooks: dep_checker
	:args: <PKG_NAME>

``<PKG_NAME>`` should be replaced with the name of the package to check, e.g. ``consolekit``.