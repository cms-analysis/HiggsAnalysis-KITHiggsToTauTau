
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.colors as colors


class ColorsDict(colors.ColorsDict):
	def __init__(self, color_scheme="default", additional_colors=None):
		super(ColorsDict, self).__init__(color_scheme=color_scheme, additional_colors=additional_colors)
		
		self.color_scheme = color_scheme
		self.colors_dict = {}
		self.colors_dict["data"] = "#000000"
		self.colors_dict["data_obs"] = self.colors_dict["data"]
		
		if color_scheme.lower() == "kit":
			self.colors_dict["zll"] = "#00A88F #4CC1A5"
			self.colors_dict["zmm"] = self.colors_dict["zll"]
			self.colors_dict["zee"] = self.colors_dict["zll"]
			self.colors_dict["zl"]  = self.colors_dict["zll"]
			self.colors_dict["zj"]  = self.colors_dict["zll"]
			self.colors_dict["ztt"] = "#A97E23 #C09D52"
			self.colors_dict["tt"] = "#4372C1 #7691D2"
			self.colors_dict["ttj"] = self.colors_dict["tt"]
			self.colors_dict["ttbar"] = self.colors_dict["tt"]
			self.colors_dict["wj"]  = "#66C42F #93D561"
			self.colors_dict["wjets"]  = self.colors_dict["wj"]
			self.colors_dict["vv"]  = self.colors_dict["wj"]
			self.colors_dict["dibosons"]  = self.colors_dict["wj"]
			self.colors_dict["ewk"]  = self.colors_dict["wj"]
			self.colors_dict["qcd"] = "#FEE701 #FEED4B"
			self.colors_dict["fakes"] = self.colors_dict["qcd"]
			self.colors_dict["htt"] = "#BF2229 #CD574A"
			self.colors_dict["ggh"] = self.colors_dict["htt"]
			self.colors_dict["qqh"] = self.colors_dict["htt"]
			self.colors_dict["vh"]  = self.colors_dict["htt"]
			self.colors_dict["totalsig"] = self.colors_dict["htt"]
		
		else: # if color_scheme.lower() == "cern":
			self.colors_dict["zll"] = "#4496C8"
			self.colors_dict["zmm"] = self.colors_dict["zll"]
			self.colors_dict["zee"] = self.colors_dict["zll"]
			self.colors_dict["zl"]  = self.colors_dict["zll"]
			self.colors_dict["zj"]  = self.colors_dict["zll"]
			self.colors_dict["ztt"] = "#FFCC66"
			self.colors_dict["tt"] = "#9999CC"
			self.colors_dict["ttj"] = self.colors_dict["tt"]
			self.colors_dict["ttbar"] = self.colors_dict["tt"]
			self.colors_dict["wj"]  = "#DE5A6A"
			self.colors_dict["wjets"]  = self.colors_dict["wj"]
			self.colors_dict["vv"]  = self.colors_dict["wj"]
			self.colors_dict["dibosons"]  = self.colors_dict["wj"]
			self.colors_dict["ewk"]  = self.colors_dict["wj"]
			self.colors_dict["qcd"] = "#FFCCFF"
			self.colors_dict["fakes"] = self.colors_dict["qcd"]
			self.colors_dict["htt"] = "#000000"
			self.colors_dict["ggh"] = self.colors_dict["htt"]
			self.colors_dict["qqh"] = self.colors_dict["htt"]
			self.colors_dict["vh"]  = self.colors_dict["htt"]
			self.colors_dict["totalsig"] = self.colors_dict["htt"]

