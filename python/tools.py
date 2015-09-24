# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import math

import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class PoissonYield(object):
	def __init__(self, root_histogram):
		error = array.array("d", [0.0])
		integral = root_histogram.IntegralAndError(1, root_histogram.GetNbinsX(), error)
		error = error[0]
		#self.poisson_yield = uncertainties.ufloat(integral, error)
		self.poisson_yield = uncertainties.ufloat(integral, math.sqrt(abs(integral)))
	
	def __call__(self):
		return self.poisson_yield

