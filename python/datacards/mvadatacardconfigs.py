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
                "mt_tight" : 1,
                "mt_loose1" : 2,
                "mt_loose2" : 3,
                "mt_bkg" : 4,
                "mt_ztt_bkg" : 5,
                "mt_ztt_mid" : 6,
                "mt_ztt_sig" : 7
                
            },
            "et" : {
                "et_inclusive" : 0,
                "et_ztt_tight" : 1,
                "et_ztt_loose1" : 2,
                "et_ztt_loose2" : 3,
                "et_ztt_bkg" : 4,
                "et_ztt_bkg" : 5,
                "et_ztt_mid" : 6,
                "et_ztt_sig" : 7
            },
            "em" : {
                "em_inclusive" : 0,
                "em_ztt_tight" : 1,
                "em_ztt_loose1" : 2,
                "em_ztt_loose2" : 3,
                "em_ztt_bkg" : 4,
                "em_ztt_bkg" : 5,
                "em_ztt_mid" : 6,
                "em_ztt_sig" : 7
            },
            "tt" : {
                "tt_inclusive" : 0,
                "tt_ztt_tight" : 1,
                "tt_ztt_loose1" : 2,
                "tt_ztt_loose2" : 3,
                "tt_ztt_bkg" : 4,
                "tt_ztt_bkg" : 5,
                "tt_ztt_mid" : 6,
                "tt_ztt_sig" : 7
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

