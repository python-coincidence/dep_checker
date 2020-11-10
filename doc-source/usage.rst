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

.. click:: dep_checker.__main__:cli
	:prog: dep-checker
