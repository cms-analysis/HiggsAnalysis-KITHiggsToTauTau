
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import math
import numpy

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)


def efficiency(m, m0, sigma, alpha, n, norm):
	"""
	Trigger turn-on parametrisation
	Code taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2012#ETau_MuTau_trigger_turn_on_Joshu
	Parameter m seems to mean pt
	"""
	sqrtPiOver2 = 1.2533141373
	sqrt2 = 1.4142135624
	sig = abs(sigma)
	t = (m - m0)/sig
	if alpha < 0.0: t = -t
	absAlpha = abs(alpha/sig)
	a = pow(n/absAlpha, n)*math.exp(-0.5*absAlpha*absAlpha)
	b = absAlpha - n/absAlpha
	ApproxErf = None
	arg = absAlpha / sqrt2
	if arg > 5.0: ApproxErf = 1.0
	elif arg < -5.0: ApproxErf = -1.0
	else: ApproxErf = math.erf(arg)
	leftArea = (1 + ApproxErf) * sqrtPiOver2
	rightArea = ( a * 1/pow(absAlpha - b, n-1)) / (n - 1)
	area = leftArea + rightArea
	if t <= absAlpha:
		arg = t / sqrt2
		if arg > 5.0: ApproxErf = 1.0
		elif arg < -5.0: ApproxErf = -1.0
		else: ApproxErf = math.erf(arg)
		return norm * (1 + ApproxErf) * sqrtPiOver2 / area
	else:
		return norm * (leftArea + a * (1.0/pow(t-b, n-1.0) - 1.0/pow(absAlpha - b, n-1.0)) / (1.0 - n)) / area


def fill_root_histogram(n_bins_pt, min_pt, max_pt, eta_bins_with_parameters, histogram_name):
	pt_bins = numpy.arange(min_pt, max_pt+1.1*(max_pt-min_pt)/n_bins_pt, (max_pt-min_pt)/n_bins_pt)
	eta_bins = array.array("d", [eta_bin["low"] for eta_bin in eta_bins_with_parameters]+[eta_bins_with_parameters[-1]["high"]])
	
	histogram = ROOT.TH2F(histogram_name, histogram_name, len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	histogram.GetXaxis().SetTitle("pt")
	histogram.GetYaxis().SetTitle("eta")
	
	for eta_index, eta_bin in enumerate(eta_bins_with_parameters):
		parameters = eta_bin["parameters"]
		for pt_index in xrange(n_bins_pt):
			pt = histogram.GetXaxis().GetBinCenter(pt_index+1)
			triggerEfficieny = efficiency(pt, *parameters)
			histogram.SetBinContent(pt_index+1, eta_index+1, triggerEfficieny)
			histogram.SetBinError(pt_index+1, eta_index+1, 0.0)
	
	return histogram
