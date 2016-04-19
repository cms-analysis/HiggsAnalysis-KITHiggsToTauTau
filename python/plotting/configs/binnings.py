
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.binnings as binnings


class BinningsDict(binnings.BinningsDict):
	def __init__(self, additional_binnings=None):
		super(BinningsDict, self).__init__(additional_binnings=additional_binnings)

		self.binnings_dict["diLepMass"] = "50,0,250"
		self.binnings_dict["svfitMass"] = "50,0,250"
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			self.binnings_dict[channel+"_integral"] = "1,0.0,1.0"
			for i in range(16):
				self.binnings_dict[channel+"_MVATestMethod_%i"%i] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
		for ch in ["ee_", "em_", "et_", "mm_", "mt_", "tt_"]:
			self.binnings_dict[ch+"all_vs_all"] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
			self.binnings_dict[ch+"all_vs_zll"] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
			self.binnings_dict[ch+"all_vs_ztt"] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
			self.binnings_dict[ch+"ggh_vs_zll"] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
			self.binnings_dict[ch+"ggh_vs_ztt"] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
			self.binnings_dict[ch+"vbf_vs_zll"] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
			self.binnings_dict[ch+"vbf_vs_ztt"] = "-1.0 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.75 1"
		self.binnings_dict["tt_decayMode_1"] = "11,0.0,11.0"
		self.binnings_dict["tt_decayMode_2"] = "11,0.0,11.0"
		self.binnings_dict["tt_eta_1"] = "10,-2.1,2.1"
		self.binnings_dict["tt_eta_2"] = "10,-2.1,2.1"
		self.binnings_dict["tt_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["tt_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["tt_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["tt_iso_1"] = "25,0.0,2.0"
		self.binnings_dict["tt_iso_2"] = "25,0.0,2.0"
		self.binnings_dict["tt_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["tt_jeta_1"] = "10,-4.7,4.7"
		self.binnings_dict["tt_jeta_2"] = "10,-4.7,4.7"
		self.binnings_dict["tt_jphi_1"] = "10,-3.2,3.2"
		self.binnings_dict["tt_jphi_2"] = "10,-3.2,3.2"
		self.binnings_dict["tt_jpt_1"] = "20,20.0,250.0"
		self.binnings_dict["tt_jpt_2"] = "20,20.0,250.0"
		self.binnings_dict["tt_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["tt_m_2"] = "25,0.0,2.5"
		self.binnings_dict["tt_m_ll"] = "60,0.0,300"
		self.binnings_dict["tt_m_llmet"] = "60,0.0,400"
		self.binnings_dict["tt_m_sv"] = "25,0.0,250"
		self.binnings_dict["tt_met"] = "40,0.0,200.0"
		self.binnings_dict["tt_metcov00"] = "25,0.0,1000.0"
		self.binnings_dict["tt_metcov01"] = "25,-500.0,500.0"
		self.binnings_dict["tt_metcov10"] = "25,-500.0,500.0"
		self.binnings_dict["tt_metcov11"] = "25,0.0,1000.0"
		self.binnings_dict["tt_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["tt_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["tt_mt_1"] = "30,0.0,150"
		self.binnings_dict["tt_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["tt_mt_ll"] = "25,75.0,300"
		self.binnings_dict["tt_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["tt_mvacov00"] = "30,0.0,40.0"
		self.binnings_dict["tt_mvacov01"] = "30,-15.0,15.0"
		self.binnings_dict["tt_mvacov10"] = "30,-15.0,15.0"
		self.binnings_dict["tt_mvacov11"] = "30,0.0,40.0"
		self.binnings_dict["tt_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["tt_mvametcov00"] = "25,0.0,1000.0"
		self.binnings_dict["tt_mvametcov01"] = "25,-500.0,500.0"
		self.binnings_dict["tt_mvametcov10"] = "25,-500.0,500.0"
		self.binnings_dict["tt_mvametcov11"] = "25,0.0,1000.0"
		self.binnings_dict["tt_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["tt_m_vis"] = "60,0.0,300"
		self.binnings_dict["tt_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["tt_njetspt30"] = "8,-0.5,7.5"
		self.binnings_dict["tt_njets"] = "8,-0.5,7.5"
		self.binnings_dict["tt_nbtag"] = "4,-0.5,3.5"
		self.binnings_dict["tt_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["tt_npu"] = "30,0.0,60.0"
		self.binnings_dict["tt_npv"] = "30,0.0,60.0"
		self.binnings_dict["tt_phi_1"] = "10,-3.2,3.2"
		self.binnings_dict["tt_phi_2"] = "10,-3.2,3.2"
		self.binnings_dict["tt_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["tt_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["tt_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["tt_pt_1"] = "20,45.0,145.0"
		self.binnings_dict["tt_pt_2"] = "20,45.0,145.0"
		self.binnings_dict["tt_pt_ll"] = "25,0.0,250"
		self.binnings_dict["tt_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["tt_pt_sv"] = "25,0.0,250"
		self.binnings_dict["tt_pt_tt"] = "20,0.0,200"
		self.binnings_dict["tt_puweight"] = "20,0.0,2.0"
		self.binnings_dict["tt_rho"] = "25,0.0,50.0"
		self.binnings_dict["tt_svfitMass"] = "30,0.0,300"
		self.binnings_dict["tt_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["tt_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["tt_pZetaMissVis"] = "50,-150.0,100.0"
		self.binnings_dict["tt_pzetamiss"] = "50,-150.0,100.0"
		self.binnings_dict["tt_pzetavis"] = "20,0.0,100.0"
		self.binnings_dict["tt_metProjectionPar"] = "20,-100.0,300.0"
		self.binnings_dict["tt_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["tt_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["mt_decayMode_2"] = "11,0.0,11.0"
		self.binnings_dict["mt_eta_1"] = "20,-2.1,2.1"
		self.binnings_dict["mt_eta_2"] = "20,-2.3,2.3"
		self.binnings_dict["mt_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["mt_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["mt_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["mt_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["mt_iso_2"] = "25,0.0,2.0"
		self.binnings_dict["mt_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["mt_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["mt_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["mt_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mt_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mt_jpt_1"] = "20,20.0,250.0"
		self.binnings_dict["mt_jpt_2"] = "20,20.0,250.0"
		self.binnings_dict["mt_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["mt_m_2"] = "25,0.0,2.5"
		self.binnings_dict["mt_m_ll"] = "60,0.0,300"
		self.binnings_dict["mt_m_llmet"] = "60,0.0,400"
		self.binnings_dict["mt_m_sv"] = "25,0.0,250"
		self.binnings_dict["mt_met"] = "40,0.0,200.0"
		self.binnings_dict["mt_metcov00"] = "25,0.0,1000.0"
		self.binnings_dict["mt_metcov01"] = "25,-500.0,500.0"
		self.binnings_dict["mt_metcov10"] = "25,-500.0,500.0"
		self.binnings_dict["mt_metcov11"] = "25,0.0,1000.0"
		self.binnings_dict["mt_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["mt_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["mt_metProjectionPar"] = "20,-100.0,300.0"
		self.binnings_dict["mt_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["mt_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["mt_mt_1"] = "30,0.0,150"
		self.binnings_dict["mt_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["mt_mt_ll"] = "25,75.0,300"
		self.binnings_dict["mt_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["mt_mvacov00"] = "30,0.0,40.0"
		self.binnings_dict["mt_mvacov01"] = "30,-15.0,15.0"
		self.binnings_dict["mt_mvacov10"] = "30,-15.0,15.0"
		self.binnings_dict["mt_mvacov11"] = "30,0.0,40.0"
		self.binnings_dict["mt_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["mt_mvametcov00"] = "25,0.0,1000.0"
		self.binnings_dict["mt_mvametcov01"] = "25,-500.0,500.0"
		self.binnings_dict["mt_mvametcov10"] = "25,-500.0,500.0"
		self.binnings_dict["mt_mvametcov11"] = "25,0.0,1000.0"
		self.binnings_dict["mt_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["mt_m_vis"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])
		self.binnings_dict["mt_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["mt_njetspt30"] = "8,-0.5,7.5"
		self.binnings_dict["mt_njets"] = "8,-0.5,7.5"
		self.binnings_dict["mt_nbtag"] = "4,-0.5,3.5"
		self.binnings_dict["mt_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["mt_npu"] = "30,0.0,60.0"
		self.binnings_dict["mt_npv"] = "30,0.0,60.0"
		self.binnings_dict["mt_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mt_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mt_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["mt_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["mt_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["mt_pt_1"] = "20,18.0,118.0"
		self.binnings_dict["mt_pt_2"] = "20,20.0,120.0"
		self.binnings_dict["mt_pt_ll"] = "25,0.0,250"
		self.binnings_dict["mt_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["mt_pt_sv"] = "25,0.0,250"
		self.binnings_dict["mt_pt_tt"] = "20,0.0,200"
		self.binnings_dict["mt_puweight"] = "20,0.0,2.0"
		self.binnings_dict["mt_rho"] = "25,0.0,50.0"
		self.binnings_dict["mt_svfitMass"] = "30,0.0,300"
		self.binnings_dict["mt_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["mt_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["mt_pZetaMissVis"] = "50,-150.0,100.0"
		self.binnings_dict["mt_pzetamiss"] = "50,-150.0,100.0"
		self.binnings_dict["mt_pzetavis"] = "20,0.0,100.0"
		self.binnings_dict["mt_metProjectionPar"] = "21,-20.0,200.0"
		self.binnings_dict["mt_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["mt_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["et_decayMode_2"] = "11,0.0,11.0"
		self.binnings_dict["et_eta_1"] = "20,-2.1,2.1"
		self.binnings_dict["et_eta_2"] = "20,-2.3,2.3"
		self.binnings_dict["et_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["et_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["et_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["et_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["et_iso_2"] = "25,0.0,2.0"
		self.binnings_dict["et_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["et_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["et_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["et_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["et_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["et_jpt_1"] = "20,20.0,250.0"
		self.binnings_dict["et_jpt_2"] = "20,20.0,250.0"
		self.binnings_dict["et_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["et_m_2"] = "25,0.0,2.5"
		self.binnings_dict["et_m_ll"] = "60,0.0,300"
		self.binnings_dict["et_m_llmet"] = "60,0.0,400"
		self.binnings_dict["et_m_sv"] = "25,0.0,250"
		self.binnings_dict["et_met"] = "40,0.0,200.0"
		self.binnings_dict["et_metcov00"] = "25,0.0,1000.0"
		self.binnings_dict["et_metcov01"] = "25,-500.0,500.0"
		self.binnings_dict["et_metcov10"] = "25,-500.0,500.0"
		self.binnings_dict["et_metcov11"] = "25,0.0,1000.0"
		self.binnings_dict["et_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["et_metProjectionPar"] = "20,-100.0,300.0"
		self.binnings_dict["et_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["et_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["et_mt_1"] = "30,0.0,150"
		self.binnings_dict["et_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["et_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["et_mt_ll"] = "25,75.0,300"
		self.binnings_dict["et_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["et_mvacov00"] = "30,0.0,40.0"
		self.binnings_dict["et_mvacov01"] = "30,-15.0,15.0"
		self.binnings_dict["et_mvacov10"] = "30,-15.0,15.0"
		self.binnings_dict["et_mvacov11"] = "30,0.0,40.0"
		self.binnings_dict["et_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["et_mvametcov00"] = "25,0.0,1000.0"
		self.binnings_dict["et_mvametcov01"] = "25,-500.0,500.0"
		self.binnings_dict["et_mvametcov10"] = "25,-500.0,500.0"
		self.binnings_dict["et_mvametcov11"] = "25,0.0,1000.0"
		self.binnings_dict["et_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["et_m_vis"] = "60,0.0,300"
		self.binnings_dict["et_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["et_njetspt30"] = "8,-0.5,7.5"
		self.binnings_dict["et_njets"] = "8,-0.5,7.5"
		self.binnings_dict["et_nbtag"] = "4,-0.5,3.5"
		self.binnings_dict["et_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["et_npu"] = "30,0.0,60.0"
		self.binnings_dict["et_npv"] = "30,0.0,60.0"
		self.binnings_dict["et_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["et_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["et_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["et_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["et_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["et_pt_1"] = "20,23.0,123.0"
		self.binnings_dict["et_pt_2"] = "20,20.0,120.0"
		self.binnings_dict["et_pt_ll"] = "25,0.0,250"
		self.binnings_dict["et_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["et_pt_sv"] = "25,0.0,250"
		self.binnings_dict["et_pt_tt"] = "20,0.0,200"
		self.binnings_dict["et_puweight"] = "20,0.0,2.0"
		self.binnings_dict["et_rho"] = "25,0.0,50.0"
		self.binnings_dict["et_svfitMass"] = "30,0.0,300"
		self.binnings_dict["et_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["et_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["et_pZetaMissVis"] = "50,-150.0,100.0"
		self.binnings_dict["et_pzetamiss"] = "50,-150.0,100.0"
		self.binnings_dict["et_pzetavis"] = "20,0.0,100.0"
		self.binnings_dict["et_metProjectionPar"] = "21,-20.0,200.0"
		self.binnings_dict["et_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["et_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["em_eta_1"] = "20,-2.5,2.5"
		self.binnings_dict["em_eta_2"] = "20,-2.4,2.4"
		self.binnings_dict["em_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["em_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["em_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["em_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["em_iso_2"] = "25,0.0,0.1"
		self.binnings_dict["em_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["em_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["em_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["em_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["em_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["em_jpt_1"] = "20,20.0,250.0"
		self.binnings_dict["em_jpt_2"] = "25,20.0,250.0"
		self.binnings_dict["em_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["em_m_2"] = "25,0.0,2.5"
		self.binnings_dict["em_m_ll"] = "60,0.0,300"
		self.binnings_dict["em_m_llmet"] = "60,0.0,400"
		self.binnings_dict["em_m_sv"] = "25,0.0,250"
		self.binnings_dict["em_met"] = "40,0.0,200.0"
		self.binnings_dict["em_metcov00"] = "25,0.0,1000.0"
		self.binnings_dict["em_metcov01"] = "25,-500.0,500.0"
		self.binnings_dict["em_metcov10"] = "25,-500.0,500.0"
		self.binnings_dict["em_metcov11"] = "25,0.0,1000.0"
		self.binnings_dict["em_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["em_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["em_metProjectionPar"] = "20,-100.0,300.0"
		self.binnings_dict["em_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["em_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["em_mt_1"] = "30,0.0,150"
		self.binnings_dict["em_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["em_mt_ll"] = "25,75.0,300"
		self.binnings_dict["em_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["em_mvacov00"] = "30,0.0,40.0"
		self.binnings_dict["em_mvacov01"] = "30,-15.0,15.0"
		self.binnings_dict["em_mvacov10"] = "30,-15.0,15.0"
		self.binnings_dict["em_mvacov11"] = "30,0.0,40.0"
		self.binnings_dict["em_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["em_mvametcov00"] = "25,0.0,1000.0"
		self.binnings_dict["em_mvametcov01"] = "25,-500.0,500.0"
		self.binnings_dict["em_mvametcov10"] = "25,-500.0,500.0"
		self.binnings_dict["em_mvametcov11"] = "25,0.0,1000.0"
		self.binnings_dict["em_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["em_m_vis"] = "60,0.0,300"
		self.binnings_dict["em_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["em_njetspt30"] = "8,-0.5,7.5"
		self.binnings_dict["em_njets"] = "8,-0.5,7.5"
		self.binnings_dict["em_nbtag"] = "4,-0.5,3.5"
		self.binnings_dict["em_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["em_npu"] = "30,0.0,60.0"
		self.binnings_dict["em_npv"] = "30,0.0,60.0"
		self.binnings_dict["em_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["em_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["em_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["em_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["em_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["em_pt_1"] = "20,13.0,113.0"
		self.binnings_dict["em_pt_2"] = "20,10.0,110.0"
		self.binnings_dict["em_pt_ll"] = "25,0.0,250"
		self.binnings_dict["em_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["em_pt_sv"] = "25,0.0,250"
		self.binnings_dict["em_pt_tt"] = "20,0.0,200"
		self.binnings_dict["em_puweight"] = "20,0.0,2.0"
		self.binnings_dict["em_rho"] = "25,0.0,50.0"
		self.binnings_dict["em_svfitMass"] = "30,0.0,300"
		self.binnings_dict["em_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["em_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["em_pZetaMissVis"] = "50,-150.0,100.0"
		self.binnings_dict["em_pzetamiss"] = "50,-150.0,100.0"
		self.binnings_dict["em_pzetavis"] = "20,0.0,100.0"
		self.binnings_dict["mm_eta_1"] = "30,-3.0,3.0"
		self.binnings_dict["mm_eta_2"] = "30,-3.0,3.0"
		self.binnings_dict["mm_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["mm_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["mm_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["mm_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["mm_iso_2"] = "25,0.0,0.1"
		self.binnings_dict["mm_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["mm_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["mm_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["mm_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mm_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mm_jpt_1"] = "20,20.0,250.0"
		self.binnings_dict["mm_jpt_2"] = "20,20.0,250.0"
		self.binnings_dict["mm_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["mm_m_2"] = "25,0.0,2.5"
		self.binnings_dict["mm_m_ll"] = "60,0.0,300"
		self.binnings_dict["mm_m_llmet"] = "60,0.0,400"
		self.binnings_dict["mm_m_sv"] = "25,0.0,250"
		self.binnings_dict["mm_met"] = "40,0.0,200.0"
		self.binnings_dict["mm_metcov00"] = "25,0.0,1000.0"
		self.binnings_dict["mm_metcov01"] = "25,-500.0,500.0"
		self.binnings_dict["mm_metcov10"] = "25,-500.0,500.0"
		self.binnings_dict["mm_metcov11"] = "25,0.0,1000.0"
		self.binnings_dict["mm_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["mm_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["mm_mt_1"] = "30,0.0,150"
		self.binnings_dict["mm_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["mm_mt_ll"] = "25,75.0,300"
		self.binnings_dict["mm_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["mm_mvacov00"] = "30,0.0,40.0"
		self.binnings_dict["mm_mvacov01"] = "30,-15.0,15.0"
		self.binnings_dict["mm_mvacov10"] = "30,-15.0,15.0"
		self.binnings_dict["mm_mvacov11"] = "30,0.0,40.0"
		self.binnings_dict["mm_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["mm_mvametcov00"] = "25,0.0,1000.0"
		self.binnings_dict["mm_mvametcov01"] = "25,-500.0,500.0"
		self.binnings_dict["mm_mvametcov10"] = "25,-500.0,500.0"
		self.binnings_dict["mm_mvametcov11"] = "25,0.0,1000.0"
		self.binnings_dict["mm_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["mm_m_vis"] = "60,0.0,300"
		self.binnings_dict["mm_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["mm_njetspt30"] = "8,-0.5,7.5"
		self.binnings_dict["mm_njets"] = "8,-0.5,7.5"
		self.binnings_dict["mm_nbtag"] = "4,-0.5,3.5"
		self.binnings_dict["mm_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["mm_npu"] = "30,0.0,60.0"
		self.binnings_dict["mm_npv"] = "30,0.0,60.0"
		self.binnings_dict["mm_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mm_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mm_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["mm_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["mm_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["mm_pt_1"] = "25,0.0,250.0"
		self.binnings_dict["mm_pt_2"] = "25,0.0,250.0"
		self.binnings_dict["mm_pt_ll"] = "25,0.0,250"
		self.binnings_dict["mm_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["mm_pt_sv"] = "25,0.0,250"
		self.binnings_dict["mm_pt_tt"] = "20,0.0,200"
		self.binnings_dict["mm_puweight"] = "20,0.0,2.0"
		self.binnings_dict["mm_rho"] = "25,0.0,50.0"
		self.binnings_dict["mm_svfitMass"] = "30,0.0,300"
		self.binnings_dict["mm_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["mm_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["ee_eta_1"] = "30,-3.0,3.0"
		self.binnings_dict["ee_eta_2"] = "30,-3.0,3.0"
		self.binnings_dict["ee_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["ee_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["ee_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["ee_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["ee_iso_2"] = "25,0.0,0.1"
		self.binnings_dict["ee_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["ee_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["ee_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["ee_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["ee_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["ee_jpt_1"] = "20,20.0,250.0"
		self.binnings_dict["ee_jpt_2"] = "20,20.0,250.0"
		self.binnings_dict["ee_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["ee_m_2"] = "25,0.0,2.5"
		self.binnings_dict["ee_m_ll"] = "60,0.0,300"
		self.binnings_dict["ee_m_llmet"] = "60,0.0,400"
		self.binnings_dict["ee_m_sv"] = "25,0.0,250"
		self.binnings_dict["ee_met"] = "40,0.0,200.0"
		self.binnings_dict["ee_metcov00"] = "25,0.0,1000.0"
		self.binnings_dict["ee_metcov01"] = "25,-500.0,500.0"
		self.binnings_dict["ee_metcov10"] = "25,-500.0,500.0"
		self.binnings_dict["ee_metcov11"] = "25,0.0,1000.0"
		self.binnings_dict["ee_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["ee_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["ee_mt_1"] = "30,0.0,150"
		self.binnings_dict["ee_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["ee_mt_ll"] = "25,75.0,300"
		self.binnings_dict["ee_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["ee_mvacov00"] = "30,0.0,40.0"
		self.binnings_dict["ee_mvacov01"] = "30,-15.0,15.0"
		self.binnings_dict["ee_mvacov10"] = "30,-15.0,15.0"
		self.binnings_dict["ee_mvacov11"] = "30,0.0,40.0"
		self.binnings_dict["ee_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["ee_mvametcov00"] = "25,0.0,1000.0"
		self.binnings_dict["ee_mvametcov01"] = "25,-500.0,500.0"
		self.binnings_dict["ee_mvametcov10"] = "25,-500.0,500.0"
		self.binnings_dict["ee_mvametcov11"] = "25,0.0,1000.0"
		self.binnings_dict["ee_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["ee_m_vis"] = "60,0.0,300"
		self.binnings_dict["ee_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["ee_njetspt30"] = "8,-0.5,7.5"
		self.binnings_dict["ee_njets"] = "8,-0.5,7.5"
		self.binnings_dict["ee_nbtag"] = "4,-0.5,3.5"
		self.binnings_dict["ee_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["ee_npu"] = "30,0.0,60.0"
		self.binnings_dict["ee_npv"] = "30,0.0,60.0"
		self.binnings_dict["ee_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["ee_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["ee_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["ee_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["ee_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["ee_pt_1"] = "25,0.0,250.0"
		self.binnings_dict["ee_pt_2"] = "25,0.0,250.0"
		self.binnings_dict["ee_pt_ll"] = "25,0.0,250"
		self.binnings_dict["ee_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["ee_pt_sv"] = "25,0.0,250"
		self.binnings_dict["ee_pt_tt"] = "20,0.0,200"
		self.binnings_dict["ee_puweight"] = "20,0.0,2.0"
		self.binnings_dict["ee_rho"] = "25,0.0,50.0"
		self.binnings_dict["ee_svfitMass"] = "30,0.0,300"
		self.binnings_dict["ee_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["ee_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["binningHtt8TeV_"+"ee_1jet_high"] = "0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 1.0"
		self.binnings_dict["binningHtt8TeV_"+"ee_1jet_low"] = "0.0 0.2 0.4 0.6 0.8 1.0"
		self.binnings_dict["binningHtt8TeV_"+"ee_2jet_vbf"] = "0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 1.0"
		self.binnings_dict["binningHtt8TeV_"+"ee_0jet_high"] = "0.0 0.2 0.4 0.6 0.8 1.0"
		self.binnings_dict["binningHtt8TeV_"+"ee_0jet_low"] = "0.0 0.2 0.4 0.6 0.8 1.0"
		self.binnings_dict["binningHtt8TeV_"+"em_inclusive"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"em_0jet_low"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"em_0jet_high"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"em_1jet_low"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"em_1jet_high"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"em_2jet_vbf_loose"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"em_2jet_vbf_tight"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_0jet_high"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_0jet_low"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_0jet_medium"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_1jet_high_lowhiggs"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_1jet_high_mediumhiggs"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_1jet_medium"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_inclusive"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_2jet_vbf"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_2jet_vbf_loose"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"et_2jet_vbf_tight"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mm_0jet_low"] = "0.0 1.0"
		self.binnings_dict["binningHtt8TeV_"+"mm_1jet_high"] = "0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 1.0"
		self.binnings_dict["binningHtt8TeV_"+"mm_1jet_low"] = "0.0 1.0"
		self.binnings_dict["binningHtt8TeV_"+"mm_2jet_vbf"] = "0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 1.0"
		self.binnings_dict["binningHtt8TeV_"+"mm_0jet_high"] = "0.0 1.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_0jet_high"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_0jet_low"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_0jet_medium"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_1jet_high_lowhiggs"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_1jet_high_mediumhiggs"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_1jet_medium"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_inclusive"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_2jet_vbf_loose"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_2jet_vbf"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"mt_2jet_vbf_tight"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"tt_1jet_high_mediumhiggs"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"tt_1jet_high_highhiggs"] = "0.0 10.0 20.0 30.0 40.0 50.0 60.0 70.0 80.0 90.0 100.0 110.0 120.0 130.0 140.0 150.0 160.0 170.0 180.0 190.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0"
		self.binnings_dict["binningHtt8TeV_"+"tt_2jet_vbf"] = "0.0 20.0 40.0 60.0 80.0 100.0 120.0 140.0 160.0 180.0 200.0 250.0 300.0 350.0"
		# H->tautau binnings
		for channel in ["mt", "et", "em"]:
			self.binnings_dict["binningHtt13TeV_"+channel+"_inclusive_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_inclusive_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_low_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_high_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 20)+range(200, 351, 50)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_inclusive_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 20)+range(200, 351, 50)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_low_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_high_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 20)+range(200, 351, 50)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_2jet_vbf_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 20)+range(200, 351, 50)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_inclusive_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])

			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_inclusive_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_low_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_high_m_vis"] = " ".join([str(float(f)) for f in range(0,45,15)+range(45, 105, 10)+range(105,151,15)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_inclusive_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_low_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_high_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_2jet_vbf_m_vis"] = " ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_2jet_inclusive_m_vis"] = " ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])

			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
		self.binnings_dict["binningHtt13TeV_tt_inclusive_svfitMass"] = " ".join([str(float(f)) for f in [0, 50]+range(90, 171, 20)+[200, 350]])
		# H->tautau MSSM binnings
		for channel in ["mt", "et", "em", "tt"]:
			self.binnings_dict[channel+"_TrainingSelectionValue"] = "10,0,100"
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_inclusive_svfitMass"] = " ".join([str(float(f)) for f in range(0,4000,10)])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_nobtag_svfitMass"] = " ".join([str(float(f)) for f in [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_btag_svfitMass"] = " ".join([str(float(f)) for f in [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
