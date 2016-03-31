# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import math

import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties
from Artus.Utility.tools import find_common_patterns


class PoissonYield(object):
	def __init__(self, root_histogram):
		error = array.array("d", [0.0])
		integral = root_histogram.IntegralAndError(0, root_histogram.GetNbinsX()+1, error)
		error = error[0]
		#self.poisson_yield = uncertainties.ufloat(integral, error)
		self.poisson_yield = uncertainties.ufloat(integral, math.sqrt(abs(integral)))
	
	def __call__(self):
		return self.poisson_yield
	
def find_common_httpipename(s1, s2):
	string = ""
	for pattern in find_common_patterns(s1, s2)[0]:
		if pattern[0] > 0:
			string += pattern[1] if pattern[1][-2:] != "_z" else pattern[1][:-2]  
		else:
			string += "Nom" if pattern[1] in ["Up","Down","Nom"] else ""
	return string