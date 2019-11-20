# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPFinalStateStudies.quantities import Quantities
from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.processorOrdering import ProcessorsOrdered

# Use mt CP Initial State config as baseline
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.mt as mtbaseconfig

import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz


class mt_ArtusConfig(mtbaseconfig.mt_ArtusConfig):

	def __init__(self):
		pass

	def build_config(self, nickname, *args, **kwargs):

		super(mt_ArtusConfig, self).build_config(nickname, *args, **kwargs)

		if re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/mt/fakeFactors.root"
			self["FakeFactorMethod"] = "cpfinalstate2017"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/FF_fractions_workspace_m_vis_njets.root"
			self["FakeFactorRooWorkspaceFunction"] = [
				"w_fracs:w_fracs_mt",
				"qcd_fracs:qcd_fracs_mt",
				"ttbar_fracs:ttbar_fracs_mt",
				"dy_fracs:real_taus_fracs_mt",
			]

		self["TauUpperAbsEtaCuts"] = ["2.1"] # tau trigger SFs only allow abs(eta) up to 2.1

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"])
		quantities_set.quantities.update(self["Quantities"])
		self["Quantities"] = list(quantities_set.quantities)
