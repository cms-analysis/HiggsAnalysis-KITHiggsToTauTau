# -*- coding: utf-8 -*-
import itertools
import pprint
import numpy as np
import copy

class CategoriesDict(object):
	def __init__(self):
		super(CategoriesDict, self).__init__()
		boosted_higgs_string = "(H_pt>100)"
		boosted_higgs_medium_string = "(H_pt>50)"
		boosted_higgs_low_string = "(H_pt>30)"
		vbf_medium_string = "(mjj>500&&jdeta>3.5)"
		vbf_loose_string = "(mjj>200&&jdeta>2)"
		jet2_string = "(njetspt30>1)"
		jet2x_string = "(njetspt30==2)"
		jet1_string = "(njetspt30==1)"
		jet0_string = "(njetspt30==0)"
		pt2_tight_string = "(pt_2>=45)"
		pt2_medium_string = "(pt_2>=35)"
		pt2_loose_string = "(pt_2>=25)"
		eta_hard_string = "jdeta>4.0"
		auto_rebin_binning = " ".join([str(float(f)) for f in range(0,251,10)])
		self.pp = pprint.PrettyPrinter(indent=4)
		self.categoriesDict = {}

		self.categoriesDict["{analysis}{channel}Vbf3D{discriminator}"] = {
				"channel":[
					"mm_",
					"ee_",
					"mt_",
					"et_",
					"em_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mm_":"(njetspt30>1)*(mjj>300)",
					"mt_":"(pt_2>40)*(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"et_":"(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"em_":"(pZetaMissVis>-10)*(njetspt30==2)*(mjj>300)",
					"tt_":"(njetspt30>1)*(jdeta>2.5)*(H_pt>100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_mjj": auto_rebin_binning,
						"_m_sv": auto_rebin_binning,
						"_jdphi": auto_rebin_binning,
						},
					"mm_": {
						"_mjj":"300.0 700.0 1100.0 1500.0 2500.0"
						},
					"mt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"et_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"em_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"tt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						}
					}
				}
		self.categoriesDict["{analysis}{channel}Vbf3D_mela_GGH_DCPPlus{discriminator}"] = {
				"channel":[
					"mm_",
					"ee_",
					"mt_",
					"et_",
					"em_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)*(melaDiscriminatorDCPGGH > 0)",
					"mm_":"(njetspt30>1)*(mjj>300)",
					"mt_":"(pt_2>40)*(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"et_":"(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"em_":"(pZetaMissVis>-10)*(njetspt30==2)*(mjj>300)",
					"tt_":"(njetspt30>1)*(jdeta>2.5)*(H_pt>100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_mjj": auto_rebin_binning,
						"_m_sv": auto_rebin_binning,
						"_melaDiscriminatorD0MinusGGH": auto_rebin_binning,
						},
					"mm_": {
						"_mjj":"300.0 700.0 1100.0 1500.0 2500.0"
						},
					"mt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						},
					"et_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						},
					"em_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						},
					"tt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						}
					}
				}
		self.categoriesDict["{analysis}{channel}Vbf3D_mela_GGH_DCPMinus{discriminator}"] = {
				"channel":[
					"mm_",
					"ee_",
					"mt_",
					"et_",
					"em_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)*(melaDiscriminatorDCPGGH < 0)",
					"mm_":"(njetspt30>1)*(mjj>300)",
					"mt_":"(pt_2>40)*(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"et_":"(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"em_":"(pZetaMissVis>-10)*(njetspt30==2)*(mjj>300)",
					"tt_":"(njetspt30>1)*(jdeta>2.5)*(H_pt>100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_mjj": auto_rebin_binning,
						"_m_sv": auto_rebin_binning,
						"_melaDiscriminatorD0MinusGGH": auto_rebin_binning,
						},
					"mm_": {
						"_mjj":"300.0 700.0 1100.0 1500.0 2500.0"
						},
					"mt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						},
					"et_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						},
					"em_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						},
					"tt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_melaDiscriminatorD0MinusGGH":"4,0,1",
						}
					}
				}
		self.categoriesDict["{analysis}{channel}Vbf4D_mela_GGH{discriminator}"] = {
				"channel":[
					"mm_",
					"ee_",
					"mt_",
					"et_",
					"em_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)*(melaDiscriminatorDCPGGH > 0)",
					"mm_":"(njetspt30>1)*(mjj>300)",
					"mt_":"(pt_2>40)*(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"et_":"(njetspt30>1)*(mjj>300)*(H_pt>50)",
					"em_":"(pZetaMissVis>-10)*(njetspt30==2)*(mjj>300)",
					"tt_":"(njetspt30>1)*(jdeta>2.5)*(H_pt>100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_mjj": auto_rebin_binning,
						"_m_sv": auto_rebin_binning,
						"_TMath::Sign(1,melaDiscriminatorDCPGGH)*melaDiscriminatorD0MinusGGH": auto_rebin_binning,

						},
					"mm_": {
						"_mjj":"300.0 700.0 1100.0 1500.0 2500.0"
						},
					"mt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_TMath::Sign(1,melaDiscriminatorDCPGGH)*melaDiscriminatorD0MinusGGH":"8,-1,1",
						},
					"et_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_TMath::Sign(1,melaDiscriminatorDCPGGH)*melaDiscriminatorD0MinusGGH": "8,-1,1",
						},
					"em_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_TMath::Sign(1,melaDiscriminatorDCPGGH)*melaDiscriminatorD0MinusGGH": "8,-1,1",
						},
					"tt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_TMath::Sign(1,melaDiscriminatorDCPGGH)*melaDiscriminatorD0MinusGGH": "8,-1,1",
						}
					}
				}

		self.categoriesDict["{analysis}{channel}Vbf3D_CP_jdeta{discriminator}"] = {
				"channel":[
					"mm_",
					"ee_",
					"mt_",
					"et_",
					"em_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mm_":"(njetspt30>1)*(mjj>300)",
					"mt_":"(pt_2>40)*(njetspt30>1)*(mjj>300)*(H_pt>150)",
					"et_":"(njetspt30>1)*(mjj>300)*(H_pt>150)",
					"em_":"(pZetaMissVis>-10)*(njetspt30==2)*(mjj>300)*(H_pt>150)",
					"tt_":"(njetspt30>1)*(jdeta>2.5)*(H_pt>150)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						#"_mjj": auto_rebin_binning,
						"_jdeta": auto_rebin_binning,
						"_m_sv": auto_rebin_binning,
						"_jdphi": auto_rebin_binning,
						},
					"mm_": {
						#"_mjj":"300.0 700.0 1100.0 1500.0 2500.0"
						"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),

						},
					"mt_": {
						#"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"et_": {
						#"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"em_": {
						#"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"tt_": {
						#"_mjj":" ".join([str(float(f)) for f in [300, 500, 8500]]),
						"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						}
					}
				}
		self.categoriesDict["{analysis}{channel}Vbf3D_CP{discriminator}"] = {
				"channel":[
					"mm_",
					"ee_",
					"mt_",
					"et_",
					"em_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mm_":"(njetspt30>1)*(mjj>300)",
					"mt_":"(pt_2>40)*(njetspt30>1)*(mjj>300)*(H_pt>150)",
					"et_":"(njetspt30>1)*(mjj>300)*(H_pt>150)",
					"em_":"(pZetaMissVis>-10)*(njetspt30==2)*(mjj>300)*(H_pt>150)",
					"tt_":"(njetspt30>1)*(jdeta>2.5)*(H_pt>150)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_mjj": auto_rebin_binning,
						#"_jdeta": auto_rebin_binning,
						"_m_sv": auto_rebin_binning,
						"_jdphi": auto_rebin_binning,
						},
					"mm_": {
						"_mjj":"300.0 700.0 1100.0 1500.0 2500.0"
						#"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),

						},
					"mt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 700, 8500]]),
						#"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"et_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 700, 8500]]),
						#"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"em_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 700, 8500]]),
						#"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						},
					"tt_": {
						"_mjj":" ".join([str(float(f)) for f in [300, 500, 700, 8500]]),
						#"_jdeta":" ".join([str(float(f)) for f in [0, 2, 3.5, 4.5,8]]),
						"_m_sv":" ".join([str(float(f)) for f in [0, 100, 400]]),
						"_jdphi":"12,-3.2,3.2",
						}
					}
				}

		"""
		Categories used in CP Final State studies.
		"""

		self.categoriesDict["{analysis}{channel}CP_IPmethod{discriminator}"] = {
				"channel":[
					"mt_",
					"et_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(decayMode_2==0)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_RHOmethod{discriminator}"] = {
				"channel":[
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(recoPhiStarCP_rho_merged!=-999)*(decayMode_1==1)*(decayMode_2==1)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_RHOmethod_0jets_lowmass{discriminator}"] = {
				"channel":[
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(recoPhiStarCP_rho_merged!=-999)*(decayMode_1==1)*(decayMode_2==1)*(njets==0)*(m_sv<100)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_RHOmethod_0jets_highmass{discriminator}"] = {
				"channel":[
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(recoPhiStarCP_rho_merged!=-999)*(decayMode_1==1)*(decayMode_2==1)*(njets==0)*(m_sv>100)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_RHOmethod_1jets_lowmass{discriminator}"] = {
				"channel":[
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(recoPhiStarCP_rho_merged!=-999)*(decayMode_1==1)*(decayMode_2==1)*(njets==1)*(m_sv<100)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_RHOmethod_1jets_highmass{discriminator}"] = {
				"channel":[
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(recoPhiStarCP_rho_merged!=-999)*(decayMode_1==1)*(decayMode_2==1)*(njets==1)*(m_sv>100)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_RHOmethod_2jets_lowmass{discriminator}"] = {
				"channel":[
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(recoPhiStarCP_rho_merged!=-999)*(decayMode_1==1)*(decayMode_2==1)*(njets==2)*(m_sv<100)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_RHOmethod_2jets_highmass{discriminator}"] = {
				"channel":[
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(recoPhiStarCP_rho_merged!=-999)*(decayMode_1==1)*(decayMode_2==1)*(njets==2)*(m_sv>100)",
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_COMBmethod{discriminator}"] = {
				"channel":[
					"mt_",
					"et_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mt_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)",
					"et_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)",
					"tt_": "(recoPhiStarCPCombMerged!=-999)*((decayMode_1==1 && decayMode_2!=1) || (decayMode_1!=1 && decayMode_2==1))"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_COMBmethod_0jets_lowmass{discriminator}"] = {
				"channel":[
					"mt_",
					"et_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mt_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==0)*(m_sv<100)",
					"et_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==0)*(m_sv<100)",
					"tt_": "(recoPhiStarCPCombMerged!=-999)*((decayMode_1==1 && decayMode_2!=1) || (decayMode_1!=1 && decayMode_2==1))*(njets==0)*(m_sv<100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_COMBmethod_0jets_highmass{discriminator}"] = {
				"channel":[
					"mt_",
					"et_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mt_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==0)*(m_sv>100)",
					"et_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==0)*(m_sv>100)",
					"tt_": "(recoPhiStarCPCombMerged!=-999)*((decayMode_1==1 && decayMode_2!=1) || (decayMode_1!=1 && decayMode_2==1))*(njets==0)*(m_sv>100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_COMBmethod_1jets_lowmass{discriminator}"] = {
				"channel":[
					"mt_",
					"et_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mt_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==1)*(m_sv<100)",
					"et_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==1)*(m_sv<100)",
					"tt_": "(recoPhiStarCPCombMerged!=-999)*((decayMode_1==1 && decayMode_2!=1) || (decayMode_1!=1 && decayMode_2==1))*(njets==1)*(m_sv<100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_COMBmethod_1jets_highmass{discriminator}"] = {
				"channel":[
					"mt_",
					"et_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mt_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==1)*(m_sv>100)",
					"et_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==1)*(m_sv>100)",
					"tt_": "(recoPhiStarCPCombMerged!=-999)*((decayMode_1==1 && decayMode_2!=1) || (decayMode_1!=1 && decayMode_2==1))*(njets==1)*(m_sv>100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_COMBmethod_2jets_lowmass{discriminator}"] = {
				"channel":[
					"mt_",
					"et_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mt_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==2)*(m_sv<100)",
					"et_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==2)*(m_sv<100)",
					"tt_": "(recoPhiStarCPCombMerged!=-999)*((decayMode_1==1 && decayMode_2!=1) || (decayMode_1!=1 && decayMode_2==1))*(njets==2)*(m_sv<100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}
		self.categoriesDict["{analysis}{channel}CP_COMBmethod_2jets_highmass{discriminator}"] = {
				"channel":[
					"mt_",
					"et_",
					"tt_"
					],
				"expressions":{
					"analysis": [
						"catHtt13TeV_"
						],
					"global":"(1.0)",
					"mt_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==2)*(m_sv>100)",
					"et_": "(recoPhiStarCPCombMerged!=-999)*(decayMode_2==1)*(njets==2)*(m_sv>100)",
					"tt_": "(recoPhiStarCPCombMerged!=-999)*((decayMode_1==1 && decayMode_2!=1) || (decayMode_1!=1 && decayMode_2==1))*(njets==2)*(m_sv>100)"
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_"
						],
					"global": {
						"_phiStarCP": auto_rebin_binning,
						}
					}
				}

		self.calculateBinnings()
		self.calculateExpressions()
		self.calculateDataCards()

	def calculateBinnings(self):
		self.binnings = {}
		for name, info in self.categoriesDict.iteritems():
			#print name
			channels = info["channel"]
			analysis = info["binnings"]["analysis"]
			global_keys = info["binnings"].get("global", {}).keys()
			for (channel,ana) in itertools.product(channels, analysis):
				#print channel, ana
				discriminators = global_keys
				if channel in info["binnings"].keys():
					discriminators += [x for x in info["binnings"][channel].keys() if not x in global_keys]
				for discriminator in discriminators:
					binning_string = info["binnings"].get(channel, info["binnings"]["global"]).get(discriminator, info["binnings"]["global"][discriminator])
					self.binnings[name.format(analysis=ana, channel=channel, discriminator=discriminator)]=binning_string

	def calculateDataCards(self):
		pass

	def calculateExpressions(self):
		self.expressions = {}
		for name, info in self.categoriesDict.iteritems():
			#print name
			channels = info["channel"]
			analysis = info["expressions"]["analysis"]
			global_expression = info["expressions"].get("global", "")
			for (channel,ana) in itertools.product(channels, analysis):
				expression = global_expression
				if channel in info["expressions"].keys():
					expression = self.combine([expression, info["expressions"][channel]])
				self.expressions[name.format(analysis=ana, channel=channel, discriminator="")]=expression
		#self.pp.pprint(self.expressions)


	def combine(self, strings_to_combine):
		return "(" + "*".join(strings_to_combine) + ")"

	def getExpressionsDict(self):
		return self.expressions

	def getBinningsDict(self):
		return self.binnings

	def getCategories(self, channels, prefix = True):
		Categories = {}
		placeholder=0
		for chan in channels:
			Categories[chan] = []
		for name, info in self.categoriesDict.iteritems():
			for chan in channels:
				if chan+"_" in info["channel"]:
					Categories[chan].append(name.format(analysis="", channel=(chan+"_") if prefix else "", discriminator=""))
				else:
					Categories[chan].append("placeholder{ph}".format(ph=placeholder))
					placeholder += 1
		return Categories

	def invert(self, expression):
		tmp_expression = "(" + expression + ")"
		return "(" + tmp_expression + "==0)"
