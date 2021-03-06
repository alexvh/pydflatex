#!/usr/bin/env python

import subprocess
import datetime
import os

from processor import Processor, LaTeXError

class Typesetter(Processor):
	"""
	Typeset a TeX file.
	Options:
		- halt_on_errors
		- xetex
	"""

	defaults = Processor.defaults.copy()
	defaults.update({
			'cmds': '',
			'halt_on_errors': True,
			'xetex': False,
			})

	def engine(self):
		return ['pdflatex','xelatex'][self.options['xetex']]

	def arguments(self):
		"""
		Arguments to the (pdf|xe)latex command.
		"""
		args = [self.engine(),
				'-8bit',
				'-no-mktex=pk',
				'-interaction=batchmode',
				'-recorder',
				]
		if self.options['halt_on_errors']:
			args.insert(-1, '-halt-on-error')
		return args

	def typeset(self, full_path, ):
		"""
		Typeset one given file.
		"""
		# make sure that the file exists
		if not os.path.exists(full_path):
			raise LaTeXError('File {0} not found'.format(full_path))
		# run pdflatex
		now = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
		self.logger.message("\t[{now}] {engine} {file}".format(engine=self.engine(), file=full_path, now=now))
		arguments = self.arguments()
		if self.options['cmds']:
			# append cmds and then \input file name
			full_cmds = "{cmds}\input{{{file}}}".format(cmds=self.options['cmds'], file=full_path)
			arguments.append(full_cmds)
		else:
			# append file name
			arguments.append(full_path)
		self.logger.debug("\n"+" ".join(arguments)+"\n")
		output = subprocess.Popen(arguments, stdout=subprocess.PIPE).communicate()[0]
		self.logger.message(output.splitlines()[0])


