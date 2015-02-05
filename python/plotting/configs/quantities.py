
# -*- coding: utf-8 -*-

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

