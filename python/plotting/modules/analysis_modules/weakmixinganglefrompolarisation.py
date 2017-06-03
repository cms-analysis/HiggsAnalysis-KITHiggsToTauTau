# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase


class WeakMixingAngleFromPolarisation(analysisbase.AnalysisBase):
	"""Convert graphs of average tau polarisation into weak mixing angle graphs using a given calibration curve."""
	
	def __init__(self):
		super(WeakMixingAngleFromPolarisation, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(WeakMixingAngleFromPolarisation, self).modify_argument_parser(parser, args)
		
		self.weak_mixing_angle_from_polarisation_options = parser.add_argument_group("{} options".format(self.name()))
		self.weak_mixing_angle_from_polarisation_options.add_argument("--polarisation-graph-nicks", type=str, nargs="+",
				help="Nick names of the polarisation graphs.")
		self.weak_mixing_angle_from_polarisation_options.add_argument("--calibration-curve-nicks", type=str, nargs="+",
				help="Nick names of the calibration curve graphs.")
		self.weak_mixing_angle_from_polarisation_options.add_argument("--weak-mixing-angle-graph-nicks", type=str, nargs="+",
				help="Nick names of the resulting weak miging angle graphs.")
	
	def prepare_args(self, parser, plotData):
		super(WeakMixingAngleFromPolarisation, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["polarisation_graph_nicks", "calibration_curve_nicks", "weak_mixing_angle_graph_nicks"])
		for polarisation_graph_nick, weak_mixing_angle_graph_nick in zip(*[plotData.plotdict[key] for key in ["polarisation_graph_nicks", "weak_mixing_angle_graph_nicks"]]):
			if not weak_mixing_angle_graph_nick in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(plotData.plotdict["nicks"].index(polarisation_graph_nick), weak_mixing_angle_graph_nick)

	def run(self, plotData=None):
		super(WeakMixingAngleFromPolarisation, self).run(plotData)
		
		for polarisation_graph_nick, calibration_curve_nick, weak_mixing_angle_graph_nick in zip(*[plotData.plotdict[key] for key in ["polarisation_graph_nicks", "calibration_curve_nicks", "weak_mixing_angle_graph_nicks"]]):
			print "\nstart conversion" # TODO: remove this line
			polarisation_graph = plotData.plotdict["root_objects"][polarisation_graph_nick]
			calibration_curve = plotData.plotdict["root_objects"][calibration_curve_nick]
			print polarisation_graph_nick, polarisation_graph # TODO: remove this line
			print calibration_curve_nick, calibration_curve # TODO: remove this line
			
			weak_mixing_angle_graph = polarisation_graph # TODO: create a new TGraphAsymmErrors object and calculate its points/errors from polarisation_graph and calibration_curve
			
			plotData.plotdict["root_objects"][weak_mixing_angle_graph_nick] = weak_mixing_angle_graph
			print weak_mixing_angle_graph_nick, weak_mixing_angle_graph # TODO: remove this line
			print "end conversion\n" # TODO: remove this line

