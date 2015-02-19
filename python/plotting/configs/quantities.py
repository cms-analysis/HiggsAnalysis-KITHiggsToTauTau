
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy



class Quantity(object):

	def __init__(self, plot_config):
		self.plot_config = plot_config
	
	def get_config(self, channel, category):
		plot_config = copy.deepcopy(self.plot_config)
		return plot_config



class VisibleMass(Quantity):
	
	def get_config(self, channel, category):
		plot_config = super(VisibleMass, self).get_config(channel, category)
		
		plot_config["x_bins"] = [str(x) for x in xrange(20, 120, 20)]
		
		return plot_config



class SvfitMass(Quantity):
	
	def get_config(self, channel, category):
		plot_config = super(SvfitMass, self).get_config(channel, category)
		
		if (channel == "mt") or (channel == "et"):
			if "vbf" in category:
				plot_config["x_bins"] = [0.0, 20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 250.0, 300.0, 350.0]
			else:
				plot_config["x_bins"] = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 225.0, 250.0, 275.0, 300.0, 325.0, 350.0]
		
		return plot_config

