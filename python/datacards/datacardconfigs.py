# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re, os


class DatacardConfigs(object):
	def __init__(self):
		super(DatacardConfigs, self).__init__()

		self._mapping_process2sample = {
			"data_obs" : "data",
			"ZTT" : "ztt",
			"ZLL" : "zll",
			"ZL" : "zl",
			"ZJ" : "zj",
			"TT" : "ttj",
			"VV" : "vv",
			"W" : "wj",
			"QCD" : "qcd",
			"ggH" : "ggh",
			"qqH" : "qqh",
			"VH" : "vh",
			"WH" : "wh",
			"ZH" : "zh",
		}

		self._mapping_category2binid = {
			"mt" : {
				"mt_inclusive" : 0,
				"mt_0jet_high" : 1,
				"mt_0jet_low" : 2,
				"mt_1jet_high" : 3,
				"mt_1jet_low" : 4,
				"mt_2jet_vbf" : 5,
				"mt_mod_vbf" : 6,
				"mt_mod_sig" : 7,
				"mt_mod_mixed" : 8,
				"mt_mod_bkg" : 9,
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
			},
		}
		categories={}
		for channel in ["tt", "mt", "et", "em"]:
			categories_path = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/%s_mvadatacards.cfg"%channel)
			with open(categories_path) as categs:
				for line in categs:
					cat = line.strip()
					self._mapping_category2binid[channel][cat] = len(self._mapping_category2binid[channel].keys())

		self.htt_datacard_filename_templates = [
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

