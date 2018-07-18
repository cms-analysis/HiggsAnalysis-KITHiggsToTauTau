# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class MinimalPlotlevelFilter():

	def __init__(self, nickname, channel=None, eTauFakeRate=False):
		self.minPlotLevelDict = {}
		self.channel = channel
		self.eTauFakeRate = eTauFakeRate
		if   channel == "EM": self.em()
		elif channel == "MT": self.mt(nickname=nickname)
		elif channel == "ET": self.et(nickname=nickname, eTauFakeRate=eTauFakeRate)
		elif channel == "TT": self.tt(nickname=nickname, eTauFakeRate=eTauFakeRate)
		elif channel == "MM": self.mm()
		elif channel == "EE": self.ee()

	def em(self):
		self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = [
			"extraelec_veto",
			"extramuon_veto"
		]
		self.minPlotLevelDict["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"

	def mt(self, nickname):
		self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = [
			"extraelec_veto",
			"extramuon_veto",
			"nDiMuonVetoPairsOS"
		]

		self.minPlotLevelDict["PlotlevelFilterExpression"] = "(nDiMuonVetoPairsOS < 0.5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
		if re.search("(Fall17|Summer17|Run2017)", nickname):
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] += [ "byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_2"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] += "*(byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"
		else:
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] += ["againstElectronVLooseMVA6_2", "againstMuonTight3_2", "byLooseIsolationMVArun2v1DBoldDMwLT_2"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] += "*(againstElectronVLooseMVA6_2 > 0.5)*(againstMuonTight3_2 > 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"

	def et(self, nickname, eTauFakeRate=False):
		#self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = ["againstMuonLoose3_2"]

		if not eTauFakeRate:
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = [
				"extraelec_veto",
				"extramuon_veto",
				"nDiElectronVetoPairsOS"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] = "(nDiElectronVetoPairsOS < 0.5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
		else:
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = ["lep1IsoOverPt", "againstMuonLoose3_2"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] = "(lep1IsoOverPt < 0.1)*(againstMuonLoose3_2 > 0.5)"

		if re.search("(Fall17|Summer17|Run2017)", nickname):
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] += [ "byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_2"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] += "*(byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"
		else:
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] += ["againstElectronTightMVA6_2", "againstMuonLoose3_2", "byLooseIsolationMVArun2v1DBoldDMwLT_2"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] += "*(againstElectronTightMVA6_2 > 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"

	def tt(self, nickname, eTauFakeRate=False):
		self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = [
			"againstElectronVLooseMVA6_2",
			"extraelec_veto",
			"againstMuonLoose3_2",
			"extramuon_veto"
		]
		self.minPlotLevelDict["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)"

		if re.search("(Fall17|Summer17|Run2017)", nickname):
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] += ["byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_1", "byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_2"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] += "*(byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5) *(byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"
		else:
			self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] += ["byLooseIsolationMVArun2v1DBoldDMwLT_1","byLooseIsolationMVArun2v1DBoldDMwLT_2"]
			self.minPlotLevelDict["PlotlevelFilterExpression"] += "*(byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5) *(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
	def mm(self):
		self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = [
			"extraelec_veto",
			"extramuon_veto"
		]
		self.minPlotLevelDict["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"

	def ee(self):
		self.minPlotLevelDict["PlotlevelFilterExpressionQuantities"] = [
			"extraelec_veto",
			"extramuon_veto"
		]
		self.minPlotLevelDict["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
