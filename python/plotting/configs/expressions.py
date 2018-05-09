
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.expressions as expressions

class ExpressionsDict(expressions.ExpressionsDict):
	def __init__(self, additional_expressions=None):
		super(ExpressionsDict, self).__init__(additional_expressions=additional_expressions)

		self.expressions_dict["integral"] = "0.5"

		# blinding (of data)
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			pass # self.expressions_dict["blind_"+channel+"_svfitMass"] = "((svfitMass<100.0)+(svfitMass>200.0))"

		# category cuts
		self.expressions_dict["cat_inclusive"] = "1.0"
		self.expressions_dict["cat_0jet"] = "njetspt20 < 1"
		self.expressions_dict["cat_1jet"] = "(njetspt20 > 0)*(njetspt20 < 2)"
		self.expressions_dict["cat_2jet"] = "njetspt20 > 1"

		# Z->tautau categories
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			self.expressions_dict["catZtt13TeV_"+channel+"_inclusive"] = "1.0"
			self.expressions_dict["catZtt13TeV_"+channel+"_2jet_inclusive"] = "(njetspt30>1)"
			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_inclusive"] = "(njetspt30>0)*(njetspt30<2)"
			self.expressions_dict["catZtt13TeV_"+channel+"_0jet_inclusive"] = "(njetspt30<1)"

			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_low"] = self.expressions_dict["catZtt13TeV_"+channel+"_1jet_inclusive"] + ("*(H_pt<50)") + ("*(nbtag<1)")
			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_medium"] = self.expressions_dict["catZtt13TeV_"+channel+"_1jet_inclusive"] + ("*(H_pt>50)*(H_pt<100)") + ("*(nbtag<1)")
			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_high"] = self.expressions_dict["catZtt13TeV_"+channel+"_1jet_inclusive"] + ("*(H_pt>100)") + ("*(nbtag<1)")

			self.expressions_dict["catZtt13TeV_"+channel+"_2jet_vbf"] = self.expressions_dict["catZtt13TeV_"+channel+"_2jet_inclusive"] + "*(mjj>500.0)*(jdeta>3.5)"

			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_exclusive"] = "(njetspt30>0)"
			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_low_exclusive"] = "(!(" + self.expressions_dict["catZtt13TeV_"+channel+"_2jet_vbf"] + "))*" + self.expressions_dict["catZtt13TeV_" + channel + "_1jet_exclusive"] + ("*(H_pt<50)") + ("*(nbtag<1)")
			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_medium_exclusive"] = "(!(" + self.expressions_dict["catZtt13TeV_"+channel+"_2jet_vbf"] + "))*" + self.expressions_dict["catZtt13TeV_" + channel + "_1jet_exclusive"] + ("*(H_pt>50)*(H_pt<100)") + ("*(nbtag<1)")
			self.expressions_dict["catZtt13TeV_"+channel+"_1jet_high_exclusive"] = "(!(" + self.expressions_dict["catZtt13TeV_"+channel+"_2jet_vbf"] + "))*" + self.expressions_dict["catZtt13TeV_" + channel + "_1jet_exclusive"] + ("*(H_pt>100)") + ("*(nbtag<1)")

			self.expressions_dict["catZtt13TeV_"+channel+"_1bjet"] = "(njets==1)*(nbtag>=1)"
			self.expressions_dict["catZtt13TeV_"+channel+"_2bjet"] = "(njets==2)*(nbtag>=2)"

		# Z->tautau polarisation categories
		for channel in ["mt", "et", "tt", "em"]:
			self.expressions_dict["catZttPol13TeV_"+channel+"_inclusive"] = "(1.0)"
			self.expressions_dict["testZttPol13TeV_"+channel+"_inclusive"] = "polarisationCombinedOmegaBarSvfit"

		for channel in ["em"]:
			for category in ["a1", "a1_1", "a1_2", "rho", "rho_1", "rho_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "-999.0"
			for category in ["oneprong", "oneprong_1", "oneprong_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(1.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "polarisationOmegaBarSvfit_2"

			for category in ["a1_a1", "a1_rho", "a1_oneprong", "rho_rho", "rho_oneprong"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "-999.0"
			for category in ["oneprong_oneprong"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "(1.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "polarisationCombinedOmegaBarSvfit"

		for channel in ["mt", "et"]:
			for category in ["a1", "a1_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(decayMode_2 == 10)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "polarisationOmegaBarSvfit_2"
			for category in ["rho", "rho_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(decayMode_2 == 1)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "polarisationOmegaBarSvfit_2"#"rhoNeutralChargedAsymmetry_2"
			for category in ["oneprong", "oneprong_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "((decayMode_2 != 10) * (decayMode_2 != 1))"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "polarisationOmegaBarSvfit_2"
			for category in ["a1_1", "rho_1"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "-999.0"
			for category in ["oneprong_1"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(1.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "polarisationOmegaBarSvfit_1"

			for category in ["a1_a1", "a1_rho", "rho_rho"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "-999.0"
			for category in ["a1_oneprong", "rho_oneprong", "oneprong_oneprong"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "catZttPol13TeV_"+channel+"_"+(category.split("_")[0])
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "polarisationCombinedOmegaBarSvfit"

		for channel in ["tt"]:
			self.expressions_dict["catZttPol13TeV_"+channel+"_a1"] = "((decayMode_1 == 10) || (decayMode_2 == 10))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_a1_1"] = "(decayMode_1 == 10)"
			self.expressions_dict["catZttPol13TeV_"+channel+"_a1_2"] = "(decayMode_2 == 10)"

			self.expressions_dict["testZttPol13TeV_"+channel+"_a1"] = "(((decayMode_1 == 10) * polarisationOmegaBarSvfit_1) + ((decayMode_1 != 10) * polarisationOmegaBarSvfit_2))"
			self.expressions_dict["testZttPol13TeV_"+channel+"_a1_1"] = "polarisationOmegaBarSvfit_1"
			self.expressions_dict["testZttPol13TeV_"+channel+"_a1_2"] = "polarisationOmegaBarSvfit_2"

			self.expressions_dict["catZttPol13TeV_"+channel+"_rho"] = "(((decayMode_1 != 10) * (decayMode_2 != 10)) * ((decayMode_1 == 1) || (decayMode_2 == 1)))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_rho_1"] = "((decayMode_1 != 10) * (decayMode_1 == 1) * (decayMode_2 != 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_rho_2"] = "((decayMode_2 != 10) * (decayMode_2 == 1) * (decayMode_1 != 1))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_rho"] = "(((decayMode_1 == 1) * polarisationOmegaBarSvfit_1) + ((decayMode_1 != 1) * polarisationOmegaBarSvfit_2))"
			self.expressions_dict["testZttPol13TeV_"+channel+"_rho_1"] = "polarisationOmegaBarSvfit_1"
			self.expressions_dict["testZttPol13TeV_"+channel+"_rho_2"] = "polarisationOmegaBarSvfit_2"

			self.expressions_dict["catZttPol13TeV_"+channel+"_oneprong"] = "((decayMode_1 != 10) * (decayMode_2 != 10) * (decayMode_1 != 1) * (decayMode_2 != 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_oneprong_1"] = "((decayMode_1 != 10) * (decayMode_1 != 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_oneprong_2"] = "((decayMode_2 != 10) * (decayMode_2 != 1))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_oneprong"] = "(((decayMode_1 != 10) *(decayMode_1 != 1) * polarisationOmegaBarSvfit_1) + ((decayMode_2 != 10) *(decayMode_2 != 1) * polarisationOmegaBarSvfit_2))"
			self.expressions_dict["testZttPol13TeV_"+channel+"_oneprong_1"] = "polarisationOmegaBarSvfit_1"
			self.expressions_dict["testZttPol13TeV_"+channel+"_oneprong_2"] = "polarisationOmegaBarSvfit_2"

			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_a1_a1"] = "((decayMode_1 == 10) * (decayMode_2 == 10))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_a1_rho"] = "(((decayMode_1 == 10) * (decayMode_2 == 1)) || ((decayMode_1 == 1) * (decayMode_2 == 10)))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_a1_oneprong"] = "(((decayMode_1 == 10) * (decayMode_2 != 10) * (decayMode_2 != 1)) || ((decayMode_1 != 10) * (decayMode_1 != 1) * (decayMode_2 == 10)))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_a1_a1"] = "polarisationCombinedOmegaBarSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_a1_rho"] = "polarisationCombinedOmegaBarSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_a1_oneprong"] = "polarisationCombinedOmegaBarSvfit"

			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_rho_rho"] = "((decayMode_1 == 1) * (decayMode_2 == 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_rho_oneprong"] = "(((decayMode_1 == 1) * (decayMode_2 != 10) * (decayMode_2 != 1)) || ((decayMode_1 != 10) * (decayMode_1 != 1) * (decayMode_2 == 1)))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_rho_rho"] = "polarisationCombinedOmegaBarSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_rho_oneprong"] = "polarisationCombinedOmegaBarSvfit"

			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_oneprong_oneprong"] = "((decayMode_1 != 1) * (decayMode_1 != 10) * (decayMode_2 != 10) * (decayMode_2 != 1))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_oneprong_oneprong"] = "polarisationCombinedOmegaBarSvfit"

		for channel in ["em", "mt", "et", "tt"]:
			self.expressions_dict["catZttPol13TeV_"+channel+"_index"] = " + ".join(["(catZttPol13TeV_"+channel+"_"+cat+" * "+str(index)+")" for index, cat in enumerate(["oneprong"] if channel == "em" else ["oneprong", "rho", "a1"])])

		# In the so-called "gen" channel, the categories are considered as tt,mt,et... for now,
		# it will be adapted later considering the decay products of tau's
		for channel in ["gen"]:
			self.expressions_dict["catZttPol13TeV_"+channel+"_tt"] = "genTauTauDecayMode==1"
			self.expressions_dict["catZttPol13TeV_"+channel+"_mt"] = "genTauTauDecayMode==2"
			self.expressions_dict["catZttPol13TeV_"+channel+"_et"] = "genTauTauDecayMode==3"

		# Z->ee(tau) electron tau fake rate categories
		for channel in ["et"]:
			for cat in ["vloose", "loose", "medium", "tight", "vtight"]:
				self.expressions_dict["catETauFakeRate13TeV_"+channel+ "_"+ cat + "_pass"] = "(1.0)"
				self.expressions_dict["catETauFakeRate13TeV_"+channel+ "_"+ cat + "_fail"] = "(1.0)"

		# H->tautau categories
		for channel in ["tt", "mt", "et", "em", "mm", "ee"]:
			pt_var = "pt_2" if channel in ["mt", "et", "em"] else "pt_1"
			pt_cut = "35.0"
			#CP-studies
			self.expressions_dict["catHtt13TeV_"+channel+"_CP_mt"] = "(genPhiStarCP>-10) * (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.55)"
			self.expressions_dict["catHtt13TeV_"+channel+"_CP_et"] = "(genPhiStarCP>-10) * (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.55)"
			self.expressions_dict["catHtt13TeV_"+channel+"_CP_em"] = "(genPhiStarCP>-10) * (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)"
			self.expressions_dict["catHtt13TeV_"+channel+"_CP_tt"] = "(genPhiStarCP>-10) * (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)"
			self.expressions_dict["catHtt13TeV_"+channel+"_CP_rho_yLhigh"] = "((decayMode_1 == 1) * (decayMode_2 == 1)) * (reco_negyTauL * reco_posyTauL > 0)"
			self.expressions_dict["catHtt13TeV_"+channel+"_CP_rho_yLlow"] = "((decayMode_1 == 1) * (decayMode_2 == 1)) * (reco_negyTauL * reco_posyTauL < 0)"
			self.expressions_dict["catHtt13TeV_"+channel+"_CP_rho_merged"] = "((decayMode_1 == 1) * (decayMode_2 == 1))"

			# Standard Model
			self.expressions_dict["catHtt13TeV_"+channel+"_inclusive"] = "(1.0)"
			self.expressions_dict["catHtt13TeV_"+channel+"_inclusivemt40"] = "(1.0)"
			self.expressions_dict["catHtt13TeV_"+channel+"_2jet_inclusive"] = "(njetspt30>1)"

			self.expressions_dict["catHtt13TeV_"+channel+"_2jet_vbf"] = self.expressions_dict["catHtt13TeV_"+channel+"_2jet_inclusive"]+"*(mjj>200.0)*(jdeta>2.0)"

			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_inclusive"] = ("(! ({vbf}))".format(
					vbf=self.expressions_dict["catHtt13TeV_"+channel+"_2jet_vbf"]
			))+"*(njetspt30>0)"
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_high"] = self.expressions_dict["catHtt13TeV_"+channel+"_1jet_inclusive"]+("*({pt_var}>{pt_cut})".format(pt_var=pt_var, pt_cut=pt_cut))
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_low"] = self.expressions_dict["catHtt13TeV_"+channel+"_1jet_inclusive"]+("*({pt_var}<={pt_cut})".format(pt_var=pt_var, pt_cut=pt_cut))
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet_inclusive"] = ("(! ({vbf}))*(! ({onejet}))".format(
					vbf=self.expressions_dict["catHtt13TeV_"+channel+"_2jet_vbf"],
					onejet=self.expressions_dict["catHtt13TeV_"+channel+"_1jet_inclusive"]
			))
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet_high"] = self.expressions_dict["catHtt13TeV_"+channel+"_0jet_inclusive"]+("*({pt_var}>{pt_cut})".format(pt_var=pt_var, pt_cut=pt_cut))
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet_low"] = self.expressions_dict["catHtt13TeV_"+channel+"_0jet_inclusive"]+("*({pt_var}<={pt_cut})".format(pt_var=pt_var, pt_cut=pt_cut))

			# Standard Model experimental
			btag_veto_string = "(nbtag == 0)"
			mjj_CP_string = "(mjj>300)"
			boosted_higgsCP_string = "(H_pt>200)"
			pZeta_CP_string = "(pZetaMissVis > -10.0)"
			
			et_antiiso_inclusive_string = "(iso_1>0.1)*(iso_1<0.5)"
			mt_antiiso_inclusive_string = "(iso_1>0.15)*(iso_1<0.5)"
			et_antiiso_near_string = "(iso_1>0.1)*(iso_1<0.17)"
			mt_antiiso_near_string = "(iso_1>0.15)*(iso_1<0.25)"
			et_antiiso_far_string = "(iso_1>0.17)*(iso_1<0.5)"
			mt_antiiso_far_string = "(iso_1>0.25)*(iso_1<0.5)"
						
			boosted_higgs_string = "(H_pt>100)"
			boosted_higgs_medium_string = "(H_pt>50)"
			boosted_higgs_low_string = "(H_pt>30)"
			vbf_medium_string = "(mjj>500&&jdeta>3.5)"
			vbf_loose_string = "(mjj>200&&jdeta>2)"
			jet2_string = "(njetspt30>1)"
			jet1_string = "(njetspt30>0)"
			jet0_string = "(njetspt30==0)"
			pt2_tight_string = "(pt_2>=45)"
			pt2_medium_string = "(pt_2>=35)"
			pt2_loose_string = "(pt_2>=25)"
			eta_hard_string = "jdeta>4.0"
			high_mt_string = "(nbtag==0)*(mt_1>80.0)"	
			mt_antiiso_string = "(iso_1>0.15)*(iso_1<0.50)"
			et_antiiso_string = "(iso_1>0.1)*(iso_1<0.50)"
			tt_antiiso_string = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
			# used in CERN signal extraction study
			self.expressions_dict["catHtt13TeV_"+channel+"_vbf"] = self.combine([vbf_medium_string, jet2_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_boosted"] = self.combine([jet1_string, self.invert(vbf_medium_string), boosted_higgs_string, pt2_tight_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_highpt2"] = self.combine([jet1_string, self.invert(vbf_medium_string), self.invert(boosted_higgs_string), pt2_tight_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_lowpt2"] = self.combine([jet1_string, self.invert(vbf_medium_string), self.invert(pt2_tight_string)])
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet_highpt2"] = self.combine([self.invert(jet1_string), pt2_tight_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet_lowpt2"] = self.combine([self.invert(jet1_string), self.invert(pt2_tight_string)])
			# motivated by s/sqrt(b) efficiency
			self.expressions_dict["catHtt13TeV_"+channel+"_vbf_tag"] = self.combine([jet2_string, boosted_higgs_medium_string, eta_hard_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_2jet_untagged"] = self.combine([jet2_string, self.invert(self.combine([boosted_higgs_medium_string, eta_hard_string]))])
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_boost_high"] = self.combine([jet1_string, boosted_higgs_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_boost_medium"] = self.combine([jet1_string, self.invert(boosted_higgs_string), boosted_higgs_low_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_1jet_boost_low"] = self.combine([jet1_string, self.invert(boosted_higgs_low_string)])
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet_nhighpt2"] = self.combine([self.invert(jet1_string), pt2_tight_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet_nlowpt2"] = self.combine([self.invert(jet1_string), self.invert(pt2_tight_string)])
			
			
		self.expressions_dict["catHtt13TeV_mm_Boosted2D"] = "((njetspt30==1)||((njetspt30>1&&mjj<=300)))"
		self.expressions_dict["catHtt13TeV_em_Boosted2D"] = "((njetspt30==1)||(njetspt30==2&&!(mjj>300&&pZetaMissVis>-10))||(njetspt30>2))"
		self.expressions_dict["catHtt13TeV_et_Boosted2D"] = "((njetspt30==1)||(njetspt30>1&&!(mjj>300&&H_pt>50)))"
		self.expressions_dict["catHtt13TeV_mt_Boosted2D"] = "((njetspt30==1)||(njetspt30>1&&!(mjj>300&&pt_2>40&&H_pt>50)))"
		self.expressions_dict["catHtt13TeV_tt_Boosted2D"] = "((njetspt30==1)||(njetspt30>1&&!(jdeta>2.5&&H_pt>100)))"
		
		# Standard Model categories
		# ZeroJet category	
		for channel in ["mm","em","et","mt","tt"]:
			self.expressions_dict["catHtt13TeV_"+channel+"_ZeroJet2D"] = self.combine([jet0_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_0jet"] = self.expressions_dict["catHtt13TeV_"+channel+"_ZeroJet2D"]
		
		self.expressions_dict["catHtt13TeV_tt_ZeroJet2D_QCDCR"] = self.combine([jet0_string, tt_antiiso_string]) 
		self.expressions_dict["catHtt13TeV_tt_antiiso_0jet_cr"] = self.expressions_dict["catHtt13TeV_tt_ZeroJet2D_QCDCR"]
		self.expressions_dict["catHtt13TeV_mt_ZeroJet2D_QCDCR"] = self.combine([jet0_string, mt_antiiso_string]) 
		self.expressions_dict["catHtt13TeV_mt_0jet_qcd_cr"] = self.expressions_dict["catHtt13TeV_mt_ZeroJet2D_QCDCR"]
		self.expressions_dict["catHtt13TeV_et_ZeroJet2D_QCDCR"] = self.combine([jet0_string, et_antiiso_string]) 
		self.expressions_dict["catHtt13TeV_et_0jet_qcd_cr"] = self.expressions_dict["catHtt13TeV_et_ZeroJet2D_QCDCR"]
		
		self.expressions_dict["catHtt13TeV_mt_ZeroJet2D_WJCR"] = self.combine([jet0_string, high_mt_string]) 
		self.expressions_dict["catHtt13TeV_mt_wjets_0jet_cr"] = self.expressions_dict["catHtt13TeV_mt_ZeroJet2D_WJCR"]
		self.expressions_dict["catHtt13TeV_et_ZeroJet2D_WJCR"] = self.combine([jet0_string, high_mt_string]) 
		self.expressions_dict["catHtt13TeV_et_wjets_0jet_cr"] = self.expressions_dict["catHtt13TeV_et_ZeroJet2D_WJCR"]		
			
		#Boosted (1jet) categories	
		self.expressions_dict["catHtt13TeV_mm_Boosted2D"] = "((njetspt30==1)||((njetspt30>1&&mjj<=300)))"
		self.expressions_dict["catHtt13TeV_em_Boosted2D"] = "((njetspt30==1)||(njetspt30>1&&!(mjj>300&&pt_2>40&&H_pt>50)))"
		self.expressions_dict["catHtt13TeV_et_Boosted2D"] = "((njetspt30==1)||(njetspt30>1&&!(mjj>300&&H_pt>50)))"
		self.expressions_dict["catHtt13TeV_mt_Boosted2D"] = "((njetspt30==1)||(njetspt30==2&&!(mjj>300&&pZetaMissVis>-10))||(njetspt30>2))"
		self.expressions_dict["catHtt13TeV_tt_Boosted2D"] = "((njetspt30==1)||(njetspt30>1&&!(jdeta>2.5&&H_pt>100)))"
		
		self.expressions_dict["catHtt13TeV_mm_boosted"] = self.expressions_dict["catHtt13TeV_mm_Boosted2D"]
		self.expressions_dict["catHtt13TeV_em_boosted"] = self.expressions_dict["catHtt13TeV_em_Boosted2D"]
		self.expressions_dict["catHtt13TeV_et_boosted"] = self.expressions_dict["catHtt13TeV_et_Boosted2D"]
		self.expressions_dict["catHtt13TeV_mt_boosted"] = self.expressions_dict["catHtt13TeV_mt_Boosted2D"]
		self.expressions_dict["catHtt13TeV_tt_boosted"] = self.expressions_dict["catHtt13TeV_tt_Boosted2D"]		
				
		self.expressions_dict["catHtt13TeV_tt_Boosted2D_QCDCR"] = self.combine([jet1_string, tt_antiiso_string, "*((njetspt30==1)||(njetspt30>1&&!(jdeta>2.5&&H_pt>100)))"]) 
		self.expressions_dict["catHtt13TeV_tt_antiiso_boosted_cr"] = self.expressions_dict["catHtt13TeV_tt_Boosted2D_QCDCR"]
		self.expressions_dict["catHtt13TeV_mt_Boosted2D_QCDCR"] = "(iso_1>0.15)*(iso_1<0.30)*((njetspt30==1)||(njetspt30>1&&!(mjj>300&&H_pt>50)))" 
		self.expressions_dict["catHtt13TeV_mt_boosted_qcd_cr"] = self.expressions_dict["catHtt13TeV_mt_Boosted2D_QCDCR"]
		self.expressions_dict["catHtt13TeV_et_Boosted2D_QCDCR"] = "(iso_1>0.10)*(iso_1<0.30)*((njetspt30==1)||(njetspt30>1&&!(mjj>300&&H_pt>50)))" 
		self.expressions_dict["catHtt13TeV_et_boosted_qcd_cr"] = self.expressions_dict["catHtt13TeV_et_Boosted2D_QCDCR"]
		
		self.expressions_dict["catHtt13TeV_mt_Boosted2D_WJCR"] = "(nbtag==0)*(mt_1>80.0)*((njetspt30==1)||(njetspt30>1&&!(mjj>300&&H_pt>50)))" 
		self.expressions_dict["catHtt13TeV_mt_wjets_boosted_cr"] = self.expressions_dict["catHtt13TeV_mt_Boosted2D_WJCR"]
		self.expressions_dict["catHtt13TeV_et_Boosted2D_WJCR"] = "(nbtag==0)*(mt_1>80.0)*((njetspt30==1)||(njetspt30>1&&!(mjj>300&&H_pt>50)))"
		self.expressions_dict["catHtt13TeV_et_wjets_boosted_cr"] = self.expressions_dict["catHtt13TeV_et_Boosted2D_WJCR"]	
		
		#Vbf categories		
		self.expressions_dict["catHtt13TeV_mm_Vbf2D"] = "(njetspt30>1)*(mjj>300)"
		self.expressions_dict["catHtt13TeV_em_Vbf2D"] = "(pt_2>40)*(njetspt30>1)*(mjj>300)*(H_pt>50)"
		self.expressions_dict["catHtt13TeV_et_Vbf2D"] = "(njetspt30>1)*(mjj>300)*(H_pt>50)"
		self.expressions_dict["catHtt13TeV_mt_Vbf2D"] = "(pZetaMissVis>-10)*(njetspt30==2)*(mjj>300)"
		self.expressions_dict["catHtt13TeV_tt_Vbf2D"] = "(njetspt30>1)*(jdeta>2.5)*(H_pt>100)"
		self.expressions_dict["catHtt13TeV_mm_vbf"] = self.expressions_dict["catHtt13TeV_mm_Vbf2D"]
		self.expressions_dict["catHtt13TeV_em_vbf"] = self.expressions_dict["catHtt13TeV_em_Vbf2D"]
		self.expressions_dict["catHtt13TeV_et_vbf"] = self.expressions_dict["catHtt13TeV_et_Vbf2D"]
		self.expressions_dict["catHtt13TeV_mt_vbf"] = self.expressions_dict["catHtt13TeV_mt_Vbf2D"]
		self.expressions_dict["catHtt13TeV_tt_vbf"] = self.expressions_dict["catHtt13TeV_tt_Vbf2D"]
		
		self.expressions_dict["catHtt13TeV_tt_Vbf2D_QCDCR"] = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))*(njetspt30>1)*(jdeta>2.5)*(H_pt>100)"		
		self.expressions_dict["catHtt13TeV_tt_antiiso_vbf_cr"] = self.expressions_dict["catHtt13TeV_tt_Vbf2D_QCDCR"]
		
		# ttbar control region
		self.expressions_dict["catHtt13TeV_ttbar_TTbarCR"] = "(pZetaMissVis < -35.0)*(m_vis>90.0)*(njetspt30>0)"
		self.expressions_dict["catHtt13TeV_ttbar_ttbar_cr"] = self.expressions_dict["catHtt13TeV_ttbar_TTbarCR"]
		
		# CP initial state category
		for channel in ["em", "et", "mt", "tt"]:
			self.expressions_dict["catHtt13TeV_"+channel+"_dijet2D_boosted"] = self.combine([boosted_higgsCP_string, mjj_CP_string, jet2_string, "(1.0)" if channel=="tt" else btag_veto_string, "(1.0)" if channel != "em" else pZeta_CP_string ]) 
			self.expressions_dict["catHtt13TeV_"+channel+"_dijet2D_lowboost"] = self.combine([self.invert(boosted_higgsCP_string), mjj_CP_string, jet2_string, "(1.0)" if channel=="tt" else btag_veto_string, "(1.0)" if channel != "em" else pZeta_CP_string ])
			self.expressions_dict["catHtt13TeV_"+channel+"_ZeroJetCP"] = self.combine([jet0_string, "(1.0)" if channel=="tt" else btag_veto_string])
			self.expressions_dict["catHtt13TeV_"+channel+"_BoostedCP"] = self.combine([self.invert(self.expressions_dict["catHtt13TeV_"+channel+"_ZeroJetCP"]), self.invert(self.expressions_dict["catHtt13TeV_"+channel+"_dijet2D_boosted"]), self.invert(self.expressions_dict["catHtt13TeV_"+channel+"_dijet2D_lowboost"]), "(1.0)" if channel=="tt" else btag_veto_string]) 
					
		# Categories for background estimation in QCD with inverted lepton isolation.
		# inclusive categories
		self.expressions_dict["catHtt13TeV_et_dijet2D_antiiso"] = self.combine([jet2_string, "(1.0)" if channel != "em" else pZeta_CP_string, et_antiiso_inclusive_string]) 
		# self.expressions_dict["catHtt13TeV_et_dijet2D_boosted_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_et_dijet2D_boosted"], et_antiiso_inclusive_string])
		self.expressions_dict["catHtt13TeV_et_dijet2D_lowboost_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_et_dijet2D_lowboost"], et_antiiso_inclusive_string]) 
		self.expressions_dict["catHtt13TeV_et_ZeroJet2D_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_et_ZeroJetCP"], et_antiiso_inclusive_string]) 
		self.expressions_dict["catHtt13TeV_et_Boosted2D_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_et_BoostedCP"], et_antiiso_inclusive_string]) 

		self.expressions_dict["catHtt13TeV_mt_dijet2D_antiiso"] = self.combine([jet2_string, "(1.0)" if channel != "em" else pZeta_CP_string, mt_antiiso_inclusive_string]) 
		# self.expressions_dict["catHtt13TeV_mt_dijet2D_boosted_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_mt_dijet2D_boosted"], mt_antiiso_inclusive_string])
		self.expressions_dict["catHtt13TeV_mt_dijet2D_lowboost_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_mt_dijet2D_lowboost"], mt_antiiso_inclusive_string]) 
		self.expressions_dict["catHtt13TeV_mt_ZeroJet2D_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_mt_ZeroJetCP"], mt_antiiso_inclusive_string]) 
		self.expressions_dict["catHtt13TeV_mt_Boosted2D_antiiso"] = self.combine([self.expressions_dict["catHtt13TeV_mt_BoostedCP"], mt_antiiso_inclusive_string]) 
			
		# near anti-isolated sideband 
		self.expressions_dict["catHtt13TeV_et_dijet2D_antiiso_near"] = self.combine([jet2_string, "(1.0)" if channel != "em" else pZeta_CP_string, et_antiiso_near_string]) 
		# self.expressions_dict["catHtt13TeV_et_dijet2D_boosted_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_et_dijet2D_boosted"], et_antiiso_near_string])
		self.expressions_dict["catHtt13TeV_et_dijet2D_lowboost_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_et_dijet2D_lowboost"], et_antiiso_near_string]) 
		self.expressions_dict["catHtt13TeV_et_ZeroJet2D_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_et_ZeroJetCP"], et_antiiso_near_string]) 
		self.expressions_dict["catHtt13TeV_et_Boosted2D_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_et_BoostedCP"], et_antiiso_near_string]) 

		self.expressions_dict["catHtt13TeV_mt_dijet2D_antiiso_near"] = self.combine([jet2_string, "(1.0)" if channel != "em" else pZeta_CP_string, mt_antiiso_near_string]) 
		# self.expressions_dict["catHtt13TeV_mt_dijet2D_boosted_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_mt_dijet2D_boosted"], mt_antiiso_near_string])
		self.expressions_dict["catHtt13TeV_mt_dijet2D_lowboost_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_mt_dijet2D_lowboost"], mt_antiiso_near_string]) 
		self.expressions_dict["catHtt13TeV_mt_ZeroJet2D_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_mt_ZeroJetCP"], mt_antiiso_near_string]) 
		self.expressions_dict["catHtt13TeV_mt_Boosted2D_antiiso_near"] = self.combine([self.expressions_dict["catHtt13TeV_mt_BoostedCP"], mt_antiiso_near_string]) 

		# far anti-isolated sideband 
		self.expressions_dict["catHtt13TeV_et_dijet2D_antiiso_far"] = self.combine([jet2_string, "(1.0)" if channel != "em" else pZeta_CP_string, et_antiiso_far_string]) 
		# self.expressions_dict["catHtt13TeV_et_dijet2D_boosted_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_et_dijet2D_boosted"], et_antiiso_far_string])
		self.expressions_dict["catHtt13TeV_et_dijet2D_lowboost_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_et_dijet2D_lowboost"], et_antiiso_far_string]) 
		self.expressions_dict["catHtt13TeV_et_ZeroJet2D_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_et_ZeroJetCP"], et_antiiso_far_string]) 
		self.expressions_dict["catHtt13TeV_et_Boosted2D_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_et_BoostedCP"], et_antiiso_far_string]) 

		self.expressions_dict["catHtt13TeV_mt_dijet2D_antiiso_far"] = self.combine([jet2_string, "(1.0)" if channel != "em" else pZeta_CP_string, mt_antiiso_far_string]) 
		# self.expressions_dict["catHtt13TeV_mt_dijet2D_boosted_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_mt_dijet2D_boosted"], mt_antiiso_far_string])
		self.expressions_dict["catHtt13TeV_mt_dijet2D_lowboost_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_mt_dijet2D_lowboost"], mt_antiiso_far_string]) 
		self.expressions_dict["catHtt13TeV_mt_ZeroJet2D_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_mt_ZeroJetCP"], mt_antiiso_far_string]) 
		self.expressions_dict["catHtt13TeV_mt_Boosted2D_antiiso_far"] = self.combine([self.expressions_dict["catHtt13TeV_mt_BoostedCP"], mt_antiiso_far_string]) 


					
		# Anti-isolation qcd control region in dijet categories
		self.expressions_dict["catHtt13TeV_tt_dijet2D_boosted_qcd_cr"] = self.combine([tt_antiiso_string, boosted_higgsCP_string, mjj_CP_string, jet2_string, btag_veto_string])
		self.expressions_dict["catHtt13TeV_tt_dijet2D_lowboost_qcd_cr"] = self.combine([tt_antiiso_string, self.invert(boosted_higgsCP_string), mjj_CP_string, jet2_string, btag_veto_string])
				
		# CP initial state control regions in Z->mm
		self.expressions_dict["catHtt13TeV_mm_dijet2D_boosted"] = self.combine([boosted_higgsCP_string, mjj_CP_string, jet2_string])
		self.expressions_dict["catHtt13TeV_mm_dijet2D_lowboost"] = self.combine([self.invert(boosted_higgsCP_string), mjj_CP_string, jet2_string])


		# MSSSM
		for channel in ["et","mt","tt","em","mm"]:
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_inclusive"] = "(1.0)"
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_inclusivemt40"] = "(1.0)"
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_nobtag"] = "(nbtag==0)"
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_btag"] = "(nbtag>=1)"
		for channel in ["et","mt"]:
			for cat in ["_nobtag","_btag","_inclusive"]:
				self.expressions_dict["catHttMSSM13TeV_"+channel+cat+"_tight"] =  self.expressions_dict["catHttMSSM13TeV_"+channel+cat]
				self.expressions_dict["catHttMSSM13TeV_"+channel+cat+"_loosemt"] =  self.expressions_dict["catHttMSSM13TeV_"+channel+cat]
				self.expressions_dict["catHttMSSM13TeV_"+channel+cat+"_looseiso"] =  self.expressions_dict["catHttMSSM13TeV_"+channel+cat]
		for cat in ["_nobtag","_btag","_inclusive"]:
			self.expressions_dict["catHttMSSM13TeV_em"+cat+"_lowPzeta"] = self.expressions_dict["catHttMSSM13TeV_em"+cat]+"*(pZetaMissVis > -50)*(pZetaMissVis < -10)"
			self.expressions_dict["catHttMSSM13TeV_em"+cat+"_mediumPzeta"] = self.expressions_dict["catHttMSSM13TeV_em"+cat]+"*(pZetaMissVis > -10)*(pZetaMissVis < 30)"
			self.expressions_dict["catHttMSSM13TeV_em"+cat+"_highPzeta"] = self.expressions_dict["catHttMSSM13TeV_em"+cat]+"*(pZetaMissVis > 30)"

		for channel in ["et","mt","tt"]:
			pt_var = "pt_2" if channel in ["mt", "et"] else "pt_1"
			pt_cut_nobtag_high = "60.0" if channel in ["mt", "et"] else "80.0"
			pt_cut_nobtag_medium = "45.0" if channel in ["mt", "et"] else "60.0"
			pt_cut_nobtag_low = "30.0" if channel in ["mt", "et"] else "45.0"
			pt_cut_btag_high = "45.0" if channel in ["mt", "et"] else "60.0"
			pt_cut_btag_low = "30.0" if channel in ["mt", "et"] else "45.0"
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_nobtag_high"] = self.expressions_dict["catHttMSSM13TeV_"+channel+"_nobtag"]+"*({pt_var}>{pt_cut})".format(pt_var=pt_var, pt_cut=pt_cut_nobtag_high)
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_nobtag_medium"] = self.expressions_dict["catHttMSSM13TeV_"+channel+"_nobtag"]+"*({pt_var}<={pt_cut_1})*({pt_var}>{pt_cut_2})".format(pt_var=pt_var, pt_cut_1=pt_cut_nobtag_high, pt_cut_2=pt_cut_nobtag_medium)
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_nobtag_low"] = self.expressions_dict["catHttMSSM13TeV_"+channel+"_nobtag"]+"*({pt_var}<={pt_cut_1})*({pt_var}>{pt_cut_2})".format(pt_var=pt_var, pt_cut_1=pt_cut_nobtag_medium, pt_cut_2=pt_cut_nobtag_low)
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_btag_high"] = self.expressions_dict["catHttMSSM13TeV_"+channel+"_btag"]+"*({pt_var}>{pt_cut})".format(pt_var=pt_var, pt_cut=pt_cut_btag_high)
			self.expressions_dict["catHttMSSM13TeV_"+channel+"_btag_low"] = self.expressions_dict["catHttMSSM13TeV_"+channel+"_btag"]+"*({pt_var}<={pt_cut_1})*({pt_var}>{pt_cut_2})".format(pt_var=pt_var, pt_cut_1=pt_cut_btag_high, pt_cut_2=pt_cut_btag_low)


		# LFV categories
		self.expressions_dict["catHttMSSM13TeV_em_LFVZeroJet"] = self.combine([jet0_string,"((((lep1LV.Px() + lep2LV.Px())**2 + (lep1LV.Py() + lep2LV.Py())**2)**0.5)<20)"])
		self.expressions_dict["catHttMSSM13TeV_et_LFVZeroJet"] = self.combine([jet0_string,"((((lep1LV.Px() + lep2LV.Px())**2 + (lep1LV.Py() + lep2LV.Py())**2)**0.5)<30)"])
		self.expressions_dict["catHttMSSM13TeV_mt_LFVZeroJet"] = self.combine([jet0_string,"((((lep1LV.Px() + lep2LV.Px())**2 + (lep1LV.Py() + lep2LV.Py())**2)**0.5)<50)"])
		self.expressions_dict["catHttMSSM13TeV_em_LFVJet"] = "(njetspt30>=1)*(nbtag == 0)*((((lep1LV.Px() + lep2LV.Px())**2 + (lep1LV.Py() + lep2LV.Py())**2)**0.5)<20)"
		self.expressions_dict["catHttMSSM13TeV_et_LFVJet"] = "(njetspt30>=1)*(nbtag == 0)*((((lep1LV.Px() + lep2LV.Px())**2 + (lep1LV.Py() + lep2LV.Py())**2)**0.5)<30)"
		self.expressions_dict["catHttMSSM13TeV_mt_LFVJet"] = "(njetspt30>=1)*(nbtag == 0)*((((lep1LV.Px() + lep2LV.Px())**2 + (lep1LV.Py() + lep2LV.Py())**2)**0.5)<50)"
		
		
		self.expressions_dict["cat_OneProng"] = "(decayMode_2 == 0)"
		self.expressions_dict["catOneProng"] = self.expressions_dict["cat_OneProng"]
		for channel in ["mt", "et"]:
			self.expressions_dict["catOneProng_"+channel] = self.expressions_dict["catOneProng"]

		self.expressions_dict["cat_OneProngPiZeros"] = "(decayMode_2 >= 1)*(decayMode_2 <= 2)"
		self.expressions_dict["catOneProngPiZeros"] = self.expressions_dict["cat_OneProngPiZeros"]
		for channel in ["mt", "et"]:
			self.expressions_dict["catOneProngPiZeros_"+channel] = self.expressions_dict["catOneProngPiZeros"]

		self.expressions_dict["cat_ThreeProng"] = "(decayMode_2 == 10)"
		self.expressions_dict["catThreeProng"] =self.expressions_dict["cat_ThreeProng"]
		for channel in ["mt", "et"]:
			self.expressions_dict["catThreeProng_"+channel] = self.expressions_dict["catThreeProng"]

		self.expressions_dict["cat_AllDMs"] = "(decayMode_2 >= 0)*(decayMode_2 <= 10)"
		self.expressions_dict["catAllDMs"] =self.expressions_dict["cat_AllDMs"]
		for channel in ["mt", "et"]:
			self.expressions_dict["catAllDMs_"+channel] = self.expressions_dict["catAllDMs"]

		self.expressions_dict["cat_AllDMsNotOneProng"] = "(decayMode_2 >= 1)*(decayMode_2 <= 10)"
		self.expressions_dict["catAllDMsNotOneProng"] =self.expressions_dict["cat_AllDMsNotOneProng"]
		for channel in ["mt", "et"]:
			self.expressions_dict["catAllDMsNotOneProng_"+channel] = self.expressions_dict["catAllDMsNotOneProng"]

		#==========================CategoriesDictUpdates=========================================================
		import Artus.Utility.jsonTools as jsonTools
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
		categoriesUpdate = Categories.CategoriesDict().getExpressionsDict()
		self.expressions_dict.update(categoriesUpdate)

		replacements = {
			"0jet" : "zerojet",
			"1jet" : "onejet",
			"2jet" : "twojet",
		}
		for short_expression, long_expression in self.expressions_dict.items():
			if any([replacement in short_expression for replacement in replacements.keys()]):
				new_short_expression = short_expression
				for replacement in replacements.iteritems():
					new_short_expression = new_short_expression.replace(*replacement)
				self.expressions_dict[new_short_expression] = long_expression
	def combine(self, strings_to_combine):
		return "(" + "*".join(strings_to_combine) + ")"				
	@staticmethod
	def static_get_expression(expression):
		exp_dict = ExpressionsDict()
		return exp_dict.expressions_dict.get(expression)

	
