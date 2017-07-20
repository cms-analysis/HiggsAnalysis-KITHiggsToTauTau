#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics

samples_dict = {
		'et' : [
			("toppt",["ttj",'ttt','ttjj',"wj","qcd"]),
			("taues1prong0pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taues1prong1pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taues3prong0pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("etaues1prong0pi", ["zl","wj","qcd"]),
			("etaues1prong1pi", ["zl","wj","qcd"]),
			("taupt",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("zpt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptes",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat0pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat40pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat80pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptttbar",["ztt","zll","zj","zl","wj","qcd"]),
			("wfake",['ztt','zll','zl','zj','ttj','ttt','ttjj','vv','vvt','vvj','wj','qcd','ggh','bbh']),
			('nominal',['ztt','zll','zl','zj','ttj','ttt','ttjj','vv','vvt','vvj','wj','qcd','ggh','bbh'])
		],
		'mt' : [
			("toppt",["ttj",'ttt','ttjj',"wj","qcd"]),
			("taues1prong0pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taues1prong1pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taues3prong0pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taupt",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("zpt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptes",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat0pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat40pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat80pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptttbar",["ztt","zll","zj","zl","wj","qcd"]),
			("wfake",['ztt','zll','zl','zj','ttj','ttt','ttjj','vv','vvt','vvj','wj','qcd','ggh','bbh']),
			('nominal',['ztt','zll','zl','zj','ttj','ttt','ttjj','vv','vvt','vvj','wj','qcd','ggh','bbh'])
		],
		'tt' : [
			("toppt",["ttj",'ttt','ttjj',"wj","qcd"]),
			("taues1prong0pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taues1prong1pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taues3prong0pi",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("taupt",["ztt","ttt", "vvt","wj","qcd","ggh","bbh"]),
			("zpt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptes",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat0pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat40pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptstat80pt",["ztt","zll","zj","zl","wj","qcd"]),
			("zptttbar",["ztt","zll","zj","zl","wj","qcd"]),
			("wfake",['ztt','zll','zl','zj','ttj','ttt','ttjj','vv','vvt','vvj','wj','qcd','ggh','bbh']),
			('nominal',['ztt','zll','zl','zj','ttj','ttt','ttjj','vv','vvt','vvj','wj','qcd','ggh','bbh'])
		],
		'em' : [
			("toppt",["ttj"]),
			("zpt",["ztt","zll"]),
			("zptes",["ztt","zll"]),
			("zptstat0pt",["ztt","zll"]),
			("zptstat40pt",["ztt","zll"]),
			("zptstat80pt",["ztt","zll"]),
			("zptttbar",["ztt","zll"]),
			('nominal',['ztt','zll','ttj','vv','wj','qcd','ggh','bbh']),
			('jec',['ttj','vv','wj','zll','ztt','ggh','bbh']),#done??
			("elees",["ttj","vv","wj","zll","ztt","ggh","bbh"]),#done
			("muones",["ttj","vv","wj","zll","ztt","ggh","bbh"]),#done??
			("metesone",["wj","zll","ztt","ggh","bbh"]),#
			("metestwo",["ttj","vv"]),#
			("efake",["vv","wj","zll"]),#done
			("mufake",["vv","wj","zll"])#done
		],
		'mm' : [
			("toppt",["ttj","wj","qcd"]),
			("zpt",["ztt","zll","wj","qcd"]),
			("wfake",['ztt','zll','ttj','vv','wj','qcd']),
			('nominal',['ztt','zll','ttj','vv','wj','qcd'])
		]
	}
shapes = {
	"btag" : "CMS_eff_b_13TeV",
	"mistag" :"CMS_fake_b_13TeV",
	"metrecoilscale" : "CMS_htt_boson_scale_met_13TeV",
	"metrecoilreso" :"CMS_htt_boson_reso_met_13TeV",
	"metjeten" : "CMS_jet_energy_met_unc_13TeV",
	"metunclustereden" :"CMS_unclustered_energy_met_unc_13TeV",
	"jec" : "CMS_scale_j_13TeV",
	"toppt" : "CMS_htt_ttbarShape_13TeV",
	"taupt" : "CMS_eff_t_mssmHigh_{CHANNEL}_13TeV",
	"taues" : "CMS_scale_t_{CHANNEL}_13TeV",
	"taues1prong0pi" : "CMS_scale_t_1prong0pi0_13TeV",
	"taues1prong1pi" : "CMS_scale_t_1prong1pi0_13TeV",
	"taues3prong0pi" : "CMS_scale_t_3prong0pi0_13TeV",
	"etaues1prong0pi" : "CMS_scale_t_efake_1prong0pi0_13TeV",
	"etaues1prong1pi" : "CMS_scale_t_efake_1prong1pi0_13TeV",
	"zpt" : "CMS_htt_dyShape_13TeV",
	"zptes" : "CMS_htt_dyShape_scale_m_13TeV",
	"zptstat0pt" : "CMS_htt_dyShape_stat_m400pt0_13TeV",
	"zptstat40pt" : "CMS_htt_dyShape_stat_m400pt40_13TeV",
	"zptstat80pt" : "CMS_htt_dyShape_stat_m400pt80_13TeV",
	"zptttbar" : "CMS_htt_dyShape_tjXsec_13TeV",
	"wfake" : "CMS_htt_wFakeShape_13TeV",
	"ff_qcd_syst" : "norm_ff_qcd_{CHANNEL}_syst",
	"ff_qcd_dm0_njet0_stat" : "norm_ff_qcd_dm0_njet0_{CHANNEL}_stat",
	"ff_qcd_dm0_njet1_stat" : "norm_ff_qcd_dm0_njet1_{CHANNEL}_stat",
	"ff_qcd_dm1_njet0_stat" : "norm_ff_qcd_dm1_njet0_{CHANNEL}_stat",
	"ff_qcd_dm1_njet1_stat" : "norm_ff_qcd_dm1_njet1_{CHANNEL}_stat",
	"ff_w_syst" : "norm_ff_w_syst",
	"ff_w_dm0_njet0_stat" : "norm_ff_w_dm0_njet0_{CHANNEL}_stat",
	"ff_w_dm0_njet1_stat" : "norm_ff_w_dm0_njet1_{CHANNEL}_stat",
	"ff_w_dm1_njet0_stat" : "norm_ff_w_dm1_njet0_{CHANNEL}_stat",
	"ff_w_dm1_njet1_stat" : "norm_ff_w_dm1_njet1_{CHANNEL}_stat",
	"ff_tt_syst" : "norm_ff_tt_syst",
	"ff_tt_dm0_njet0_stat" : "norm_ff_tt_dm0_njet0_stat",
	"ff_tt_dm0_njet1_stat" : "norm_ff_tt_dm0_njet1_stat",
	"ff_tt_dm1_njet0_stat" : "norm_ff_tt_dm1_njet0_stat",
	"ff_tt_dm1_njet1_stat" : "norm_ff_tt_dm1_njet1_stat",
	"ff_w_syst_tt" : "norm_ff_w_{CHANNEL}_syst",
	"ff_tt_syst_tt" : "norm_ff_tt_{CHANNEL}_syst",
	"ff_qcd_syst_tt" : "norm_ff_qcd_{CHANNEL}_syst",
	"ff_qcd_dm0_njet0_stat_tt" : "norm_ff_qcd_dm0_njet0_{CHANNEL}_stat",
	"ff_qcd_dm0_njet1_stat_tt" : "norm_ff_qcd_dm0_njet1_{CHANNEL}_stat",
	"ff_qcd_dm1_njet0_stat_tt" : "norm_ff_qcd_dm1_njet0_{CHANNEL}_stat",
	"ff_qcd_dm1_njet1_stat_tt" : "norm_ff_qcd_dm1_njet1_{CHANNEL}_stat",
	"ff_dy_frac" : "norm_ff_dy_frac_{CHANNEL}_syst",
	"ff_w_frac" : "norm_ff_w_frac_{CHANNEL}_syst",
	"ff_tt_frac" : "norm_ff_tt_frac_{CHANNEL}_syst",
	"elees" : "CMS_scale_e_{CHANNEL}_13TeV",
	"muones" : "CMS_scale_m_{CHANNEL}_13TeV",
	"metesone" : "CMS_scale_met_13TeV",
	"metestwo" : "CMS_scale_met_13TeV",
	"efake" : "CMS_htt_{CHANNEL}_eFake_13TeV",
	"mufake" : "CMS_htt_{CHANNEL}_muFake_13TeV"
	}
shapes_weight_dict = {
		"btag" : ("1.0", "1.0"),
		"mistag" : ("1.0", "1.0"),
		"metrecoilscale" : ("1.0", "1.0"),
		"metrecoilreso" : ("1.0", "1.0"),
		"metjeten" : ("1.0", "1.0"),
		"metunclustereden" : ("1.0", "1.0"),
		"jec" : ("1.0", "1.0"),
		"toppt" : ("1.0/topPtReweightWeight","topPtReweightWeight"),
		"zpt" : ("1.0/zPtReweightWeight","zPtReweightWeight"),
		"zptes" : ("zPtWeightEsDown/zPtReweightWeight","zPtWeightEsUp/zPtReweightWeight"),
		"zptstat0pt" : ("zPtWeightStatPt0Down/zPtReweightWeight","zPtWeightStatPt0Up/zPtReweightWeight"),
		"zptstat40pt" : ("zPtWeightStatPt40Down/zPtReweightWeight","zPtWeightStatPt40Up/zPtReweightWeight"),
		"zptstat80pt" : ("zPtWeightStatPt80Down/zPtReweightWeight","zPtWeightStatPt80Up/zPtReweightWeight"),
		"zptttbar" : ("zPtWeightTTbarDown/zPtReweightWeight","zPtWeightTTbarUp/zPtReweightWeight"),
		"taupt" : ("max(0,(1-0.0005*had_gen_match_pT_1)*(1-0.0005*had_gen_match_pT_2))", "(1+0.00005*had_gen_match_pT_1)*(1+0.00005*had_gen_match_pT_2)"),
		"taues" : ("1.0", "1.0"),
		"taues1prong0pi" : ("1.0", "1.0"),
		"taues1prong1pi" : ("1.0", "1.0"),
		"taues3prong0pi" : ("1.0", "1.0"),
		"etaues1prong0pi" : ("1.0", "1.0"),
		"etaues1prong1pi" : ("1.0", "1.0"),
		"wfake" : ("((gen_match_1 != 6) + (gen_match_1 == 6)*(1-0.002*pt_1))*((gen_match_2 != 6) + (gen_match_2 == 6)*(1-0.002*pt_2))", "((gen_match_1 != 6) + (gen_match_1 == 6)*(1+0.002*pt_1))*((gen_match_2 != 6) + (gen_match_2 == 6)*(1+0.002*pt_2))"),
		"ff_qcd_syst" : ("jetToTauFakeWeight_qcd_syst_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_syst_up/jetToTauFakeWeight_comb"),
		"ff_qcd_dm0_njet0_stat" : ("jetToTauFakeWeight_qcd_dm0_njet0_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_dm0_njet0_stat_up/jetToTauFakeWeight_comb"),
		"ff_qcd_dm0_njet1_stat" : ("jetToTauFakeWeight_qcd_dm0_njet1_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_dm0_njet1_stat_up/jetToTauFakeWeight_comb"),
		"ff_qcd_dm1_njet0_stat" : ("jetToTauFakeWeight_qcd_dm1_njet0_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_dm1_njet0_stat_up/jetToTauFakeWeight_comb"),
		"ff_qcd_dm1_njet1_stat" : ("jetToTauFakeWeight_qcd_dm1_njet1_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_dm1_njet1_stat_up/jetToTauFakeWeight_comb"),
		"ff_w_syst" : ("jetToTauFakeWeight_w_syst_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_syst_up/jetToTauFakeWeight_comb"),
		"ff_w_dm0_njet0_stat" : ("jetToTauFakeWeight_w_dm0_njet0_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_dm0_njet0_stat_up/jetToTauFakeWeight_comb"),
		"ff_w_dm0_njet1_stat" : ("jetToTauFakeWeight_w_dm0_njet1_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_dm0_njet1_stat_up/jetToTauFakeWeight_comb"),
		"ff_w_dm1_njet0_stat" : ("jetToTauFakeWeight_w_dm1_njet0_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_dm1_njet0_stat_up/jetToTauFakeWeight_comb"),
		"ff_w_dm1_njet1_stat" : ("jetToTauFakeWeight_w_dm1_njet1_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_dm1_njet1_stat_up/jetToTauFakeWeight_comb"),
		"ff_tt_syst" : ("jetToTauFakeWeight_tt_syst_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_syst_up/jetToTauFakeWeight_comb"),
		"ff_tt_dm0_njet0_stat" : ("jetToTauFakeWeight_tt_dm0_njet0_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_dm0_njet0_stat_up/jetToTauFakeWeight_comb"),
		"ff_tt_dm0_njet1_stat" : ("jetToTauFakeWeight_tt_dm0_njet1_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_dm0_njet1_stat_up/jetToTauFakeWeight_comb"),
		"ff_tt_dm1_njet0_stat" : ("jetToTauFakeWeight_tt_dm1_njet0_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_dm1_njet0_stat_up/jetToTauFakeWeight_comb"),
		"ff_tt_dm1_njet1_stat" : ("jetToTauFakeWeight_tt_dm1_njet1_stat_down/jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_dm1_njet1_stat_up/jetToTauFakeWeight_comb"),
		"ff_tt_syst_tt" : ("jetToTauFakeWeight_tt_syst_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_tt_syst_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_tt_syst_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_tt_syst_up_2/jetToTauFakeWeight_comb_2"),
		"ff_w_syst_tt" : ("jetToTauFakeWeight_w_syst_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_w_syst_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_w_syst_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_w_syst_up_2/jetToTauFakeWeight_comb_2"),
		"ff_qcd_syst_tt" : ("jetToTauFakeWeight_qcd_syst_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_syst_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_qcd_syst_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_syst_up_2/jetToTauFakeWeight_comb_2"),
		"ff_qcd_dm0_njet0_stat_tt" : ("jetToTauFakeWeight_qcd_dm0_njet0_stat_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm0_njet0_stat_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_qcd_dm0_njet0_stat_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm0_njet0_stat_up_2/jetToTauFakeWeight_comb_2"),
		"ff_qcd_dm0_njet1_stat_tt" : ("jetToTauFakeWeight_qcd_dm0_njet1_stat_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm0_njet1_stat_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_qcd_dm0_njet1_stat_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm0_njet1_stat_up_2/jetToTauFakeWeight_comb_2"),
		"ff_qcd_dm1_njet0_stat_tt" : ("jetToTauFakeWeight_qcd_dm1_njet0_stat_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm1_njet0_stat_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_qcd_dm1_njet0_stat_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm1_njet0_stat_up_2/jetToTauFakeWeight_comb_2"),
		"ff_qcd_dm1_njet1_stat_tt" : ("jetToTauFakeWeight_qcd_dm1_njet1_stat_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm1_njet1_stat_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_qcd_dm1_njet1_stat_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_qcd_dm1_njet1_stat_up_2/jetToTauFakeWeight_comb_2"),
		"ff_w_frac" : ("jetToTauFakeWeight_w_frac_syst_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_w_frac_syst_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_w_frac_syst_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_w_frac_syst_up_2/jetToTauFakeWeight_comb_2"),
		"ff_dy_frac" : ("jetToTauFakeWeight_dy_frac_syst_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_dy_frac_syst_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_dy_frac_syst_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_dy_frac_syst_up_2/jetToTauFakeWeight_comb_2"),
		"ff_tt_frac" : ("jetToTauFakeWeight_tt_frac_syst_down_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_tt_frac_syst_down_2/jetToTauFakeWeight_comb_2", "jetToTauFakeWeight_tt_frac_syst_up_1/jetToTauFakeWeight_comb_1*jetToTauFakeWeight_tt_frac_syst_up_2/jetToTauFakeWeight_comb_2"),
		"nominal" : ("1.0", "1.0"),
		"elees" : ("1.0", "1.0"),
		"muones" : ("1.0", "1.0"),
		"metesone" : ("1.0", "1.0"),
		"metestwo" : ("1.0", "1.0"),
		"efake" : ("(0.003*pt_1+0.883)", "0.702"),
		"mufake" : ("0.005*pt_1+0.992", "0.812"),
	}
mapping_process2sample = {
	"data_obs" : "data",
	"ZTT" : "ztt",
	"ZLL" : "zll",
	"ZL" : "zl",
	"ZJ" : "zj",
	"TT" : "ttj",
	"TTT" : "ttt",
	"TTJ" : "ttjj",
	"VV" : "vv",
	"VVT" : "vvt",
	"VVJ" : "vvj",
	"W" : "wj",
	"QCD" : "qcd",
	"EWK" : "ewk",
	"jetFakes" : "ff",
	"ggH" : "ggh",
	"bbH" : "bbh",
	"qqH" : "qqh",
	"VH" : "vh",
	"WH" : "wh",
	"WplusH" : "wph",
	"WminusH" : "wmh",
	"ZH" : "zh",
}

def sample2process(sample):
	tmp_sample = re.match("(?P<sample>[^0-9]*).*", sample).groupdict().get("sample", "")
	return sample.replace(tmp_sample, dict([reversed(item) for item in mapping_process2sample.iteritems()]).get(tmp_sample, tmp_sample))

def getcategory(basecategory, sample):
	regions = {"_os_highmt" : "_wjets_cr", "_ss_highmt" : "_wjets_ss_cr", "_ss_lowmt" : "_qcd_cr"}
	for cat in regions:
		if cat in sample:
			return basecategory+regions[cat]
	return basecategory

def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for SM HTT analysis.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action="append", nargs="+",
	                    default=["em"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=[["em_btag"]],#, "em_btag_highPzeta", "em_btag_lowPzeta", "em_btag_mediumPzeta", "em_nobtag_highPzeta", "em_nobtag_lowPzeta", "em_nobtag_mediumPzeta", "em_nobtag", "em_inclusive"
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["all"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-s", "--samples", nargs="+", default=[],
	                    help="Samples used. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="mt_tot",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--bbh-nlo", default=False, action="store_true",
	                    help="Enables using NLO bbh samples. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=None,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-e", "--era", default="",
	                    help="Era for which the datacards will be build. [Default: %(default)s]")
	parser.add_argument("-ff", "--fakefactor-method", choices = ["standard", "individual"],
	                    help="Optional background estimation using the Fake-Factor method. [Default: %(default)s]")
	parser.add_argument("--for-dcsync", action="store_true", default=False,
	                    help="Produces simplified datacards for the synchronization exercise. [Default: %(default)s]")
	parser.add_argument("--workingpoint", default="",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-b", "--background-method", default="classic",
	                    help="Background estimation method to be used. [Default: %(default)s]")
	parser.add_argument("--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--controlregions", action="store_true", default=False,
	                    help="Also create histograms for control regions. [Default: %(default)s]")
	parser.add_argument("--SMHiggs", action="store_true", default=False,
	                    help="Also create histograms for SM Higgs. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/htt_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("-p", "--postfix",
	                    default="-mttot",
	                    help="Postfix for the datacard root files. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--mass-dependent", action="store_true", default=False,
	                    help="Create mass dependent plots (one seperate rootfile per mass). Use {mass} in --quantity and/or --categories as wildcard for the mass. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)

	if args.era == "2015":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
	
#	if args.fakefactor_method is not None:
#		for channel in ['mt','et','tt']:
#			for shape_variation in samples_dict[channel]:
#				if shape_variation[0] in ['btag','mistag','nominal']:
#					shape_variation[1].append('ff')
#		for syst in ["ff_qcd_syst", "ff_qcd_dm0_njet0_stat", "ff_qcd_dm0_njet1_stat", "ff_qcd_dm1_njet0_stat", "ff_qcd_dm1_njet1_stat", "ff_w_syst", "ff_w_dm0_njet0_stat", "ff_w_dm0_njet1_stat", "ff_w_dm1_njet0_stat", "ff_w_dm1_njet1_stat", "ff_tt_syst", "ff_tt_dm0_njet0_stat", "ff_tt_dm0_njet1_stat", "ff_tt_dm1_njet0_stat", "ff_tt_dm1_njet1_stat"]:
#			samples_dict['et'].append((syst,["ff"]))
#			samples_dict['mt'].append((syst,["ff"]))
#		for syst in ["ff_w_syst_tt", "ff_tt_syst_tt", "ff_qcd_syst_tt", "ff_qcd_dm0_njet0_stat_tt", "ff_qcd_dm0_njet1_stat_tt", "ff_qcd_dm1_njet0_stat_tt", "ff_qcd_dm1_njet1_stat_tt", "ff_dy_frac", "ff_w_frac", "ff_tt_frac"]:
#			samples_dict['tt'].append((syst,["ff"]))

	if not args.lumi:
		args.lumi = samples.default_lumi/1000.0
	
	# initialisations for plotting
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	output_files = []
	hadd_commands = []
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}{MASS}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}{MASS}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	#sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	#sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	if args.for_dcsync:
		output_root_filename_template = "datacards/common/${ANALYSIS}.inputs-sm-${ERA}-mvis.root"
	
	# args.categories = (args.categories * len(args.channel))[:len(args.channel)]
	if args.higgs_masses[0] == "all":
		args.higgs_masses = ["90","100","110","120","130","140","160","180","200","250","350","400","450","500","600","700","800","900","1000","1200","1400","1600","1800","2000","2300","2600","2900","3200"]
	looplist = [""]
	prefix = ""
	if args.mass_dependent:
		looplist = args.higgs_masses
		prefix = "_M"
	for mass in looplist:
		for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
			tmp_output_files = []
			output_file = os.path.join(args.output_dir, "htt_%s%s%s.inputs-mssm-13TeV%s.root"%(channel.replace("mm","zmm"),prefix,mass,args.postfix))
			output_files.append(output_file)
			
			for categorytemplate in categories:
				category = categorytemplate.format(mass=mass) if args.mass_dependent else categorytemplate
				exclude_cuts = []
				if args.for_dcsync:
					if category[3:] == 'inclusive':
						exclude_cuts=["mt", "pzeta"]
					elif category[3:] == 'inclusivenotwoprong':
						exclude_cuts=["pzeta"]

				#determine cut_type based on category and era
				cut_type = "mssm2016"
				if args.era == "2015":
					cut_type = "mssm"
				elif args.era == "2016":
					cut_type = "mssm2016"
				elif "looseiso" in category:
#					if args.fakefactor_method is not None:
#						cut_type = "mssm2016fflooseiso"
#					else:
					cut_type = "mssm2016looseiso"
				elif "loosemt" in category:
					cut_type = "mssm2016loosemt"
				elif "tight" in category:
					cut_type = "mssm2016tight"
				else:
#					if args.fakefactor_method is not None:
#						cut_type = "mssm2016fffull"
#					else:
					cut_type = "mssm2016full"
				
				for shape_systematic, list_of_samples in samples_dict[channel]:
					nominal = (shape_systematic == "nominal")
					#if not nominal:
					#	continue
					list_of_samples = (["data"] if nominal else []) + list_of_samples
					if args.samples:
						list_of_samples = args.samples
					
					for shift_up in ([True] if nominal else [True, False]):
						systematic = "nominal" if nominal else (shapes[shape_systematic].format(CHANNEL = channel) + ("Up" if shift_up else "Down"))
						
						log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
								samples="\", \"".join(list_of_samples),
								channel=channel,
								category=category,
								systematic=systematic
						))
						# modify weight for toppt, taupt
						additional_weight = shapes_weight_dict[shape_systematic][1] if shift_up else shapes_weight_dict[shape_systematic][0]
	
						# prepare plotting configs for retrieving the input histograms
						config = sample_settings.get_config(
								samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
								channel=channel,
								category="catHttMSSM13TeV_"+category,
								weight=args.weight,
								lumi = args.lumi * 1000,
								exclude_cuts=args.exclude_cuts,
								higgs_masses=args.higgs_masses,
								mssm=True,
								estimationMethod=args.background_method,
								controlregions=args.controlregions,
								fakefactor_method=args.fakefactor_method,
								cut_type=cut_type,
								no_ewk_samples = True,
								no_ewkz_as_dy = True,
								bbh_nlo = args.bbh_nlo
						)
						
						# systematics_settings = systematics_factory.get(shape_systematic)(config)
						# config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))

						# set qcd os-ss extrapolation factors
						if category in ["em_btag", "em_nobtag", "em_inclusive"]:
							config["qcd_extrapolation_factors_ss_os"] = 1.00#TODO
#						if category in ["mt_nobtag_tight", "mt_nobtag_loosemt", "mt_nobtag"]:
#							config["qcd_extrapolation_factors_ss_os"] = 1.14
#						elif category in ["mt_btag_tight", "mt_btag_loosemt", "mt_btag"]:
#							config["qcd_extrapolation_factors_ss_os"] = 1.01
#						elif category in ["mt_inclusive_tight", "mt_inclusive_loosemt", "mt_inclusive"]:
#							config["qcd_extrapolation_factors_ss_os"] = 1.12
#						elif category in ["et_nobtag_tight", "et_nobtag_loosemt", "et_nobtag"]:
#							config["qcd_extrapolation_factors_ss_os"] = 1.11
#						elif category in ["et_btag_tight", "et_btag_loosemt", "et_btag"]:
#							config["qcd_extrapolation_factors_ss_os"] = 1.16
#						elif category in ["et_inclusive_tight", "et_inclusive_loosemt", "et_inclusive"]:
#							config["qcd_extrapolation_factors_ss_os"] = 1.13

						# modify cut strings for shape uncertainties. Do not apply weights to data 
						for index,value in enumerate(config["weights"]):
							if not "Run201" in config["files"][index] or args.fakefactor_method is not None:
								# exclude ff-norm samples from additional weights
								if not "ff_norm" in config["nicks"][index]:
									config["weights"][index] += "*"+additional_weight

						# modify cut for ff samples. Cut string does not include tau iso
						# also need to replace ff weight with channel specific weights
#						if  args.fakefactor_method is not None:
#							for index,value in enumerate(config["weights"]):
#								if "ff_norm" in config["nicks"][index]:
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_comb","jetToTauFakeWeight_comb_"+category.replace(channel+"_","",1))
#								if config["nicks"][index] == "ff" or "ff_control" in config["nicks"][index]:
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_comb","jetToTauFakeWeight_comb_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_syst_up","jetToTauFakeWeight_qcd_syst_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_syst_down","jetToTauFakeWeight_qcd_syst_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet0_stat_up","jetToTauFakeWeight_qcd_dm0_njet0_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet0_stat_down","jetToTauFakeWeight_qcd_dm0_njet0_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet1_stat_up","jetToTauFakeWeight_qcd_dm0_njet1_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet1_stat_down","jetToTauFakeWeight_qcd_dm0_njet1_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet0_stat_up","jetToTauFakeWeight_qcd_dm1_njet0_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet0_stat_down","jetToTauFakeWeight_qcd_dm1_njet0_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet1_stat_up","jetToTauFakeWeight_qcd_dm1_njet1_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet1_stat_down","jetToTauFakeWeight_qcd_dm1_njet1_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_syst_up","jetToTauFakeWeight_w_syst_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_syst_down","jetToTauFakeWeight_w_syst_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm0_njet0_stat_up","jetToTauFakeWeight_w_dm0_njet0_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm0_njet0_stat_down","jetToTauFakeWeight_w_dm0_njet0_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm0_njet1_stat_up","jetToTauFakeWeight_w_dm0_njet1_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm0_njet1_stat_down","jetToTauFakeWeight_w_dm0_njet1_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm1_njet0_stat_up","jetToTauFakeWeight_w_dm1_njet0_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm1_njet0_stat_down","jetToTauFakeWeight_w_dm1_njet0_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm1_njet1_stat_up","jetToTauFakeWeight_w_dm1_njet1_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_dm1_njet1_stat_down","jetToTauFakeWeight_w_dm1_njet1_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_syst_up","jetToTauFakeWeight_tt_syst_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_syst_down","jetToTauFakeWeight_tt_syst_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm0_njet0_stat_up","jetToTauFakeWeight_tt_dm0_njet0_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm0_njet0_stat_down","jetToTauFakeWeight_tt_dm0_njet0_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm0_njet1_stat_up","jetToTauFakeWeight_tt_dm0_njet1_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm0_njet1_stat_down","jetToTauFakeWeight_tt_dm0_njet1_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm1_njet0_stat_up","jetToTauFakeWeight_tt_dm1_njet0_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm1_njet0_stat_down","jetToTauFakeWeight_tt_dm1_njet0_stat_down_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm1_njet1_stat_up","jetToTauFakeWeight_tt_dm1_njet1_stat_up_"+category.replace(channel+"_","",1))
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_dm1_njet1_stat_down","jetToTauFakeWeight_tt_dm1_njet1_stat_down_"+category.replace(channel+"_","",1))

#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_syst_up_1","jetToTauFakeWeight_qcd_syst_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_syst_up_2","jetToTauFakeWeight_qcd_syst_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_syst_down_1","jetToTauFakeWeight_qcd_syst_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_syst_down_2","jetToTauFakeWeight_qcd_syst_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_syst_up_1","jetToTauFakeWeight_w_syst_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_syst_up_2","jetToTauFakeWeight_w_syst_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_syst_down_1","jetToTauFakeWeight_w_syst_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_syst_down_2","jetToTauFakeWeight_w_syst_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_syst_up_1","jetToTauFakeWeight_tt_syst_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_syst_up_2","jetToTauFakeWeight_tt_syst_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_syst_down_1","jetToTauFakeWeight_tt_syst_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_syst_down_2","jetToTauFakeWeight_tt_syst_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_frac_syst_up_1","jetToTauFakeWeight_w_frac_syst_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_frac_syst_up_2","jetToTauFakeWeight_w_frac_syst_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_frac_syst_down_1","jetToTauFakeWeight_w_frac_syst_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_w_frac_syst_down_2","jetToTauFakeWeight_w_frac_syst_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_dy_frac_syst_up_1","jetToTauFakeWeight_dy_frac_syst_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_dy_frac_syst_up_2","jetToTauFakeWeight_dy_frac_syst_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_dy_frac_syst_down_1","jetToTauFakeWeight_dy_frac_syst_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_dy_frac_syst_down_2","jetToTauFakeWeight_dy_frac_syst_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_frac_syst_up_1","jetToTauFakeWeight_tt_frac_syst_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_frac_syst_up_2","jetToTauFakeWeight_tt_frac_syst_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_frac_syst_down_1","jetToTauFakeWeight_tt_frac_syst_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_tt_frac_syst_down_2","jetToTauFakeWeight_tt_frac_syst_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet0_stat_up_1","jetToTauFakeWeight_qcd_dm0_njet0_stat_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet0_stat_up_2","jetToTauFakeWeight_qcd_dm0_njet0_stat_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet0_stat_down_1","jetToTauFakeWeight_qcd_dm0_njet0_stat_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet0_stat_down_2","jetToTauFakeWeight_qcd_dm0_njet0_stat_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet1_stat_up_1","jetToTauFakeWeight_qcd_dm0_njet1_stat_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet1_stat_up_2","jetToTauFakeWeight_qcd_dm0_njet1_stat_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet1_stat_down_1","jetToTauFakeWeight_qcd_dm0_njet1_stat_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm0_njet1_stat_down_2","jetToTauFakeWeight_qcd_dm0_njet1_stat_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet0_stat_up_1","jetToTauFakeWeight_qcd_dm1_njet0_stat_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet0_stat_up_2","jetToTauFakeWeight_qcd_dm1_njet0_stat_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet0_stat_down_1","jetToTauFakeWeight_qcd_dm1_njet0_stat_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet0_stat_down_2","jetToTauFakeWeight_qcd_dm1_njet0_stat_down_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet1_stat_up_1","jetToTauFakeWeight_qcd_dm1_njet1_stat_up_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet1_stat_up_2","jetToTauFakeWeight_qcd_dm1_njet1_stat_up_"+category.replace(channel+"_","",1)+"_2")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet1_stat_down_1","jetToTauFakeWeight_qcd_dm1_njet1_stat_down_"+category.replace(channel+"_","",1)+"_1")
#									config["weights"][index] = config["weights"][index].replace("jetToTauFakeWeight_qcd_dm1_njet1_stat_down_2","jetToTauFakeWeight_qcd_dm1_njet1_stat_down_"+category.replace(channel+"_","",1)+"_2")



						
						if args.workingpoint:
							for index, folder in enumerate(config["weights"]):
								config["weights"][index] = config["weights"][index].replace("nbtag","n"+args.workingpoint+"btag")
						# modify folder for taues
						if shape_systematic == "taues":
							replacestring = "jecUncNom_tauEsUp" if shift_up else "jecUncNom_tauEsDown"
							for index, folder in enumerate(config["folders"]):
								if any([(proc in config["nicks"][index]) for proc in ["ggh","bbh","ztt"]]):
									# hack to only substitute the folder for those where it is needed
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)

						# For em channel
						if shape_systematic == "jec":
							replacestring = "jecUncUp" if shift_up else "jecUncDown"
							for index, folder in enumerate(config["folders"]):
								if not "Run201" in config["files"][index]:
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
						if shape_systematic == "elees":
							replacestring = "eleEsUp" if shift_up else "eleEsDown"
							for index, folder in enumerate(config["folders"]):
								if not "Run201" in config["files"][index]:
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
						if shape_systematic == "muones":
							replacestring = "muonEsUp" if shift_up else "muonEsDown"
							for index, folder in enumerate(config["folders"]):
								if not "Run201" in config["files"][index]:
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)

						# taues
						if shape_systematic == "taues1prong0pi":
							replacestring = "tauEsOneProngUp" if shift_up else "tauEsOneProngDown"
							for index, folder in enumerate(config["folders"]):
								if not "Run201" in config["files"][index]:
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
						if shape_systematic == "taues1prong1pi":
							replacestring = "tauEsOneProngOnePiZeroUp" if shift_up else "tauEsOneProngOnePiZeroDown"
							for index, folder in enumerate(config["folders"]):
								if not "Run201" in config["files"][index]:
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
						if shape_systematic == "taues3prong0pi":
							replacestring = "tauEsThreeProngUp" if shift_up else "tauEsThreeProngDown"
							for index, folder in enumerate(config["folders"]):
								if not "Run201" in config["files"][index]:
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)

						if shape_systematic == "etaues1prong0pi":
							replacestring = "eleTauEsOneProngZeroPiZeroUp" if shift_up else "eleTauEsOneProngZeroPiZeroDown"
							for index, folder in enumerate(config["folders"]):
								if re.search("DY\d?JetsToLL",config["files"][index]):
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
						
						if shape_systematic == "etaues1prong1pi":
							replacestring = "eleTauEsOneProngOnePiZeroUp" if shift_up else "eleTauEsOneProngOnePiZeroDown"
							for index, folder in enumerate(config["folders"]):
								if re.search("DY\d?JetsToLL",config["files"][index]):
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
						
						config["x_expressions"] = [args.quantity.format(mass=mass)] if args.mass_dependent else [args.quantity]
						
						binnings_key = "binningHttMSSM13TeV_"+category+"_"+(args.quantity.format(mass=mass) if args.mass_dependent else args.quantity)
						if binnings_key in binnings_settings.binnings_dict:
							config["x_bins"] = [binnings_key]
						else:
							config["x_bins"] = ["35,0.0,350.0"]
						
						config["directories"] = [args.input_dir]
						
						histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
						config["labels"] = [histogram_name_template.replace("$", "").format(
								PROCESS=sample2process(re.sub("_(os|ss)_(low|high)mt","",sample)),
								BIN = getcategory(category,sample).replace("mm_","zmm_"),
								SYSTEMATIC=systematic
						) for sample in config["labels"]]
						
						tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
								ANALYSIS="htt",
								CHANNEL="zmm" if channel == "mm" else channel,
								BIN=category.replace("mm","zmm"),
								SYSTEMATIC=systematic,
								ERA="13TeV",
								MASS=prefix+mass
						))
						tmp_output_files.append(tmp_output_file)
						config["output_dir"] = os.path.dirname(tmp_output_file)
						config["filename"] = os.path.splitext(os.path.basename(tmp_output_file))[0]
					
						config["plot_modules"] = ["ExportRoot"]
						config["file_mode"] = "UPDATE"
				
						if "legend_markers" in config:
							config.pop("legend_markers")
						if args.for_dcsync:
							config["wjets_from_mc"] = [True,True]
				
						plot_configs.append(config)
						if args.SMHiggs and "ggh" in list_of_samples:
							log.debug("Create SM inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
									samples="\", \"".join(list_of_samples),
									channel=channel,
									category=category,
									systematic=systematic
							))
							# modify weight for toppt, taupt
							additional_weight = shapes_weight_dict[shape_systematic][1] if shift_up else shapes_weight_dict[shape_systematic][0]
							# samples will be normalized later on
							additional_weight += "/crossSectionPerEventWeight"
		
							# prepare plotting configs for retrieving the input histograms
							config = sample_settings.get_config(
									samples=[getattr(samples.Samples, sample) for sample in ["ggh","qqh","wminush","wplush","zh"]],
									channel=channel,
									category="catHttMSSM13TeV_"+category,
									weight=args.weight+"*"+additional_weight,
									lumi = args.lumi * 1000,
									exclude_cuts=args.exclude_cuts,
									higgs_masses=['125'],
									mssm=False,
									estimationMethod=args.background_method,
									controlregions=args.controlregions,
									fakefactor_method=args.fakefactor_method,
									cut_type=cut_type,
									no_ewk_samples = True,
									no_ewkz_as_dy = True,
									bbh_nlo = args.bbh_nlo
							)
							
							if args.workingpoint:
								for index, folder in enumerate(config["weights"]):
									config["weights"][index] = config["weights"][index].replace("nbtag","n"+args.workingpoint+"btag")
							# modify folder for taues
							if shape_systematic == "taues":
								replacestring = "jecUncNom_tauEsUp" if shift_up else "jecUncNom_tauEsDown"
								for index, folder in enumerate(config["folders"]):
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)

							if shape_systematic == "jec":
								replacestring = "jecUncUp" if shift_up else "jecUncDown"
								for index, folder in enumerate(config["folders"]):
									if not "Run201" in config["files"][index]:
										config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
							# taues
							if shape_systematic == "taues1prong0pi":
								replacestring = "tauEsOneProngUp" if shift_up else "tauEsOneProngDown"
								for index, folder in enumerate(config["folders"]):
									if not "Run201" in config["files"][index]:
										config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
							if shape_systematic == "taues1prong1pi":
								replacestring = "tauEsOneProngOnePiZeroUp" if shift_up else "tauEsOneProngOnePiZeroDown"
								for index, folder in enumerate(config["folders"]):
									if not "Run201" in config["files"][index]:
										config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
							if shape_systematic == "taues3prong0pi":
								replacestring = "tauEsThreeProngUp" if shift_up else "tauEsThreeProngDown"
								for index, folder in enumerate(config["folders"]):
									if not "Run201" in config["files"][index]:
										config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
							if shape_systematic == "etaues1prong0pi":
								replacestring = "eleTauEsOneProngZeroPiZeroUp" if shift_up else "eleTauEsOneProngZeroPiZeroDown"
								for index, folder in enumerate(config["folders"]):
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
							
							if shape_systematic == "etaues1prong1pi":
								replacestring = "eleTauEsOneProngOnePiZeroUp" if shift_up else "eleTauEsOneProngOnePiZeroDown"
								for index, folder in enumerate(config["folders"]):
									config["folders"][index] = config["folders"][index].replace("nominal", replacestring)
							
							config["x_expressions"] = [args.quantity.format(mass=mass)] if args.mass_dependent else [args.quantity]
							
							binnings_key = "binningHttMSSM13TeV_"+category+"_"+(args.quantity.format(mass=mass) if args.mass_dependent else args.quantity)
							if binnings_key in binnings_settings.binnings_dict:
								config["x_bins"] = [binnings_key]
							else:
								config["x_bins"] = ["35,0.0,350.0"]
							
							config["directories"] = [args.input_dir]
							
							histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
							config["labels"] = [histogram_name_template.replace("$", "").format(
									PROCESS=sample2process(sample).replace("H","H_SM"),
									BIN = getcategory(category,sample),
									SYSTEMATIC=systematic
							) for sample in config["labels"]]
							
							tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
									ANALYSIS="htt",
									CHANNEL="zmm" if channel == "mm" else channel,
									BIN=category.replace("mm","zmm")+"_SM",
									SYSTEMATIC=systematic,
									ERA="13TeV",
									MASS=prefix+mass
							))
							tmp_output_files.append(tmp_output_file)
							config["output_dir"] = os.path.dirname(tmp_output_file)
							config["filename"] = os.path.splitext(os.path.basename(tmp_output_file))[0]
						
							config["plot_modules"] = ["ExportRoot"]
							config["file_mode"] = "UPDATE"
					
							if "legend_markers" in config:
								config.pop("legend_markers")
					
							plot_configs.append(config)
				
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
					DST=output_file,
					SRC=" ".join(tmp_output_files)
			))
		
	#if log.isEnabledFor(logging.DEBUG):
	#	import pprint
	#	pprint.pprint(plot_configs)
	
	# delete existing output files
	tmp_output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
	for output_file in tmp_output_files:
		if os.path.exists(output_file):
			os.remove(output_file)
			log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	output_files = list(set(output_files))
	
	# create input histograms with HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])
	tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	
	debug_plot_configs = []
	# for output_file in output_files:
		# debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
	# higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])
