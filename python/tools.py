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
		dims = root_histogram.GetDimension()
		integral_ranges=[]
		for dim in range(dims):
			if dim==0:
				integral_ranges.append(0)
				integral_ranges.append(root_histogram.GetNbinsX()+1)
			elif dim==1:
				integral_ranges.append(0)
				integral_ranges.append(root_histogram.GetNbinsY()+1)
			elif dim==2:
				integral_ranges.append(0)
				integral_ranges.append(root_histogram.GetNbinsZ()+1)
		integral_ranges.append(error)
		integral = root_histogram.IntegralAndError(*integral_ranges)
		error = error[0]
		#self.poisson_yield = uncertainties.ufloat(integral, error)
		self.poisson_yield = uncertainties.ufloat(integral, math.sqrt(abs(integral)))

	def __call__(self):
		return self.poisson_yield
