# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

from sets import Set
import re

class Run2Quantities():

	def __init__(self, nickname):
		pass

	@staticmethod
	def fourVectorQuantities():
		return [
			"leadingLepLV",
			"lep1LV",
			"posLepLV",
			"trailingLepLV",
			"lep2LV",
			"negLepLV",
			"leadingGenMatchedLepLV",
			"genMatchedLep1LV",
			"posGenMatchedLepLV",
			"leadingGenMatchedLepFound",
			"genMatchedLep1Found",
			"posGenMatchedLepFound",
			"trailingGenMatchedLepLV",
			"genMatchedLep2LV",
			"negGenMatchedLepLV",
			"trailingGenMatchedLepFound",
			"genMatchedLep2Found",
			"negGenMatchedLepFound",
			"diLepLV",
			"genDiLepLV",
			"genDiLepFound",
			"genDiTauLV",
			"genDiTauFound",
			"leadingJetLV",
			"trailingJetLV",
			"thirdJetLV",
			"fourthJetLV",
			"fifthJetLV",
			"sixthJetLV"
		]

	@staticmethod
	def fakeFactorQuantities():
		return [
			"jetToTauFakeWeight_comb",
			"jetToTauFakeWeight_qcd_up",
			"jetToTauFakeWeight_qcd_down",
			"jetToTauFakeWeight_w_up",
			"jetToTauFakeWeight_w_down",
			"jetToTauFakeWeight_tt_corr_up",
			"jetToTauFakeWeight_tt_corr_down",
			"jetToTauFakeWeight_tt_stat_up",
			"jetToTauFakeWeight_tt_stat_down",
			"jetToTauFakeWeight_frac_w_up",
			"jetToTauFakeWeight_frac_w_down",
			"jetToTauFakeWeight_frac_qcd_up",
			"jetToTauFakeWeight_frac_qcd_down",
			"jetToTauFakeWeight_frac_tt_up",
			"jetToTauFakeWeight_frac_tt_down",
			"jetToTauFakeWeight_frac_dy_up",
			"jetToTauFakeWeight_frac_dy_down",
			"jetToTauFakeWeight_ff_qcd_ss",
			"jetToTauFakeWeight_ff_qcd_ss_up",
			"jetToTauFakeWeight_ff_qcd_ss_down",
			"jetToTauFakeWeight_ff_qcd_os",
			"jetToTauFakeWeight_ff_qcd_os_up",
			"jetToTauFakeWeight_ff_qcd_os_down",
			"jetToTauFakeWeight_ff_w",
			"jetToTauFakeWeight_ff_w_up",
			"jetToTauFakeWeight_ff_w_down",
			"jetToTauFakeWeight_ff_tt",
			"jetToTauFakeWeight_ff_tt_corr_up",
			"jetToTauFakeWeight_ff_tt_corr_down",
			"jetToTauFakeWeight_ff_tt_stat_up",
			"jetToTauFakeWeight_ff_tt_stat_down"
		]

	@staticmethod
	def extraTauQuantities():
		return [
			"decayDistX_1",
			"decayDistX_2",
			"decayDistY_1",
			"decayDistY_2",
			"decayDistZ_1",
			"decayDistZ_2",
			"decayDistM_1",
			"decayDistM_2",
			"nPhoton_1",
			"nPhoton_2",
			"ptWeightedDetaStrip_1",
			"ptWeightedDetaStrip_2",
			"ptWeightedDphiStrip_1",
			"ptWeightedDphiStrip_2",
			"ptWeightedDrSignal_1",
			"ptWeightedDrSignal_2",
			"ptWeightedDrIsolation_1",
			"ptWeightedDrIsolation_2",
			"leadingTrackChi2_1",
			"leadingTrackChi2_2",
			"eRatio_1",
			"eRatio_2",
			"MVAdxy_sign_1",
			"MVAdxy_sign_2",
			"MVAdxy_abs_1",
			"MVAdxy_abs_2",
			"MVAdxy_signal_1",
			"MVAdxy_signal_2",
			"MVAdxy_ip3d_sign_1",
			"MVAdxy_ip3d_sign_2",
			"MVAdxy_ip3d_abs_1",
			"MVAdxy_ip3d_abs_2",
			"MVAdxy_ip3d_signal_1",
			"MVAdxy_ip3d_signal_2",
			"hasSecondaryVertex_1",
			"hasSecondaryVertex_2",
			"flightLengthSig_1",
			"flightLengthSig_2"
		]

	@staticmethod
	def lheWeightsDYQuantities():
		return [
			"minPdfLheWeight",
			"maxPdfLheWeight",
			"meanPdfLheWeight",
			"stdevPdfLheWeight",
			"meanPdfLheWeightUp",
			"stdevPdfLheWeightUp",
			"meanPdfLheWeightDown",
			"stdevPdfLheWeightDown",
			"minAlphaSLheWeight",
			"maxAlphaSLheWeight",
			"meanAlphaSLheWeight",
			"stdevAlphaSLheWeight",
			"meanAlphaSLheWeightUp",
			"stdevAlphaSLheWeightUp",
			"meanAlphaSLheWeightDown",
			"stdevAlphaSLheWeightDown",
			"minScaleLheWeight",
			"maxScaleLheWeight",
			"meanScaleLheWeight",
			"stdevScaleLheWeight",
			"meanScaleLheWeightUp",
			"stdevScaleLheWeightUp",
			"meanScaleLheWeightDown",
			"stdevScaleLheWeightDown",
			"NNPDF30_lo_as_0130_LHgrid__Member_0",
			"NNPDF30_lo_as_0130_LHgrid__Member_1",
			"NNPDF30_lo_as_0130_LHgrid__Member_10",
			"NNPDF30_lo_as_0130_LHgrid__Member_100",
			"NNPDF30_lo_as_0130_LHgrid__Member_11",
			"NNPDF30_lo_as_0130_LHgrid__Member_12",
			"NNPDF30_lo_as_0130_LHgrid__Member_13",
			"NNPDF30_lo_as_0130_LHgrid__Member_14",
			"NNPDF30_lo_as_0130_LHgrid__Member_15",
			"NNPDF30_lo_as_0130_LHgrid__Member_16",
			"NNPDF30_lo_as_0130_LHgrid__Member_17",
			"NNPDF30_lo_as_0130_LHgrid__Member_18",
			"NNPDF30_lo_as_0130_LHgrid__Member_19",
			"NNPDF30_lo_as_0130_LHgrid__Member_2",
			"NNPDF30_lo_as_0130_LHgrid__Member_20",
			"NNPDF30_lo_as_0130_LHgrid__Member_21",
			"NNPDF30_lo_as_0130_LHgrid__Member_22",
			"NNPDF30_lo_as_0130_LHgrid__Member_23",
			"NNPDF30_lo_as_0130_LHgrid__Member_24",
			"NNPDF30_lo_as_0130_LHgrid__Member_25",
			"NNPDF30_lo_as_0130_LHgrid__Member_26",
			"NNPDF30_lo_as_0130_LHgrid__Member_27",
			"NNPDF30_lo_as_0130_LHgrid__Member_28",
			"NNPDF30_lo_as_0130_LHgrid__Member_29",
			"NNPDF30_lo_as_0130_LHgrid__Member_3",
			"NNPDF30_lo_as_0130_LHgrid__Member_30",
			"NNPDF30_lo_as_0130_LHgrid__Member_31",
			"NNPDF30_lo_as_0130_LHgrid__Member_32",
			"NNPDF30_lo_as_0130_LHgrid__Member_33",
			"NNPDF30_lo_as_0130_LHgrid__Member_34",
			"NNPDF30_lo_as_0130_LHgrid__Member_35",
			"NNPDF30_lo_as_0130_LHgrid__Member_36",
			"NNPDF30_lo_as_0130_LHgrid__Member_37",
			"NNPDF30_lo_as_0130_LHgrid__Member_38",
			"NNPDF30_lo_as_0130_LHgrid__Member_39",
			"NNPDF30_lo_as_0130_LHgrid__Member_4",
			"NNPDF30_lo_as_0130_LHgrid__Member_40",
			"NNPDF30_lo_as_0130_LHgrid__Member_41",
			"NNPDF30_lo_as_0130_LHgrid__Member_42",
			"NNPDF30_lo_as_0130_LHgrid__Member_43",
			"NNPDF30_lo_as_0130_LHgrid__Member_44",
			"NNPDF30_lo_as_0130_LHgrid__Member_45",
			"NNPDF30_lo_as_0130_LHgrid__Member_46",
			"NNPDF30_lo_as_0130_LHgrid__Member_47",
			"NNPDF30_lo_as_0130_LHgrid__Member_48",
			"NNPDF30_lo_as_0130_LHgrid__Member_49",
			"NNPDF30_lo_as_0130_LHgrid__Member_5",
			"NNPDF30_lo_as_0130_LHgrid__Member_50",
			"NNPDF30_lo_as_0130_LHgrid__Member_51",
			"NNPDF30_lo_as_0130_LHgrid__Member_52",
			"NNPDF30_lo_as_0130_LHgrid__Member_53",
			"NNPDF30_lo_as_0130_LHgrid__Member_54",
			"NNPDF30_lo_as_0130_LHgrid__Member_55",
			"NNPDF30_lo_as_0130_LHgrid__Member_56",
			"NNPDF30_lo_as_0130_LHgrid__Member_57",
			"NNPDF30_lo_as_0130_LHgrid__Member_58",
			"NNPDF30_lo_as_0130_LHgrid__Member_59",
			"NNPDF30_lo_as_0130_LHgrid__Member_6",
			"NNPDF30_lo_as_0130_LHgrid__Member_60",
			"NNPDF30_lo_as_0130_LHgrid__Member_61",
			"NNPDF30_lo_as_0130_LHgrid__Member_62",
			"NNPDF30_lo_as_0130_LHgrid__Member_63",
			"NNPDF30_lo_as_0130_LHgrid__Member_64",
			"NNPDF30_lo_as_0130_LHgrid__Member_65",
			"NNPDF30_lo_as_0130_LHgrid__Member_66",
			"NNPDF30_lo_as_0130_LHgrid__Member_67",
			"NNPDF30_lo_as_0130_LHgrid__Member_68",
			"NNPDF30_lo_as_0130_LHgrid__Member_69",
			"NNPDF30_lo_as_0130_LHgrid__Member_7",
			"NNPDF30_lo_as_0130_LHgrid__Member_70",
			"NNPDF30_lo_as_0130_LHgrid__Member_71",
			"NNPDF30_lo_as_0130_LHgrid__Member_72",
			"NNPDF30_lo_as_0130_LHgrid__Member_73",
			"NNPDF30_lo_as_0130_LHgrid__Member_74",
			"NNPDF30_lo_as_0130_LHgrid__Member_75",
			"NNPDF30_lo_as_0130_LHgrid__Member_76",
			"NNPDF30_lo_as_0130_LHgrid__Member_77",
			"NNPDF30_lo_as_0130_LHgrid__Member_78",
			"NNPDF30_lo_as_0130_LHgrid__Member_79",
			"NNPDF30_lo_as_0130_LHgrid__Member_8",
			"NNPDF30_lo_as_0130_LHgrid__Member_80",
			"NNPDF30_lo_as_0130_LHgrid__Member_81",
			"NNPDF30_lo_as_0130_LHgrid__Member_82",
			"NNPDF30_lo_as_0130_LHgrid__Member_83",
			"NNPDF30_lo_as_0130_LHgrid__Member_84",
			"NNPDF30_lo_as_0130_LHgrid__Member_85",
			"NNPDF30_lo_as_0130_LHgrid__Member_86",
			"NNPDF30_lo_as_0130_LHgrid__Member_87",
			"NNPDF30_lo_as_0130_LHgrid__Member_88",
			"NNPDF30_lo_as_0130_LHgrid__Member_89",
			"NNPDF30_lo_as_0130_LHgrid__Member_9",
			"NNPDF30_lo_as_0130_LHgrid__Member_90",
			"NNPDF30_lo_as_0130_LHgrid__Member_91",
			"NNPDF30_lo_as_0130_LHgrid__Member_92",
			"NNPDF30_lo_as_0130_LHgrid__Member_93",
			"NNPDF30_lo_as_0130_LHgrid__Member_94",
			"NNPDF30_lo_as_0130_LHgrid__Member_95",
			"NNPDF30_lo_as_0130_LHgrid__Member_96",
			"NNPDF30_lo_as_0130_LHgrid__Member_97",
			"NNPDF30_lo_as_0130_LHgrid__Member_98",
			"NNPDF30_lo_as_0130_LHgrid__Member_99",
			"NNPDF30_lo_as_0118_LHgrid__Member_0",
			"Central_scale_variation__mur_0_5_muf_0_5",
			"Central_scale_variation__mur_0_5_muf_1",
			#"Central_scale_variation__mur_0_5_muf_2",
			"Central_scale_variation__mur_1_muf_0_5",
			"Central_scale_variation__mur_1_muf_1",
			"Central_scale_variation__mur_1_muf_2",
			#"Central_scale_variation__mur_2_muf_0_5",
			"Central_scale_variation__mur_2_muf_1",
			"Central_scale_variation__mur_2_muf_2"
		]

	@staticmethod
	def lheWeightsHTTQuantities():
		return [
			"minPdfLheWeight",
			"maxPdfLheWeight",
			"meanPdfLheWeight",
			"stdevPdfLheWeight",
			"meanPdfLheWeightUp",
			"stdevPdfLheWeightUp",
			"meanPdfLheWeightDown",
			"stdevPdfLheWeightDown",
			"minAlphaSLheWeight",
			"maxAlphaSLheWeight",
			"meanAlphaSLheWeight",
			"stdevAlphaSLheWeight",
			"meanAlphaSLheWeightUp",
			"stdevAlphaSLheWeightUp",
			"meanAlphaSLheWeightDown",
			"stdevAlphaSLheWeightDown",
			"minScaleLheWeight",
			"maxScaleLheWeight",
			"meanScaleLheWeight",
			"stdevScaleLheWeight",
			"meanScaleLheWeightUp",
			"stdevScaleLheWeightUp",
			"meanScaleLheWeightDown",
			"stdevScaleLheWeightDown",
			"PDF_variation__PDF_set___260001",
			"PDF_variation__PDF_set___260002",
			"PDF_variation__PDF_set___260003",
			"PDF_variation__PDF_set___260004",
			"PDF_variation__PDF_set___260005",
			"PDF_variation__PDF_set___260006",
			"PDF_variation__PDF_set___260007",
			"PDF_variation__PDF_set___260008",
			"PDF_variation__PDF_set___260009",
			"PDF_variation__PDF_set___260010",
			"PDF_variation__PDF_set___260011",
			"PDF_variation__PDF_set___260012",
			"PDF_variation__PDF_set___260013",
			"PDF_variation__PDF_set___260014",
			"PDF_variation__PDF_set___260015",
			"PDF_variation__PDF_set___260016",
			"PDF_variation__PDF_set___260017",
			"PDF_variation__PDF_set___260018",
			"PDF_variation__PDF_set___260019",
			"PDF_variation__PDF_set___260020",
			"PDF_variation__PDF_set___260021",
			"PDF_variation__PDF_set___260022",
			"PDF_variation__PDF_set___260023",
			"PDF_variation__PDF_set___260024",
			"PDF_variation__PDF_set___260025",
			"PDF_variation__PDF_set___260026",
			"PDF_variation__PDF_set___260027",
			"PDF_variation__PDF_set___260028",
			"PDF_variation__PDF_set___260029",
			"PDF_variation__PDF_set___260030",
			"PDF_variation__PDF_set___260031",
			"PDF_variation__PDF_set___260032",
			"PDF_variation__PDF_set___260033",
			"PDF_variation__PDF_set___260034",
			"PDF_variation__PDF_set___260035",
			"PDF_variation__PDF_set___260036",
			"PDF_variation__PDF_set___260037",
			"PDF_variation__PDF_set___260038",
			"PDF_variation__PDF_set___260039",
			"PDF_variation__PDF_set___260040",
			"PDF_variation__PDF_set___260041",
			"PDF_variation__PDF_set___260042",
			"PDF_variation__PDF_set___260043",
			"PDF_variation__PDF_set___260044",
			"PDF_variation__PDF_set___260045",
			"PDF_variation__PDF_set___260046",
			"PDF_variation__PDF_set___260047",
			"PDF_variation__PDF_set___260048",
			"PDF_variation__PDF_set___260049",
			"PDF_variation__PDF_set___260050",
			"PDF_variation__PDF_set___260051",
			"PDF_variation__PDF_set___260052",
			"PDF_variation__PDF_set___260053",
			"PDF_variation__PDF_set___260054",
			"PDF_variation__PDF_set___260055",
			"PDF_variation__PDF_set___260056",
			"PDF_variation__PDF_set___260057",
			"PDF_variation__PDF_set___260058",
			"PDF_variation__PDF_set___260059",
			"PDF_variation__PDF_set___260060",
			"PDF_variation__PDF_set___260061",
			"PDF_variation__PDF_set___260062",
			"PDF_variation__PDF_set___260063",
			"PDF_variation__PDF_set___260064",
			"PDF_variation__PDF_set___260065",
			"PDF_variation__PDF_set___260066",
			"PDF_variation__PDF_set___260067",
			"PDF_variation__PDF_set___260068",
			"PDF_variation__PDF_set___260069",
			"PDF_variation__PDF_set___260070",
			"PDF_variation__PDF_set___260071",
			"PDF_variation__PDF_set___260072",
			"PDF_variation__PDF_set___260073",
			"PDF_variation__PDF_set___260074",
			"PDF_variation__PDF_set___260075",
			"PDF_variation__PDF_set___260076",
			"PDF_variation__PDF_set___260077",
			"PDF_variation__PDF_set___260078",
			"PDF_variation__PDF_set___260079",
			"PDF_variation__PDF_set___260080",
			"PDF_variation__PDF_set___260081",
			"PDF_variation__PDF_set___260082",
			"PDF_variation__PDF_set___260083",
			"PDF_variation__PDF_set___260084",
			"PDF_variation__PDF_set___260085",
			"PDF_variation__PDF_set___260086",
			"PDF_variation__PDF_set___260087",
			"PDF_variation__PDF_set___260088",
			"PDF_variation__PDF_set___260089",
			"PDF_variation__PDF_set___260090",
			"PDF_variation__PDF_set___260091",
			"PDF_variation__PDF_set___260092",
			"PDF_variation__PDF_set___260093",
			"PDF_variation__PDF_set___260094",
			"PDF_variation__PDF_set___260095",
			"PDF_variation__PDF_set___260096",
			"PDF_variation__PDF_set___260097",
			"PDF_variation__PDF_set___260098",
			"PDF_variation__PDF_set___260099",
			"PDF_variation__PDF_set___260100",
			"PDF_variation__PDF_set___265000",
			"PDF_variation__PDF_set___266000",
			"scale_variation__muR_1_muF_1",
			"scale_variation__muR_1_muF_2",
			"scale_variation__muR_1_muF_0_5",
			"scale_variation__muR_2_muF_1",
			"scale_variation__muR_2_muF_2",
			#"scale_variation__muR_2_muF_0_5",
			"scale_variation__muR_0_5_muF_1",
			#"scale_variation__muR_0_5_muF_2",
			"scale_variation__muR_0_5_muF_0_5"
		]
	#TODO, etah and etasep?
	@staticmethod
	def splitJecUncertaintyQuantities(observables = ["njetspt30", "mjj", "jdeta", "jdphi"]):
		l = []
		jec_sources = ["_AbsoluteFlavMap",
			"_AbsoluteMPFBias",
			"_AbsoluteScale",
			"_AbsoluteStat",
			"_FlavorQCD",
			"_Fragmentation",
			"_PileUpDataMC",
			"_PileUpPtBB",
			"_PileUpPtEC1",
			"_PileUpPtEC2",
			"_PileUpPtHF",
			"_PileUpPtRef",
			"_RelativeBal",
			"_RelativeFSR",
			"_RelativeJEREC1",
			"_RelativeJEREC2",
			"_RelativeJERHF",
			"_RelativePtBB",
			"_RelativePtEC1",
			"_RelativePtEC2",
			"_RelativePtHF",
			"_RelativeStatEC",
			"_RelativeStatFSR",
			"_RelativeStatHF",
			"_SinglePionECAL",
			"_SinglePionHCAL",
			"_TimePtEta",
			"_Total",
			"_Eta0To5",
			"_Eta3To5",
			"_Eta0To3",
			"_Closure",
			"_ClosureCPGroupings"
		]

		for observable in observables:
			l += [observable + source + "Up" for source in jec_sources]
			l += [observable + source + "Down" for source in jec_sources]

		return l

	@staticmethod
	def svfitSyncQuantities(m91=False, m125=False):
		l = [
			"m_sv",
			"pt_sv",
			"eta_sv",
			"phi_sv",
			"#met_sv",
			"#m_sv_Up",
			"#m_sv_Down",

			"svfitAvailable",
			"svfitLV",
			"svfitTau1Available",
			"svfitTau1LV",
			"svfitTau1ERatio",
			"svfitTau2Available",
			"svfitTau2LV",
			"svfitTau2ERatio"
		]
		if m91:
			l+=[
				"svfitM91Available",
				"svfitM91LV",
				"svfitM91Tau1Available",
				"svfitM91Tau1LV",
				"svfitM91Tau1ERatio",
				"svfitM91Tau2Available",
				"svfitM91Tau2LV",
				"svfitM91Tau2ERatio"
			]
		if m125:
			l+=[
				"svfitM125Available",
				"svfitM125LV",
				"svfitM125Tau1Available",
				"svfitM125Tau1LV",
				"svfitM125Tau1ERatio",
				"svfitM125Tau2Available",
				"svfitM125Tau2LV",
				"svfitM125Tau2ERatio"
			]
		return l

	@staticmethod
	def syncQuantities(nickname):
		sync_quantities_list = [
			"nickname",
			"input",
			"run",
			"lumi",
			"event",
			"evt",
			"npv",
			"npu",
			"rho",
			#"mcweight",
			"puweight",
			#"idweight_1",
			#"idweight_2",
			#"isoweight_1",
			#"isoweight_2",
			#"effweight",
			"weight",
			#"embeddedWeight",
			"m_vis",
			"H_mass",
			"H_pt",
			"diLepMass",
			"diLepMassSmearUp",
			"diLepMassSmearDown",
			"diLepGenMass",
			"diLepMetMt",
			"pt_1",
			"phi_1",
			"eta_1",
			"m_1",
			"q_1",
			"iso_1",
			#"mva_1",
			"d0_1",
			"dZ_1",
			#"passid_1",
			#"passiso_1",
			"mt_1",
			"pt_2",
			"phi_2",
			"eta_2",
			"m_2",
			"q_2",
			"iso_2",
			"d0_2",
			"dZ_2",
			#"mva_2",
			#"passid_2",
			#"passiso_2",
			"mt_2",
			"met",
			"metphi",
			#"l1met",
			#"l1metphi",
			#"l1metcorr",
			#"calomet",
			#"calometphi",
			#"calometcorr",
			#"calometphicorr",
			"mvamet",
			"mvametphi",
			"pzetavis",
			"pzetamiss",
			"pZetaMissVis",
			"metcov00",
			"metcov01",
			"metcov10",
			"metcov11",
			"mvacov00",
			"mvacov01",
			"mvacov10",
			"mvacov11",
			"jpt_1",
			"jeta_1",
			"jphi_1",
			"jm_1",
			"jmva_1",
			"jcsv_1",
			"bpt_1",
			"beta_1",
			"bphi_1",
			"bmva_1",
			"bcsv_1",
			"jpt_2",
			"jeta_2",
			"jphi_2",
			"jm_2",
			"jmva_2",
			"jcsv_2",
			"bpt_2",
			"beta_2",
			"bphi_2",
			"bmva_2",
			"bcsv_2",
			"mjj",
			"jdeta",
			"njetingap",
			"njetingap20",
			"jdphi",
			"etaSep",
			"etaH_cut",

			"etaH_cut_CP",
			"diJetPt_CP1",
			"diJetPhi_CP1",
			"diJetEta_CP1",
			"mjj_CP1",
			"jdphi_CP1",
			"jdeta_CP1",
			"etasep_CP1",
			"jpt_1_CP1",
			"jpt_2_CP1",
			"jeta_1_CP1",
			"jeta_2_CP1",
			"jphi_1_CP1",
			"jphi_2_CP1",

			"diJetPt_CP2",
			"diJetPhi_CP2",
			"diJetEta_CP2",
			"mjj_CP2",
			"jdphi_CP2",
			"jdeta_CP2",
			"etasep_CP2",
			"jpt_1_CP2",
			"jpt_2_CP2",
			"jeta_1_CP2",
			"jeta_2_CP2",
			"jphi_1_CP2",
			"jphi_2_CP2",

			"dijetpt",
			"dijetphi",
			"hdijetphi",
			"ptvis",
			"nbtag",
			"njets",
			"njetspt20",
			"njetspt30",
			#"mva_gf",
			#"mva_vbf",
			"trigweight_1",
			"chargedIsoPtSum_1",
			"neutralIsoPtSum_1",
			"puCorrPtSum_1",
			"footprintCorrection_1",
			"photonPtSumOutsideSignalCone_1",
			"againstMuonLoose3_1",
			"againstMuonTight3_1",
			"againstElectronLooseMVA6_1",
			"againstElectronMediumMVA6_1",
			"againstElectronTightMVA6_1",
			"againstElectronVLooseMVA6_1",
			"againstElectronVTightMVA6_1",
			"byCombinedIsolationDeltaBetaCorrRaw3Hits_1",
			"byLooseCombinedIsolationDeltaBetaCorr3Hits_1",
			"byMediumCombinedIsolationDeltaBetaCorr3Hits_1",
			"byTightCombinedIsolationDeltaBetaCorr3Hits_1",
			"byIsolationMVArun2v1DBoldDMwLTraw_1",
			"byVLooseIsolationMVArun2v1DBoldDMwLT_1",
			"byLooseIsolationMVArun2v1DBoldDMwLT_1",
			"byMediumIsolationMVArun2v1DBoldDMwLT_1",
			"byTightIsolationMVArun2v1DBoldDMwLT_1",
			"byVTightIsolationMVArun2v1DBoldDMwLT_1",
			"byVVTightIsolationMVArun2v1DBoldDMwLT_1",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1raw_1",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose_1",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1Loose_1",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1Medium_1",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1Tight_1",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1VTight_1",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight_1",
			"decayModeFinding_1",
			"decayModeFindingNewDMs_1",
			"trigweight_2",
			"chargedIsoPtSum_2",
			"neutralIsoPtSum_2",
			"puCorrPtSum_2",
			"footprintCorrection_2",
			"photonPtSumOutsideSignalCone_2",
			"againstMuonLoose3_2",
			"againstMuonTight3_2",
			"againstElectronLooseMVA6_2",
			"againstElectronMediumMVA6_2",
			"againstElectronTightMVA6_2",
			"againstElectronVLooseMVA6_2",
			"againstElectronVTightMVA6_2",
			"byCombinedIsolationDeltaBetaCorrRaw3Hits_2",
			"byLooseCombinedIsolationDeltaBetaCorr3Hits_2",
			"byMediumCombinedIsolationDeltaBetaCorr3Hits_2",
			"byTightCombinedIsolationDeltaBetaCorr3Hits_2",
			"byIsolationMVArun2v1DBoldDMwLTraw_2",
			"byVLooseIsolationMVArun2v1DBoldDMwLT_2",
			"byLooseIsolationMVArun2v1DBoldDMwLT_2",
			"byMediumIsolationMVArun2v1DBoldDMwLT_2",
			"byTightIsolationMVArun2v1DBoldDMwLT_2",
			"byVTightIsolationMVArun2v1DBoldDMwLT_2",
			"byVVTightIsolationMVArun2v1DBoldDMwLT_2",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1raw_2",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose_2",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1Loose_2",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1Medium_2",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1Tight_2",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1VTight_2",
			"rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight_2",
			"decayModeFinding_2",
			"decayModeFindingNewDMs_2",
			"NUP",
			"id_m_loose_1",
			"id_m_medium_1",
			"id_m_tight_1",
			"id_m_highpt_1",
			"id_e_mva_nt_loose_1",
			"id_e_cut_veto_1",
			"id_e_cut_loose_1",
			"id_e_cut_medium_1",
			"id_e_cut_tight_1",
			"pt_tt",
			"dilepton_veto",
			"extraelec_veto",
			"extramuon_veto",
			"gen_match_1",
			"gen_match_2",
			"decayMode_1",
			"decayMode_2",
			"npartons",
			"genbosonmass",
			"leadingJetGenMatch",
			"trailingJetGenMatch",
			"metfilter_flag",
		]
		if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
			sync_quantities_list += [
					"byIsolationMVArun2017v1DBoldDMwLTraw2017_1",
					"byVVLooseIsolationMVArun2017v1DBoldDMwLT2017_1",
					"byVLooseIsolationMVArun2017v1DBoldDMwLT2017_1",
					"byLooseIsolationMVArun2017v1DBoldDMwLT2017_1",
					"byMediumIsolationMVArun2017v1DBoldDMwLT2017_1",
					"byTightIsolationMVArun2017v1DBoldDMwLT2017_1",
					"byVTightIsolationMVArun2017v1DBoldDMwLT2017_1",
					"byVVTightIsolationMVArun2017v1DBoldDMwLT2017_1",
					"byIsolationMVArun2017v1DBoldDMwLTraw2017_2",
					"byVVLooseIsolationMVArun2017v1DBoldDMwLT2017_2",
					"byVLooseIsolationMVArun2017v1DBoldDMwLT2017_2",
					"byLooseIsolationMVArun2017v1DBoldDMwLT2017_2",
					"byMediumIsolationMVArun2017v1DBoldDMwLT2017_2",
					"byTightIsolationMVArun2017v1DBoldDMwLT2017_2",
					"byVTightIsolationMVArun2017v1DBoldDMwLT2017_2",
					"byVVTightIsolationMVArun2017v1DBoldDMwLT2017_2",
					"byIsolationMVArun2017v2DBoldDMwLTraw2017_1",
					"byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_1",
					"byVLooseIsolationMVArun2017v2DBoldDMwLT2017_1",
					"byLooseIsolationMVArun2017v2DBoldDMwLT2017_1",
					"byMediumIsolationMVArun2017v2DBoldDMwLT2017_1",
					"byTightIsolationMVArun2017v2DBoldDMwLT2017_1",
					"byVTightIsolationMVArun2017v2DBoldDMwLT2017_1",
					"byVVTightIsolationMVArun2017v2DBoldDMwLT2017_1",
					"byIsolationMVArun2017v2DBoldDMwLTraw2017_2",
					"byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_2",
					"byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2",
					"byLooseIsolationMVArun2017v2DBoldDMwLT2017_2",
					"byMediumIsolationMVArun2017v2DBoldDMwLT2017_2",
					"byTightIsolationMVArun2017v2DBoldDMwLT2017_2",
					"byVTightIsolationMVArun2017v2DBoldDMwLT2017_2",
					"byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2",
					"byIsolationMVArun2017v2DBnewDMwLTraw2017_1",
					"byVVLooseIsolationMVArun2017v2DBnewDMwLT2017_1",
					"byVLooseIsolationMVArun2017v2DBnewDMwLT2017_1",
					"byLooseIsolationMVArun2017v2DBnewDMwLT2017_1",
					"byMediumIsolationMVArun2017v2DBnewDMwLT2017_1",
					"byTightIsolationMVArun2017v2DBnewDMwLT2017_1",
					"byVTightIsolationMVArun2017v2DBnewDMwLT2017_1",
					"byVVTightIsolationMVArun2017v2DBnewDMwLT2017_1",
					"byIsolationMVArun2017v2DBnewDMwLTraw2017_2",
					"byVVLooseIsolationMVArun2017v2DBnewDMwLT2017_2",
					"byVLooseIsolationMVArun2017v2DBnewDMwLT2017_2",
					"byLooseIsolationMVArun2017v2DBnewDMwLT2017_2",
					"byMediumIsolationMVArun2017v2DBnewDMwLT2017_2",
					"byTightIsolationMVArun2017v2DBnewDMwLT2017_2",
					"byVTightIsolationMVArun2017v2DBnewDMwLT2017_2",
					"byVVTightIsolationMVArun2017v2DBnewDMwLT2017_2",
					"byIsolationMVArun2017v2DBoldDMdR0p3wLTraw2017_1",
					"byVVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017_1",
					"byVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017_1",
					"byLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017_1",
					"byMediumIsolationMVArun2017v2DBoldDMdR0p3wLT2017_1",
					"byTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017_1",
					"byVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017_1",
					"byVVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017_1",
					"byIsolationMVArun2017v2DBoldDMdR0p3wLTraw2017_2",
					"byVVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017_2",
					"byVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017_2",
					"byLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017_2",
					"byMediumIsolationMVArun2017v2DBoldDMdR0p3wLT2017_2",
					"byTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017_2",
					"byVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017_2",
					"byVVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017_2",
					"byDeepTau2017v2p1VSjetraw_1",
					"byVVVLooseDeepTau2017v2p1VSjet_1",
					"byVVLooseDeepTau2017v2p1VSjet_1",
					"byVLooseDeepTau2017v2p1VSjet_1",
					"byLooseDeepTau2017v2p1VSjet_1",
					"byMediumDeepTau2017v2p1VSjet_1",
					"byTightDeepTau2017v2p1VSjet_1",
					"byVTightDeepTau2017v2p1VSjet_1",
					"byVVTightDeepTau2017v2p1VSjet_1",
					"byDeepTau2017v2p1VSeraw_1",
					"byVVVLooseDeepTau2017v2p1VSe_1",
					"byVVLooseDeepTau2017v2p1VSe_1",
					"byVLooseDeepTau2017v2p1VSe_1",
					"byLooseDeepTau2017v2p1VSe_1",
					"byMediumDeepTau2017v2p1VSe_1",
					"byTightDeepTau2017v2p1VSe_1",
					"byVTightDeepTau2017v2p1VSe_1",
					"byVVTightDeepTau2017v2p1VSe_1",
					"byDeepTau2017v2p1VSmuraw_1",
					"byVLooseDeepTau2017v2p1VSmu_1",
					"byLooseDeepTau2017v2p1VSmu_1",
					"byMediumDeepTau2017v2p1VSmu_1",
					"byTightDeepTau2017v2p1VSmu_1",
					"byDeepTau2017v2p1VSjetraw_2",
					"byVVVLooseDeepTau2017v2p1VSjet_2",
					"byVVLooseDeepTau2017v2p1VSjet_2",
					"byVLooseDeepTau2017v2p1VSjet_2",
					"byLooseDeepTau2017v2p1VSjet_2",
					"byMediumDeepTau2017v2p1VSjet_2",
					"byTightDeepTau2017v2p1VSjet_2",
					"byVTightDeepTau2017v2p1VSjet_2",
					"byVVTightDeepTau2017v2p1VSjet_2",
					"byDeepTau2017v2p1VSeraw_2",
					"byVVVLooseDeepTau2017v2p1VSe_2",
					"byVVLooseDeepTau2017v2p1VSe_2",
					"byVLooseDeepTau2017v2p1VSe_2",
					"byLooseDeepTau2017v2p1VSe_2",
					"byMediumDeepTau2017v2p1VSe_2",
					"byTightDeepTau2017v2p1VSe_2",
					"byVTightDeepTau2017v2p1VSe_2",
					"byVVTightDeepTau2017v2p1VSe_2",
					"byDeepTau2017v2p1VSmuraw_2",
					"byVLooseDeepTau2017v2p1VSmu_2",
					"byLooseDeepTau2017v2p1VSmu_2",
					"byMediumDeepTau2017v2p1VSmu_2",
					"byTightDeepTau2017v2p1VSmu_2",
					"decayModeMVA_1",
					"decayModeMVA_2",
			]
		return sync_quantities_list
