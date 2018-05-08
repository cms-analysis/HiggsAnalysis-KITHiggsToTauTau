# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase
import HiggsAnalysis.KITHiggsToTauTau.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class CalculateWJetsOSSSFactor(estimatebase.EstimateBase):
    def __init__(self):
    	super(CalculateWJetsOSSSFactor, self).__init__()

    def modify_argument_parser(self, parser, args):
    	super(CalculateWJetsOSSSFactor, self).modify_argument_parser(parser, args)
    		
    	self.calculate_wjets_osss_factor_options = parser.add_argument_group("WJets estimation options")
    	self.calculate_wjets_osss_factor_options.add_argument("--wjets-from-mc-os-nicks", nargs="+",
                default=["wj_mc_os"],
                help="Nicks for Wjets estimate in opposite-sign region. [Default: %(default)s]")
    	self.calculate_wjets_osss_factor_options.add_argument("--wjets-from-mc-ss-nicks", nargs="+",
                default=["wj_mc_ss"],
                help="Nicks for Wjets estimate in same-sign region. [Default: %(default)s]")
               
                    
    def prepare_args(self, parser, plotData):
        super(CalculateWJetsOSSSFactor, self).prepare_args(parser, plotData)
        self._plotdict_keys = ["wjets_from_mc_os_nicks", "wjets_from_mc_ss_nicks"]
        self.prepare_list_args(plotData, self._plotdict_keys)
            
	def run(self, plotData=None):
		super(CalculateWJetsOSSSFactor, self).run(plotData)
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif not isinstance(nick, bool):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
		
        for wjets_from_mc_os_nicks, wjets_from_mc_ss_nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
         
            yield_wj_mc_os = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_from_mc_os_nicks])()
            yield_wj_mc_ss = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_from_mc_ss_nicks])()
            # make sure we don't have negative yields
            	
            yield_wj_mc_os = uncertainties.ufloat(max(0.0, yield_wj_mc_os.nominal_value), yield_wj_mc_os.std_dev)
            yield_wj_mc_ss = uncertainties.ufloat(max(0.0, yield_wj_mc_ss.nominal_value), yield_wj_mc_ss.std_dev)
            print(yield_wj_mc_os, yield_wj_mc_ss)
            assert (yield_wj_mc_os != 0.0) or (yield_wj_mc_ss != 0.0)
			# the final yield in the signal region is N_data, WJ^{SR} = N_data, WJ^{CR} * N_MC,WJ^{SR} / N_MC,WJ^{CR}
            os_ss_factor = yield_wj_mc_os / yield_wj_mc_ss
            
            plotData.metadata[wjets_from_mc_os_nicks] = {
				"os_ss_factor" : os_ss_factor.nominal_value,
				"os_ss_factor_unc" : os_ss_factor.std_dev,
				"yield_unc_rel" : abs(os_ss_factor.std_dev/os_ss_factor.nominal_value if os_ss_factor.nominal_value != 0.0 else 0.0),
			}
            plotData.metadata
            print(plotData.metadata)
			# # scale the wj file by the ratio of the estimated yield and the yield given by MC.
			# integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_shape_nick])()
			# if integral_shape != 0.0:
			# 	scale_factor = final_yield / integral_shape
			# 	log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_shape_nick, scale_factor=scale_factor))
			# 	plotData.plotdict["root_objects"][wjets_shape_nick].Scale(scale_factor.nominal_value)
            # 
