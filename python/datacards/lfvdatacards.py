# -*- coding: utf-8 -*-

import CombineHarvester.CombineTools.ch as ch

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as SystLib


class LFVDatacards(datacards.Datacards):
	def __init__(self, channel_list, signal_list, category_list, cb=None, lnN_syst_enable = False, shape_syst_enable = False):
		super(LFVDatacards, self).__init__(cb)
		
		if cb is None:
			
			###Define all background processes for each channel

			backgrounds = {
					"em": ["ZTT", "ZLL", "EWKZ", "TT", "VV", "hww_gg125", "hww_qq125", "W", "QCD"],
					"et": ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"],
					"mt": ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			}
			
			##Generate instance of systematic libary, in which the relevant information about the systematics are safed

			systematics_list = SystLib.SystematicLibary()		
			
			###Fill Combine Harvester object with relevant information
			
			for channel in channel_list:
			
				###Add channels as process in Combine Harvester			
	
				self.add_processes(
					channel=channel,
					categories= [channel + "_" + category for category in category_list],
					bkg_processes=backgrounds[channel],  
					sig_processes= [self.configs.sample2process(signal) for signal in signal_list],
					analysis=["LFV"],
					era=["13TeV"],
					mass=["125"]
					)					

				###Add lnN/shape uncertanty for each channel, process and category

				if lnN_syst_enable:
					for (systematic, process, category) in systematics_list.get_LFV_systs(channel, lnN = lnN_syst_enable):
						if category == "":
							self.cb.cp().channel([channel]).process(process).AddSyst(self.cb, *systematic)
						else:
							self.cb.cp().channel([channel]).process(process).bin([category]).AddSyst(self.cb, *systematic)
			
				if shape_syst_enable:
					for (systematic, process, category) in systematics_list.get_LFV_systs(channel, shape = shape_syst_enable):
						if category == "":
							self.cb.cp().channel([channel]).process(process).AddSyst(self.cb, *systematic)
						else:
							self.cb.cp().channel([channel]).process(process).bin([category]).AddSyst(self.cb, *systematic)
			

	
