
# -*- coding: utf-8 -*-

import math
import multiprocessing
import os
import string
import sys
import tempfile


def me2(args):
	cartesian_four_momenta = args[0]
	madgraph_process_directory = args[1]
	madgraph_param_card = args[2]
	alpha_s = args[3]
	
	cwd = os.getcwd()
	os.chdir(madgraph_process_directory)

	sys.path.insert(0, madgraph_process_directory)
	import matrix2py
	sys.path.pop(0)

	matrix2py.initialise(madgraph_param_card)
	result = matrix2py.get_me(zip(*cartesian_four_momenta), alpha_s, 0)
	
	os.chdir(cwd)
	
	return result


class MadGraphTools(object):
	def __init__(self, mixing_angle_over_pi_half, madgraph_process_directory, madgraph_param_card, alpha_s):
		cos_mixing_angle = math.cos(mixing_angle_over_pi_half * math.pi / 2.0)
		self.madgraph_process_directory = madgraph_process_directory
		self.alpha_s = alpha_s
		
		# read param_card and modify it in a temporary file
		madgraph_param_card_content = ""
		with open(madgraph_param_card) as madgraph_param_card_file:
			madgraph_param_card_content = madgraph_param_card_file.read().rstrip("\n")
	
		self.madgraph_param_card = None
		with tempfile.NamedTemporaryFile(prefix="param_card_", suffix=os.path.splitext(madgraph_param_card)[-1], delete=False) as param_card_file:
			self.madgraph_param_card = param_card_file.name
			param_card_file.write(string.Template(madgraph_param_card_content).safe_substitute(cosa=str(cos_mixing_angle)))
	
	def __del__(self):
		os.remove(self.madgraph_param_card)
	
	def matrix_element_squared(self, cartesian_four_momenta):
		arguments = [cartesian_four_momenta, self.madgraph_process_directory, self.madgraph_param_card, self.alpha_s]
		pool = multiprocessing.Pool(processes=1)
		pool.daemon = True
		result = pool.apply(me2, [arguments])
		pool.terminate()
		return result
