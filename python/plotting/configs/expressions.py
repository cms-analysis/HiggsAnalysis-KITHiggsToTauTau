
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.expressions as expressions


class ExpressionsDict(expressions.ExpressionsDict):
	def __init__(self, additional_expressions=None):
		super(ExpressionsDict, self).__init__(additional_expressions=additional_expressions)
		
		# category cuts
		self.expressions_dict["cat_inclusive"] = "1.0"
		self.expressions_dict["catZtt13TeV_inclusive"] = self.expressions_dict["cat_inclusive"]
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			self.expressions_dict["catZtt13TeV_"+channel+"_inclusive"] = self.expressions_dict["catZtt13TeV_inclusive"]
		
		self.expressions_dict["cat_0jet"] = "njetspt20 < 1"
		self.expressions_dict["catZtt13TeV_0jet"] = self.expressions_dict["cat_0jet"]
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			self.expressions_dict["catZtt13TeV_"+channel+"_0jet"] = self.expressions_dict["catZtt13TeV_0jet"]
		
		self.expressions_dict["cat_1jet"] = "(njetspt20 > 0)*(njetspt20 < 2)"
		self.expressions_dict["catZtt13TeV_1jet"] = self.expressions_dict["cat_1jet"]
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			self.expressions_dict["catZtt13TeV_"+channel+"_1jet"] = self.expressions_dict["catZtt13TeV_1jet"]
		
		self.expressions_dict["cat_2jet"] = "njetspt20 > 1"
		self.expressions_dict["catZtt13TeV_2jet"] = self.expressions_dict["cat_2jet"]
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			self.expressions_dict["catZtt13TeV_"+channel+"_2jet"] = self.expressions_dict["catZtt13TeV_2jet"]
		
		replacements = {
			"0jet" : "zerojet",
			"1jet" : "onejet",
			"2jet" : "twojet",
		}
		for short_expression, long_expression in self.expressions_dict.items():
			if any([replacement in short_expression for replacement in replacements.keys()]):
				new_short_expression = short_expression
				for replacement in replacements.iteritems():
					new_short_expression = new_short_expression.replace(*replacement)
				self.expressions_dict[new_short_expression] = long_expression

