# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class DatacardConfigs(object):
	def __init__(self):
		super(DatacardConfigs, self).__init__()
		
		self._mapping_process2sample = {
			"data_obs" : "data",
			"ZTT" : "ztt",
			"ZLL" : "zll",
			"ZL" : "zl",
			"ZJ" : "zj",
			"TTJ" : "ttj",
			"VV" : "vv",
			"WJ" : "wj",
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
			},
			"et" : {
				"et_inclusive" : 0,
				"et_0jet_high" : 1,
				"et_0jet_low" : 2,
				"et_1jet_high" : 3,
				"et_1jet_low" : 4,
				"et_2jet_vbf" : 5,
			},
			"em" : {
				"em_inclusive" : 0,
				"em_0jet_high" : 1,
				"em_0jet_low" : 2,
				"em_1jet_high" : 3,
				"em_1jet_low" : 4,
				"em_2jet_vbf" : 5,
			},
			"tt" : {
				"tt_inclusive" : 0,
				"tt_0jet_high" : 1,
				"tt_0jet_low" : 2,
				"tt_1jet_high" : 3,
				"tt_1jet_low" : 4,
				"tt_2jet_vbf" : 5,
			},
		}
		
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

