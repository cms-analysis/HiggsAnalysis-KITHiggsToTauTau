# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class MinimalPlotlevelFilter(dict):

	def em(self):
		self["PlotlevelFilterExpressionQuantities"] =  ["extraelec_veto",
								"extramuon_veto"
    							]
    		self["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"

	def mt(self):
		self["PlotlevelFilterExpressionQuantities"] = ["againstElectronVLooseMVA6_2",
								"extraelec_veto",
								"againstMuonTight3_2",
								"extramuon_veto",
								"byLooseIsolationMVArun2v1DBoldDMwLT_2",
								"nDiMuonVetoPairsOS"
						    	]
    		self["PlotlevelFilterExpression"] = "(nDiMuonVetoPairsOS < 0.5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
	
	def et(self):
		self["PlotlevelFilterExpressionQuantities"] = ["againstElectronTightMVA6_2",
								"extraelec_veto",
								"againstMuonLoose3_2",
								"extramuon_veto",
								"byLooseIsolationMVArun2v1DBoldDMwLT_2",
								"nDiElectronVetoPairsOS"
    							]
    		self["PlotlevelFilterExpression"] = "(nDiElectronVetoPairsOS < 0.5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronTightMVA6_2 > 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"

	def tt(self):
		self["PlotlevelFilterExpressionQuantities"] = ["againstElectronVLooseMVA6_2",
								"extraelec_veto",
								"againstMuonLoose3_2",
								"extramuon_veto",
								"byLooseIsolationMVArun2v1DBoldDMwLT_1",
								"byLooseIsolationMVArun2v1DBoldDMwLT_2"
   							 ]
    		self["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"

	def mm(self):
		self["PlotlevelFilterExpressionQuantities"] = ["extraelec_veto",
								"extramuon_veto"
    							]
    		self["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"

	def ee(self):
		self["PlotlevelFilterExpressionQuantities"] = ["extraelec_veto",
								"extramuon_veto"
						    ]
    		self["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"

