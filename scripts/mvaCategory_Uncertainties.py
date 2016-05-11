#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re
import Artus.Utility.jsonTools as jsonTools
import sys
import glob
import itertools
import ROOT
from string import strip

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Calculate lnN uncertainty from integral values of categories and their shifts",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-file", required=True, nargs="+",
						help="File with integral values, give as many files as there are categories (mt_Integrals.txt)")
	parser.add_argument("-b", "--bdt-names", nargs = "+", required=True,
						help="names of all bdts used for basic categorization (bkg,mixed,signal)")
	parser.add_argument("--vbfs", nargs = "+", default=[],
						help="name of the vbf-tagges [Default: %(default)s]")
	parser.add_argument("-c", "--channel", default=["mt"], nargs="+",
						help="Channels. Default %(default)s")
	parser.add_argument("-o", "--output-path",
							default="./",
							help="Output path, files will be named Reg_BDT.txt and VBF_BDT.txt. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	#Channel = args.channel
	#full_path = os.path.expandvars(args.input_file)
	#o_path = os.path.expandvars(args.output_path)
	##path, filename = os.path.split(full_path)
	#integral_dict = {}
	#with open(full_path, "r") as integral_file:
		#for line in integral_file:
			#category, value = map(strip, line.split(": "))
			#integral_dict[category] = float(value)
	##jsonTools.JsonDict(integral_dict).save(os.path.join(path, "ReadInIntegrals.json"), indent=4)
	o_path = os.path.expandvars(args.output_path)

	reg_unc_dict = {}
	vbf_unc_dict = {}
	for Channel, infile in zip(args.channel, args.input_file):
		full_path = os.path.expandvars(infile)
		#path, filename = os.path.split(full_path)
		integral_dict = {}
		with open(full_path, "r") as integral_file:
			for line in integral_file:
				category, value = map(strip, line.split(": "))
				integral_dict[category] = float(value)
		for reg_bdt_name in args.bdt_names:
			for cat in ["bkg", "mixed", "signal"]:
				name = "{ch}_{reg_bdt}_{cat}".format(ch=Channel, reg_bdt=reg_bdt_name, cat=cat)
				up = integral_dict[name+"_up"]
				nom = integral_dict[name]
				down = integral_dict[name+"_down"]
				reg_unc_dict[name] = (down/nom, up/nom)
			for vbf_tagger in args.vbfs:
				for tag in ("tagged", "not_tagged"):
					name = "{ch}_{tagger}_{reg_bdt}_{tag}_signal".format(ch=Channel, tagger=vbf_tagger, reg_bdt=reg_bdt_name, tag=tag)
					up_up = integral_dict[name+"_up_up"]
					up_nom = integral_dict[name+"_up_nom"]
					nom_up = integral_dict[name+"_nom_up"]
					nom_nom = integral_dict[name]
					nom_down = integral_dict[name+"_nom_down"]
					down_nom = integral_dict[name+"_down_nom"]
					down_down = integral_dict[name+"_down_down"]
					uncorr_vbf = [nom_down/nom_nom, nom_up/nom_nom]
					uncorr_reg = (down_nom/nom_nom, up_nom/nom_nom)
					tot_unc = (down_down/nom_nom-1, up_up/nom_nom-1)
					corr_reg = [0, 0]
					#abs_reg = (corr_reg[0]), corr_reg[1]))
					try:
						intermediate_reg = ((tot_unc[0]**2-(uncorr_vbf[0]-1.)**2)**0.5, (tot_unc[1]**2-(uncorr_vbf[1]-1.)**2)**0.5)
						log.info(intermediate_reg)
						if tot_unc[0] < 0.0:
							corr_reg[0] = 1-intermediate_reg[0]
						else:
							corr_reg[0] = 1+intermediate_reg[0]
						if tot_unc[1] < 0.0:
							corr_reg[1] = 1-intermediate_reg[1]
						else:
							corr_reg[1] = 1+intermediate_reg[1]
					except ValueError:
						log.fatal("negative square root: %s"%name)
						log.info(abs_reg)
						log.info(uncorr_reg)
						log.info(abs_vbf)
						log.info(uncorr_vbf)
					for i,val in enumerate(corr_reg):
						if val == 0.0:
							corr_reg[i]=0.01
					for i,val in enumerate(uncorr_vbf):
						if val == 0.0:
							uncorr_vbf[i]=0.01
					reg_unc_dict[name] = corr_reg
					vbf_unc_dict[name] = uncorr_vbf
	jsonTools.JsonDict(reg_unc_dict).save(os.path.join(o_path, "Reg_BDT.txt"), indent=4)
	jsonTools.JsonDict(vbf_unc_dict).save(os.path.join(o_path, "VBF_BDT.txt"), indent=4)


