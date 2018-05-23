# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import re, os


class DatacardConfigs(object):
	def __init__(self):
		super(DatacardConfigs, self).__init__()

		self._mapping_process2sample = {
			"data_obs" : "data",
			"ZTT" : "ztt",
			"ZTTPOSPOL" : "zttpospol",
			"ZTTNEGPOL" : "zttnegpol",
			"ZLL" : "zll",
			"ZL" : "zl",
			"ZJ" : "zj",
			"EWKZ" : "ewkz",
			"TT" : "ttj",
			"TTTAUTAU" : "tttautau",
			"TTT" : "ttt",
			"TTJJ" : "ttjj",
			"TTJT" : "ttjt",
			"TTJL" : "ttjl",
			"VV" : "vv",
			"VVT" : "vvt",
			"VVJ" : "vvj",
			"VVL" : "vvl",
			"W" : "wj",
			"WJT" : "wjt",
			"WJL" : "wjl",
			"QCD" : "qcd",
			"EWK" : "ewk",
			"FF" : "ff",
			"ggH" : "ggh",
			"qqH" : "qqh",
			"VH" : "vh",
			"WH" : "wh",
			"ZH" : "zh",
			"ggH_htt" : "ggh",
			"qqH_htt" : "qqh",
			"VH_htt" : "vh",
			"WH_htt" : "wh",
			"ZH_htt" : "zh",
			"ggH_hww" : "hww_gg",
			"qqH_hww" : "hww_qq",
			"HTT" : "htt",
			"ggHsm" : "gghjhusm",
			"ggHmm" : "gghjhumm",
			"ggHps" : "gghjhups",
			"qqHsm" : "qqhjhusm",
			"qqHmm" : "qqhjhumm",
			"qqHps" : "qqhjhups",
			"smHcpeven": "httcpeven",
			"susyHcpodd_ALT": "susycpodd",
			"CPODD_ALT": "httcpodd",
			"CPMIX_ALT": "httcpmix",
		}

		self._mapping_category2binid = {
			"mt" : {
				"mt_inclusive" : 0,
				"mt_0jet_high" : 1,
				"mt_0jet_low" : 2,
				"mt_1jet_high" : 3,
				"mt_1jet_low" : 4,
				"mt_2jet_vbf" : 5,
				"mt_CP_mt" : 10,
				"mt_vbf" : 11,
				"mt_1jet_boosted" : 12,
				"mt_1jet_highpt2" : 13,
				"mt_1jet_lowpt2" : 14,
				"mt_0jet_highpt2" : 15,
				"mt_0jet_lowpt2" : 16,
				"mt_vbf_tag" : 17,
				"mt_2jet_untagged" : 18,
				"mt_1jet_boost_high" : 19,
				"mt_1jet_boost_medium" : 20,
				"mt_1jet_boost_low" : 21,
				"mt_0jet_nhighpt2" : 22,
				"mt_0jet_nlowpt2" : 23,
				"mt_0jet_inclusive" : 30,
				"mt_1jet_inclusive" : 31,
				"mt_2jet_inclusive" : 32,
				
				"mt_ZeroJet2D" : 100,
				"mt_Boosted2D" : 101,
				"mt_Vbf2D" : 102,
				
				"mt_a1" : 1010,
				"mt_rho" : 1020,
				"mt_oneprong" : 1030,
				
				"mt_dijet_boosted" : 2001, 
				"mt_dijet_highM" : 2002, 
				"mt_dijet_lowM" : 2003,
				"mt_dijet_lowMjj" : 2004 

			},
			"et" : {
				"et_inclusive" : 0,
				"et_0jet_high" : 1,
				"et_0jet_low" : 2,
				"et_1jet_high" : 3,
				"et_1jet_low" : 4,
				"et_2jet_vbf" : 5,
				"et_CP_et": 10,
				"et_vbf" : 11,
				"et_1jet_boosted" : 12,
				"et_1jet_highpt2" : 13,
				"et_1jet_lowpt2" : 14,
				"et_0jet_highpt2" : 15,
				"et_0jet_lowpt2" : 16,
				"et_vbf_tag" : 17,
				"et_2jet_untagged" : 18,
				"et_1jet_boost_high" : 19,
				"et_1jet_boost_medium" : 20,
				"et_1jet_boost_low" : 21,
				"et_0jet_nhighpt2" : 22,
				"et_0jet_nlowpt2" : 23,
				"et_0jet_inclusive" : 30,
				"et_1jet_inclusive" : 31,
				"et_2jet_inclusive" : 32,
				
				"et_ZeroJet2D" : 100,
				"et_Boosted2D" : 101,
				"et_Vbf2D" : 102,
				
				"et_a1" : 1010,
				"et_rho" : 1020,
				"et_oneprong" : 1030,
				
				"et_dijet_boosted" : 2001, 
				"et_dijet_highM" : 2002, 
				"et_dijet_lowM" : 2003, 
				"et_dijet_lowMjj" : 2004
			},
			"em" : {
				"em_inclusive" : 0,
				"em_0jet_high" : 1,
				"em_0jet_low" : 2,
				"em_1jet_high" : 3,
				"em_1jet_low" : 4,
				"em_2jet_vbf" : 5,
				"em_CP_em" :10,
				"em_vbf" : 11,
				"em_1jet_boosted" : 12,
				"em_1jet_highpt2" : 13,
				"em_1jet_lowpt2" : 14,
				"em_0jet_highpt2" : 15,
				"em_0jet_lowpt2" : 16,
				"em_vbf_tag" : 17,
				"em_2jet_untagged" : 18,
				"em_1jet_boost_high" : 19,
				"em_1jet_boost_medium" : 20,
				"em_1jet_boost_low" : 21,
				"em_0jet_nhighpt2" : 22,
				"em_0jet_nlowpt2" : 23,
				"em_0jet_inclusive" : 30,
				"em_1jet_inclusive" : 31,
				"em_2jet_inclusive" : 32,
				
				"em_ZeroJet2D" : 100,
				"em_Boosted2D" : 101,
				"em_Vbf2D" : 102,
				
				"em_oneprong" : 1030,
				
				"em_dijet_boosted" : 2001, 
				"em_dijet_highM" : 2002, 
				"em_dijet_lowM" : 2003, 
				"em_dijet_lowMjj" : 2004
			},
			"tt" : {
				"tt_inclusive" : 0,
				"tt_0jet_high" : 1,
				"tt_0jet_low" : 2,
				"tt_1jet_high" : 3,
				"tt_1jet_low" : 4,
				"tt_2jet_vbf" : 5,
				"tt_CP_tt" : 10,
				"tt_vbf" : 11,
				"tt_1jet_boosted" : 12,
				"tt_1jet_highpt2" : 13,
				"tt_1jet_lowpt2" : 14,
				"tt_0jet_highpt2" : 15,
				"tt_0jet_lowpt2" : 16,
				"tt_vbf_tag" : 17,
				"tt_2jet_untagged" : 18,
				"tt_1jet_boost_high" : 19,
				"tt_1jet_boost_medium" : 20,
				"tt_1jet_boost_low" : 21,
				"tt_0jet_nhighpt2" : 22,
				"tt_0jet_nlowpt2" : 23,
				"tt_0jet_inclusive" : 30,
				"tt_1jet_inclusive" : 31,
				"tt_2jet_inclusive" : 32,
				
				"tt_ZeroJet2D" : 100,
				"tt_Boosted2D" : 101,
				"tt_Vbf2D" : 102,
				
				"tt_a1" : 1010,
				"tt_rho" : 1020,
				"tt_oneprong" : 1030,
				
				"tt_dijet_boosted" : 2001, 
				"tt_dijet_highM" : 2002, 
				"tt_dijet_lowM" : 2003, 
				"tt_dijet_lowMjj" : 2004,
			},
			"mm" : {
				"mm_inclusive" : 0,
				"mm_0jet_high" : 1,
				"mm_0jet_low" : 2,
				"mm_1jet_high" : 3,
				"mm_1jet_low" : 4,
				"mm_2jet_vbf" : 5,
				"mm_CP_em" :10,
				"mm_vbf" : 11,
				"mm_1jet_boosted" : 12,
				"mm_1jet_highpt2" : 13,
				"mm_1jet_lowpt2" : 14,
				"mm_0jet_highpt2" : 15,
				"mm_0jet_lowpt2" : 16,
				"mm_vbf_tag" : 17,
				"mm_2jet_untagged" : 18,
				"mm_1jet_boost_high" : 19,
				"mm_1jet_boost_medium" : 20,
				"mm_1jet_boost_low" : 21,
				"mm_0jet_nhighpt2" : 22,
				"mm_0jet_nlowpt2" : 23,
				
				"mm_ZeroJet2D" : 100,
				"mm_Boosted2D" : 101,
				"mm_Vbf2D" : 102,
			},
		}
		#for channel in ["tt", "mt", "et", "em"]:
			#categories_path = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/%s_mvadatacards.cfg"%channel)
			#with open(categories_path) as categs:
				#for line in categs:
					#cat = line.strip()
					#self._mapping_category2binid[channel][cat] = len(self._mapping_category2binid[channel].keys())
		channels=["mt", "et", "tt", "em","mm"]
		# ==========================Copy here!=========================================
		categories=Categories.CategoriesDict().getCategories(channels=channels)
		import operator
		#TODO get maximum binvalue for categories already there
		max_number = 1 + max([max(v.iteritems(), key=operator.itemgetter(1))[1] for k,v in self._mapping_category2binid.iteritems()])
		for chan in channels:
			for i, cat in enumerate(categories[chan]):
				self._mapping_category2binid[chan][cat] = max_number + i
		self.htt_datacard_filename_templates = [
			"datacards/individual/${BIN}/${MASS}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
			"datacards/channel/${CHANNEL}/${MASS}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
			"datacards/category/${BINID}/${MASS}/${ANALYSIS}_${BINID}_${ERA}.txt",
			"datacards/combined/${MASS}/${ANALYSIS}_${ERA}.txt",
		]
		self.cp_datacard_filename_templates = [
			"/cmb/${MASS}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
			"/${CHANNEL}/${MASS}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",

		]

		self.LFV_datacard_filename_templates = [
			"datacards/individual/${BIN}/${MASS}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
			"datacards/channel/${CHANNEL}/${MASS}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
			"datacards/category/${BINID}/${MASS}/${ANALYSIS}_${BINID}_${ERA}.txt",
			"datacards/combined/${MASS}/${ANALYSIS}_${ERA}.txt",
		]

	def process2sample(self, process):
		tmp_process = re.match("(?P<process>[^0-9]*).*", process).groupdict().get("process", "")
		return process.replace(tmp_process, self._mapping_process2sample.get(tmp_process, tmp_process))

	def sample2process(self, sample):
		tmp_sample = re.match("(?P<sample>[^0-9]*).*", sample).groupdict().get("sample", "")
		return sample.replace(tmp_sample, dict([reversed(item) for item in self._mapping_process2sample.iteritems()]).get(tmp_sample, tmp_sample))

	def category2binid(self, category, channel="default"):
		return self._mapping_category2binid.get(channel, {}).get(category, 0)

	def binid2category(self, binid, channel="default"):
		return dict([reversed(item) for item in self._mapping_category2binid.get(channel, {}).iteritems()]).get(binid, "inclusive")

