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
                "mt_Nall_150_4_up" : 1,
                "mt_Nall_150_4_down" : 2,
                "mt_Nall_150_4_mid" : 3,
                "mt_Nall_250_4_up" : 4,
                "mt_Nall_250_4_down" : 5,
                "mt_Nall_250_4_mid" : 6,
                "mt_Nall_350_4_up" : 7,
                "mt_Nall_350_4_down" : 8,
                "mt_Nall_350_4_mid" : 9,
                "mt_Nall_450_4_up" : 10,
                "mt_Nall_450_4_down" : 11,
                "mt_Nall_450_4_mid" : 12,
                "mt_Nall_150_up" : 13,
                "mt_Nall_150_down" : 14,
                "mt_Nall_150_mid" : 15,
                "mt_Nall_250_up" : 16,
                "mt_Nall_250_down" :17,
                "mt_Nall_250_mid" : 18,
                "mt_Nall_350_up" : 19,
                "mt_Nall_350_down" : 20,
                "mt_Nall_350_mid" : 21,
                "mt_Nall_450_up" : 22,
                "mt_Nall_450_down" : 23,
                "mt_Nall_450_mid" : 24,
                "mt_all_150_4_up" : 25,
                "mt_all_150_4_down" : 26,
                "mt_all_150_4_mid" : 27,
                "mt_all_250_4_up" : 28,
                "mt_all_250_4_down" : 29,
                "mt_all_250_4_mid" : 30,
                "mt_all_350_4_up" : 31,
                "mt_all_350_4_down" : 32,
                "mt_all_350_4_mid" : 33,
                "mt_all_450_4_up" : 34,
                "mt_all_450_4_down" : 35,
                "mt_all_450_4_mid" : 36,
                "mt_all_150_up" : 37,
                "mt_all_150_down" : 38,
                "mt_all_150_mid" : 39,
                "mt_all_250_up" : 40,
                "mt_all_250_down" :41,
                "mt_all_250_mid" : 42,
                "mt_all_350_up" : 43,
                "mt_all_350_down" : 44,
                "mt_all_350_mid" : 45,
                "mt_all_450_up" : 46,
                "mt_all_450_down" : 47,
                "mt_all_450_mid" : 48,
            },
            "et" : {
                "et_inclusive" : 0,
                "et_2jet_vbf" : 1,
                "et_loose" : 2
            },
            "em" : {
                "em_inclusive" : 0,
                "em_2jet_vbf" : 1,
                "em_tight" : 2
            },
            "tt" : {
                "tt_inclusive" : 0,
                "tt_2jet_vbf" : 1,
                "tt_loose" : 2
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

