# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPFinalStateStudies.quantities import Quantities

# Use gen CP Initial State config as baseline
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.gen as genbaseconfig

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC


class gen_ArtusConfig(genbaseconfig.gen_ArtusConfig):

	def __init__(self):
		pass