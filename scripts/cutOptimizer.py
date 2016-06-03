#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, copy, os, sys, itertools
import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import ROOT

def make_Histogram():
	pass

def optimize(root_histogram): # axes=[x="VariableName", y="...", z="..."] maximum 3 dimensions, give list of strings with
	pass

def test_function(**kwargs):
	return 1

class CutOptimizer(object):
	def __init__(self, axisNames=[], cutHistogram=None):
		super(CutOptimizer, self).__init__()
		self.axisNames=axisNames
		self.setCutHistograms(ROOT.TH1F("CutOptimizerSig", "InputVariables", "20,-1,1"), ROOT.TH1F("CutOptimizerBkg", "InputVariables", "20,-1,1")) if cutHistogram is None else self.setCutHistograms(*cutHistogram)
		self.binValueFunction = self.SoverSqrtSplusB
		self.binTupleList = []
		self.binValueList = []

	def setCutHistograms(self, root_histogram_sig, root_histogram_bkg):
		self.cutHistogram_bkg = root_histogram_bkg
		self.cutHistogram_sig = root_histogram_sig
		self.dimension = self.cutHistogram_sig.GetDimension()
		self.dimBinsList = []
		for dim in range(self.dimension):
			if dim == 0:
				self.dimBinsList.append([x for x in range(1,self.cutHistogram_sig.GetNbinsX()+1)])
			elif dim == 1:
				self.dimBinsList.append([x for x in range(1,self.cutHistogram_sig.GetNbinsY()+1)])
			elif dim == 2:
				self.dimBinsList.append([x for x in range(1,self.cutHistogram_sig.GetNbinsZ()+1)])

	def setBinValueFunction(self, function):
		self.binValueFunction = function

	def fromBintoValue(self, binTuple):
		valueTuple = []
		for dim,dBin in enumerate(binTuple):
			if dim == 0:
				valueTuple.append(self.cutHistogram_sig.GetXaxis().GetBinLowEdge(dBin))
			elif dim == 1:
				valueTuple.append(self.cutHistogram_sig.GetYaxis().GetBinLowEdge(dBin))
			elif dim == 2:
				valueTuple.append(self.cutHistogram_sig.GetZaxis().GetBinLowEdge(dBin))
		return valueTuple

	def SoverSqrtSplusB(self,binValues,**kwargs):
		call_list = []
		for dim,dBin in enumerate(binValues):
			call_list.append(dBin)
			call_list.append(max(self.dimBinsList[dim]))
		signal = self.cutHistogram_sig.Integral(*call_list)
		bkg = self.cutHistogram_bkg.Integral(*call_list)
		if signal >= 1.0 and bkg >= 1.0:
			return 1.0*signal/(signal+bkg)**0.5
		else:
			return 0

	def optimize(self):
		for tup in itertools.product(*self.dimBinsList):
			self.binTupleList.append(tup)
			self.binValueList.append(self.binValueFunction(histogram_sig=self.cutHistogram_sig, histogram_bkg=self.cutHistogram_bkg, binValues=tup, realValues=self.fromBintoValue(tup)))
		return max(self.binValueList), self.binTupleList[self.binValueList.index(max(self.binValueList))], self.fromBintoValue(self.binTupleList[self.binValueList.index(max(self.binValueList))])

