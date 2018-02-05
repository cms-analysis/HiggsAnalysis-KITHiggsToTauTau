
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.expressions as expressions
import os
from string import strip


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
			self.expressions_dict["testZttPol13TeV_"+channel+"_inclusive"] = "tauPolarisationDiscriminatorSvfit"

		for channel in ["em"]:
			for category in ["a1", "a1_1", "a1_2", "rho", "rho_1", "rho_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "tauPolarisationDiscriminatorSvfit"
			for category in ["oneprong", "oneprong_1", "oneprong_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(1.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "tauPolarisationDiscriminatorSvfit"
			
			for category in ["a1_a1", "a1_rho", "a1_oneprong", "rho_rho", "rho_oneprong"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "tauPolarisationDiscriminatorSvfit"
			for category in ["oneprong_oneprong"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "(1.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "tauPolarisationDiscriminatorSvfit"

		for channel in ["mt", "et"]:
			for category in ["a1", "a1_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(decayMode_2 == 10)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "tauPolarisationDiscriminatorSvfit"
			for category in ["rho", "rho_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(decayMode_2 == 1)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "polarisationOmegaSvfit_1"#"rhoNeutralChargedAsymmetry_2"
			for category in ["oneprong", "oneprong_2"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "((decayMode_2 != 10) * (decayMode_2 != 1))"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "tauPolarisationDiscriminatorSvfit"
			for category in ["a1_1", "rho_1"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "tauPolarisationDiscriminatorSvfit"
			for category in ["oneprong_1"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_"+category] = "(1.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_"+category] = "tauPolarisationDiscriminatorSvfit"
			
			for category in ["a1_a1", "a1_rho", "rho_rho"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "(0.0)"
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "tauPolarisationDiscriminatorSvfit"
			for category in ["a1_oneprong", "rho_oneprong", "oneprong_oneprong"]:
				self.expressions_dict["catZttPol13TeV_"+channel+"_combined_"+category] = "catZttPol13TeV_"+channel+"_"+(category.split("_")[0])
				self.expressions_dict["testZttPol13TeV_"+channel+"_combined_"+category] = "testZttPol13TeV_"+channel+"_"+(category.split("_")[0])

		for channel in ["tt"]:
			self.expressions_dict["catZttPol13TeV_"+channel+"_a1"] = "((decayMode_1 == 10) || (decayMode_2 == 10))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_a1_1"] = "(decayMode_1 == 10)"
			self.expressions_dict["catZttPol13TeV_"+channel+"_a1_2"] = "(decayMode_2 == 10)"
			self.expressions_dict["testZttPol13TeV_"+channel+"_a1"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_a1_1"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_a1_2"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["catZttPol13TeV_"+channel+"_rho"] = "(((decayMode_1 != 10) * (decayMode_2 != 10)) * ((decayMode_1 == 1) || (decayMode_2 == 1)))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_rho_1"] = "((decayMode_1 != 10) * (decayMode_1 == 1) * (decayMode_2 != 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_rho_2"] = "((decayMode_2 != 10) * (decayMode_2 == 1) * (decayMode_1 != 1))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_rho"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_rho_1"] = "polarisationOmegaSvfit_1" #"rhoNeutralChargedAsymmetry_1"
			self.expressions_dict["testZttPol13TeV_"+channel+"_rho_2"] = "polarisationOmegaSvfit_2" #"rhoNeutralChargedAsymmetry_2"

			self.expressions_dict["catZttPol13TeV_"+channel+"_oneprong"] = "((decayMode_1 != 10) * (decayMode_2 != 10) * (decayMode_1 != 1) * (decayMode_2 != 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_oneprong_1"] = "((decayMode_1 != 10) * (decayMode_1 != 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_oneprong_2"] = "((decayMode_2 != 10) * (decayMode_2 != 1))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_oneprong"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_oneprong_1"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_oneprong_2"] = "tauPolarisationDiscriminatorSvfit"

			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_a1_a1"] = "((decayMode_1 == 10) * (decayMode_2 == 10))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_a1_rho"] = "(((decayMode_1 == 10) * (decayMode_2 == 1)) || ((decayMode_1 == 1) * (decayMode_2 == 10)))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_a1_oneprong"] = "(((decayMode_1 == 10) * (decayMode_2 != 10) * (decayMode_2 != 1)) || ((decayMode_1 != 10) * (decayMode_1 != 1) * (decayMode_2 == 10)))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_a1_a1"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_a1_rho"] = "tauPolarisationDiscriminatorSvfit"
			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_a1_oneprong"] = "tauPolarisationDiscriminatorSvfit"

			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_rho_rho"] = "((decayMode_1 == 1) * (decayMode_2 == 1))"
			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_rho_oneprong"] = "(((decayMode_1 == 1) * (decayMode_2 != 10) * (decayMode_2 != 1)) || ((decayMode_1 != 10) * (decayMode_1 != 1) * (decayMode_2 == 1)))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_rho_rho"] = "(rhoNeutralChargedAsymmetry_1+rhoNeutralChargedAsymmetry_1)/(1+rhoNeutralChargedAsymmetry_1*rhoNeutralChargedAsymmetry_1)"
			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_rho_oneprong"] = "tauPolarisationDiscriminatorSvfit"

			self.expressions_dict["catZttPol13TeV_"+channel+"_combined_oneprong_oneprong"] = "((decayMode_1 != 1) * (decayMode_1 != 10) * (decayMode_2 != 10) * (decayMode_2 != 1))"

			self.expressions_dict["testZttPol13TeV_"+channel+"_combined_oneprong_oneprong"] = "m_vis"

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
			boosted_higgs_string = "(H_pt>100)"
			boosted_higgs_medium_string = "(H_pt>50)"
			boosted_higgs_low_string = "(H_pt>30)"
			vbf_medium_string = "(mjj>500&&jdeta>3.5)"
			vbf_loose_string = "(mjj>200&&jdeta>2)"
			jet2_string = "(njetspt30>1)"
			jet1_string = "(njetspt30>0)"
			pt2_tight_string = "(pt_2>=45)"
			pt2_medium_string = "(pt_2>=35)"
			pt2_loose_string = "(pt_2>=25)"
			eta_hard_string = "jdeta>4.0"
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

		# MVA Htt categories
		#self.expressions_dict["mt_vbf_pre"] = "((0.3<=ttj_1)*(0.45<=ztt_1))"
		#self.expressions_dict["mt_vbf_sig"] = "{pre}*(0.8<=vbf_1)".format(pre=self.expressions_dict["mt_vbf_pre"])
		#self.expressions_dict["mt_vbf_like"] = "{pre}*(-0.5<=vbf_1&&vbf_1<0.8)".format(pre=self.expressions_dict["mt_vbf_pre"])
		#self.expressions_dict["mt_vbf_bkg"] = "{pre}*(vbf_1<-0.5)".format(pre=self.expressions_dict["mt_vbf_pre"])
		#self.expressions_dict["mt_vbf_rest"] = "!{pre}".format(pre=self.expressions_dict["mt_vbf_pre"])
		#self.expressions_dict["mt_2jets_all"] = "(njetspt30>1)"
		#self.expressions_dict["mt_1jets_all"] = "(njetspt30==1)"
		#self.expressions_dict["mt_0jets_all"] = "(njetspt30==0)"
		#self.expressions_dict["mt_2jets_vbfbdt"] = "(0.8<=vbf_1)"
		#self.expressions_dict["mt_2jet_vbf_bdt"] = "({pre}*(0.8<=vbf_1))".format(pre=self.expressions_dict["mt_vbf_pre"])
		#self.expressions_dict["mt_1jet_inclusive_bdt"] = ("((! {vbf})".format(
				#vbf=self.expressions_dict["mt_2jet_vbf_bdt"]
		#))+"*(njetspt30>0))"
		#self.expressions_dict["mt_1jet_sig"] = self.expressions_dict["mt_1jet_inclusive_bdt"]+"*((0.4<=ttj_1)*(0.4<=ztt_1))"
		#self.expressions_dict["mt_1jet_bkg"] = self.expressions_dict["mt_1jet_inclusive_bdt"]+"*(!((0.4<=ttj_1)*(0.4<=ztt_1)))"
		#self.expressions_dict["mt_0jet_inclusive_bdt"] = ("(!{vbf})*(!{onejet})".format(
				#vbf=self.expressions_dict["mt_2jet_vbf_bdt"],
				#onejet=self.expressions_dict["mt_1jet_inclusive_bdt"]
		#))
		#self.expressions_dict["mt_0jet_sig"] = self.expressions_dict["mt_0jet_inclusive_bdt"]+"*((-0.6<=ttj_1)*(0.2<=ztt_1))"
		#self.expressions_dict["mt_0jet_bkg"] = self.expressions_dict["mt_0jet_inclusive_bdt"]+"*(!((-0.6<=ttj_1)*(0.2<=ztt_1)))"

		#for channel in ["tt", "mt", "et", "em"]:
			#for classic in ["0jet_high", "0jet_low", "1jet_high", "1jet_low", "2jet_vbf"]:
				#self.expressions_dict["{channel}_{classic}".format(channel=channel, classic=classic)] = self.expressions_dict["catHtt13TeV_{channel}_{classic}".format(channel=channel, classic=classic)]
		##========================================Copy here!========================================
			#expressions_path = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/%s_expressions.cfg"%channel)
			#if not os.path.exists(expressions_path):
				#continue
			#self.expressions_dict["%s_inclusive"%(channel)] = "(1.0)"
			#with open(expressions_path, "r") as exps:
				#regular_name = ""
				#for line in exps:
					##log.info(line)
					#vbf, name, values = map(strip, line.split(" : "))
					#values = map(float, values.split(" "))
					#values.pop(0)
					#values.pop(-1)
					#if vbf == "regular_name":
						#self.expressions_dict["%s_%s_signal"%(channel,name)] = "(%f <= %s)"%(values[1], name)
						#self.expressions_dict["%s_%s_mixed"%(channel,name)] = "(%f <= %s && %s < %f)"%(values[0], name, name, values[1])
						#self.expressions_dict["%s_%s_bkg"%(channel,name)] = "(%s < %f)"%(name, values[0])
						#regular_name= name
						#continue
					#elif vbf == "vbf_tagger":
						#if regular_name == "":
							#log.fatal("Please check if cuts in file %s are in correct order"%expressions_path)
							#sys.exit()
						#self.expressions_dict["{channel}_{vbf_tagger}_{mva_name}_tagged_signal".format(
							#channel=channel, vbf_tagger=name, mva_name=regular_name)]=self.expressions_dict["{channel}_{reg_name}_signal".format(channel=channel, reg_name=regular_name)]+"*({upper} <= {vbf_tagger})".format(upper=values[0], vbf_tagger=name)
						#self.expressions_dict["{channel}_{vbf_tagger}_{mva_name}_not_tagged_signal".format(
							#channel=channel, vbf_tagger=name, mva_name=regular_name)]=self.expressions_dict["{channel}_{reg_name}_signal".format(channel=channel, reg_name=regular_name)]+"*({lower} > {vbf_tagger})".format(lower=values[0], vbf_tagger=name)
			#expressions_path = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/%s_shift_expressions.cfg"%channel)
			#if not os.path.exists(expressions_path):
				#continue
			#shifts_dict = jsonTools.JsonDict(expressions_path)
			#self.expressions_dict.update(shifts_dict)
		#========================================Copy here!=======================================
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
	@staticmethod
	def static_get_expression(expression):
		exp_dict = ExpressionsDict()
		return exp_dict.expressions_dict.get(expression)
