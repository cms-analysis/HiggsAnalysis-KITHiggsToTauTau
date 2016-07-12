#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import re

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs


def parse_table(table_file):
	xsecs_vs_masses = {}
	with open(os.path.expandvars(table_file)) as table:
		for line in table:
			match = re.match("(?P<mass>\d*.\d*)\s*(?P<xsec>\d*.\d*)\s*.*", line)
			if match:
				xsecs_vs_masses[match.groupdict()["mass"]] = match.groupdict()["xsec"]
	return xsecs_vs_masses


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Print signal cross sections.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("--ggh-table", help="XSxBR Table for ggH process. [Default: %(default)s]",
	                    default="$CMSSW_BASE/src/CombineHarvester/CombineTools/input/xsecs_brs/ggH_8TeV_YR3.txt")
	parser.add_argument("--qqh-table", help="XSxBR Table for qqH process. [Default: %(default)s]",
	                    default="$CMSSW_BASE/src/CombineHarvester/CombineTools/input/xsecs_brs/qqH_8TeV_YR3.txt")
	parser.add_argument("--wh-table", help="XSxBR Table for WH process. [Default: %(default)s]",
	                    default="$CMSSW_BASE/src/CombineHarvester/CombineTools/input/xsecs_brs/WH_8TeV_YR3.txt")
	parser.add_argument("--zh-table", help="XSxBR Table for ZH process. [Default: %(default)s]",
	                    default="$CMSSW_BASE/src/CombineHarvester/CombineTools/input/xsecs_brs/ZH_8TeV_YR3.txt")
	parser.add_argument("--tth-table", help="XSxBR Table for ttH process. [Default: %(default)s]",
	                    default=None)
	
	parser.add_argument("--ggh-nick", help="Nickname for ggH sample. [Default: %(default)s]",
	                    default="SM_GluGluToHToTauTau_M_%d_powheg_pythia_8TeV")
	parser.add_argument("--qqh-nick", help="Nickname for qqH sample. [Default: %(default)s]",
	                    default="SM_VBFHToTauTau_M_%d_powheg_pythia_8TeV")
	parser.add_argument("--wh-zh-tth-nick", help="Nickname for (WH+ZH+ttH) sample. [Default: %(default)s]",
	                    default="SM_WH_ZH_TTH_HToTauTau_M_%d_powheg_pythia_8TeV")
	                    
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=[str(m) for m in xrange(90, 161, 5)],
	                    help="Higgs masses. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.higgs_masses = parseArgs(args.higgs_masses)
	
	ggH_xsecs = parse_table(args.ggh_table) if args.ggh_table else {}
	for mass in args.higgs_masses:
		if str(float(mass)) in ggH_xsecs:
			log.info(("\"" + args.ggh_nick + "\" : %f,") % (int(mass), float(ggH_xsecs[str(float(mass))])))
	
	qqH_xsecs = parse_table(args.qqh_table) if args.qqh_table else {}
	for mass in args.higgs_masses:
		if str(float(mass)) in qqH_xsecs:
			log.info(("\"" + args.qqh_nick + "\" : %f,") % (int(mass), float(qqH_xsecs[str(float(mass))])))
	
	WH_xsecs = parse_table(args.wh_table) if args.wh_table else {}
	ZH_xsecs = parse_table(args.zh_table) if args.zh_table else {}
	ttH_xsecs = parse_table(args.tth_table) if args.tth_table else {}
	for mass in args.higgs_masses:
		WH_ZH_ttH_xsec = 0.0
		if str(float(mass)) in WH_xsecs:
			WH_ZH_ttH_xsec += float(WH_xsecs[str(float(mass))])
		if str(float(mass)) in ZH_xsecs:
			WH_ZH_ttH_xsec += float(ZH_xsecs[str(float(mass))])
		if str(float(mass)) in ttH_xsecs:
			WH_ZH_ttH_xsec += float(ttH_xsecs[str(float(mass))])
		if WH_ZH_ttH_xsec > 0:
			log.info(("\"" + args.wh_zh_tth_nick + "\" : %f,") % (int(mass), WH_ZH_ttH_xsec))

