
# -*- coding: utf-8 -*-

import math
import os
import string
import sys
import tempfile


class MadGraphMatrixElements(object):
	def __init__(self, mixing_angle_over_pi_half, madgraph_param_card, madgraph_process_directory, alpha_s=0.118):
		
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
		os.chdir(self.madgraph_process_directory) # change to subprocess directory
		self.matrix2py.initialise(self.madgraph_param_card)
		#os.remove(self.madgraph_param_card)
		
		self.alpha_s = alpha_s
	
	def matrix_element_squared(self, *cartesian_four_momenta):
		os.chdir(self.madgraph_process_directory) # change to subprocess directory
		self.matrix2py.initialise(self.madgraph_param_card)
		return self.matrix2py.get_me(zip(*cartesian_four_momenta), self.alpha_s, 0) # if not loop else self.matrix2py.get_me(zip(*cartesian_four_momenta), self.alpha_s, mu, -1)[0]


class MadGraphMatrixElementTools(object):
	def __init__(self, mixing_angles_over_pi_half, madgraph_param_card, madgraph_process_directories):
		
		self.calculators = {}
		for madgraph_process_directory in [madgraph_process_directories]:
			for mixing_angle_over_pi_half in mixing_angles_over_pi_half:
				mixing_angle_key = MadGraphMatrixElementTools.get_mixing_angle_key(mixing_angle_over_pi_half)
				self.calculators.setdefault(madgraph_process_directory, {})[mixing_angle_key] = MadGraphMatrixElements(
						mixing_angle_over_pi_half, madgraph_param_card, madgraph_process_directory
				)
	
	def matrix_element_squared(self, mixing_angle_over_pi_half, madgraph_process_directory, *cartesian_four_momenta):
		#print self, mixing_angle_over_pi_half, madgraph_process_directory, cartesian_four_momenta
		mixing_angle_key = MadGraphMatrixElementTools.get_mixing_angle_key(mixing_angle_over_pi_half)
		me2 = self.calculators[madgraph_process_directory][mixing_angle_key].matrix_element_squared(*cartesian_four_momenta)
		#print mixing_angle_over_pi_half, "-->", me2#, ",", self.calculators[madgraph_process_directory][mixing_angle_key], ",", self.calculators[madgraph_process_directory][mixing_angle_key].matrix2py
		return me2

	@staticmethod
	def get_mixing_angle_key(mixing_angle_over_pi_half):
		#return "%03d" % (mixing_angle_over_pi_half * 100.0)
		return int(mixing_angle_over_pi_half * 100.0)

def madgraph_weight_ggh(mixing_angle_over_pi_half, gluon1_lv, gluon2_lv, higgs_lv, madgraph_param_card, madgraph_process_directory):
	#print mixing_angle_over_pi_half, gluon1_lv, gluon2_lv, higgs_lv, madgraph_param_card, madgraph_process_directory
	
	cos_mixing_angle = math.cos(mixing_angle_over_pi_half * math.pi / 2.0)
	
	# read param_card and modify it in a temporary file
	madgraph_param_card_content = ""
	with open(madgraph_param_card) as madgraph_param_card_file:
		madgraph_param_card_content = madgraph_param_card_file.read().rstrip("\n")
	
	tmp_param_card_filename = None
	with tempfile.NamedTemporaryFile(prefix="param_card_", suffix=os.path.splitext(madgraph_param_card)[-1], delete=False) as tmp_param_card_file:
		tmp_param_card_filename = tmp_param_card_file.name
		tmp_param_card_file.write(string.Template(madgraph_param_card_content).safe_substitute(cosa=str(cos_mixing_angle)))
	
	
	momentum_particles = zip(gluon1_lv, gluon2_lv, higgs_lv) # list of 4-momenta of the particles
	alphas, mu = 0.118, 0
	loop = False
	
	sys.path.insert(0, madgraph_process_directory)
	ME = __import__("matrix2py")
	sys.path.pop(0)
	
	os.chdir(madgraph_process_directory) # change to subprocess directory
	ME.initialise(tmp_param_card_filename)
	
	matrix_element_squared = ME.get_me(momentum_particles, alphas, 0) # if not loop else ME.get_me(momentum_particles, alphas, mu, -1)[0]
	
	# clean up
	os.remove(tmp_param_card_filename)
	
	print matrix_element_squared, cos_mixing_angle
	return matrix_element_squared

