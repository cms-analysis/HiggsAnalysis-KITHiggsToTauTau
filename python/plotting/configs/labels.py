
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.labels as labels


class LabelsDict(labels.LabelsDict):
	def __init__(self, latex_version="latex", additional_labels=None):
		super(LabelsDict, self).__init__(latex_version=latex_version, additional_labels=additional_labels)
		
		if latex_version == "root":
			self.labels_dict["data"] = "Data"
			self.labels_dict["data_obs"] = self.labels_dict["data"]
			self.labels_dict["zll"] = "Z #rightarrow ll"
			self.labels_dict["zl"]  = self.labels_dict["zll"]
			self.labels_dict["zj"]  = self.labels_dict["zll"]
			self.labels_dict["zmm"] = "Z #rightarrow #mu#mu"
			self.labels_dict["zee"] = "Z #rightarrow ee"
			self.labels_dict["ztt"] = "Z #rightarrow #tau#tau"
			self.labels_dict["tt"] = "t#bar{t} + jets"
			self.labels_dict["ttj"] = self.labels_dict["tt"]
			self.labels_dict["ttbar"] = self.labels_dict["tt"]
			self.labels_dict["wj"]  = "W + jets"
			self.labels_dict["wjets"]  = self.labels_dict["wj"]
			self.labels_dict["vv"]  = "Di-bosons"
			self.labels_dict["dibosons"]  = self.labels_dict["vv"]
			self.labels_dict["ewk"]  = self.labels_dict["vv"]
			self.labels_dict["qcd"] = "QCD"
			self.labels_dict["fakes"] = self.labels_dict["qcd"]
			self.labels_dict["htt"] = "H #rightarrow #tau#tau"
			self.labels_dict["ggh"] = "ggH"
			self.labels_dict["qqh"] = "qqH"
			self.labels_dict["vh"]  = "VH"
			self.labels_dict["totalsig"] = self.labels_dict["htt"]
			
		else:
			# put labels for MPL plots here
			pass
		
		for higgs_mass in xrange(90, 161, 5):
			self.labels_dict["htt{mass:d}".format(mass=higgs_mass)] = self.labels_dict["htt"].replace("H", "H({mass:d})".format(mass=higgs_mass))
			self.labels_dict["ggh{mass:d}".format(mass=higgs_mass)] = self.labels_dict["ggh"].replace("H", "H({mass:d})".format(mass=higgs_mass))
			self.labels_dict["qqh{mass:d}".format(mass=higgs_mass)] = self.labels_dict["qqh"].replace("H", "H({mass:d})".format(mass=higgs_mass))
			self.labels_dict["vh{mass:d}".format(mass=higgs_mass)] = self.labels_dict["vh"].replace("H", "H({mass:d})".format(mass=higgs_mass))

