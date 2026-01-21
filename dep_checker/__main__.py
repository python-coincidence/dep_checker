#!/usr/bin/env python3
#
#  __main__.py
"""
Tool to check all requirements are actually required.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import sys
from typing import List, Optional, Set

# 3rd party
import click
import dom_toml
from consolekit import click_command
from consolekit.options import colour_option, flag_option
from consolekit.utils import abort

# this package
from dep_checker import check_imports

__all__ = ("main", )


@colour_option()
@click.option(
		"-d",
		"--work-dir",
		type=click.STRING,
		default='.',
		help="The directory to find the source of the package in. Useful with the src/ layout.",
		)
@click.option(
		"-a",
		"--allowed-unused",
		type=click.STRING,
		multiple=True,
		help="Requirements which are allowed to be unused in the source code.",
		)
@click.option(
		"--req-file",
		type=click.STRING,
		metavar="FILENAME",
		help="Parse the requirements from the given requirements file (or pyproject.toml file with --pyproject).",
		)
@flag_option(
		"-p",
		"--pyproject",
		help="Parse the requirements from 'pyproject.toml'.",
		default=False,
		)
@click.argument(
		"pkg-name",
		type=click.STRING,
		)
@click_command()
def main(
		pkg_name: str,
		allowed_unused: Optional[List[str]],
		colour: Optional[bool] = None,
		req_file: Optional[str] = None,
		work_dir: str = '.',
		pyproject: bool = False
		) -> None:
	"""
	Tool to check all requirements are actually required.
	"""

	# 3rd party
	from domdf_python_tools.paths import PathLike, PathPlus
	from shippinglabel.requirements import ComparableRequirement, parse_pyproject_dependencies, read_requirements

	if allowed_unused == ():
		allowed_unused = None

	work_dir_p = PathPlus(work_dir)

	def read_req_file(req_file: PathLike) -> Set[ComparableRequirement]:
		req_file = PathPlus(req_file)

		if not req_file.is_absolute():
			req_file = work_dir_p / req_file

		return read_requirements(req_file)[0]

	if pyproject:
		if req_file is None:
			req_file = "pyproject.toml"
		dynamic = dom_toml.load(req_file)["project"].get("dynamic", ())

		if "requirements" in dynamic:
			requirements = read_requirements("requirements.txt")[0]
		else:
			requirements = parse_pyproject_dependencies(req_file, flavour="pep621")

	else:
		if req_file is None:
			req_file = "requirements.txt"

		requirements = read_req_file(req_file)

	try:
		ret = check_imports(
				pkg_name,
				*requirements,
				allowed_unused=allowed_unused,
				colour=colour,
				work_dir=work_dir_p,
				)
		sys.exit(ret)
	except FileNotFoundError as e:
		raise abort(str(e))


if __name__ == "__main__":
	sys.exit(main())