if __name__ == "__main__":
	import logging
	import Artus.Utility.logger as logger
	log = logging.getLogger(__name__)
	import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
	import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
	import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zll", "zl", "zj", "ttj", "vv", "wj", "qcd", "data"],
	                    choices=["ztt", "zll", "zl", "zj", "ttj", "vv", "wj", "qcd", "ff", "ggh", "qqh", "vh", "htt", "data"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--scale-signal", type=int, default=1,
	                    help="Scale signal (htt). Allowed values are 1, 10, 25, 100 and 250. [Default: %(default)s]")
	parser.add_argument("--ztt-from-mc", default=False, action="store_true",
	                    help="Use MC simulation to estimate ZTT. [Default: %(default)s]")
	parser.add_argument("-ff", "--fakefactor-method", choices = ["standard", "comparison"],
			help="Optional background estimation using the Fake-Factor method. [Default: %(default)s]")
	parser.add_argument("--scale-mc-only", default="1.0",
                        help="scales only MC events. [Default: %(default)s]")
	parser.add_argument("--cut-mc-only", default="1.0",
                        help="cut applied only on MC. [Default: %(default)s]")
	parser.add_argument("--project-to-lumi", default=1.0,
                        help="multiplies current lumi. 2 would mean double lumi you have right now [Default: %(default)s]")
	parser.add_argument("-c", "--channel",
	                    default="tt",
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--category", default=None,
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--x-quantity",default="pt_2",
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-y", "--y-quantity",default=None,
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-z", "--z-quantity",default=None,
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-xr", "--x-range", nargs="+", default=[0,1000],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-yr", "--y-range", nargs="+", default=[0,1000],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-zr", "--z-range", nargs="+", default=[0,1000],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]
		args.samples.remove("zl")
		args.samples.remove("zj")
	if ("zj" in args.samples or "zl" in args.samples):
		log.critical("Plot will fail: zl or zj samples given as input. Remove to continue")
		sys.exit(1)

	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	bkg_samples = [sample for sample in args.samples if sample not in ["data", "htt", "ggh", "qqh", "vh"]]
	sig_samples_raw = [sample for sample in args.samples if sample in ["htt", "ggh", "qqh", "vh"]]
	sig_samples = []
	for mass in args.higgs_masses:
		scale_str = "_%i"%args.scale_signal
		if int(args.scale_signal) == 1:
			scale_str = ""
		for sample in sig_samples_raw:
			if sample is not "htt":
				sig_samples.append(sample+"%s"%(mass))
			else:
				sig_samples.append(sample+"%s%s"%(mass, scale_str))
	binnings_settings = binnings.BinningsDict()

	category_string = None
	if args.category != None:
		if(args.mssm):
			category_string = "catHttMSSM13TeV"
		else:
			category_string = "catHtt13TeV"
		category_string = (category_string + "_{channel}_{category}").format(channel=args.channel, category=args.category)
		if args.mva:
			category_string = args.category
	config = sample_settings.get_config(
			samples=list_of_samples,
			channel=args.channel,
			category=category_string,
			higgs_masses=args.higgs_masses,
			normalise_signal_to_one_pb=False,
			ztt_from_mc=args.ztt_from_mc,
			weight="({0})".format(args.weight),
			lumi = args.lumi * 1000,
			exclude_cuts=args.exclude_cuts,
			fakefactor_method=args.fakefactor_method,
			scale_signal=args.scale_signal,
			project_to_lumi=args.project_to_lumi,
			cut_mc_only=args.cut_mc_only,
			scale_mc_only=args.scale_mc_only
	)
	config["directories"] = [args.input_dir]
	config["output_dir"] = os.path.expandvars(args.output_dir)
	config["filename"] = "CutOptimizerStorage"
	config["plot_modules"] = ["ExportRoot"]
	if "qcd" in bkg_samples:
		config["qcd_subtract_shape"] =[args.qcd_subtract_shapes]

	x_bins = [x for x in range(int(float(args.x_range[0])*100),int(float(args.x_range[1])*100)+1, int((float(args.x_range[1])-float(args.x_range[0]))*4))]
	y_bins = []
	z_bins = []
	config["x_bins"]= " ".join([str(x/100.0) for x in x_bins])
	config["x_expressions"] = [args.x_quantity]
	variables = [args.x_quantity]
	if args.y_quantity is not None:
		y_bins = [x for x in range(int(float(args.y_range[0])*100),int(float(args.y_range[1])*100)+1, int((float(args.y_range[1])-float(args.y_range[0]))*4))]
		config["y_expressions"] = [args.y_quantity]
		config["y_bins"] = [" ".join([str(x/100.0) for x in y_bins])]
		variables.append(args.y_quantity)
	if args.z_quantity is not None:
		z_bins = [x for x in range(int(float(args.z_range[0])*100),int(int(float(args.z_range[1])*100)+1), int((float(args.z_range[1])-float(args.z_range[0]))*4))]
		config["z_expressions"] = [args.z_quantity]
		config["z_bins"] = [" ".join([str(x/100.0) for x in z_bins])]
		variables.append(args.z_quantity)
	current_cuts = []
	current_max = 0
	real_values = []
	for i in range(3):
		if i == 0:
			higgsplot.HiggsPlotter(list_of_config_dicts=[config])
		else:
			b_max_index = current_cuts[0]-1
			b_min = x_bins[b_max_index-3] if b_max_index >=3 else x_bins[0]
			b_max = x_bins[b_max_index+3] if (len(x_bins) - b_max_index) >3 else x_bins[-1]
			b_min = int(b_min*100)
			b_max = int(b_max*100)
			step = (b_max-b_min)/10 if (b_max-b_min)/10 >= 1 else 1
			x_bins = [x_bins[0]]+[x/100.0 for x in range(b_min, b_max, int(step))]+[x_bins[-1]]
			config["x_bins"] = [" ".join([str(x/100.0) for x in x_bins])]
			print config["x_bins"]
			if args.y_quantity is not None:
				b_max_index = current_cuts[1]-1
				b_min = y_bins[b_max_index-3] if b_max_index >=3 else y_bins[0]
				b_max = y_bins[b_max_index+3] if (len(y_bins) - b_max_index) >3 else y_bins[-1]
				b_min = int(b_min*100)
				b_max = int(b_max*100)
				step = (b_max-b_min)/10 if (b_max-b_min)/10 >= 1 else 1
				y_bins = [y_bins[0]]+[x/100.0 for x in range(b_min, b_max, int(step))]+[y_bins[-1]]
				config["y_bins"] = [" ".join([str(x/100.0) for x in y_bins])]
				print config["y_bins"]
			if args.z_quantity is not None:
				b_max_index = current_cuts[2]-1
				b_min = z_bins[b_max_index-3] if b_max_index >=3 else z_bins[0]
				b_max = z_bins[b_max_index+3] if (len(z_bins) - b_max_index) >3 else z_bins[-1]
				b_min = int(b_min*100)
				b_max = int(b_max*100)
				step = (b_max-b_min)/10 if (b_max-b_min)/10 >= 1 else 1
				z_bins = [z_bins[0]]+[x/100.0 for x in range(b_min, b_max, int(step))]+[z_bins[-1]]
				config["z_bins"] = [" ".join([str(x/100.0) for x in z_bins])]
				print config["z_bins"]
			higgsplot.HiggsPlotter(list_of_config_dicts=[config])

		tfile = ROOT.TFile(os.path.expandvars(os.path.join(args.output_dir, "CutOptimizerStorage.root")), "READ")
		hist_list = [tfile.Get(name) for name in bkg_samples]
		htt = tfile.Get("htt125")
		bkg_hist = hist_list.pop(0)
		for hist in hist_list:
			bkg_hist.Add(bkg_hist, hist)
		opt_test = CutOptimizer(variables, [htt,bkg_hist])
		current_max, current_cuts, real_values = opt_test.optimize()
	print variables, current_max, current_cuts, real_values

