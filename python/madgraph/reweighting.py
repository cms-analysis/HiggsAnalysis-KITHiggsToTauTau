
# -*- coding: utf-8 -*-

import math
import os
import string
import sys
import tempfile


class MadGraphTools(object):
	def __init__(self, mixing_angle_over_pi_half, madgraph_process_directory, madgraph_param_card, alpha_s):
		cos_mixing_angle = math.cos(mixing_angle_over_pi_half * math.pi / 2.0)
		
		# read param_card and modify it in a temporary file
		madgraph_param_card_content = ""
		with open(madgraph_param_card) as madgraph_param_card_file:
			madgraph_param_card_content = madgraph_param_card_file.read().rstrip("\n")
	
		self.madgraph_param_card = None
		with tempfile.NamedTemporaryFile(prefix="param_card_", suffix=os.path.splitext(madgraph_param_card)[-1], delete=False) as param_card_file:
			self.madgraph_param_card = param_card_file.name
			param_card_file.write(string.Template(madgraph_param_card_content).safe_substitute(cosa=str(cos_mixing_angle)))
		
		sys.path.insert(0, madgraph_process_directory)
		self.matrix2py = __import__("matrix2py")
		#sys.path.pop(0)
		
		self.madgraph_process_directory = madgraph_process_directory
		#os.chdir(self.madgraph_process_directory)
		#self.matrix2py.initialise(self.madgraph_param_card)
		
		self.alpha_s = alpha_s
	
	def __del__(self):
		os.remove(self.madgraph_param_card)
	
	def matrix_element_squared(self, cartesian_four_momenta):
		os.chdir(self.madgraph_process_directory)
		self.matrix2py.initialise(self.madgraph_param_card)
		return self.matrix2py.get_me(zip(*cartesian_four_momenta), self.alpha_s, 0) # if not loop else self.matrix2py.get_me(zip(*cartesian_four_momenta), self.alpha_s, mu, -1)[0]

