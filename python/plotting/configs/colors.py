
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.colors as colors


class ColorsDict(colors.ColorsDict):
	def __init__(self, color_scheme="default", additional_colors=None):
		super(ColorsDict, self).__init__(color_scheme=color_scheme, additional_colors=additional_colors)

		self.colors_dict["kit_gruen_1"] = "#00A88F"
		self.colors_dict["kit_gruen_2"] = "#4CC1A5"
		self.colors_dict["kit_gruen_3"] = "#7FD2B8"
		self.colors_dict["kit_gruen_4"] = "#B2E4D1"
		self.colors_dict["kit_gruen_5"] = "#D9F1E6"

		self.colors_dict["kit_blau_1"] = "#4372C1"
		self.colors_dict["kit_blau_2"] = "#7691D2"
		self.colors_dict["kit_blau_3"] = "#9AABDD"
		self.colors_dict["kit_blau_4"] = "#C0C9EA"
		self.colors_dict["kit_blau_5"] = "#E0E3F4"

		self.colors_dict["kit_maigruen_1"] = "#66C42F"
		self.colors_dict["kit_maigruen_2"] = "#93D561"
		self.colors_dict["kit_maigruen_3"] = "#B2E088"
		self.colors_dict["kit_maigruen_4"] = "#D1ECB4"
		self.colors_dict["kit_maigruen_5"] = "#E8F5D8"

		self.colors_dict["kit_gelb_1"] = "#FEE701"
		self.colors_dict["kit_gelb_2"] = "#FEED4B"
		self.colors_dict["kit_gelb_3"] = "#FEF27D"
		self.colors_dict["kit_gelb_4"] = "#FEF7B0"
		self.colors_dict["kit_gelb_5"] = "#FEFBD8"

		self.colors_dict["kit_orange_1"] = "#F69110"
		self.colors_dict["kit_orange_2"] = "#F9AE49"
		self.colors_dict["kit_orange_3"] = "#FAC376"
		self.colors_dict["kit_orange_4"] = "#FCD9A8"
		self.colors_dict["kit_orange_5"] = "#FDECD2"

		self.colors_dict["kit_braun_1"] = "#A97E23"
		self.colors_dict["kit_braun_2"] = "#C09D52"
		self.colors_dict["kit_braun_3"] = "#D0B47A"
		self.colors_dict["kit_braun_4"] = "#E2D0A8"
		self.colors_dict["kit_braun_5"] = "#F0E6D2"

		self.colors_dict["kit_rot_1"] = "#BF2229"
		self.colors_dict["kit_rot_2"] = "#CD574A"
		self.colors_dict["kit_rot_3"] = "#DA806E"
		self.colors_dict["kit_rot_4"] = "#E7AE9D"
		self.colors_dict["kit_rot_5"] = "#F2D5CB"

		self.colors_dict["kit_lila_1"] = "#BC0C8D"
		self.colors_dict["kit_lila_2"] = "#CC4DAE"
		self.colors_dict["kit_lila_3"] = "#D97CC4"
		self.colors_dict["kit_lila_4"] = "#E7AEDB"
		self.colors_dict["kit_lila_5"] = "#F2D6ED"

		self.colors_dict["kit_cyanblau_1"] = "#1CAEEB"
		self.colors_dict["kit_cyanblau_2"] = "#5EC5F1"
		self.colors_dict["kit_cyanblau_3"] = "#8CD4F4"
		self.colors_dict["kit_cyanblau_4"] = "#B9E5F8"
		self.colors_dict["kit_cyanblau_5"] = "#DCF2FB"

		self.colors_dict["kit_grau_1"] = "#231F20"
		self.colors_dict["kit_grau_2"] = "#656263"
		self.colors_dict["kit_grau_3"] = "#918F90"
		self.colors_dict["kit_grau_4"] = "#BDBCBC"
		self.colors_dict["kit_grau_5"] = "#DEDDDE"

		# rwth colors
		self.colors_dict["rwth_blau_100"] = "#00549F"
		self.colors_dict["rwth_blau_075"] = "#407FB7"
		self.colors_dict["rwth_blau_050"] = "#8EBAE5"
		self.colors_dict["rwth_blau_025"] = "#C7DDF2"
		self.colors_dict["rwth_blau_010"] = "#E8F1FA"

		self.colors_dict["rwth_schwarz_100"] = "#000000"
		self.colors_dict["rwth_schwarz_075"] = "#646567"
		self.colors_dict["rwth_schwarz_050"] = "#9C9E9F"
		self.colors_dict["rwth_schwarz_025"] = "#CFD1D2"
		self.colors_dict["rwth_schwarz_010"] = "#ECEDED"

		self.colors_dict["rwth_magenta_100"] = "#E30066"
		self.colors_dict["rwth_magenta_075"] = "#E96088"
		self.colors_dict["rwth_magenta_050"] = "#F19EB1"
		self.colors_dict["rwth_magenta_025"] = "#F9D2DA"
		self.colors_dict["rwth_magenta_010"] = "#FDEEF0"

		self.colors_dict["rwth_gelb_100"] = "#FFED00"
		self.colors_dict["rwth_gelb_075"] = "#FFF055"
		self.colors_dict["rwth_gelb_050"] = "#FFF59B"
		self.colors_dict["rwth_gelb_025"] = "#FFFAD1"
		self.colors_dict["rwth_gelb_010"] = "#FFFDEE"

		self.colors_dict["rwth_petrol_100"] = "#006165"
		self.colors_dict["rwth_petrol_075"] = "#2D7F83"
		self.colors_dict["rwth_petrol_050"] = "#7DA4A7"
		self.colors_dict["rwth_petrol_025"] = "#BFD0D1"
		self.colors_dict["rwth_petrol_010"] = "#E6ECEC"

		self.colors_dict["rwth_tuerkis_100"] = "#0098A1"
		self.colors_dict["rwth_tuerkis_075"] = "#00B1B7"
		self.colors_dict["rwth_tuerkis_050"] = "#89CCCF"
		self.colors_dict["rwth_tuerkis_025"] = "#CAE7E7"
		self.colors_dict["rwth_tuerkis_010"] = "#EBF6F6"

		self.colors_dict["rwth_gruen_100"] = "#57AB27"
		self.colors_dict["rwth_gruen_075"] = "#8DC060"
		self.colors_dict["rwth_gruen_050"] = "#B8D698"
		self.colors_dict["rwth_gruen_025"] = "#DDEBCE"
		self.colors_dict["rwth_gruen_010"] = "#F2F7EC"

		self.colors_dict["rwth_maigruen_100"] = "#BDCD00"
		self.colors_dict["rwth_maigruen_075"] = "#D0D95C"
		self.colors_dict["rwth_maigruen_050"] = "#E0E69A"
		self.colors_dict["rwth_maigruen_025"] = "#F0F3D0"
		self.colors_dict["rwth_maigruen_010"] = "#F9FAED"

		self.colors_dict["rwth_orange_100"] = "#F6A800"
		self.colors_dict["rwth_orange_075"] = "#FABE50"
		self.colors_dict["rwth_orange_050"] = "#FDD48F"
		self.colors_dict["rwth_orange_025"] = "#FEEAC9"
		self.colors_dict["rwth_orange_010"] = "#FFF7EA"

		self.colors_dict["rwth_rot_100"] = "#CC071E"
		self.colors_dict["rwth_rot_075"] = "#D85C41"
		self.colors_dict["rwth_rot_050"] = "#E69679"
		self.colors_dict["rwth_rot_025"] = "#F3CDBB"
		self.colors_dict["rwth_rot_010"] = "#FAEBE3"

		self.colors_dict["rwth_bordeaux_100"] = "#A11035"
		self.colors_dict["rwth_bordeaux_075"] = "#B65256"
		self.colors_dict["rwth_bordeaux_050"] = "#CD8B87"
		self.colors_dict["rwth_bordeaux_025"] = "#E5C5C0"
		self.colors_dict["rwth_bordeaux_010"] = "#F5E8E5"

		self.colors_dict["rwth_violett_100"] = "#612158"
		self.colors_dict["rwth_violett_075"] = "#834E75"
		self.colors_dict["rwth_violett_050"] = "#A8859E"
		self.colors_dict["rwth_violett_025"] = "#D2C0CD"
		self.colors_dict["rwth_violett_010"] = "#EDE5EA"

		self.colors_dict["rwth_lila_100"] = "#7A6FAC"
		self.colors_dict["rwth_lila_075"] = "#9B91C1"
		self.colors_dict["rwth_lila_050"] = "#BCB5D7"
		self.colors_dict["rwth_lila_025"] = "#DEDAEB"
		self.colors_dict["rwth_lila_010"] = "#F2F0F7"

		#vega 10-color categorical palette as used by mlp2
		self.colors_dict["vega_cat1_01"] = "#1f77b4"
		self.colors_dict["vega_cat1_02"] = "#ff7f0e"
		self.colors_dict["vega_cat1_03"] = "#2ca02c"
		self.colors_dict["vega_cat1_04"] = "#d62728"
		self.colors_dict["vega_cat1_05"] = "#9467bd"
		self.colors_dict["vega_cat1_06"] = "#8c564b"
		self.colors_dict["vega_cat1_07"] = "#e377c2"
		self.colors_dict["vega_cat1_08"] = "#7f7f7f"
		self.colors_dict["vega_cat1_09"] = "#bcbd22"
		self.colors_dict["vega_cat1_10"] = "#17becf"

		self.colors_dict["data"] = "#000000"
		self.colors_dict["data_obs"] = self.colors_dict["data"]
		self.colors_dict["tttautau"] = "#000000 #00FF00"
		if color_scheme.lower() == "kit":
			self.colors_dict["zll"] = self.colors_dict["kit_gruen_2"]+" "+self.colors_dict["kit_gruen_2"]
			self.colors_dict["zmm"] = self.colors_dict["zll"]
			self.colors_dict["zee"] = self.colors_dict["zll"]
			self.colors_dict["zl"]  = self.colors_dict["zll"]
			self.colors_dict["zj"]  = self.colors_dict["zll"]
			self.colors_dict["ztt"] = self.colors_dict["kit_braun_1"]+" "+self.colors_dict["kit_braun_2"]
			self.colors_dict["tt"] = self.colors_dict["kit_blau_1"]+" "+self.colors_dict["kit_blau_2"]
			self.colors_dict["ttt"] = self.colors_dict["kit_blau_1"]+" "+self.colors_dict["kit_blau_2"]
			self.colors_dict["ttjj"] = self.colors_dict["kit_blau_1"]+" "+self.colors_dict["kit_blau_2"]
			self.colors_dict["ttj"] = self.colors_dict["tt"]
			self.colors_dict["ttjt"] = self.colors_dict["kit_blau_1"]
			self.colors_dict["ttjl"] = self.colors_dict["kit_blau_2"]
			self.colors_dict["ttbar"] = self.colors_dict["tt"]
			self.colors_dict["vv"]  = self.colors_dict["kit_gelb_1"]+" "+self.colors_dict["kit_gelb_2"]
			self.colors_dict["vvt"]  = self.colors_dict["kit_gelb_1"]
			self.colors_dict["vvl"]  = self.colors_dict["kit_gelb_2"]
			self.colors_dict["vvj"]  = self.colors_dict["kit_gelb_3"]
			self.colors_dict["dibosons"]  = self.colors_dict["vv"]
			self.colors_dict["ewk"]  = self.colors_dict["vv"]
			self.colors_dict["ewkz"]  = self.colors_dict["vv"]
			self.colors_dict["qcd"] = self.colors_dict["kit_maigruen_1"]+" "+self.colors_dict["kit_maigruen_2"]
			self.colors_dict["fakes"] = self.colors_dict["qcd"]
			self.colors_dict["wj"]  = self.colors_dict["kit_cyanblau_2"]+" "+self.colors_dict["kit_cyanblau_3"]
			self.colors_dict["wjt"]  = self.colors_dict["kit_cyanblau_2"]
			self.colors_dict["wjl"]  = self.colors_dict["kit_cyanblau_3"]
			self.colors_dict["wjets"]  = self.colors_dict["wj"]
			self.colors_dict["w"]  = self.colors_dict["wj"]
			self.colors_dict["qcdwj"] = self.colors_dict["qcd"]
			self.colors_dict["htt"] = self.colors_dict["kit_rot_1"]+" "+self.colors_dict["kit_rot_2"]
			self.colors_dict["ggh"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["susy_ggh"] = self.colors_dict["rwth_lila_100"]
			self.colors_dict["bbh"] = self.colors_dict["kit_gruen_1"]
			self.colors_dict["gghsm"] = self.colors_dict["kit_gelb_1"]
			self.colors_dict["gghmm"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["gghps_alt"] = self.colors_dict["kit_cyanblau_1"]
			self.colors_dict["gghmm_alt"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["gghps"] = self.colors_dict["kit_cyanblau_1"]
			self.colors_dict["qqh"] = self.colors_dict["kit_orange_1"]
			self.colors_dict["vh"]  = self.colors_dict["kit_lila_1"]
			self.colors_dict["totalsig"] = self.colors_dict["htt"]
			self.colors_dict["hww"] = self.colors_dict["kit_lila_3"]+" "+self.colors_dict["kit_lila_4"]
			self.colors_dict["hww120"] = self.colors_dict["hww"]
			self.colors_dict["hww125"] = self.colors_dict["hww"]
			self.colors_dict["hww130"] = self.colors_dict["hww"]
			self.colors_dict["hww_gg120"] = self.colors_dict["hww"]
			self.colors_dict["hww_gg125"] = self.colors_dict["hww"]
			self.colors_dict["hww_gg130"] = self.colors_dict["hww"]
			self.colors_dict["hww_qq120"] = self.colors_dict["hww"]
			self.colors_dict["hww_qq125"] = self.colors_dict["hww"]
			self.colors_dict["hww_qq130"] = self.colors_dict["hww"]
			self.colors_dict["totalbkg"] = "#000000 transgrey"
			self.colors_dict["ff"] = self.colors_dict["kit_grau_2"]
			self.colors_dict["httcpeven"] = self.colors_dict["rwth_magenta_100"]
			self.colors_dict["httcpmix"] = self.colors_dict["rwth_gruen_100"]
			self.colors_dict["httcpodd"] = self.colors_dict["rwth_rot_100"]
			self.colors_dict["cpeven"] = self.colors_dict["rwth_blau_050"]
			self.colors_dict["cpmix_alt"] = self.colors_dict["rwth_gelb_100"]
			self.colors_dict["cpodd_alt"] = self.colors_dict["rwth_gelb_100"]

			self.colors_dict["channel_tt"] = self.colors_dict["kit_blau_1"]
			self.colors_dict["channel_mt"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["channel_mm"] = self.colors_dict["kit_gruen_1"]

		else: # if color_scheme.lower() == "cern":
			self.colors_dict["zll"] = "#000000 #4496C8"
			self.colors_dict["zmm"] = self.colors_dict["zll"]
			self.colors_dict["zee"] = self.colors_dict["zll"]
			self.colors_dict["zl"]  = "#000000 #4496C8"
			self.colors_dict["zj"]  = "#000000 #64DE6A"
			self.colors_dict["ztt"] = "#000000 #FFCC66"
			self.colors_dict["zmt"] = "#000000 #CE66FF"
			self.colors_dict["zet"] = "#000000 #CE66FF"
			self.colors_dict["zem"] = "#000000 #CE66FF"
			self.colors_dict["zttpospol"] = "#000000 #FFEEBB"
			self.colors_dict["zttnegpol"] = "#000000 #FFCC66"
			self.colors_dict["tt"] = "#000000 #9999CC"
			self.colors_dict["ttt"] = self.colors_dict["tt"]
			self.colors_dict["ttjj"] = self.colors_dict["tt"]
			self.colors_dict["ttj"] = self.colors_dict["tt"]
			self.colors_dict["ttjt"] = self.colors_dict["kit_blau_1"]
			self.colors_dict["ttjl"] = self.colors_dict["kit_blau_2"]
			self.colors_dict["ttbar"] = self.colors_dict["tt"]
			self.colors_dict["wj"]  = "#000000 #DE5A6A"
			self.colors_dict["wjt"]  = self.colors_dict["kit_cyanblau_2"]
			self.colors_dict["wjl"]  = self.colors_dict["kit_cyanblau_3"]
			self.colors_dict["wjets"]  = self.colors_dict["wj"]
			self.colors_dict["w"]  = self.colors_dict["wj"]
			self.colors_dict["vv"]  = "#000000 #6F2D35"
			self.colors_dict["vvt"]  = self.colors_dict["kit_gelb_1"]
			self.colors_dict["vvl"]  = self.colors_dict["kit_gelb_2"]
			self.colors_dict["vvj"]  = self.colors_dict["kit_gelb_3"]
			self.colors_dict["dibosons"]  = self.colors_dict["wj"]
			self.colors_dict["ewk"]  = self.colors_dict["wj"]
			self.colors_dict["ewkz"] = self.colors_dict["wj"]
			self.colors_dict["qcd"] = "#000000 #FFCCFF"
			self.colors_dict["fakes"] = self.colors_dict["qcd"]
			self.colors_dict["qcdwj"] = self.colors_dict["qcd"]
			self.colors_dict["htt"] = "#0000FF"
			self.colors_dict["ggh"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["susy_ggh"] = self.colors_dict["rwth_lila_100"]
			self.colors_dict["bbh"] = self.colors_dict["kit_gruen_1"]
			self.colors_dict["gghsm"] = self.colors_dict["kit_gelb_1"]
			self.colors_dict["gghmm"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["gghps"] = self.colors_dict["kit_cyanblau_1"]
			self.colors_dict["gghps_alt"] = self.colors_dict["kit_cyanblau_1"]
			self.colors_dict["gghmm_alt"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["qqh"] = self.colors_dict["kit_gruen_1"]
			self.colors_dict["qqhsm"] = self.colors_dict["kit_gelb_2"]
			self.colors_dict["qqhmm"] = self.colors_dict["kit_rot_2"]
			self.colors_dict["qqhps"] = self.colors_dict["kit_cyanblau_2"]
			self.colors_dict["qqhps_alt"] = self.colors_dict["kit_gruen_1"]
			self.colors_dict["qqhmm_alt"] = self.colors_dict["kit_rot_2"]
			self.colors_dict["vh"]  = self.colors_dict["kit_lila_1"]
			self.colors_dict["zh"]  = self.colors_dict["kit_lila_1"]
			self.colors_dict["wh"]  = self.colors_dict["kit_lila_1"]			
			self.colors_dict["totalsig"] = self.colors_dict["htt"]
			self.colors_dict["hww"] = self.colors_dict["kit_lila_3"]+" "+self.colors_dict["kit_lila_4"]
			self.colors_dict["hww120"] = self.colors_dict["hww"]
			self.colors_dict["hww125"] = self.colors_dict["hww"]
			self.colors_dict["hww130"] = self.colors_dict["hww"]
			self.colors_dict["hww_gg120"] = self.colors_dict["hww"]
			self.colors_dict["hww_gg125"] = self.colors_dict["hww"]
			self.colors_dict["hww_gg130"] = self.colors_dict["hww"]
			self.colors_dict["hww_qq120"] = self.colors_dict["hww"]
			self.colors_dict["hww_qq125"] = self.colors_dict["hww"]
			self.colors_dict["hww_qq130"] = self.colors_dict["hww"]
			self.colors_dict["totalbkg"] = "#000000 transgrey"
			self.colors_dict["ff"] = self.colors_dict["kit_grau_2"]
			self.colors_dict["httcpeven"] = self.colors_dict["rwth_magenta_100"]
			self.colors_dict["httcpmix"] = self.colors_dict["rwth_gruen_100"]
			self.colors_dict["httcpodd"] = self.colors_dict["rwth_rot_100"]
			self.colors_dict["cpeven"] = self.colors_dict["rwth_blau_050"]
			self.colors_dict["cpmix_alt"] = self.colors_dict["rwth_gelb_100"]
			self.colors_dict["cpodd_alt"] = self.colors_dict["rwth_gelb_100"]
			

		for higgs_mass in xrange(90, 161, 5):
			self.colors_dict["htt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["htt"]
			self.colors_dict["ggh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["ggh"]
			self.colors_dict["susy_ggh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["susy_ggh"]
			self.colors_dict["bbh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["bbh"]

			self.colors_dict["gghsm{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghsm"]
			self.colors_dict["gghmm{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghmm"]
			self.colors_dict["gghps{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghps"]

			self.colors_dict["gghmm_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghmm"]
			self.colors_dict["gghps_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghps"]

			self.colors_dict["httcpeven{mass:d}".format(mass=higgs_mass)] = self.colors_dict["httcpeven"]
			self.colors_dict["httcpmix{mass:d}".format(mass=higgs_mass)] = self.colors_dict["httcpmix"]
			self.colors_dict["httcpodd{mass:d}".format(mass=higgs_mass)] = self.colors_dict["httcpodd"]

			self.colors_dict["cpeven{mass:d}".format(mass=higgs_mass)] = self.colors_dict["cpeven"]
			self.colors_dict["cpmix_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["cpmix_alt"]
			self.colors_dict["cpodd_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["cpodd_alt"]

			self.colors_dict["qqh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["qqh"]
			self.colors_dict["vh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["vh"]
			for scale in [10, 25, 100, 250]:
				self.colors_dict["htt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["htt{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["ggh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["ggh{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["susy_ggh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["susy_ggh{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["bbh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["bbh{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["gghsm{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghsm{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["gghmm{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghmm{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["gghps{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghps{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["gghmm_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghmm{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["gghps_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghps{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["httcpeven{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["httcpeven{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["httcpmix{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["httcpmix{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["httcpodd{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["httcpodd{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["cpeven{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["cpeven{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["cpmix_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["cpmix_alt{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["cpodd_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["cpodd_alt{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["qqh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["qqh{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["vh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["vh{mass:d}".format(mass=higgs_mass)]
		for higgs_mass in xrange(90, 3201, 10):
			self.colors_dict["htt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["htt"]
			self.colors_dict["ggh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["ggh"]
			self.colors_dict["susy_ggh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["susy_ggh"]
			self.colors_dict["bbh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["bbh"]

			self.colors_dict["gghsm{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghsm"]
			self.colors_dict["gghmm{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghmm"]
			self.colors_dict["gghps{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghps"]
			
			self.colors_dict["gghmm_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghmm"]
			self.colors_dict["gghps_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["gghps"]

			self.colors_dict["httcpeven{mass:d}".format(mass=higgs_mass)] = self.colors_dict["httcpeven"]
			self.colors_dict["httcpmix{mass:d}".format(mass=higgs_mass)] = self.colors_dict["httcpmix"]
			self.colors_dict["httcpodd{mass:d}".format(mass=higgs_mass)] = self.colors_dict["httcpodd"]

			self.colors_dict["cpeven{mass:d}".format(mass=higgs_mass)] = self.colors_dict["cpeven"]
			self.colors_dict["cpmix_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["cpmix_alt"]
			self.colors_dict["cpodd_alt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["cpodd_alt"]

			self.colors_dict["bbh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["bbh"]
			for scale in [10, 25, 100, 250]:
				self.colors_dict["htt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["htt{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["ggh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["ggh{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["susy_ggh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["susy_ggh{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["bbh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["bbh{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["gghsm{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghsm{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["gghmm{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghmm{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["gghps{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghps{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["gghmm_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghmm{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["gghps_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["gghps{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["httcpeven{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["httcpeven{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["httcpmix{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["httcpmix{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["httcpodd{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["httcpodd{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["cpeven{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["cpeven{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["cpmix_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["cpmix_alt{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["cpodd_alt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["cpodd_alt{mass:d}".format(mass=higgs_mass)]

				self.colors_dict["bbh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["bbh{mass:d}".format(mass=higgs_mass)]

