# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.input_modules.inputroot as inputroot

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.expressions as expressions


class InputRootHtt(inputroot.InputRoot):
	def __init__(self):
		super(InputRootHtt, self).__init__()
		
		self.expressions = expressions.ExpressionsDict()
		self.binnings = binnings.BinningsDict()
	
	def prepare_args(self, parser, plotData):
		super(InputRootHtt, self).prepare_args(parser, plotData)

