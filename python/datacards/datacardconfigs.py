# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class DatacardConfigs(object):
	def __init__(self):
		super(DatacardConfigs, self).__init__()
		
		self._mapping_process2sample = {
			"data_obs" : "data",
			"ZTT" : "ztt",
			"TTJ" : "ttj",
			"VV" : "vv",
			"WJ" : "wj",
			"QCD" : "qcd",
		}
		
		self._mapping_category2binid = {
			"mt" : {
				"inclusive" : 0,
				"0jet" : 1,
				"1jet" : 2,
				"2jet" : 3,
			},
			"et" : {
				"inclusive" : 0,
				"0jet" : 1,
				"1jet" : 2,
				"2jet" : 3,
			},
		}
	
	def process2sample(self, process):
		return self._mapping_process2sample.get(process, process)
	
	def sample2process(self, sample):
		return dict([reversed(item) for item in self._mapping_process2sample.iteritems()]).get(sample, sample)
	
	def category2binid(self, category, channel="default"):
		return self._mapping_category2binid.get(channel, {}).get(category, 0)
	
	def binid2category(self, binid, channel="default"):
		return dict([reversed(item) for item in self._mapping_category2binid.get(channel, {}).iteritems()]).get(binid, "inclusive")

