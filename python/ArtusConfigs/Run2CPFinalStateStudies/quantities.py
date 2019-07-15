# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.quantities as Run2CPQuantities

class Quantities(Run2CPQuantities.Quantities):

	def __init__(self):
		Run2CPQuantities.Quantities.__init__(self)
		# self.quantities = set()
		# quantities = {"Quantities" : set()}
		# self.quantities = set()

	def build_quantities(self, nickname, channel):

		#super(Quantities, self).build_quantities(nickname, channel)

		print "build_quantities"
		self.quantities.update(self.recoCPFinalStateQuantities())
		if channel == "GEN":
			pass
		else:
			if re.search('(DY.?JetsToLL).*(?=(Spring16|Summer16|Summer17|Fall17))', nickname):
				self.quantities.update(self.recoCPQuantities(melaQuantities=False))
		# ************ datasets(groups, samples) common across all except mm channels are all the rest
			else:
				if not channel == "MM" and re.search('(HTo.*TauTau|H2JetsToTauTau|Higgs|JJHiggs).*(?=(Spring16|Summer16|Summer17|Fall17))', nickname):
					self.quantities.update(self.recoCPQuantities(melaQuantities=True))

	@classmethod
	def recoCPFinalStateQuantities(klass, melaQuantities=True):

		s = klass.recoCPQuantities(melaQuantities)

		s += [
			"helixQOverP_1",
			"helixLambda_1",
			"helixPhi_1",
			"helixDxy_1",
			"helixDsz_1",

			"helixQOverP_2",
			"helixLambda_2",
			"helixPhi_2",
			"helixDxy_2",
			"helixDsz_2",
			]
		return s
