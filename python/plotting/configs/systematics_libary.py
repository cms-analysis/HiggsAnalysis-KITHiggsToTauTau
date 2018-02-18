# -*- coding: utf-8 -*-

import CombineHarvester.CombineTools.ch as ch

class SystematicLibary(object):
	def __init__(self):
		
	##----------------------------------------------------------lnN uncertanties----------------------------------------------------------##

		##-------------------------------Luminosity-------------------------------##
		
		self.lumi_syst_args = [
			"lumi_$ERA",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.026)
				(       ["13TeV"], 1.027) # CMS-PAS-LUM-15-001
		]
		self.lumi2016_syst_args = [
			"lumi_$ERA",
			"lnN",
			ch.SystMap("era")
				(       ["13TeV"], 1.025)

		]
		##-------------------------------Cross section-------------------------------##
		
		self.ztt_cross_section_syst_args = [
			"CMS_$ANALYSIS_zttNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["7TeV", "8TeV"], ["ZTT", "ZLL", "ZL", "ZJ"], 1.03)
				(       ["13TeV"], ["ZTT", "ZLL", "ZL", "ZJ"], 1.04)
		]
		self.zll_cross_section_syst_args = [
			"CMS_$ANALYSIS_zjXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["ZLL", "ZL", "ZJ"], 1.04) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.ttj_cross_section_syst_args = [
			"CMS_$ANALYSIS_ttjXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				( ["7TeV"], ["TTJ"], 1.08)
				( ["8TeV"], ["TTJ"], 1.1)
				(["13TeV"], ["TTJ", "TT", "TTT", "TTJJ"], 1.06) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581HttNuisanceParamUpdate_2016Apr13.pdf
		]

		self.singlet_cross_section_syst_args = [
			"CMS_$ANALYSIS_singletXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["VV"], 1.04) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.vv_cross_section_syst_args = [
			"CMS_$ANALYSIS_vvXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["7TeV", "8TeV"], ["VV"], 1.15)
				(       ["13TeV"], ["VV", "VVT", "VVJ"], 1.10) # https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.vv_cross_section2016_syst_args = [
			"CMS_$ANALYSIS_vvXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["VV", "VVT", "VVJ"], 1.05) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.wj_cross_section_syst_args = [
			"CMS_$ANALYSIS_wjXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["WJ", "W"], 1.04) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]

		##-------------------------------Efficiencies-------------------------------##
		
		self.trigger_efficiency2016_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L76-L88
			"CMS_eff_trigger_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt", "et"], 1.02)
				(["13TeV"], ["tt"], 1.10)
		]
		self.trigger_efficiency2016_em_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L82-L84
			"CMS_eff_trigger_em_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em", "ttbar"], 1.02)
		]
		self.electron_efficiency_syst_args = [
			"CMS_eff_e",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.02)
				(       ["13TeV"], 1.04) # https://github.com/cms-analysis/CombineHarvester/blob/HIG15007/HIG15007/scripts/setupDatacards.py#L107-L110
		]
		self.electron_efficiency2016_syst_args = [
			"CMS_eff_e",
			"lnN",
			ch.SystMap("era")
				(       ["13TeV"], 1.02) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.muon_efficiency_syst_args = [
			"CMS_eff_m",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.02)
				(       ["13TeV"], 1.03) # https://github.com/cms-analysis/CombineHarvester/blob/HIG15007/HIG15007/scripts/setupDatacards.py#L101-L105
		]
		self.muon_efficiency2016_syst_args = [
			"CMS_eff_m",
			"lnN",
			ch.SystMap("era")
				(       ["13TeV"], 1.02) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.tau_efficiency_corr_syst_args = [
			"CMS_eff_t_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["7TeV", "8TeV"], ["mt", "et"], 1.08)
				(["7TeV", "8TeV"], ["tt"],       1.19)
				(       ["13TeV"], ["mt", "et", "tt"], 1.05) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.tau_efficiency_syst_args = [
			"CMS_eff_t_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["7TeV", "8TeV"], ["mt", "et"], 1.08)
				(["7TeV", "8TeV"], ["tt"],       1.19)
				(       ["13TeV"], ["mt", "et", "tt"], 1.03) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.tau_efficiency2016_corr_syst_args = [
			"CMS_eff_t_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(       ["13TeV"], ["mt", "et"], 1.045) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.tau_efficiency2016_tt_corr_syst_args = [
			"CMS_eff_t_$ERA",
			"lnN",
			ch.SystMap("era", "channel", "process")
				(       ["13TeV"], ["tt"], ["ZTT", "EWKZ", "VVT", "TTT", "ggH", "qqH", "WH", "ZH"], 1.09) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
				(       ["13TeV"], ["tt"], ["ZJ", "VVJ", "TTJJ", "W"], 1.06) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.tau_efficiency2016_syst_args = [
			"CMS_eff_t_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(       ["13TeV"], ["mt", "et"], 1.02) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.tau_efficiency2016_tt_syst_args = [
			"CMS_eff_t_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel", "process")
				(       ["13TeV"], ["tt"], ["ZTT", "EWKZ", "VVT", "TTT", "ggH", "qqH", "WH", "ZH"], 1.04) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
				(       ["13TeV"], ["tt"], ["ZJ", "VVJ", "TTJJ", "W"], 1.02) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.btag_efficiency2016_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L151-L154
			"CMS_htt_eff_b_$ERA",
			"lnN",
			ch.SystMap("era", "channel", "bin", "process")
				(["13TeV"], ["em"], ["TTJ", "TTJJ", "TTT", "TT"], ["em_ZeroJet2D"], 1.035)
				(["13TeV"], ["em"], ["TTJ", "TTJJ", "TTT", "TT"], ["em_Boosted2D", "em_Vbf2D"], 1.05)
				(["13TeV"], ["em"], ["VVJ", "VVT", "VV"], ["em_Boosted2D", "em_Vbf2D"], 1.015)
		]
		
		##-------------------------------Normalization-------------------------------##

		self.zee_norm_syst_args = [
			"CMS_$ANALYSIS_zeeNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["ZLL", "ZL"], 1.03) # Source?
		]
		self.htt_zmm_norm_extrap_0jet = [
			"CMS_htt_zmm_norm_extrap_0jet_$CHANNEL_$ERA", 
			"lnN", 
			ch.SystMap("channel", "era", "process")
				(["em"], ["13TeV"], ["ZTT", "ZLL", "EWKZ"], 1.07)
				(["et"], ["13TeV"], ["ZTT", "ZL", "ZJ", "EWKZ"], 1.07)
				(["mt"], ["13TeV"], ["ZTT", "ZL", "ZJ", "EWKZ"], 1.07)
		]
		self.htt_zmm_norm_extrap_boosted = [
			"CMS_htt_zmm_norm_extrap_boosted_$CHANNEL_$ERA", 
			"lnN", 
			ch.SystMap("channel", "era", "process")
				(["em"], ["13TeV"], ["ZTT", "ZLL", "EWKZ"], 1.07)
				(["et"], ["13TeV"], ["ZTT", "ZL", "ZJ", "EWKZ"], 1.07)
				(["mt"], ["13TeV"], ["ZTT", "ZL", "ZJ", "EWKZ"], 1.07)
		]

		##-------------------------------Scale-------------------------------##

		self.met_scale_syst_args = [
			"CMS_$ANALYSIS_scale_met_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH", "qqH", "WH", "ZH", "VH"], 0.98) # copied from 8TeV
				(["13TeV"], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TTJJ", "TTT", "TT", "VV", "WJ", "W"], 1.03) # copied from 8TeV
		]
		self.boson_scale_met_syst_args = [
			"CMS_$ANALYSIS_boson_scale_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.02)
		]
		self.ewk_top_scale_met_syst_args = [
			"CMS_$ANALYSIS_ewkTop_scale_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.03)
		]
		self.htt_qcd_scale_syst_args = [	# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV2014#s_13_0_TeV
			"QCD_scale_$PROCESS",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH"], 1.079)
				(["13TeV"], ["qqH"], 1.007)
				(["13TeV"], ["VH"], 1.015)
				(["13TeV"], ["WH"], 1.015)
				(["13TeV"], ["ZH"], 1.038)
		]
		self.htt_pdf_scale_syst_args = [
			"PDF_scale_$PROCESS",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH"], 1.071)
				(["13TeV"], ["qqH"], 1.032)
				(["13TeV"], ["VH"], 1.022)
				(["13TeV"], ["WH"], 1.022)
				(["13TeV"], ["ZH"], 1.022)
		]
		self.htt_qcd_scale_qqh_syst_args = [ # for 13 TeV ggH gets shape uncertainty
			"CMS_qqH_QCDUnc",
			"lnN",
			ch.SystMap("channel", "bin", "process")
				(["em"], ["em_ZeroJet2D"], ["qqH"], 0.997)
				(["em"], ["em_Boosted2D"], ["qqH"], 1.004)
				(["em"], ["em_Vbf2D"], ["qqH"], 1.005)
				
				(["et"], ["et_ZeroJet2D"], ["qqH"], 1.003)
				(["et"], ["et_Boosted2D"], ["qqH"], 1.004)
				(["et"], ["et_Vbf2D"], ["qqH"], 1.005)
				
				(["mt"], ["mt_ZeroJet2D"], ["qqH"], 0.998)
				(["mt"], ["mt_Boosted2D"], ["qqH"], 1.002)
				(["mt"], ["mt_Vbf2D"], ["qqH"], 1.002)
				
				(["tt"], ["tt_ZeroJet2D"], ["qqH"], 0.997)
				(["tt"], ["tt_Boosted2D"], ["qqH"], 1.003)
				(["tt"], ["tt_Vbf2D"], ["qqH"], 1.003)
		]
		self.htt_pdf_scale_smhtt_syst_args = [
			"CMS_$PROCESS_PDF",
			"lnN",
			ch.SystMap("channel", "bin", "process")
				(["em"], ["em_ZeroJet2D"], ["ggH"], 1.007)
				(["em"], ["em_Boosted2D"], ["ggH"], 1.007)
				(["em"], ["em_Vbf2D"], ["ggH"], 1.007)
				(["em"], ["em_ZeroJet2D"], ["qqH"], 1.011)
				(["em"], ["em_Boosted2D"], ["qqH"], 1.005)
				(["em"], ["em_Vbf2D"], ["qqH"], 1.005)
				
				(["et"], ["et_ZeroJet2D"], ["ggH"], 1.007)
				(["et"], ["et_Boosted2D"], ["ggH"], 1.007)
				(["et"], ["et_Vbf2D"], ["ggH"], 1.007)
				(["et"], ["et_ZeroJet2D"], ["qqH"], 1.005)
				(["et"], ["et_Boosted2D"], ["qqH"], 1.002)
				(["et"], ["et_Vbf2D"], ["qqH"], 1.005)
				
				(["mt"], ["mt_ZeroJet2D"], ["ggH"], 1.007)
				(["mt"], ["mt_Boosted2D"], ["ggH"], 1.007)
				(["mt"], ["mt_Vbf2D"], ["ggH"], 1.007)
				(["mt"], ["mt_ZeroJet2D"], ["qqH"], 1.005)
				(["mt"], ["mt_Boosted2D"], ["qqH"], 1.002)
				(["mt"], ["mt_Vbf2D"], ["qqH"], 1.005)
				
				(["tt"], ["tt_ZeroJet2D"], ["ggH"], 1.009)
				(["tt"], ["tt_Boosted2D"], ["ggH"], 1.009)
				(["tt"], ["tt_Vbf2D"], ["ggH"], 1.009)
				(["tt"], ["tt_ZeroJet2D"], ["qqH"], 1.008)
				(["tt"], ["tt_Boosted2D"], ["qqH"], 1.003)
				(["tt"], ["tt_Vbf2D"], ["qqH"], 1.005)
		]
		self.ztt_qcd_scale_syst_args = [
			"CMS_$ANALYSIS_QCDscale_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ZTT"], 1.005) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.ztt_qcd_scale_tt_syst_args = [
			"CMS_$ANALYSIS_QCDscale_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(["13TeV"], ["ZTT"], ["tt"], 1.06)
		]
		self.ztt_pdf_scale_syst_args = [
			"CMS_$ANALYSIS_pdf_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ZTT"], 1.015) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]

		##-------------------------------Resolution-------------------------------##

		self.boson_resolution_met_syst_args = [
			"CMS_$ANALYSIS_boson_reso_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.02)
		]
		self.ewk_top_resolution_met_syst_args = [
			"CMS_$ANALYSIS_ewkTop_reso_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.01)
		]
		
		##-------------------------------Fake rate-------------------------------##
		
		self.zllFakeTau_syst_args = [
			"CMS_$ANALYSIS_eFakeTau_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(["7TeV", "8TeV"], ["ZLL"], ["mt", "et"], 1.30)
				(       ["13TeV"], ["ZLL", "ZL", "ZJ"], ["mt", "tt"], 1.15) #CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
				(       ["13TeV"], ["ZLL", "ZL", "ZJ"], ["et"], 1.30) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.eFakeTau_vloose_syst_args = [
			"CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(       ["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.eFakeTau_tight_syst_args = [
			"CMS_$ANALYSIS_rate_eFakeTau_tight_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(       ["13TeV"], ["ZLL", "ZL"], ["et"], 1.30) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.eFakeTau2016_syst_args = [
			"CMS_$ANALYSIS_eFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["ZLL", "ZL"], 1.12) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.muFakeTau_syst_args = [
			"CMS_$ANALYSIS_mFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZLL", "ZL"], 2.00) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.muFakeTau2016_syst_args = [
			"CMS_$ANALYSIS_mFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZLL", "ZL"], 1.25) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.zjFakeTau_syst_args = [
			"CMS_$ANALYSIS_zjFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZLL", "ZL"], 1.30) # From Yuta's polarisation analysis
		]
		self.jetFakeTau_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZJ", "TTJJ", "VVJ"], 1.20)
		]		

		##-------------------------------QCD-------------------------------##
		
		self.ttj_extrapol_syst_args = [
			"CMS_$ANALYSIS_ttjExtrapol_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["TTJ", "TT"], 1.10) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.wj_extrapol_syst_args = [
			"CMS_$ANALYSIS_wjExtrapol_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["WJ", "W"], 1.2) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.qcd_syst_args = [
			"CMS_$ANALYSIS_qcdSyst_$BIN_$ERA",
			"lnN",
			ch.SystMap("era", "process", "bin")
				(["13TeV"], ["QCD"], ["mt_inclusive", "et_inclusive"], 1.06) # copied from 8TeV

				(["13TeV"], ["QCD"], ["mt_0jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_0jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_1jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_1jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_2jet_vbf"], 1.3) # copied from 8TeV

				(["13TeV"], ["QCD"], ["et_0jet_high"], 1.06) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_0jet_low"], 1.06) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_1jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_1jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_2jet_vbf"], 1.3) # copied from 8TeV

				(["13TeV"], ["QCD"], ["tt_inclusive"], 1.35) # copied from 8TeV
		]
		self.qcd_syst_inclusive_args = [
			"CMS_$ANALYSIS_qcdSyst_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["QCD"], 1.10)
		]
		self.htt_QCD_0jet_syst_args = [
			"CMS_htt_QCD_0jet_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("channel", "era", "process")
				(["em"], ["13TeV"], ["QCD"], 1.10)
		]
		self.htt_QCD_boosted_syst_args = [
			"CMS_htt_QCD_boosted_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("channel", "era", "process")
				(["em"], ["13TeV"], ["QCD"], 1.20)
		]	
		self.QCD_Extrap_Iso_nonIso_syst_args = [
			"CMS_QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("channel", "era", "process")
				(["mt"], ["13TeV"], ["QCD"], 1.20)
				(["et"], ["13TeV"], ["QCD"], 1.20)
		]
		self.WHighMTtoLowMT_0jet_syst_args = [
			"CMS_WHighMTtoLowMT_0jet_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("channel", "era", "process")
				(["mt"], ["13TeV"], ["W"], 1.10)
				(["et"], ["13TeV"], ["W"], 1.10)
		]
		self.WHighMTtoLowMT_boosted_syst_args = [
			"CMS_WHighMTtoLowMT_boosted_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("channel", "era", "process")
				(["mt"], ["13TeV"], ["W"], 1.05)
				(["et"], ["13TeV"], ["W"], 1.05)
		]

		##-------------------------------Theoretical uncertanty-------------------------------##

		self.lfv_BR_syst_args = [
			"CMS_lfv_BR_$PROCESS_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["zem"], 1.00)
				(["13TeV"], ["zet"], 1.00)
				(["13TeV"], ["zmt"], 1.00)
				
		]
	
		##-------------------------------Uncategorized-------------------------------##
		
		self.CMS_ggH_STXSVBF2j_syst_args = [
			"CMS_ggH_STXSVBF2j",
			"lnN",
			ch.SystMap("bin", "process")
				(["em_ZeroJet2D"], ["ggH"], 1.000)
				(["em_Boosted2D"], ["ggH"], 1.000)
				(["em_dijet_boosted"], ["ggH", "gghjhusm", "gghjhumm", "gghjhups"], 1.2)
				(["em_dijet_lowM"], ["ggH", "gghjhusm", "gghjhumm", "gghjhups"], 1.2)
				(["em_dijet_highM"], ["ggH", "gghjhusm", "gghjhumm", "gghjhups"], 1.2)
				(["em_dijet_lowMjj"], ["ggH", "gghjhusm", "gghjhumm", "gghjhups"], 1.2)

				(["et_ZeroJet2D"], ["ggH"], 1.000)
				(["et_Boosted2D"], ["ggH"], 1.000)
				(["et_Vbf2D"], ["ggH"], 1.2)
				
				(["mt_ZeroJet2D"], ["ggH"], 1.000)
				(["mt_Boosted2D"], ["ggH"], 1.000)
				(["mt_Vbf2D"], ["ggH"], 1.2)
				
				(["tt_ZeroJet2D"], ["ggH"], 1.000)
				(["tt_Boosted2D"], ["ggH"], 1.000)
				(["tt_Vbf2D"], ["ggH"], 1.2) 								
		]
		self.htt_ueps_smhtt_syst_args = [
			"CMS_$PROCESS_UEPS",
			"lnN",
			ch.SystMap("channel", "bin", "process")
				(["em"], ["em_ZeroJet2D"], ["ggH"], 1.015)
				(["em"], ["em_Boosted2D"], ["ggH"], 0.945)
				(["em"], ["em_Vbf2D"], ["ggH"], 1.03)
				(["em"], ["em_ZeroJet2D"], ["qqH"], 1.015)
				(["em"], ["em_Boosted2D"], ["qqH"], 0.945)
				(["em"], ["em_Vbf2D"], ["qqH"], 1.03)
				
				(["et"], ["et_ZeroJet2D"], ["ggH"], 1.015)
				(["et"], ["et_Boosted2D"], ["ggH"], 0.945)
				(["et"], ["et_Vbf2D"], ["ggH"], 1.03)
				(["et"], ["et_ZeroJet2D"], ["qqH"], 1.015)
				(["et"], ["et_Boosted2D"], ["qqH"], 0.945)
				(["et"], ["et_Vbf2D"], ["qqH"], 1.03)
				
				(["mt"], ["mt_ZeroJet2D"], ["ggH"], 1.015)
				(["mt"], ["mt_Boosted2D"], ["ggH"], 0.945)
				(["mt"], ["mt_Vbf2D"], ["ggH"], 1.03)
				(["mt"], ["mt_ZeroJet2D"], ["qqH"], 1.015)
				(["mt"], ["mt_Boosted2D"], ["qqH"], 0.945)
				(["mt"], ["mt_Vbf2D"], ["qqH"], 1.03)
				
				(["tt"], ["tt_ZeroJet2D"], ["ggH"], 1.015)
				(["tt"], ["tt_Boosted2D"], ["ggH"], 0.945)
				(["tt"], ["tt_Vbf2D"], ["ggH"], 1.03)
				(["tt"], ["tt_ZeroJet2D"], ["qqH"], 1.015)
				(["tt"], ["tt_Boosted2D"], ["qqH"], 0.945)
				(["tt"], ["tt_Vbf2D"], ["qqH"], 1.03)
		]
		self.htt_ueps_syst_args = [# CMS AN-13-262 (v8, table 3)
			"UEPS",
			"lnN",
			ch.SystMap("era", "process", "bin")
				(["13TeV"], ["ggH"], ["mt_0jet_high"], 1.060) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_0jet_low"], 1.073) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_1jet_high"], 0.996) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_1jet_low"], 1.007) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_2jet_vbf"], 0.988) # copied from 8TeV

				(["13TeV"], ["ggH"], ["et_0jet_high"], 1.060) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_0jet_low"], 1.073) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_1jet_high"], 0.996) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_1jet_low"], 1.007) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_2jet_vbf"], 0.988) # copied from 8TeV

				(["13TeV"], ["ggH"], ["em_0jet_high"], 1.063) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_0jet_low"], 1.089) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_1jet_high"], 1.004) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_1jet_low"], 1.000) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_2jet_vbf"], 0.988) # copied from 8TeV

				(["13TeV"], ["ggH"], ["tt_inclusive"], 1.025) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_0jet_high"], 1.028) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_0jet_low"], 1.018) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_1jet_high"], 0.954) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_1jet_low"], 0.946) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_2jet_vbf"], 0.893) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_0jet_high"], 1.028) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_0jet_low"], 1.018) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_1jet_high"], 0.954) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_1jet_low"], 0.946) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_2jet_vbf"], 0.893) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_0jet_high"], 1.042) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_0jet_low"], 1.035) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_1jet_high"], 0.978) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_1jet_low"], 0.984) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_2jet_vbf"], 0.893) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["tt_inclusive"], 1.025) # copied from 8TeV
		]

	##----------------------------------------------------------Shape uncertanties----------------------------------------------------------##
		
		##-------------------------------Fake Taus-------------------------------##		
		
		self.mFakeTau_1prong_syst_args = [
			"CMS_mFakeTau_1prong_$ERA",
			"shape",
			ch.SystMap("channel", "era", "process")
				(["mt"], ["13TeV"], ["ZL"], 1.0)
		]
		self.mFakeTau_1prong1pizero_syst_args = [
			"CMS_mFakeTau_1prong1pizero_$ERA",
			"shape",
			ch.SystMap("channel", "era", "process")
				(["mt"], ["13TeV"], ["ZL"], 1.0)
		]
		self.eFakeTau_1prong_syst_args = [
			"CMS_eFakeTau_1prong_$ERA",
			"shape",
			ch.SystMap("channel", "era", "process")
				(["et"], ["13TeV"], ["ZL"], 1.0)
		]
		self.eFakeTau_1prong1pizero_syst_args = [
			"CMS_eFakeTau_1prong1pizero_$ERA",
			"shape",
			ch.SystMap("channel", "era", "process")
				(["et"], ["13TeV"], ["ZL"], 1.0)
		]
		self.jetFakeTau_qcd_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_qcd_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_w_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_w_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_tt_corr_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_tt_corr_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_tt_stat_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_tt_stat_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_qcd_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_qcd_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_tt_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_tt_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_w_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_w_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_dy_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_dy_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		
		##-------------------------------Energy scale-------------------------------##		
		
		self.tau_es_syst_args = [
			"CMS_scale_t_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt"], 1.0)
				(["13TeV"], ["et"], 1.0)
				(["13TeV"], ["tt"], 1.0)
		]
		self.tau_es_corr_syst_args = [
			"CMS_scale_t_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.ele_es_syst_args = [
			"CMS_scale_e_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em"], 1.0)
				(["13TeV"], ["et"], 1.0)
		]
		self.mu_es_syst_args = [
			"CMS_scale_m_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em"], 1.0)
				(["13TeV"], ["mt"], 1.0)
		]
		self.probetau_es_syst_args = [
			"CMS_scale_probetau_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		self.probeele_es_syst_args = [
			"CMS_scale_probeele_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		self.tagele_es_syst_args = [
			"CMS_scale_tagele_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		self.muFakeTau_es_syst_args = [
			"CMS_$ANALYSIS_scale_mFakeTau_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt"], 1.0)
		]
		self.eleFakeTau_es_syst_args = [
			"CMS_$ANALYSIS_scale_eFakeTau_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		self.jec_syst_args = [
			"CMS_scale_j_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]

		##-------------------------------Shape-------------------------------##
		
		self.dy_shape_syst_args = [
			"CMS_htt_dyShape_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.zl_shape_1prong_syst_args = [
			"CMS_ZLShape_$CHANNEL_1prong_$ERA",
			"shape",
			ch.SystMap("channel", "era", "process")
				(["et"], ["13TeV"], ["ZL"], 1.0)
				(["mt"], ["13TeV"], ["ZL"], 1.0)
		]
		self.zl_shape_1prong1pizero_syst_args = [
			"CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA",
			"shape",
			ch.SystMap("channel", "era", "process")
				(["et"], ["13TeV"], ["ZL"], 1.0)
				(["mt"], ["13TeV"], ["ZL"], 1.0)
		]

		##-------------------------------Scale-------------------------------##

		self.scale_t_1prong_syst_args = [
			"CMS_scale_t_1prong_$ERA",
			"shape",
			ch.SystMap("channel", "era")
				(["et"], ["13TeV"], 1.0)
				(["mt"], ["13TeV"], 1.0)
				(["tt"], ["13TeV"], 1.0)
		]
		self.scale_t_3prong_syst_args = [
			"CMS_scale_t_3prong_$ERA",
			"shape",
			ch.SystMap("channel", "era")
				(["et"], ["13TeV"], 1.0)
				(["mt"], ["13TeV"], 1.0)
				(["tt"], ["13TeV"], 1.0)
		]
		self.scale_t_1prong1pizero_syst_args = [
			"CMS_scale_t_1prong1pizero_$ERA",
			"shape",
			ch.SystMap("channel", "era")
				(["et"], ["13TeV"], 1.0)
				(["mt"], ["13TeV"], 1.0)
				(["tt"], ["13TeV"], 1.0)
		]

		##-------------------------------QCD-------------------------------##

		self.btag_mistag_syst_args = [
			"CMS_mistag_b_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em","et","mt"], 1.0)
		]
		self.btag_efficiency_syst_args = [
			"CMS_eff_b_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em","et","mt"], 1.0)
		]
		self.ttj_syst_args = [
			"CMS_htt_ttbarShape_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.htt_jetFakeLep_syst_args = [
			"CMS_htt_jetFakeLep_$ERA",
			"lnN",
			ch.SystMap("channel", "era", "process")
				(["em"], ["13TeV"], ["W"], 1.20)
		]
		
		##-------------------------------Uncategorized-------------------------------##
	
		self.met_resp_syst_args = [
			"CMS_scale_met_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em"], 1.0)
				(["13TeV"], ["et"], 1.0)
				(["13TeV"], ["mt"], 1.0)
				(["13TeV"], ["tt"], 1.0)
		]
		self.massres_syst_args = [
			"CMS_scale_massRes_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]


	##----------------------------------Member function for retrieving systematics information for your analysis----------------------------------##

	def get_LFV_systs(self, channel, lnN = False, shape = False):
	
		##Define background processes
		
		all_mc_bkgs = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]
		all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "hww_gg125", "hww_qq125"]	
		
		##Define dictionary for with channel as keys, where a list is saved as [systematic, processes, category]. If no special category is choosen, an empty string "" is given

		lnN_syst = {
			"em": [
				[self.trigger_efficiency2016_em_syst_args, 	["zem"]+all_mc_bkgs,			""],
				[self.electron_efficiency2016_syst_args, 	["zem"]+all_mc_bkgs,			""],
				[self.muon_efficiency2016_syst_args,		["zem"]+all_mc_bkgs, 			""],
				[self.lumi2016_syst_args, 			["ZL", "ZJ", "ZLL"], 			""],
				[self.htt_jetFakeLep_syst_args, 		["W"], 					""],
				[self.htt_QCD_0jet_syst_args,			["QCD"],				"em_LFVZeroJet"],
				[self.htt_QCD_boosted_syst_args,		["QCD"],				"em_LFVJet"],
				[self.htt_zmm_norm_extrap_0jet,			["ZTT", "ZLL", "EWKZ"],			"em_LFVZeroJet"],
				[self.ttj_cross_section_syst_args,		["TT", "TTT", "TTJJ"],			""],				
				[self.vv_cross_section2016_syst_args, 		["VV", "VVT", "VVJ"], 			""]
			],

			"et": [
				[self.trigger_efficiency2016_syst_args, 	["zet"]+all_mc_bkgs_no_W,		""],
				[self.electron_efficiency2016_syst_args, 	["zet"]+all_mc_bkgs_no_W,		""],
				[self.tau_efficiency2016_syst_args,		["zet"]+all_mc_bkgs, 		""],
				[self.lumi2016_syst_args, 			["ZL", "ZJ", "ZLL", "ZTT"], 		""],
				[self.tau_efficiency2016_corr_syst_args, 	["zet"]+all_mc_bkgs, 		""],
				[self.QCD_Extrap_Iso_nonIso_syst_args,		["QCD"],				""],
				[self.WHighMTtoLowMT_0jet_syst_args,		["W"],					"et_LFVZeroJet"],
				[self.WHighMTtoLowMT_boosted_syst_args,		["W"],					"et_LFVJet"],
				[self.htt_zmm_norm_extrap_0jet,			["ZTT", "ZL", "ZJ", "EWKZ"],		"et_LFVZeroJet"],
				[self.ttj_cross_section_syst_args,		["TT", "TTT", "TTJJ"],			""],
				[self.vv_cross_section2016_syst_args, 		["VV", "VVT", "VVJ"], 			""]
			],
				
			"mt": [
				[self.trigger_efficiency2016_syst_args, 	["zmt"]+all_mc_bkgs_no_W,		""],
				[self.muon_efficiency2016_syst_args, 		["zmt"]+all_mc_bkgs_no_W,		""],
				[self.tau_efficiency2016_syst_args,		["zmt"]+all_mc_bkgs, 		""],
				[self.lumi2016_syst_args, 			["ZL", "ZJ", "ZLL", "ZTT"], 		""],
				[self.tau_efficiency2016_corr_syst_args, 	["zmt"]+all_mc_bkgs, 		""],
				[self.QCD_Extrap_Iso_nonIso_syst_args,		["QCD"],				""],
				[self.WHighMTtoLowMT_0jet_syst_args,		["W"],					"mt_LVFZeroJet"],
				[self.WHighMTtoLowMT_boosted_syst_args,		["W"],					"mt_LFVJet"],
				[self.htt_zmm_norm_extrap_0jet,			["ZTT", "ZL", "ZJ", "EWKZ"],		"mt_LFVZeroJet"],
				[self.ttj_cross_section_syst_args,		["TT", "TTT", "TTJJ"],			""],
				[self.vv_cross_section2016_syst_args, 		["VV", "VVT", "VVJ"], 			""]	
			]
						
		}


		shape_syst = {
				"em" : [],
					
				"et": [
					[self.zl_shape_1prong_syst_args,		["ZL"],					""],
					[self.zl_shape_1prong1pizero_syst_args,		["ZL"],					""],
				],
					
				"mt": [	
					[self.zl_shape_1prong_syst_args,		["ZL"],					""],
					[self.zl_shape_1prong1pizero_syst_args,		["ZL"],					""],
					[self.mFakeTau_1prong_syst_args,		["ZL"], 				""],
					[self.scale_t_1prong_syst_args,			["zmt"]+all_mc_bkgs,		""],
					[self.scale_t_3prong_syst_args,			["zmt"]+all_mc_bkgs, 		""],
					[self.scale_t_1prong1pizero_syst_args,		["zmt"]+all_mc_bkgs,		""]
				]
		}
			
			
		##Check which systematic should be returned

		if lnN:	
			return lnN_syst[channel]

		if shape: 
			return shape_syst[channel]
			
			
			
			
