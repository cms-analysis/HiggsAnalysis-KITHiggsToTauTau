# -*- coding: utf-8 -*-

import logging
import numpy
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.binnings as binnings


class BinningsDict(binnings.BinningsDict):
	def __init__(self, additional_binnings=None):
		super(BinningsDict, self).__init__(additional_binnings=additional_binnings)
		self.binnings_dict["mt_reg_1"] = "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
		self.binnings_dict["mt_ztt_1"] = "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
		self.binnings_dict["mt_vbf_1"] = "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
		self.binnings_dict["mt_disc_1"] = "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
		self.binnings_dict["mt_ttj_1"] = "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
		self.binnings_dict["diLepMass"] = "50,0,250"
		self.binnings_dict["svfitMass"] = "50,0,250"
		self.binnings_dict["zmumu_selection_for_embedding_ZMass"] = "19,50,240"
		self.binnings_dict["zmumu_selection_for_embedding_integral"] = "1,0,1"
		auto_rebin_binning = " ".join([str(float(f)) for f in range(0,251,10)])
		
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			self.binnings_dict[channel+"_integral"] = "1,0.0,1.0"
			self.binnings_dict[channel+"_min_ll_jet_eta"] = "16,-8,8"
			self.binnings_dict[channel+"_diLepBoost"] = "25,0,2000"
			self.binnings_dict[channel+"_diLepDeltaR"] = "20,0,10"
			self.binnings_dict[channel+"_diLepJet1DeltaR"] = "20,0,10"
			
			self.binnings_dict[channel+"_rhoNeutralChargedAsymmetry"] = "20,-1.00001,1.00001"
			self.binnings_dict[channel+"_rhoNeutralChargedAsymmetry_1"] = "20,-1.00001,1.00001"
			self.binnings_dict[channel+"_rhoNeutralChargedAsymmetry_2"] = "20,-1.00001,1.00001"
			
			for suffix in ["", "Svfit", "HHKinFit"]:
				self.binnings_dict[channel+"_visibleOverFullEnergy"+suffix] = "20,0.0,1.00001"
				self.binnings_dict[channel+"_visibleOverFullEnergy"+suffix+"_1"] = "20,0.0,1.00001"
				self.binnings_dict[channel+"_visibleOverFullEnergy"+suffix+"_2"] = "20,0.0,1.00001"
				
				self.binnings_dict[channel+"_visibleToFullAngleSvfit"+suffix] = "20,0.0,0.1"
				self.binnings_dict[channel+"_visibleToFullAngleSvfit"+suffix+"_1"] = "20,0.0,0.1"
				self.binnings_dict[channel+"_visibleToFullAngleSvfit"+suffix+"_2"] = "20,0.0,0.1"
				
				self.binnings_dict[channel+"tauPolarisationDiscriminator"+suffix] = "20,-1.00001,1.00001"
			
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
			for metstring in ["met", "mva"]:
				for matrix in ["cov00", "cov11"]:
					self.binnings_dict[ch+metstring+matrix] = "25,0.0,1000.0"
				for matrix in ["cov01", "cov10"]:
					self.binnings_dict[ch+metstring+matrix] = "25,-500.0,500.0"
			self.binnings_dict[ch+"npu"] = "30,0.0,30.0"
			self.binnings_dict[ch+"npv"] = "30,0.0,30.0"
			self.binnings_dict[ch+"H_mass"] = "40,0.0,2000.0"
			self.binnings_dict[ch+"H_pt"] = "40,0.0,300.0"
			self.binnings_dict[ch+"ptvis"] = "40,0.0,300.0"
			self.binnings_dict[ch+"jpt_1"] = "20,20.0,250.0"
			self.binnings_dict[ch+"jpt_2"] = "20,20.0,250.0"
		
		self.binnings_dict["tt_decayMode_1"] = "11,0.0,11.0"
		self.binnings_dict["tt_decayMode_2"] = "11,0.0,11.0"
		self.binnings_dict["tt_eta_1"] = "30,-3,3"
		self.binnings_dict["tt_eta_2"] = "30,-3,3"
		self.binnings_dict["tt_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["tt_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["tt_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["tt_iso_1"] = "25,0.0,2.0"
		self.binnings_dict["tt_iso_2"] = "25,0.0,2.0"
		self.binnings_dict["tt_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["tt_jdphi"] = "12,-3.2,3.2"
		self.binnings_dict["tt_absjdphi"] = "20,0,3.2"
		self.binnings_dict["tt_jeta_1"] = "10,-4.7,4.7"
		self.binnings_dict["tt_jeta_2"] = "10,-4.7,4.7"
		self.binnings_dict["tt_jphi_1"] = "10,-3.2,3.2"
		self.binnings_dict["tt_jphi_2"] = "10,-3.2,3.2"
		self.binnings_dict["tt_m_1"] = "25,0.0,2.5"
		self.binnings_dict["tt_m_2"] = "25,0.0,2.5"
		self.binnings_dict["tt_m_ll"] = "60,0.0,300"
		self.binnings_dict["tt_m_llmet"] = "60,0.0,400"
		self.binnings_dict["tt_m_sv"] = "25,0.0,250"
		self.binnings_dict["tt_mt_tot"] = "30,0.0,300"
		self.binnings_dict["tt_met"] = "40,0.0,200.0"
		self.binnings_dict["tt_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["tt_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["tt_mt_1"] = "20,0.0,160"
		self.binnings_dict["tt_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["tt_mt_ll"] = "25,75.0,300"
		self.binnings_dict["tt_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["tt_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["tt_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["tt_m_vis"] = "60,0.0,300"
		self.binnings_dict["tt_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["tt_njetspt30"] = "10,-0.5,9.5"
		self.binnings_dict["tt_njets"] = "8,-0.5,7.5"
		self.binnings_dict["tt_nbtag"] = "5,-0.5,4.5"
		self.binnings_dict["tt_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["tt_phi_1"] = "10,-3.2,3.2"
		self.binnings_dict["tt_phi_2"] = "10,-3.2,3.2"
		self.binnings_dict["tt_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["tt_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["tt_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["tt_pt_1"] = "25,0.0,100.0"
		self.binnings_dict["tt_pt_2"] = "25,0.0,100.0"
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
		self.binnings_dict["tt_phiStarCP"] = "20,0.0,6.28"
		
		for ch in ["em_", "et_", "mt_", "tt_"]:
			self.binnings_dict[ch+"melaProbCPEvenGGH"] = "20,0,1"
			self.binnings_dict[ch+"melaProbCPOddGGH"] = "20,0,1"
			self.binnings_dict[ch+"melaProbCPMixGGH"] = "20,0,1"
			self.binnings_dict[ch+"melaProbCPEvenVBF"] = "20,0,1"
			self.binnings_dict[ch+"melaProbCPOddVBF"] = "20,0,1"
			self.binnings_dict[ch+"melaProbCPMixVBF"] = "20,0,1"
			
			self.binnings_dict[ch+"melaM125ProbCPEvenGGH"] = self.binnings_dict[ch+"melaProbCPEvenGGH"]
			self.binnings_dict[ch+"melaM125ProbCPOddGGH"] = self.binnings_dict[ch+"melaProbCPOddGGH"]
			self.binnings_dict[ch+"melaM125ProbCPMixGGH"] = self.binnings_dict[ch+"melaProbCPMixGGH"]
			self.binnings_dict[ch+"melaM125ProbCPEvenVBF"] = self.binnings_dict[ch+"melaProbCPEvenVBF"]
			self.binnings_dict[ch+"melaM125ProbCPOddVBF"] = self.binnings_dict[ch+"melaProbCPOddVBF"]
			self.binnings_dict[ch+"melaM125ProbCPMixVBF"] = self.binnings_dict[ch+"melaProbCPMixVBF"]
			
			self.binnings_dict[ch+"melaDiscriminatorD0MinusGGH"] = "20,0.0,1.0"
			self.binnings_dict[ch+"melaDiscriminatorDCPGGH"] = "20,-1.0,1.0"
			self.binnings_dict[ch+"melaDiscriminatorD0MinusVBF"] = "20,0.0,1.0"
			self.binnings_dict[ch+"melaDiscriminatorDCPVBF"] = "20,-1.0,1.0"
			self.binnings_dict[ch+"melaDiscriminatorD0MinusGGH_signDCP"] = "8,-1.0,1.0"
			self.binnings_dict[ch+"melaDiscriminatorD0MinusVBF_signDCP"] = "8,-1.0,1.0"
			
			self.binnings_dict[ch+"melaM125DiscriminatorD0MinusGGH"] = self.binnings_dict[ch+"melaDiscriminatorD0MinusGGH"]
			self.binnings_dict[ch+"melaM125DiscriminatorDCPGGH"] = self.binnings_dict[ch+"melaDiscriminatorDCPGGH"]
			self.binnings_dict[ch+"melaM125DiscriminatorD0MinusVBF"] = self.binnings_dict[ch+"melaDiscriminatorD0MinusVBF"]
			self.binnings_dict[ch+"melaM125DiscriminatorDCPVBF"] = self.binnings_dict[ch+"melaDiscriminatorDCPVBF"]
			self.binnings_dict[ch+"melaM125DiscriminatorD0MinusGGH_signDCP"] = self.binnings_dict[ch+"melaDiscriminatorD0MinusGGH_signDCP"]
			self.binnings_dict[ch+"melaM125DiscriminatorD0MinusVBF_signDCP"] = self.binnings_dict[ch+"melaDiscriminatorD0MinusVBF_signDCP"]
		
		self.binnings_dict["mt_decayMode_2"] = "11,0.0,11.0"
		self.binnings_dict["mt_eta_1"] = "30,-3,3"
		self.binnings_dict["mt_eta_2"] = "30,-3,3"
		self.binnings_dict["mt_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["mt_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["mt_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["mt_iso_1"] = "50,0.0,1.0"
		self.binnings_dict["mt_iso_2"] = "25,0.5,1.0"
		self.binnings_dict["mt_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["mt_jdphi"] = "12,-3.2,3.2"
		self.binnings_dict["mt_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["mt_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["mt_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mt_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mt_m_1"] = "10,0.0,0.2"
		self.binnings_dict["mt_m_2"] = "25,0.0,2.5"
		self.binnings_dict["mt_m_ll"] = "60,0.0,300"
		self.binnings_dict["mt_m_llmet"] = "60,0.0,400"
		self.binnings_dict["mt_m_sv"] = "25,0.0,250"
		self.binnings_dict["mt_mt_tot"] = "30,0.0,300"
		self.binnings_dict["mt_met"] = "40,0.0,200.0"
		self.binnings_dict["mt_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["mt_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["mt_metProjectionPar"] = "20,-100.0,300.0"
		self.binnings_dict["mt_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["mt_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["mt_mt_1"] = "20,0.0,160"
		self.binnings_dict["mt_mt_2"] = "20,0.0,160"
		self.binnings_dict["mt_mt_tt"] = "30,0.0,300"
		self.binnings_dict["mt_mt_tot"] = "20,0.0,1000"
		self.binnings_dict["mt_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["mt_mt_ll"] = "25,75.0,300"
		self.binnings_dict["mt_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["mt_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["mt_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["mt_m_vis"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])
		self.binnings_dict["mt_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["mt_njetspt30"] = "10,-0.5,9.5"
		self.binnings_dict["mt_njets"] = "8,-0.5,7.5"
		self.binnings_dict["mt_nbtag"] = "5,-0.5,4.5"
		self.binnings_dict["mt_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["mt_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mt_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mt_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["mt_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["mt_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["mt_pt_1"] = "25,0.0,100.0"
		self.binnings_dict["mt_pt_2"] = "25,0.0,100.0"
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
		self.binnings_dict["mt_gen_match_1"] = "7,0,7"
		self.binnings_dict["mt_gen_match_2"] = "7,0,7"
		self.binnings_dict["mt_phiStarCP"] = "20,0.0,6.28"

		self.binnings_dict["et_decayMode_2"] = "11,0.0,11.0"
		self.binnings_dict["et_eta_1"] = "30,-3,3"
		self.binnings_dict["et_eta_2"] = "30,-3,3"
		self.binnings_dict["et_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["et_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["et_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["et_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["et_iso_2"] = "25,0.0,2.0"
		self.binnings_dict["et_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["et_jdphi"] = "12,-3.2,3.2"
		self.binnings_dict["et_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["et_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["et_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["et_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["et_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["et_m_2"] = "25,0.0,2.5"
		self.binnings_dict["et_m_ll"] = "60,0.0,300"
		self.binnings_dict["et_m_llmet"] = "60,0.0,400"
		self.binnings_dict["et_m_sv"] = "25,0.0,250"
		self.binnings_dict["et_mt_tot"] = "30,0.0,300"
		self.binnings_dict["et_met"] = "40,0.0,200.0"
		self.binnings_dict["et_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["et_metProjectionPar"] = "20,-100.0,300.0"
		self.binnings_dict["et_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["et_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["et_mt_1"] = "20,0.0,160"
		self.binnings_dict["et_mt_2"] = "20,0.0,160"
		self.binnings_dict["et_mt_tt"] = "30,0.0,300"
		self.binnings_dict["et_mt_tot"] = "20,0.0,1000"
		self.binnings_dict["et_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["et_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["et_mt_ll"] = "25,75.0,300"
		self.binnings_dict["et_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["et_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["et_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["et_m_vis"] = "60,0.0,300"
		self.binnings_dict["et_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["et_njetspt30"] = "10,-0.5,9.5"
		self.binnings_dict["et_njets"] = "8,-0.5,7.5"
		self.binnings_dict["et_nbtag"] = "5,-0.5,4.5"
		self.binnings_dict["et_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["et_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["et_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["et_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["et_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["et_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["et_pt_1"] = "25,0.0,100.0"
		self.binnings_dict["et_pt_2"] = "25,0.0,100.0"
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
		self.binnings_dict["et_gen_match_1"] = "7,0,7"
		self.binnings_dict["et_gen_match_2"] = "7,0,7"
		self.binnings_dict["et_phiStarCP"] = "20,0.0,6.28"

		self.binnings_dict["em_eta_1"] = "30,-3,3"
		self.binnings_dict["em_eta_2"] = "30,-3,3"
		self.binnings_dict["em_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["em_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["em_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["em_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["em_iso_2"] = "25,0.0,0.1"
		self.binnings_dict["em_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["em_jdphi"] = "12,-3.2,3.2"
		self.binnings_dict["em_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["em_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["em_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["em_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["em_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["em_m_2"] = "10,0.0,0.2"
		self.binnings_dict["em_m_ll"] = "60,0.0,300"
		self.binnings_dict["em_m_llmet"] = "60,0.0,400"
		self.binnings_dict["em_m_sv"] = "25,0.0,250"
		self.binnings_dict["em_mt_tot"] = "30,0.0,300"
		self.binnings_dict["em_met"] = "40,0.0,200.0"
		self.binnings_dict["em_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["em_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["em_metProjectionPar"] = "20,-100.0,300.0"
		self.binnings_dict["em_metProjectionPerp"] = "50,-50.0,50.0"
		self.binnings_dict["em_metProjectionPhi"] = "20,-3.141,3.141"
		self.binnings_dict["em_mt_1"] = "20,0.0,160"
		self.binnings_dict["em_mt_2"] = "20,0.0,160"
		self.binnings_dict["em_mt_tt"] = "30,0.0,300"
		self.binnings_dict["em_mt_tot"] = "20,0.0,1000"
		self.binnings_dict["em_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["em_mt_ll"] = "25,75.0,300"
		self.binnings_dict["em_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["em_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["em_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["em_m_vis"] = "60,0.0,300"
		self.binnings_dict["em_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["em_njetspt30"] = "10,-0.5,9.5"
		self.binnings_dict["em_njets"] = "8,-0.5,7.5"
		self.binnings_dict["em_nbtag"] = "5,-0.5,4.5"
		self.binnings_dict["em_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["em_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["em_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["em_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["em_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["em_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["em_pt_1"] = "25,0.0,100.0"
		self.binnings_dict["em_pt_2"] = "25,0.0,100.0"
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
		self.binnings_dict["em_phiStarCP"] = "20,0.0,6.28"
		
		self.binnings_dict["mm_eta_1"] = "30,-3.0,3.0"
		self.binnings_dict["mm_eta_2"] = "30,-3.0,3.0"
		self.binnings_dict["mm_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["mm_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["mm_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["mm_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["mm_iso_2"] = "25,0.0,0.1"
		self.binnings_dict["mm_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["mm_jdphi"] = "12,-3.2,3.2"
		self.binnings_dict["mm_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["mm_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["mm_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mm_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mm_m_1"] = "10,0.0,0.2"
		self.binnings_dict["mm_m_2"] = "10,0.0,0.2"
		self.binnings_dict["mm_m_ll"] = "60,0.0,300"
		self.binnings_dict["mm_m_llmet"] = "60,0.0,400"
		self.binnings_dict["mm_m_sv"] = "25,0.0,250"
		self.binnings_dict["mm_met"] = "40,0.0,200.0"
		self.binnings_dict["mm_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["mm_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["mm_mt_1"] = "20,0.0,160"
		self.binnings_dict["mm_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["mm_mt_ll"] = "25,75.0,300"
		self.binnings_dict["mm_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["mm_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["mm_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["mm_m_vis"] = "40,50,130"
		self.binnings_dict["mm_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["mm_njetspt30"] = "10,-0.5,9.5"
		self.binnings_dict["mm_njets"] = "8,-0.5,7.5"
		self.binnings_dict["mm_nbtag"] = "5,-0.5,4.5"
		self.binnings_dict["mm_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["mm_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["mm_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["mm_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["mm_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["mm_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["mm_pt_1"] = "25,0.0,100.0"
		self.binnings_dict["mm_pt_2"] = "25,0.0,100.0"
		self.binnings_dict["mm_pt_ll"] = "25,0.0,250"
		self.binnings_dict["mm_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["mm_pt_sv"] = "25,0.0,250"
		self.binnings_dict["mm_pt_tt"] = "20,0.0,200"
		self.binnings_dict["mm_puweight"] = "20,0.0,2.0"
		self.binnings_dict["mm_rho"] = "25,0.0,50.0"
		self.binnings_dict["mm_svfitMass"] = "30,0.0,300"
		self.binnings_dict["mm_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["mm_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["mm_phiStarCP"] = "20,0.0,6.28"
		
		self.binnings_dict["ee_eta_1"] = "30,-3.0,3.0"
		self.binnings_dict["ee_eta_2"] = "30,-3.0,3.0"
		self.binnings_dict["ee_eta_ll"] = "25,-5.0,5.0"
		self.binnings_dict["ee_eta_llmet"] = "25,-5.0,5.0"
		self.binnings_dict["ee_eta_sv"] = "25,-5.0,5.0"
		self.binnings_dict["ee_iso_1"] = "25,0.0,0.1"
		self.binnings_dict["ee_iso_2"] = "25,0.0,0.1"
		self.binnings_dict["ee_jdeta"] = "20,0.0,10.0"
		self.binnings_dict["ee_jdphi"] = "12,-3.2,3.2"
		self.binnings_dict["ee_jeta_1"] = "20,-4.7,4.7"
		self.binnings_dict["ee_jeta_2"] = "20,-4.7,4.7"
		self.binnings_dict["ee_jphi_1"] = "20,-3.2,3.2"
		self.binnings_dict["ee_jphi_2"] = "20,-3.2,3.2"
		self.binnings_dict["ee_m_1"] = "20,-0.2,0.2"
		self.binnings_dict["ee_m_2"] = "20,-0.2,0.2"
		self.binnings_dict["ee_m_ll"] = "60,0.0,300"
		self.binnings_dict["ee_m_llmet"] = "60,0.0,400"
		self.binnings_dict["ee_m_sv"] = "25,0.0,250"
		self.binnings_dict["ee_met"] = "40,0.0,200.0"
		self.binnings_dict["ee_metphi"] = "32,-3.2,3.2"
		self.binnings_dict["ee_mjj"] = "20,0.0,1500.0"
		self.binnings_dict["ee_mt_1"] = "20,0.0,160"
		self.binnings_dict["ee_mt_lep1met"] = "30,0.0,300"
		self.binnings_dict["ee_mt_ll"] = "25,75.0,300"
		self.binnings_dict["ee_mt_llmet"] = "40,0.0,400"
		self.binnings_dict["ee_mvamet"] = "40,0.0,200.0"
		self.binnings_dict["ee_mvametphi"] = "32,-3.2,3.2"
		self.binnings_dict["ee_m_vis"] = "60,0.0,300"
		self.binnings_dict["ee_nJets30"] = "8,-0.5,7.5"
		self.binnings_dict["ee_njetspt30"] = "10,-0.5,9.5"
		self.binnings_dict["ee_njets"] = "8,-0.5,7.5"
		self.binnings_dict["ee_nbtag"] = "5,-0.5,4.5"
		self.binnings_dict["ee_njetingap"] = "5,-0.5,4.5"
		self.binnings_dict["ee_phi_1"] = "20,-3.2,3.2"
		self.binnings_dict["ee_phi_2"] = "20,-3.2,3.2"
		self.binnings_dict["ee_phi_ll"] = "32,-3.2,3.2"
		self.binnings_dict["ee_phi_llmet"] = "32,-3.2,3.2"
		self.binnings_dict["ee_phi_sv"] = "32,-3.2,3.2"
		self.binnings_dict["ee_pt_1"] = "25,0.0,100.0"
		self.binnings_dict["ee_pt_2"] = "25,0.0,100.0"
		self.binnings_dict["ee_pt_ll"] = "25,0.0,250"
		self.binnings_dict["ee_pt_llmet"] = "25,0.0,250"
		self.binnings_dict["ee_pt_sv"] = "25,0.0,250"
		self.binnings_dict["ee_pt_tt"] = "20,0.0,200"
		self.binnings_dict["ee_puweight"] = "20,0.0,2.0"
		self.binnings_dict["ee_rho"] = "25,0.0,50.0"
		self.binnings_dict["ee_svfitMass"] = "30,0.0,300"
		self.binnings_dict["ee_trigweight_1"] = "20,0.5,1.5"
		self.binnings_dict["ee_trigweight_2"] = "20,0.5,1.5"
		self.binnings_dict["ee_phiStarCP"] = "20,0.0,6.28"
		
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
		
		# Z->tautau polarisation binnings
		for channel in ["mt", "et", "tt", "em"]:
			for category in ["a1", "a1_1", "a1_2", "rho", "rho_1", "rho_2", "oneprong", "oneprong_1", "oneprong_2", "combined_a1_a1", "combined_a1_rho", "combined_a1_oneprong", "combined_rho_rho", "combined_rho_oneprong", "combined_oneprong_oneprong"]:
				for reco_fit in ["Svfit", "SvfitM91", "SimpleFit", "HHKinFit"]:
					suffix = "_{m_{Z}}" if "M91" in reco_fit else ""
					self.binnings_dict["binningZttPol13TeV_"+channel+"_"+category+"_polarisationCombinedOmega"+reco_fit] = "25,-1,1"
					self.binnings_dict["binningZttPol13TeV_"+channel+"_"+category+"_polarisationCombinedOmegaBar"+reco_fit] = "25,-1,1"
					self.binnings_dict["binningZttPol13TeV_"+channel+"_"+category+"_polarisationCombinedOmegaVisible"+reco_fit] = "25,-1,1"
					for lepton_index in ["1", "2"]:
						self.binnings_dict["binningZttPol13TeV_"+channel+"_"+category+"_polarisationOmega"+reco_fit+"_"+lepton_index] = "25,-1,1"
						self.binnings_dict["binningZttPol13TeV_"+channel+"_"+category+"_polarisationOmegaBar"+reco_fit+"_"+lepton_index] = "25,-1,1"
						self.binnings_dict["binningZttPol13TeV_"+channel+"_"+category+"_polarisationOmegaVisible"+reco_fit+"_"+lepton_index] = "25,-1,1"
		
			self.binnings_dict["binningZttPol13TeV_"+channel+"_a1"] = self.binnings_dict[channel+"_visibleOverFullEnergy"] # TODO change to dedicated a1 variable
			self.binnings_dict["binningZttPol13TeV_"+channel+"_rho"] = self.binnings_dict[channel+"_rhoNeutralChargedAsymmetry"]
			self.binnings_dict["binningZttPol13TeV_"+channel+"_oneprong"] = self.binnings_dict[channel+"_visibleOverFullEnergy"]
			self.binnings_dict["binningZttPol13TeV_"+channel+"_catZttPol13TeV_"+channel+"_index"] = "3,0,3"
		
		# H->tautau binnings
		for channel in ["mt", "et", "em", "tt", "mm"]:
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
			
			self.binnings_dict["binningHtt13TeV_"+channel+"_ZeroJet2D_WJCR_mt_1"] = " ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_Boosted2D_WJCR_mt_1"] = " ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_2jet_inclusive_m_vis"] = " ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
		
		# Binnings for the SM H->tautau analysis.		
		#ZeroJet	
		self.binnings_dict["binningHtt13TeV_mm_ZeroJet2D_ptvis"] = "0.0 100.0 150.0 200.0 250.0 300.0 1000.0"
		self.binnings_dict["binningHtt13TeV_mm_0jet_ptvis"] = self.binnings_dict["binningHtt13TeV_mm_ZeroJet2D_ptvis"]

		self.binnings_dict["binningHtt13TeV_mm_ZeroJet2D_m_vis"] = "70.0 110.0"
		self.binnings_dict["binningHtt13TeV_mm_0jet_m_vis"] = self.binnings_dict["binningHtt13TeV_mm_ZeroJet2D_m_vis"]
				
		self.binnings_dict["binningHtt13TeV_em_ZeroJet2D_m_vis"] = "0.0 "+" ".join([str(float(f)) for f in range(50, 100, 5)+range(100,401,300)])
		self.binnings_dict["binningHtt13TeV_em_0jet_m_vis"] = self.binnings_dict["binningHtt13TeV_em_ZeroJet2D_m_vis"]
		self.binnings_dict["binningHtt13TeV_em_ZeroJet2D_pt_2"] = " ".join([str(float(f)) for f in range(15, 35, 10)+range(35,10001,9965)])
		self.binnings_dict["binningHtt13TeV_em_0jet_pt_2"] = self.binnings_dict["binningHtt13TeV_em_ZeroJet2D_pt_2"]
		
		self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_QCDCR_m_vis"] = "40.0 80.0 120.0 160.0 200.0"
		self.binnings_dict["binningHtt13TeV_mt_0jet_qcd_cr_m_vis"] = self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_QCDCR_m_vis"]
		self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_m_vis"] = "0.0 "+" ".join([str(float(f)) for f in range(60, 110, 5)+range(110,401,290)])
		self.binnings_dict["binningHtt13TeV_mt_0jet_m_vis"] = self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_m_vis"]		
		self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_decayMode_2"] = "0 1 10 11"
		self.binnings_dict["binningHtt13TeV_mt_0jet_decayMode_2"] = self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_decayMode_2"]	
		self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_WJCR_mt_1"] = "80.0 200.0"
		self.binnings_dict["binningHtt13TeV_mt_wjets_0jet_cr_mt_1"] = self.binnings_dict["binningHtt13TeV_mt_ZeroJet2D_WJCR_mt_1"]			
		
		self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_QCDCR_m_vis"] = "40.0 80.0 120.0 160.0 200.0"
		self.binnings_dict["binningHtt13TeV_et_0jet_qcd_cr_m_vis"] = self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_QCDCR_m_vis"]		
		self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_m_vis"] = "0.0 "+" ".join([str(float(f)) for f in range(60, 110, 5)+range(110,401,290)])
		self.binnings_dict["binningHtt13TeV_et_0jet_m_vis"] = self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_m_vis"]	
		self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_decayMode_2"] = "0 1 10 11"
		self.binnings_dict["binningHtt13TeV_et_0jet_decayMode_2"] = self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_decayMode_2"]	
		self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_WJCR_mt_1"] = "80.0 200.0"
		self.binnings_dict["binningHtt13TeV_et_wjets_0jet_cr_mt_1"] = self.binnings_dict["binningHtt13TeV_et_ZeroJet2D_WJCR_mt_1"]
				
		self.binnings_dict["binningHtt13TeV_tt_ZeroJet2D_QCDCR_m_sv"] = "0.0 300.0"
		self.binnings_dict["binningHtt13TeV_tt_antiiso_0jet_cr_m_sv"] = self.binnings_dict["binningHtt13TeV_tt_ZeroJet2D_QCDCR_m_sv"]
		self.binnings_dict["binningHtt13TeV_tt_ZeroJet2D_m_sv"] = "0.0 "+" ".join([str(float(f)) for f in range(50,301,10)])
		self.binnings_dict["binningHtt13TeV_tt_0jet_m_sv"] = self.binnings_dict["binningHtt13TeV_tt_ZeroJet2D_m_sv"]
		
		#Boosted (1jet) category
		self.binnings_dict["binningHtt13TeV_ttbar_TTbarCR_0"] = "1,0,1000"
		self.binnings_dict["binningHtt13TeV_ttbar_TTbarCR_m_vis"] = "0.0 10000.0"
	
		self.binnings_dict["binningHtt13TeV_mm_Boosted2D_ptvis"] = "0.0 100.0 150.0 200.0 250.0 300.0 1000.0" 	
		self.binnings_dict["binningHtt13TeV_mm_boosted_ptvis"] = self.binnings_dict["binningHtt13TeV_mm_Boosted2D_ptvis"] 	
	
		self.binnings_dict["binningHtt13TeV_em_Boosted2D_m_sv"] = "0.0 "+" ".join([str(float(f)) for f in range(80, 160, 10)+range(160,301,140)])
		self.binnings_dict["binningHtt13TeV_em_boostedD_m_sv"] = self.binnings_dict["binningHtt13TeV_em_Boosted2D_m_sv"]
		self.binnings_dict["binningHtt13TeV_em_Boosted2D_H_pt"] = "0.0 "+" ".join([str(float(f)) for f in range(100, 300, 50)+range(300,10001,9700)])
		self.binnings_dict["binningHtt13TeV_em_boosted_H_pt"] = self.binnings_dict["binningHtt13TeV_em_Boosted2D_H_pt"]
		
		self.binnings_dict["binningHtt13TeV_mt_Boosted2D_QCDCR_m_sv"] = "40.0 80.0 120.0 160.0 200.0"
		self.binnings_dict["binningHtt13TeV_mt_boosted_qcd_cr_m_sv"] = self.binnings_dict["binningHtt13TeV_mt_Boosted2D_QCDCR_m_sv"]
		self.binnings_dict["binningHtt13TeV_mt_Boosted2D_m_sv"] = "0.0 "+" ".join([str(float(f)) for f in range(80, 160, 10)+range(160,301,140)])
		self.binnings_dict["binningHtt13TeV_mt_boosted_m_sv"] = self.binnings_dict["binningHtt13TeV_mt_Boosted2D_m_sv"]
		self.binnings_dict["binningHtt13TeV_mt_Boosted2D_H_pt"] = "0.0 "+" ".join([str(float(f)) for f in range(100, 300, 50)+range(300,10001,9700)]),
		self.binnings_dict["binningHtt13TeV_mt_boosted_H_pt"] = self.binnings_dict["binningHtt13TeV_mt_Boosted2D_H_pt"]
		self.binnings_dict["binningHtt13TeV_mt_Boosted2D_WJCR_mt_1"] = "80.0 200.0"
		self.binnings_dict["binningHtt13TeV_mt_wjets_boosted_cr_mt_1"] = self.binnings_dict["binningHtt13TeV_mt_Boosted2D_WJCR_mt_1"]
				
		self.binnings_dict["binningHtt13TeV_et_Boosted2D_QCDCR_m_sv"] = "40.0 80.0 120.0 160.0 200.0"	
		self.binnings_dict["binningHtt13TeV_et_boosted_qcd_cr_m_sv"] = self.binnings_dict["binningHtt13TeV_et_Boosted2D_QCDCR_m_sv"]			
		self.binnings_dict["binningHtt13TeV_et_Boosted2D_m_sv"] = "0.0 "+" ".join([str(float(f)) for f in range(80, 160, 10)+range(160,301,140)])
		self.binnings_dict["binningHtt13TeV_et_boosted_m_sv"] = self.binnings_dict["binningHtt13TeV_et_Boosted2D_m_sv"]
		self.binnings_dict["binningHtt13TeV_et_Boosted2D_H_pt"] = "0.0 "+" ".join([str(float(f)) for f in range(100, 300, 50)+range(300,10001,9700)])
		self.binnings_dict["binningHtt13TeV_et_boosted_H_pt"] = self.binnings_dict["binningHtt13TeV_et_Boosted2D_H_pt"]
		self.binnings_dict["binningHtt13TeV_et_Boosted2D_WJCR_mt_1"] = "80.0 200.0"
		self.binnings_dict["binningHtt13TeV_et_wjets_boosted_cr_mt_1"] = self.binnings_dict["binningHtt13TeV_et_Boosted2D_WJCR_mt_1"]
				
		self.binnings_dict["binningHtt13TeV_tt_Boosted2D_QCDCR_m_sv"] = "0.0 250.0"	
		self.binnings_dict["binningHtt13TeV_tt_antiiso_boosted_cr_m_sv"] = self.binnings_dict["binningHtt13TeV_tt_Boosted2D_QCDCR_m_sv"]	
		self.binnings_dict["binningHtt13TeV_tt_Boosted2D_H_pt"] = "0.0 100.0 170.0 300.0 10000.0"
		self.binnings_dict["binningHtt13TeV_tt_boosted_H_pt"] = self.binnings_dict["binningHtt13TeV_tt_Boosted2D_H_pt"]
		self.binnings_dict["binningHtt13TeV_tt_Boosted2D_m_sv"] = "0.0 40.0 "+" ".join([str(float(f)) for f in range(60, 131, 10)+range(150,251,50)])	
		self.binnings_dict["binningHtt13TeV_tt_boosted_m_sv"] = self.binnings_dict["binningHtt13TeV_tt_Boosted2D_m_sv"]
		
		# Vbf category
		self.binnings_dict["binningHtt13TeV_mm_Vbf2D_mjj"] = "300.0 700.0 1100.0 1500.0 2500.0"
		self.binnings_dict["binningHtt13TeV_mm_vbf_mjj"] = self.binnings_dict["binningHtt13TeV_mm_Vbf2D_mjj"]
		
		self.binnings_dict["binningHtt13TeV_em_Vbf2D_mjj"] = " ".join([str(float(f)) for f in range(300, 1500, 400)+range(1500,10001,8500)])
		self.binnings_dict["binningHtt13TeV_em_vbf_mjj"] = self.binnings_dict["binningHtt13TeV_em_Vbf2D_mjj"]
		self.binnings_dict["binningHtt13TeV_em_Vbf2D_m_sv"] = "0.0 "+" ".join([str(float(f)) for f in range(95, 155, 20)+range(155,401,245)])
		self.binnings_dict["binningHtt13TeV_em_vbf_m_sv"] = self.binnings_dict["binningHtt13TeV_em_Vbf2D_m_sv"]
				
		self.binnings_dict["binningHtt13TeV_et_Vbf2D_mjj"] = " ".join([str(float(f)) for f in range(300, 1500, 400)+range(1500,10001,8500)])
		self.binnings_dict["binningHtt13TeV_et_vbf_mjj"] = self.binnings_dict["binningHtt13TeV_et_Vbf2D_mjj"]
		self.binnings_dict["binningHtt13TeV_et_Vbf2D_m_sv"] = "0.0 "+" ".join([str(float(f)) for f in range(95, 155, 20)+range(155,401,245)])
		self.binnings_dict["binningHtt13TeV_et_vbf_m_sv"] = self.binnings_dict["binningHtt13TeV_et_Vbf2D_m_sv"]
		
		self.binnings_dict["binningHtt13TeV_mt_Vbf2D_mjj"] = " ".join([str(float(f)) for f in range(300, 1500, 400)+range(1500,10001,8500)])
		self.binnings_dict["binningHtt13TeV_mt_vbf_mjj"] = self.binnings_dict["binningHtt13TeV_mt_Vbf2D_mjj"]
		self.binnings_dict["binningHtt13TeV_mt_Vbf2D_m_sv"] = "0.0 "+" ".join([str(float(f)) for f in range(95, 155, 20)+range(155,401,245)])
		self.binnings_dict["binningHtt13TeV_mt_vbf_m_sv"] = self.binnings_dict["binningHtt13TeV_mt_Vbf2D_m_sv"]		

		self.binnings_dict["binningHtt13TeV_tt_Vbf2D_mjj"] = " ".join([str(float(f)) for f in range(300, 1500, 400)+range(1500,10001,8500)])
		self.binnings_dict["binningHtt13TeV_tt_vbf_mjj"] = self.binnings_dict["binningHtt13TeV_tt_Vbf2D_mjj"]		
		self.binnings_dict["binningHtt13TeV_tt_Vbf2D_QCDCR_m_sv"] = "0.0 250.0"
		self.binnings_dict["binningHtt13TeV_tt_antiiso_vbf_cr_m_sv"] = self.binnings_dict["binningHtt13TeV_tt_Vbf2D_QCDCR_m_sv"] 
		self.binnings_dict["binningHtt13TeV_tt_Vbf2D_m_sv"] = "0.0 40.0 "+" ".join([str(float(f)) for f in range(60, 131, 10)+range(150,251,50)])
		self.binnings_dict["binningHtt13TeV_tt_vbf_m_sv"] = self.binnings_dict["binningHtt13TeV_tt_Vbf2D_m_sv"]
		
		for channel in ["mt", "et", "em", "tt", "mm"]:
			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningMVA13TeV_"+channel+"_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			for i in range(11):
				self.binnings_dict["binningMVA13TeV_"+channel+"_reg_%i"%i] = self.binnings_dict["mt_reg_1"]
				self.binnings_dict["binningMVA13TeV_"+channel+"_disc_%i"%i] = self.binnings_dict["mt_disc_1"]
				self.binnings_dict["binningMVA13TeV_"+channel+"_ztt_%i"%i] = self.binnings_dict["mt_ztt_1"]
				self.binnings_dict["binningMVA13TeV_"+channel+"_vbf_%i"%i] = self.binnings_dict["mt_vbf_1"]
		self.binnings_dict["binningHtt13TeV_tt_inclusive_svfitMass"] = " ".join([str(float(f)) for f in [0, 50]+range(90, 171, 20)+[200, 350]])
		
		#H->tautau CP binnings
		for channel in ["mt", "et", "em", "tt", "mm"]:
			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_CP_boosted_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 10)+range(200, 351, 25)])
			
			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_CP_boosted_svfitMass"] = " ".join([str(float(f)) for f in range(0, 200, 20)+range(200, 351, 50)])
			
			self.binnings_dict["binningHtt13TeV_"+channel+"_0jet_CP_boosted_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])

			self.binnings_dict["binningHtt13TeV_"+channel+"_1jet_CP_boosted_m_vis"] = " ".join([str(float(f)) for f in range(0,30,10)+range(30, 120, 5)+range(120,151,10)])
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet_boosted_jdphi"] = "12,-3.2,3.2"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_boosted_jdphi"] = "12,-3.2,3.2"
			
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_boosted_dcp_star"] = "12,-1.0,1.0"		
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_boosted_melaDiscriminatorDCPGGH"] = "-1.0 -0.4 0.4 1.0"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_boosted_melaDiscriminatorD0MinusGGH"] = "0.0 0.25 0.5 0.75 1.0"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_lowboost_jdphi"] = "12,-3.2,3.2"
			
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_lowboost_dcp_star"] = "12,-1.0,1.0"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_lowboost_melaDiscriminatorDCPGGH"] = "-1.0 -0.4 0.4 1.0"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_lowboost_melaDiscriminatorD0MinusGGH"] = "0.0 0.25 0.5 0.75 1.0"	
					
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_boosted_m_sv"] = "0.0 80.0 100.0 115.0 130.0 150.0 10000.0"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet2D_lowboost_m_sv"] = "0.0 80.0 100.0 115.0 130.0 150.0 10000.0"
			self.binnings_dict["binningHtt13TeV_tt_dijet_boosted_qcd_cr_m_sv"] = "0.0 250.0"
			self.binnings_dict["binningHtt13TeV_tt_dijet_lowboost_qcd_cr_m_sv"] = "0.0 250.0"
			self.binnings_dict["binningHtt13TeV_tt_dijet_boosted_qcd_cr_jdphi"] = "-3.2 3.2"
			self.binnings_dict["binningHtt13TeV_tt_dijet2D_boosted_qcd_cr_jdphi"] = "-3.2 3.2"
			self.binnings_dict["binningHtt13TeV_tt_dijet2D_boosted_qcd_cr_dcp_star"] = "-1 1"
			self.binnings_dict["binningHtt13TeV_tt_dijet2D_lowboost_qcd_cr_jdphi"] = "-3.2 3.2"
			self.binnings_dict["binningHtt13TeV_tt_dijet2D_lowboost_qcd_cr_dcp_star"] = "-1 1"
			self.binnings_dict["binningHtt13TeV_tt_dijet_lowM_qcd_cr_m_sv"] = "0.0 250.0"
			self.binnings_dict["binningHtt13TeV_tt_dijet_lowM_qcd_cr_jdphi"] = "-3.2 3.2"
			self.binnings_dict["binningHtt13TeV_tt_dijet_highM_qcd_cr_m_sv"] = "0.0 250.0"
			self.binnings_dict["binningHtt13TeV_tt_dijet_highM_qcd_cr_jdphi"] = "-3.2 3.2"
			self.binnings_dict["binningHtt13TeV_tt_dijet_lowMjj_qcd_cr_m_sv"] = "0.0 250.0"
			self.binnings_dict["binningHtt13TeV_tt_dijet_lowMjj_qcd_cr_jdphi"] = "-3.2 3.2"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet_lowM_jdphi"] = "12,-3.2,3.2"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet_highM_jdphi"] = "12,-3.2,3.2"
			self.binnings_dict["binningHtt13TeV_"+channel+"_dijet_lowMjj_jdphi"] = "12,-3.2,3.2"
				
			# 0jet CP category	
			self.binnings_dict["binningHttCP13TeV_"+channel+"_ZeroJet2D_m_sv"] = "0 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 220 240 260 280 300" if channel != "tt" else "0 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300"
			
			# boosted CP category
			self.binnings_dict["binningHttCP13TeV_"+channel+"_Boosted2D_H_pt"] = "0 100 150 200 250 300" if channel != "tt" else "0 100 170 300"
			self.binnings_dict["binningHttCP13TeV_"+channel+"_Boosted2D_m_sv"] = "0 80 90 100 110 120 130 140 150 160 300" if channel != "tt" else "0 40 60 70 80 90 100 110 120 130 150 200 250"


		# H->tautau MSSM binnings
		for channel in ["mt", "et", "em", "tt"]:
			self.binnings_dict[channel+"_mt_2"] = "30,0,150"
			self.binnings_dict[channel+"_lep1_centrality"] = "10,0,1"
			self.binnings_dict[channel+"_lep2_centrality"] = "10,0,1"
			self.binnings_dict[channel+"_diLep_centrality"] = "10,0,1"
			self.binnings_dict[channel+"_diLep_diJet_deltaR"] = "10,0,10"
			self.binnings_dict[channel+"_delta_lep_centrality"] = "10,0,1"
			self.binnings_dict[channel+"_product_lep_centrality"] = "10,0,1"
			self.binnings_dict[channel+"_pVecSum"] = "25,0,2500"
			self.binnings_dict[channel+"_pScalSum"] = "25,0,2500"
			self.binnings_dict[channel+"_ptvis"] = "25,0.0,250"
			self.binnings_dict[channel+"_H_pt"] = "25,0.0,250"
			self.binnings_dict[channel+"_TrainingSelectionValue"] = "10,0,100"
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_inclusive_svfitMass"] = " ".join([str(float(f)) for f in range(0,4000,10)])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_nobtag_mt_tot"] = " ".join([str(float(f)) for f in [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_btag_mt_tot"] = " ".join([str(float(f)) for f in [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
			for i in ["looseiso", "loosemt", "tight"]:
				self.binnings_dict["binningHttMSSM13TeV_"+channel+"_nobtag_"+i+"_mt_tot"] = " ".join([str(float(f)) for f in [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
				self.binnings_dict["binningHttMSSM13TeV_"+channel+"_btag_"+i+"_mt_tot"] = " ".join([str(float(f)) for f in [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_nobtag_mt_sv"] = " ".join([str(float(f)) for f in [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_btag_mt_sv"] = " ".join([str(float(f)) for f in [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_nobtag_m_sv"] = " ".join([str(float(f)) for f in [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_btag_m_sv"] = " ".join([str(float(f)) for f in [0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,2700,2900,3100,3300,3500,3700,3900]])

		# Z->tautau binnings	
		for channel in ["em", "et", "mt"]:
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_LFVJet_m_vis"] = auto_rebin_binning
			self.binnings_dict["binningHttMSSM13TeV_"+channel+"_LFVZeroJet_m_vis"] = auto_rebin_binning
				
				#==========================CategoriesDictUpdates=========================================================
		
		import Artus.Utility.jsonTools as jsonTools
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
		categoriesUpdate = Categories.CategoriesDict().getBinningsDict
