
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import decimal
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
	
	# there are parametrisations that require more precision then float.
	m = decimal.Decimal(m)
	m0 = decimal.Decimal(m0)
	sigma = decimal.Decimal(sigma)
	alpha = decimal.Decimal(alpha)
	n = decimal.Decimal(n)
	norm = decimal.Decimal(norm)
	
	sqrtPiOver2 = decimal.Decimal(1.2533141373)
	sqrt2 = decimal.Decimal(1.4142135624)
	sig = abs(sigma)
	t = (m - m0)/sig
	if alpha < 0.0: t = -t
	absAlpha = abs(alpha/sig)
	a = pow(n/absAlpha, n)*decimal.Decimal(math.exp(decimal.Decimal(-0.5)*absAlpha*absAlpha))
	b = absAlpha - n/absAlpha
	ApproxErf = None
	arg = absAlpha / sqrt2
	if arg > 5.0: ApproxErf = decimal.Decimal(1.0)
	elif arg < -5.0: ApproxErf = decimal.Decimal(-1.0)
	else: ApproxErf = decimal.Decimal(math.erf(arg))
	leftArea = (decimal.Decimal(1.0) + ApproxErf) * sqrtPiOver2
	rightArea = ( a * decimal.Decimal(1.0)/pow(absAlpha - b, n-decimal.Decimal(1.0))) / (n - decimal.Decimal(1.0))
	area = leftArea + rightArea
	if t <= absAlpha:
		arg = t / sqrt2
		if arg > 5.0: ApproxErf = decimal.Decimal(1.0)
		elif arg < -5.0: ApproxErf = decimal.Decimal(-1.0)
		else: ApproxErf = decimal.Decimal(math.erf(arg))
		return norm * (decimal.Decimal(1) + ApproxErf) * sqrtPiOver2 / area
	else:
		return norm * (leftArea + a * (decimal.Decimal(1.0)/pow(t-b, n-decimal.Decimal(1.0)) - decimal.Decimal(1.0)/pow(absAlpha - b, n-decimal.Decimal(1.0))) / (decimal.Decimal(1.0) - n)) / area


def fill_root_histogram(n_bins_pt, min_pt, max_pt, eta_bins_with_parameters, histogram_name):
	pt_bins = numpy.arange(min_pt, max_pt+1.1*(max_pt-min_pt)/n_bins_pt, (max_pt-min_pt)/n_bins_pt)
	eta_bins = array.array("d", [eta_bin[0] for eta_bin in eta_bins_with_parameters]+[eta_bins_with_parameters[-1][1]])
	
	histogram = ROOT.TH2F(histogram_name, histogram_name, len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	histogram.GetXaxis().SetTitle("pt")
	histogram.GetYaxis().SetTitle("eta")
	
	for eta_index, eta_bin in enumerate(eta_bins_with_parameters):
		parameters = eta_bin[2]
		for pt_bin in xrange(n_bins_pt+3):
			pt = histogram.GetXaxis().GetBinLowEdge(pt_bin)
			triggerEfficieny = efficiency(pt, *parameters)
			histogram.SetBinContent(pt_bin, eta_index+1, triggerEfficieny)
			histogram.SetBinError(pt_bin, eta_index+1, 0.0)
	
	return histogram


# this method seems to be even more imprecise than histograms
def fill_root_function(n_bins_pt, min_pt, max_pt, eta_bins_with_parameters, function_name):
	min_eta = min([eta_bin[0] for eta_bin in eta_bins_with_parameters])
	max_eta = max([eta_bin[1] for eta_bin in eta_bins_with_parameters])
	
	def function(x):
		pt = x[0] if x[0] <= max_pt else max_pt
		eta = x[1]
		if eta < min_eta:
			eta = 0.99 * min_eta
		if eta > max_eta:
			eta = 0.99 * max_eta
		for eta_bin_with_parameters in eta_bins_with_parameters:
			if eta >= eta_bin_with_parameters[0] and eta < eta_bin_with_parameters[1]:
				return efficiency(pt, *(eta_bin_with_parameters[2]))
		return 1.0
	
	return ROOT.TF2(function_name, function, min_pt, max_pt, min_eta, max_eta, 0)

