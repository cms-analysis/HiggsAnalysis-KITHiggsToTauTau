# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib
import math

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools


class CPHypotheses(analysisbase.AnalysisBase):
	"""Construct any CP hypothesis from three different hypotheses."""
	# https://indico.cern.ch/event/608147/contributions/2830241/attachments/1577687/2492186/presentation_tmuller.pdf

	def modify_argument_parser(self, parser, args):
		super(CPHypotheses, self).modify_argument_parser(parser, args)

		self.cp_hypotheses_options = parser.add_argument_group("{} options".format(self.name()))
		self.cp_hypotheses_options.add_argument(
				"--cp-scalar-nicks", nargs="+",
				help="Nick names for the scalar (CP even) histograms"
		)
		self.cp_hypotheses_options.add_argument(
				"--cp-pseudoscalar-nicks", nargs="+",
				help="Nick names for the pseudoscalar (CP odd) histograms"
		)
		self.cp_hypotheses_options.add_argument(
				"--cp-violation-nicks", nargs="+",
				help="Nick names for the CP violating (CP mixing) histograms"
		)
		self.cp_hypotheses_options.add_argument(
				"--cp-violation-scalar-couplings", nargs="+", type=float, default=[1.0],
				help="Scalar coupling components of the CP violating inputs"
		)
		self.cp_hypotheses_options.add_argument(
				"--cp-violation-pseudoscalar-couplings", nargs="+", type=float, default=[1.0],
				help="Pseudoscalar coupling components of the CP violating inputs"
		)
		self.cp_hypotheses_options.add_argument(
				"--cp-mixing-angles", nargs="+",
				help="CP mixing angles in units of pi/2 (whitespace separated)."
		)
		self.cp_hypotheses_options.add_argument(
				"--cp-result-nicks", nargs="+",
				help="Nick names for the resulting sum histograms (without mixing angle label)."
		)

	def prepare_args(self, parser, plotData):
		super(CPHypotheses, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["cp_scalar_nicks", "cp_pseudoscalar_nicks", "cp_violation_nicks", "cp_violation_scalar_couplings", "cp_violation_pseudoscalar_couplings", "cp_mixing_angles", "cp_result_nicks"])
		
		for index, (cp_scalar_nick, cp_pseudoscalar_nick, cp_violation_nick, cp_violation_scalar_coupling, cp_violation_pseudoscalar_coupling, cp_mixing_angles, cp_result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["cp_scalar_nicks", "cp_pseudoscalar_nicks", "cp_violation_nicks", "cp_violation_scalar_couplings", "cp_violation_pseudoscalar_couplings", "cp_mixing_angles", "cp_result_nicks"]]
		)):
			cp_mixing_angles_over_pi_half = [float(angle) for angle in cp_mixing_angles.split()]
			plotData.plotdict["cp_mixing_angles"][index] = [angle*math.pi/2.0 for angle in cp_mixing_angles_over_pi_half]
			
			if cp_result_nick is None:
				cp_result_nick = "cp_" + ("_".join([cp_scalar_nick, cp_pseudoscalar_nick, cp_violation_nick]))
			cp_result_nicks = [cp_result_nick+"_{angle:03d}".format(angle=int(round(angle*100.0, 0))) for angle in cp_mixing_angles_over_pi_half]
			plotData.plotdict["cp_result_nicks"][index] = cp_result_nicks
			for tmp_cp_result_nick in cp_result_nicks[::-1]:
				if not tmp_cp_result_nick in plotData.plotdict["nicks"]:
					plotData.plotdict["nicks"].insert(
							max([plotData.plotdict["nicks"].index(nick) for nick in [cp_scalar_nick, cp_pseudoscalar_nick, cp_violation_nick]])+1,
							tmp_cp_result_nick
					)

	def run(self, plotData=None):
		super(CPHypotheses, self).run(plotData)
		
		for index, (cp_scalar_nick, cp_pseudoscalar_nick, cp_violation_nick, cp_violation_scalar_coupling, cp_violation_pseudoscalar_coupling, cp_mixing_angles, cp_result_nicks) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["cp_scalar_nicks", "cp_pseudoscalar_nicks", "cp_violation_nicks", "cp_violation_scalar_couplings", "cp_violation_pseudoscalar_couplings", "cp_mixing_angles", "cp_result_nicks"]]
		)):
			cp_scalar_histogram = plotData.plotdict["root_objects"][cp_scalar_nick]
			cp_pseudoscalar_histogram = plotData.plotdict["root_objects"][cp_pseudoscalar_nick]
			cp_violating_histogram = plotData.plotdict["root_objects"][cp_violation_nick]
			
			a_old = cp_violation_scalar_coupling
			b_old = cp_violation_pseudoscalar_coupling
			
			for cp_mixing_angle, cp_result_nick in zip(cp_mixing_angles, cp_result_nicks):
				new_name = "cp_hypotheses_"+hashlib.md5("_".join([str(item) for item in [cp_scalar_nick, cp_pseudoscalar_nick, cp_violation_nick, cp_violation_scalar_coupling, cp_violation_pseudoscalar_coupling, cp_mixing_angle, cp_result_nick]])).hexdigest()
				cp_result_histogram = cp_scalar_histogram.Clone(new_name)
				
				a_new = math.cos(cp_mixing_angle)
				b_new = math.sin(cp_mixing_angle)
				
				scalar_scaling = a_new*a_new - a_new*b_new*a_old/b_old
				pseudoscalar_scaling = b_new*b_new - a_new*b_new*b_old/a_old
				violating_scaling = a_new*b_new/(a_old*b_old)
				
				log.debug("")
				log.debug("CPHypotheses: {result} = ({a_new}*{a_new} - {a_new}*{b_new}*{a_old}/{b_old}) * {scalar} + ({b_new}*{b_new} - {a_new}*{b_new}*{b_old}/{a_old}) * {pseudoscalar} + ({a_new}*{b_new}/({a_old}*{b_old})) * {violating}".format(scalar=cp_scalar_nick, pseudoscalar=cp_pseudoscalar_nick, violating=cp_violation_nick, result=cp_result_nick, a_old=a_old, b_old=b_old, a_new=a_new, b_new=b_new))
				log.debug("              {result} = {scalar_scaling} * {scalar} + {pseudoscalar_scaling} * {pseudoscalar} + {violating_scaling} * {violating}".format(scalar=cp_scalar_nick, pseudoscalar=cp_pseudoscalar_nick, violating=cp_violation_nick, result=cp_result_nick, scalar_scaling=scalar_scaling, pseudoscalar_scaling=pseudoscalar_scaling, violating_scaling=violating_scaling))
				
				cp_result_histogram.Scale(scalar_scaling)
				cp_result_histogram.Add(cp_pseudoscalar_histogram, pseudoscalar_scaling)
				cp_result_histogram.Add(cp_violating_histogram, violating_scaling)
				
				plotData.plotdict["root_objects"][cp_result_nick] = cp_result_histogram

