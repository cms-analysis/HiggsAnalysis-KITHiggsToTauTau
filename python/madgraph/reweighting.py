#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
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
	
	# TODO calculations
	matrix_element_squared = 1.0
	
	# clean up
	os.remove(tmp_param_card_filename)
	
	return matrix_element_squared

