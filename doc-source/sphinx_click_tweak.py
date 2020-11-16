# Based on https://github.com/click-contrib/sphinx-click
# Copyright (c) 2017 Stephen Finucane http://that.guru/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# stdlib
import warnings

# 3rd party
import click
from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.util.docutils import SphinxDirective
from sphinx_click.ext import CLICK_VERSION, NESTED_FULL, NESTED_SHORT, ClickDirective, _format_command
from sphinx_toolbox.utils import Purger

click_purger = Purger("all_click")


class NoHeadingClickDirective(SphinxDirective):

	has_content = False
	required_arguments = 1
	option_spec = ClickDirective.option_spec

	def _generate_nodes(self, name, command, parent, nested, commands=None):
		"""Generate the relevant Sphinx nodes.

		Format a `click.Group` or `click.Command`.

		:param name: Name of command, as used on the command line
		:param command: Instance of `click.Group` or `click.Command`
		:param parent: Instance of `click.Context`, or None
		:param nested: The granularity of subcommand details.
		:param commands: Display only listed commands or skip the section if empty

		:returns: A list of nested docutils nodes
		"""
		ctx = click.Context(command, info_name=name, parent=parent)

		if CLICK_VERSION >= (7, 0) and command.hidden:
			return []

		targetid = f'click-{self.env.new_serialno("click"):d}'
		targetnode = nodes.target('', '', ids=[targetid])

		content = []

		# Summary
		lines = _format_command(ctx, nested, commands)
		for line in lines:
			content.append(line)

		view = ViewList(content)

		click_node = nodes.paragraph(rawsource='\n'.join(content))
		self.state.nested_parse(view, self.content_offset, click_node)  # type: ignore

		click_purger.add_node(self.env, click_node, targetnode, self.lineno)

		return [targetnode, click_node]

	def run(self):
		command = ClickDirective._load_module(self, self.arguments[0])

		if "prog" not in self.options:
			raise self.error(":prog: must be specified")

		prog_name = self.options.get("prog")
		show_nested = "show-nested" in self.options
		nested = self.options.get("nested")

		if show_nested:
			if nested:
				raise self.error("':nested:' and ':show-nested:' are mutually exclusive")
			else:
				warnings.warn(
						"':show-nested:' is deprecated; use ':nested: full'",
						DeprecationWarning,
						)
				nested = NESTED_FULL if show_nested else NESTED_SHORT

		commands = self.options.get("commands")

		return self._generate_nodes(prog_name, command, None, nested, commands)


def setup(app):
	app.add_directive("click", NoHeadingClickDirective)
	app.connect("env-purge-doc", click_purger.purge_nodes)
