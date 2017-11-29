
# -*- coding: utf-8 -*-

import math
import multiprocessing
import os
import string
import sys
import tempfile


def me2(connection):
	
	args = connection.recv()
	cartesian_four_momenta = args[0]
	pdgs = args[1]
	madgraph_process_directory = args[2]
	madgraph_param_card = args[3]
	alpha_s = args[4]
	
	
	
	cwd = os.getcwd()
	os.chdir(madgraph_process_directory)
	sys.path.insert(0, madgraph_process_directory)
	

	if "allmatrix2py" not in sys.modules:
		import allmatrix2py
		
	elif "allmatrix2py" in sys.modules:	
		del sys.modules["allmatrix2py"]
		import allmatrix2py
	
	allmatrix2py.initialise(madgraph_param_card)
	result = allmatrix2py.smatrixhel(pdgs,zip(*cartesian_four_momenta), alpha_s, 0,-1)

	sys.path.pop(0)
	os.chdir(cwd)
	connection.send([result])
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
	
	def matrix_element_squared(self, cartesian_four_momenta, pdgs):
		arguments = [cartesian_four_momenta, pdgs, self.madgraph_process_directory, self.madgraph_param_card, self.alpha_s]
		parent_connection, child_connection = multiprocessing.Pipe()
		parent_connection.send(arguments)
		
		process = multiprocessing.Process(target=me2, args=(child_connection,))
		process.start()
		
		timeout = 10 # in seconds
		process.join(timeout)
		

		result = -999.0
		if parent_connection.poll(timeout):
			result = parent_connection.recv()[0]
		process.terminate()
		return result


