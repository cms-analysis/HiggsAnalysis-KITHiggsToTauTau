#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import argparse
import numpy as np
import matrix2py as ME
import math
import string
import tempfile


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
	
		
	#infile = os.path.abspath(args.infile)
	#params = str(params_card)
	#outfile = os.path.abspath(output)
	loop = False 

	os.chdir(str(madgraph_process_directory))	# change to subprocess directory

	#p = np.genfromtxt(infile,skip_header=1,unpack=True)				# read momenta (phase-space point) skipping first line of the input file

	


	momentum_particles=[gluon1_lv, gluon2_lv, higgs_lv] 	# list of 4-momenta of the particles 

	#print momentum_particles
	momentum_particles=zip(*momentum_particles)
	#print momentum_particles
	#alphas, mu = np.genfromtxt(infile, skip_footer=p.shape[1])		# read alpha_strong and mu (needed for loop-ME call) from fist line of the input file
	alphas, mu = 0.118, 0

	ME.initialise(tmp_param_card_filename)


	# TODO calculations
	matrix_element_squared = ME.get_me(momentum_particles, alphas, 0)
	
	# clean up
	os.remove(tmp_param_card_filename)
	
	print matrix_element_squared, cos_mixing_angle
	return matrix_element_squared

	'''
	# calculate squared ME:
	if loop:
		me2 = ME.get_me(p, alphas, mu, -1)[0]
	else:
		me2 = ME.get_me(p, alphas, 0)
	print me2
	
	# write squared ME to output file
	outfile = open(outfile,'w')
	outfile.write(str(me2)+"\n")
	outfile.close()	'''

