
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
		
		self.colors_dict["data"] = "#000000"
		self.colors_dict["data_obs"] = self.colors_dict["data"]
		
		if color_scheme.lower() == "kit":
			self.colors_dict["zll"] = self.colors_dict["kit_gruen_1"]+" "+self.colors_dict["kit_gruen_2"]
			self.colors_dict["zmm"] = self.colors_dict["zll"]
			self.colors_dict["zee"] = self.colors_dict["zll"]
			self.colors_dict["zl"]  = self.colors_dict["zll"]
			self.colors_dict["zj"]  = self.colors_dict["zll"]
			self.colors_dict["ztt"] = self.colors_dict["kit_braun_1"]+" "+self.colors_dict["kit_braun_2"]
			self.colors_dict["tt"] = self.colors_dict["kit_blau_1"]+" "+self.colors_dict["kit_blau_2"]
			self.colors_dict["ttj"] = self.colors_dict["tt"]
			self.colors_dict["ttbar"] = self.colors_dict["tt"]
			self.colors_dict["vv"]  = self.colors_dict["kit_gelb_1"]+" "+self.colors_dict["kit_gelb_2"]
			self.colors_dict["dibosons"]  = self.colors_dict["vv"]
			self.colors_dict["ewk"]  = self.colors_dict["vv"]
			self.colors_dict["qcd"] = self.colors_dict["kit_maigruen_1"]+" "+self.colors_dict["kit_maigruen_2"]
			self.colors_dict["fakes"] = self.colors_dict["qcd"]
			self.colors_dict["wj"]  = self.colors_dict["kit_cyanblau_2"]+" "+self.colors_dict["kit_cyanblau_3"]
			self.colors_dict["wjets"]  = self.colors_dict["wj"]
			self.colors_dict["qcdwj"] = self.colors_dict["qcd"]
			self.colors_dict["htt"] = self.colors_dict["kit_rot_1"]+" "+self.colors_dict["kit_rot_2"]
			self.colors_dict["ggh"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["qqh"] = self.colors_dict["kit_orange_1"]
			self.colors_dict["vh"]  = self.colors_dict["kit_lila_1"]
			self.colors_dict["totalsig"] = self.colors_dict["htt"]
			self.colors_dict["hww"] = self.colors_dict["kit_lila_3"]+" "+self.colors_dict["kit_lila_4"]
			self.colors_dict["hww125"] = self.colors_dict["hww"]
			self.colors_dict["totalbkg"] = "#000000"
			
			self.colors_dict["channel_tt"] = self.colors_dict["kit_blau_1"]
			self.colors_dict["channel_mt"] = self.colors_dict["kit_rot_1"]
			self.colors_dict["channel_mm"] = self.colors_dict["kit_gruen_1"]
		
		else: # if color_scheme.lower() == "cern":
			self.colors_dict["zll"] = "#000000 #4496C8"
			self.colors_dict["zmm"] = self.colors_dict["zll"]
			self.colors_dict["zee"] = self.colors_dict["zll"]
			self.colors_dict["zl"]  = self.colors_dict["zll"]
			self.colors_dict["zj"]  = self.colors_dict["zll"]
			self.colors_dict["ztt"] = "#000000 #FFCC66"
			self.colors_dict["tt"] = "#000000 #9999CC"
			self.colors_dict["ttj"] = self.colors_dict["tt"]
			self.colors_dict["ttbar"] = self.colors_dict["tt"]
			self.colors_dict["wj"]  = "#000000 #DE5A6A"
			self.colors_dict["wjets"]  = self.colors_dict["wj"]
			self.colors_dict["vv"]  = "#000000 #6F2D35"
			self.colors_dict["dibosons"]  = self.colors_dict["wj"]
			self.colors_dict["ewk"]  = self.colors_dict["wj"]
			self.colors_dict["qcd"] = "#000000 #FFCCFF"
			self.colors_dict["fakes"] = self.colors_dict["qcd"]
			self.colors_dict["qcdwj"] = self.colors_dict["qcd"]
			self.colors_dict["htt"] = "#FF0000"
			self.colors_dict["ggh"] = self.colors_dict["htt"]
			self.colors_dict["qqh"] = self.colors_dict["htt"]
			self.colors_dict["vh"]  = self.colors_dict["htt"]
			self.colors_dict["totalsig"] = self.colors_dict["htt"]
			self.colors_dict["totalbkg"] = "#000000"

		for higgs_mass in xrange(90, 161, 5):
			self.colors_dict["htt{mass:d}".format(mass=higgs_mass)] = self.colors_dict["htt"]
			self.colors_dict["ggh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["ggh"]
			self.colors_dict["qqh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["qqh"]
			self.colors_dict["vh{mass:d}".format(mass=higgs_mass)] = self.colors_dict["vh"]
			
			for scale in [10, 25, 100]:
				self.colors_dict["htt{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["htt{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["ggh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["htt{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["qqh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["htt{mass:d}".format(mass=higgs_mass)]
				self.colors_dict["vh{mass:d}_{scale:d}".format(mass=higgs_mass, scale=scale)] = self.colors_dict["htt{mass:d}".format(mass=higgs_mass)]

