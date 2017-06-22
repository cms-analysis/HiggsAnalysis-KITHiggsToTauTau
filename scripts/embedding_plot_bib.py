#!/usr/bin/env python

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
from HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib import *

def plot_root_variable(channel=['mt'],variable='pt_1',x_bins = "30,0,120",decay_mode="all",isocut=True,xlabel=''):
	
	if decay_mode=="all":
		decay_weight=""
	elif decay_mode=="0":
		decay_weight="(decayMode_2==0)*"
	elif decay_mode=="1":
		decay_weight="(decayMode_2==1)*"
	elif decay_mode=="10":
		decay_weight="(decayMode_2==10)*"
	if isocut:
		isocut="(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*"
	else:
		isocut="(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*"
	stitching_weight = "(((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.25449124172134e-6) + ((genbosonmass >= 150.0 && npartons == 1)*1.17272893569016e-6) + ((genbosonmass >= 150.0 && npartons == 2)*1.17926755938344e-6) + ((genbosonmass >= 150.0 && npartons == 3)*1.18242445124698e-6) + ((genbosonmass >= 150.0 && npartons == 4)*1.16077776187804e-6)+((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*1.15592e-4) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.5569730365e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.68069486078868e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.74717616341537e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.3697397756176e-5)+((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
	#(againstMuonTight3_2 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*
	stitching_weight = "(1.0)"
	#(againstMuonTight3_2 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*
	selection_weight_mt = decay_weight+isocut+"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.15)*((q_1*q_2)<0.0)"

	selection_weight_et = decay_weight+isocut+"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronTightMVA6_2 > 0.5)*(mt_1<40.0)*(iso_1 < 0.1)*((q_1*q_2)<0.0)"

	selection_weight_tt = decay_weight+isocut+"(pt_1 > 42.0 && pt_2 > 42.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*((q_1*q_2)<0.0)"

	#selection_weight_em = "(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"
	selection_weight_em = decay_weight+"(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"
	mt_emb_weight="(gen_match_2 == 5)*(((((1.0)))))*((((run >= 272007) && (run < 275657))*3768958.+((run >= 275657) && (run < 276315))*1583897.+((run >= 276315) && (run < 276831))*2570815.+((run >= 276831) && (run < 277772))*2514506.+((run >= 277772) && (run < 278820))*1879819.+((run >= 278820) && (run < 280919))*5008746.+((run >= 280919) && (run < 284045))*6367665.)/(3768958.+1583897.+2570815.+2514506.+1879819.+5008746.+6367665.))*(eventWeight)*((eventWeight<1.0))*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singlemuon == 1)*(againstElectronVLooseMVA6_2 > 0.5)*(mt_1<40.0)*(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*zPtReweightWeight"
	mt_dy_weight="1.0"#(gen_match_2 == 5)*(((((1.0)))))*((((run >= 272007) && (run < 275657))*3768958.+((run >= 275657) && (run < 276315))*1583897.+((run >= 276315) && (run < 276831))*2570815.+((run >= 276831) && (run < 277772))*2514506.+((run >= 277772) && (run < 278820))*1879819.+((run >= 278820) && (run < 280919))*5008746.+((run >= 280919) && (run < 284045))*6367665.)/(3768958.+1583897.+2570815.+2514506.+1879819.+5008746.+6367665.))*(eventWeight)*((eventWeight<1.0))*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singlemuon == 1)*(againstElectronVLooseMVA6_2 > 0.5)*(mt_1<40.0)*(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*zPtReweightWeight"
	
	genmatching_weight_xt = "*(gen_match_2 == 5)"
	genmatching_weight_tt = "*(gen_match_1 == 5 && gen_match_2 == 5)"
	genmatching_weight_em = "*(gen_match_1 > 2 && gen_match_2 > 3)"
	visibleMassMuTau = pltcl.single_plot(
		name = variable+"MuTau_decayMode "+decay_mode,
		title = "#mu#tau_{h}: shape comparison. decayMode "+decay_mode,
		x_expression = [variable,variable],
		normalized_to_hist1 = True,
		x_bins = x_bins,
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		x_label = xlabel,
		weight = selection_weight_mt+"*eventWeight*(eventWeight<1.0)*"+stitching_weight+genmatching_weight_xt,#[mt_dy_weight,mt_dy_weight,mt_emb_weight],
		#~ weight =  stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_mt,
		y_label = "Events per bin width",
		#y_lims = [0,0.058],
		plot_type = "absolute",
		legend = [0.53,0.44,0.92,0.88],
		subplot_denominator = 0,
		subplot_numerators = [1,2],
		output_dir=output_dir+'/mt/decayMode'+decay_mode,
		wwwfolder = web_dir,
		y_subplot_lims = [0.6,1.4],
		y_subplot_label = "Ratio",
		print_infos = True,
		plotlines = [DYFileMuTauFile, DYFileMuTauSmeared, EmbeddingMuTauFileNominal]
	)        

	if 'mt' in channel:
		configs.extend(visibleMassMuTau.return_json_with_changed_x_and_weight(x_expressions = [variable]))
	if variable=='pt_1':
		xlabel='Electron p_{T} / GeV'
	visibleMassElTau = visibleMassMuTau.clone(
		name = variable+"visibleMassElTau "+decay_mode,
		x_label = xlabel,
		weight = ["(gen_match_2 == 5)*(((((1.0)))))*((((run >= 272007) && (run < 275657))*3768958.+((run >= 275657) && (run < 276315))*1583897.+((run >= 276315) && (run < 276831))*2570815.+((run >= 276831) && (run < 277772))*2514506.+((run >= 277772) && (run < 278820))*1879819.+((run >= 278820) && (run < 280919))*5008746.+((run >= 280919) && (run < 284045))*6367665.)/(3768958.+1583897.+2570815.+2514506.+1879819.+5008746.+6367665.))*(eventWeight)*((eventWeight<1.0))*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singleelectron == 1)*(againstElectronTightMVA6_2 > 0.5)*(mt_1<50.0)*(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.1)*((q_1*q_2)<0.0)*zPtReweightWeight",   "(gen_match_2 == 5)*(((((1.0)))))*(eventWeight)*((((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*3.95423374e-5) + ((genbosonmass >= 150.0 && npartons == 1)*1.27486147e-5) + ((genbosonmass >= 150.0 && npartons == 2)*1.3012785e-5) + ((genbosonmass >= 150.0 && npartons == 3)*1.33802133e-5) + ((genbosonmass >= 150.0 && npartons == 4)*1.09698723e-5)+((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*3.95423374e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.27486147e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.3012785e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.33802133e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.09698723e-5)+((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight))*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singleelectron == 1)*(againstElectronTightMVA6_2 > 0.5)*(mt_1<50.0)*(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.1)*((q_1*q_2)<0.0)*zPtReweightWeight"],
		output_dir=output_dir+'/et/decayMode'+decay_mode,
		title = "e#tau_{h}: shape comparison  decayMode "+decay_mode,
		#~ weight = stitching_weight + genmatching_weight_xt + "*generatorWeight*(generatorWeight<=1)*" + selection_weight_et,
		plotlines = [EmbeddingElTauFileNominal, DYFileElTauFile]
	)
	if 'et' in channel:
		configs.extend(visibleMassElTau.return_json_with_changed_x_and_weight(x_expressions = [variable]))
	visibleMassTauTau = visibleMassMuTau.clone(
		name = variable+"visibleMassTauTau "+decay_mode,
		title = "#tau_{h}#tau_{h}: shape comparison}  decayMode "+decay_mode,
		x_bins = "11,30,250",
		y_lims = [0,0.026],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + "*generatorWeight*(generatorWeight<=1)*" + selection_weight_tt,
		plotlines = [EmbeddingTauTauFileNominal, EmbeddingTauTauFileUp, EmbeddingTauTauFileDown, DYFileTauTauFile]
	)

	#configs.extend(visibleMassTauTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassElMu = visibleMassMuTau.clone(
		name = "visibleMassElMu",
		title = "#scale[1.3]{e#mu: shape comparison}",
		subplot_denominator = 0,
		x_bins = "30,30,120",
		y_lims = [0,0.062],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + genmatching_weight_em + "*eventWeight*(eventWeight<=1)*" + selection_weight_em,
		plotlines = [EmbeddingElMuFileNominal, EmbeddingElMuFileUp, EmbeddingElMuFileDown, DYFileElMuFile, HToTauTauElMuFile]
	)

	#configs.extend(visibleMassElMu.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

def plot_iso_variable(channel=['mt'],variable='pt_1',x_bins = "30,0,120",decay_mode="all",isocut=True):
	
	if decay_mode=="all":
		decay_weight=""
	elif decay_mode=="0":
		decay_weight="(decayMode_2==0)*"
	elif decay_mode=="1":
		decay_weight="(decayMode_2==1)*"
	elif decay_mode=="10":
		decay_weight="(decayMode_2==10)*"
	if isocut:
		isocut="(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*"
	else:
		isocut=""
	#stitching_weight = "(((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.25449124172134e-6) + ((genbosonmass >= 150.0 && npartons == 1)*1.17272893569016e-6) + ((genbosonmass >= 150.0 && npartons == 2)*1.17926755938344e-6) + ((genbosonmass >= 150.0 && npartons == 3)*1.18242445124698e-6) + ((genbosonmass >= 150.0 && npartons == 4)*1.16077776187804e-6)+((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*1.15592e-4) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.5569730365e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.68069486078868e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.74717616341537e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.3697397756176e-5)+((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
	
	stitching_weight = "(1.0)"
	
	selection_weight_mt = decay_weight+isocut+"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(mt_1<40.0)*(iso_1 < 0.15)*((q_1*q_2)<0.0)"

	selection_weight_et = decay_weight+isocut+"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronTightMVA6_2 > 0.5)*(mt_1<40.0)*(iso_1 < 0.1)*((q_1*q_2)<0.0)"

	selection_weight_tt = decay_weight+isocut+"(pt_1 > 42.0 && pt_2 > 42.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*((q_1*q_2)<0.0)"

	#selection_weight_em = "(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"
	selection_weight_em = decay_weight+"(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"

	genmatching_weight_xt = "*(gen_match_2 == 5)"
	genmatching_weight_tt = "*(gen_match_1 == 5 && gen_match_2 == 5)"
	genmatching_weight_em = "*(gen_match_1 > 2 && gen_match_2 > 3)"
	
	visibleMassMuTau = pltcl.single_plot(
		name = variable+"MuTau_decayMode "+decay_mode,
		title = "#mu#tau_{h}: shape comparison. decayMode "+decay_mode,
		x_expression = variable,
		normalized_to_hist1 = True,
		x_bins = x_bins,
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		x_label = variable,
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_mt,
		y_label = "Events per bin width",
		#y_lims = [0,0.058],
		plot_type = "absolute",
		legend = [0.53,0.44,0.92,0.88],
		subplot_denominator = 0,
		subplot_numerators = [1],
		output_dir=output_dir+'/decayMode'+decay_mode,
		wwwfolder = web_dir,
		y_subplot_lims = [0.5,1.5],
		y_subplot_label = "Ratio",
		print_infos = True,
		plotlines = [EmbeddingMuTauFileNominal, DYFileISOMuTauFile]
	)

	configs.extend(visibleMassMuTau.return_json_with_changed_x_and_weight(x_expressions = [variable]))

	visibleMassElTau = visibleMassMuTau.clone(
		name = variable+"visibleMassElTau"+decay_mode,
		title = "#scale[1.3]{e#tau_{h}: shape comparison} decayMode "+decay_mode,
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_et,
		plotlines = [EmbeddingElTauFileNominal, EmbeddingElTauFileUp, EmbeddingElTauFileDown, DYFileElTauFile, HToTauTauElTauFile]
	)

	#configs.extend(visibleMassElTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassTauTau = visibleMassMuTau.clone(
		name = "visibleMassTauTau",
		title = "#scale[1.3]{#tau_{h}#tau_{h}: shape comparison}",
		x_bins = "11,30,250",
		y_lims = [0,0.026],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + "*eventWeight*(eventWeight<=1)*" + selection_weight_tt,
		plotlines = [EmbeddingTauTauFileNominal, EmbeddingTauTauFileUp, EmbeddingTauTauFileDown, DYFileTauTauFile, HToTauTauTauTauFile]
	)

	#configs.extend(visibleMassTauTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassElMu = visibleMassMuTau.clone(
		name = "visibleMassElMu",
		title = "#scale[1.3]{e#mu: shape comparison}",
		subplot_denominator = 0,
		x_bins = "30,30,120",
		y_lims = [0,0.062],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + genmatching_weight_em + "*eventWeight*(eventWeight<=1)*" + selection_weight_em,
		plotlines = [EmbeddingElMuFileNominal, EmbeddingElMuFileUp, EmbeddingElMuFileDown, DYFileElMuFile, HToTauTauElMuFile]
	)

	#configs.extend(visibleMassElMu.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

def default_plot_root_variable(channel=['mt'],variable='pt_1'):
	stitching_weight = "(((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.25449124172134e-6) + ((genbosonmass >= 150.0 && npartons == 1)*1.17272893569016e-6) + ((genbosonmass >= 150.0 && npartons == 2)*1.17926755938344e-6) + ((genbosonmass >= 150.0 && npartons == 3)*1.18242445124698e-6) + ((genbosonmass >= 150.0 && npartons == 4)*1.16077776187804e-6)+((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*1.15592e-4) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.5569730365e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.68069486078868e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.74717616341537e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.3697397756176e-5)+((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"

	selection_weight_mt = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(mt_1<40.0)*(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.15)*((q_1*q_2)<0.0)"

	selection_weight_et = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronTightMVA6_2 > 0.5)*(mt_1<40.0)*(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.1)*((q_1*q_2)<0.0)"

	selection_weight_tt = "(pt_1 > 42.0 && pt_2 > 42.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((q_1*q_2)<0.0)"

	#selection_weight_em = "(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"
	selection_weight_em = "(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"

	genmatching_weight_xt = "*(gen_match_2 == 5)"
	genmatching_weight_tt = "*(gen_match_1 == 5 && gen_match_2 == 5)"
	genmatching_weight_em = "*(gen_match_1 > 2 && gen_match_2 > 3)"

	visibleMassMuTau = pltcl.single_plot(
		name = variable+"MuTau",
		title = "#scale[1.3]{#mu#tau_{h}: shape comparison}",
		x_expression = variable,
		normalized_to_hist1 = True,
	#	x_bins = "30,30,120",
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		x_label = variable,
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_mt,
		y_label = "Events per bin width",
		#y_lims = [0,0.058],
		plot_type = "absolute",
		legend = [0.53,0.44,0.92,0.88],
		subplot_denominator = 0,
		subplot_numerators = [1],
		output_dir=output_dir,
		wwwfolder = web_dir,
		y_subplot_lims = [0.5,1.5],
		y_subplot_label = "Ratio",
		print_infos = True,
		#plotlines = [EmbeddingMuTauFileNominal, DYFileMuTauFile]
		plotlines =[DYPrefitShape,EmbeddingPrefitShape]
	)

	configs.extend(visibleMassMuTau.return_json_with_changed_x_and_weight(x_expressions = [variable]))

	visibleMassElTau = visibleMassMuTau.clone(
		name = "PT1 comparison",
		title = "e#tau_{h}: PT comparison",
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_et,
		plotlines = [EmbeddingElTauFileNominal, DYFileElTauFile]
	)

	#~ configs.extend(visibleMassElTau.return_json_with_changed_x_and_weight(x_expressions = [variable]))

	visibleMassTauTau = visibleMassMuTau.clone(
		name = "visibleMassTauTau",
		title = "#scale[1.3]{#tau_{h}#tau_{h}: shape comparison}",
		x_bins = "11,30,250",
		y_lims = [0,0.026],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + "*eventWeight*(eventWeight<=1)*" + selection_weight_tt,
		plotlines = [EmbeddingTauTauFileNominal, EmbeddingTauTauFileUp, EmbeddingTauTauFileDown, DYFileTauTauFile, HToTauTauTauTauFile]
	)

	#configs.extend(visibleMassTauTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassElMu = visibleMassMuTau.clone(
		name = "visibleMassElMu",
		title = "#scale[1.3]{e#mu: shape comparison}",
		subplot_denominator = 0,
		x_bins = "30,30,120",
		y_lims = [0,0.062],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + genmatching_weight_em + "*eventWeight*(eventWeight<=1)*" + selection_weight_em,
		plotlines = [EmbeddingElMuFileNominal, EmbeddingElMuFileUp, EmbeddingElMuFileDown, DYFileElMuFile, HToTauTauElMuFile]
	)
		#configs.extend(visibleMassElMu.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

def plot_VV_variable(channel=['mt'],variable='pt_1',x_bins = "30,0,120",decay_mode="all",isocut=True):
	
	if decay_mode=="all":
		decay_weight=""
	elif decay_mode=="0":
		decay_weight="(decayMode_2==0)*"
	elif decay_mode=="1":
		decay_weight="(decayMode_2==1)*"
	elif decay_mode=="10":
		decay_weight="(decayMode_2==10)*"
	if isocut:
		isocut="(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*"
	else:
		isocut=""
	#stitching_weight = "(((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.25449124172134e-6) + ((genbosonmass >= 150.0 && npartons == 1)*1.17272893569016e-6) + ((genbosonmass >= 150.0 && npartons == 2)*1.17926755938344e-6) + ((genbosonmass >= 150.0 && npartons == 3)*1.18242445124698e-6) + ((genbosonmass >= 150.0 && npartons == 4)*1.16077776187804e-6)+((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*1.15592e-4) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.5569730365e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.68069486078868e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.74717616341537e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.3697397756176e-5)+((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
	
	stitching_weight = "(1.0)"
	
	selection_weight_mt = decay_weight+isocut+"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(mt_1<40.0)*(iso_1 < 0.15)*((q_1*q_2)<0.0)"

	selection_weight_et = decay_weight+isocut+"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronTightMVA6_2 > 0.5)*(mt_1<40.0)*(iso_1 < 0.1)*((q_1*q_2)<0.0)"

	selection_weight_tt = decay_weight+isocut+"(pt_1 > 42.0 && pt_2 > 42.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*((q_1*q_2)<0.0)"

	#selection_weight_em = "(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"
	selection_weight_em = decay_weight+"(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"

	genmatching_weight_xt = "*(gen_match_2 == 5)"
	genmatching_weight_tt = "*(gen_match_1 == 5 && gen_match_2 == 5)"
	genmatching_weight_em = "*(gen_match_1 > 2 && gen_match_2 > 3)"
	
	visibleMassMuTau = pltcl.single_plot(
		name = variable+"MuTau_decayMode "+decay_mode,
		title = "#mu#tau_{h}: shape comparison. decayMode "+decay_mode,
		x_expression = variable,
		normalized_to_hist1 = True,
		x_bins = x_bins,
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		x_label = variable,
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_mt,
		y_label = "Events per bin width",
		#y_lims = [0,0.058],
		plot_type = "absolute",
		legend = [0.53,0.44,0.92,0.88],
		subplot_denominator = 0,
		subplot_numerators = [1],
		output_dir=output_dir+'/decayMode'+decay_mode,
		wwwfolder = web_dir,
		y_subplot_lims = [0.5,1.5],
		y_subplot_label = "Ratio",
		print_infos = True,
		plotlines = [VVFileMuTauFile, DYISOFileMuTauFile]
	)

	#configs.extend(visibleMassMuTau.return_json_with_changed_x_and_weight(x_expressions = [variable]))

	visibleMassElTau = visibleMassMuTau.clone(
		name = "visibleMassElTau",
		title = "#scale[1.3]{e#tau_{h}: shape comparison}",
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_et,
		plotlines = [EmbeddingElTauFileNominal, EmbeddingElTauFileUp, EmbeddingElTauFileDown, DYFileElTauFile, HToTauTauElTauFile]
	)

	configs.extend(visibleMassElTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassTauTau = visibleMassMuTau.clone(
		name = "visibleMassTauTau",
		title = "#scale[1.3]{#tau_{h}#tau_{h}: shape comparison}",
		x_bins = "11,30,250",
		y_lims = [0,0.026],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + "*eventWeight*(eventWeight<=1)*" + selection_weight_tt,
		plotlines = [EmbeddingTauTauFileNominal, EmbeddingTauTauFileUp, EmbeddingTauTauFileDown, DYFileTauTauFile, HToTauTauTauTauFile]
	)

	#configs.extend(visibleMassTauTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassElMu = visibleMassMuTau.clone(
		name = "visibleMassElMu",
		title = "#scale[1.3]{e#mu: shape comparison}",
		subplot_denominator = 0,
		x_bins = "30,30,120",
		y_lims = [0,0.062],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + genmatching_weight_em + "*eventWeight*(eventWeight<=1)*" + selection_weight_em,
		plotlines = [EmbeddingElMuFileNominal, EmbeddingElMuFileUp, EmbeddingElMuFileDown, DYFileElMuFile, HToTauTauElMuFile]
	)

	#configs.extend(visibleMassElMu.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

def ptflow_photon_histograms(binarea="[0.01,0.02]",peakwidth="10 GeV"):
	
	if binarea=="[0.01,0.02]":
		if peakwidth=="10 GeV":
			plotlines = [DoubleMuonSelectedPtFlowDistribution, DoubleMuonMirroredPtFlowDistribution, DoubleMuonRandomPtFlowDistribution, DoubleMuonEmbeddedPtFlowDistribution]
		elif peakwidth=="5 GeV":
			filepath="/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_5GeV/"
			plotlines = [DoubleMuonSelectedPtFlowDistribution5GeV, DoubleMuonMirroredPtFlowDistribution5GeV, DoubleMuonRandomPtFlowDistribution5GeV, DoubleMuonEmbeddedPtFlowDistribution5GeV]
	elif binarea=="[0.21,0.22]":
		filepath="/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_midbin_10GeV/"
		plotlines = [DoubleMuonSelectedPtFlowDistributionMid, DoubleMuonMirroredPtFlowDistributionMid, DoubleMuonRandomPtFlowDistributionMid, DoubleMuonEmbeddedPtFlowDistributionMid]
	ptflow_check_lMu_PPV = pltcl.single_plot(
	name = "ptflow_check_lMu_PPV",
	title = "#DeltaR in "+binarea+"; full region",
	x_expression = "PtFlow",
	x_bins = "40,0.,4.",
	normalized_by_binwidth = False,
	wwwfolder = web_dir,
	legend = data_embedded_mirrored_random_legend_upper_right,
	plot_type = "absolute",
	y_lims = [1,3e6],
	output_dir = output_dir,
	subplot_denominator = 0,
	subplot_numerators = [],
	y_subplot_lims = [0.85,1.15],
	y_subplot_label = "Ratio",
	y_label = "Events",
	x_label = "p_{T}-flow (photons) [GeV]",
	y_log = True,
	plotlines = plotlines
	)

	configs.extend(ptflow_check_lMu_PPV.return_json_with_changed_x_and_weight(
	x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_full"]
	))

	ptflow_check_lMu_PPV_peak = ptflow_check_lMu_PPV.clone(
		name = "ptflow_check_lMu_PPV_peak",
		legend = data_embedded_mirrored_random_legend_upper_right,
		title = "#DeltaR in "+binarea+"; peak region #pm ("+peakwidth+")",
		)

	configs.extend(ptflow_check_lMu_PPV_peak.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_peak"]
		))

	ptflow_check_lMu_PPV_sideband = ptflow_check_lMu_PPV.clone(
		name = "ptflow_check_lMu_PPV_sideband",
		legend = data_embedded_mirrored_random_legend_upper_right,
		title = "#DeltaR in "+binarea+"; sideband region ("+peakwidth+")",
		)

	configs.extend(ptflow_check_lMu_PPV_sideband.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_sideband"]
		))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Make embedding plots.",
									 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=False, default = ".",
						help="Input directory [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir", required=False, default = "plots",
						help="Output directory [Default: %(default)s]")
	parser.add_argument("--www", "--web-dir", required=False, default = "",
						help="Set www directory [Default: False]")
	parser.add_argument("-b","--binarea", required=False, default = "1",
						help="Toggle first (1) or middle (2) Delta R bin [Default: %(default)s]")
	parser.add_argument("-p","--peakwidth", required=False, default = "10",
						help="Toggle Z peak width between 10 and 5 GeV [Default: %(default)s]")
	parser.add_argument("-c","--channel", required=False, default = ['mt','et'], nargs="*", help="Select decay channel. [Default: %(default)s]")
	parser.add_argument("-d","--decaymode", required=False, default = "all", help="Select decay mode to plot data in. Options: all, 0 (1 prong no pi0), 1 (1 prong 1 pi0), 10 (3 prong no pi0), split (plot all three decay modes in different subdirs) [Default: %(default)s]")
	parser.add_argument("--no-iso-cut", required=False, action="store_true", default=False, help = "Set to remove Tau isolation cut (byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)")
	parser.add_argument("-n","--n-processes",required=False, default=1, help="Number of parallel processes. [Default: %(default)s]")
	parser.add_argument("-x","--quantities", required=False, default = None, nargs="*", help="Select quantities to plot. [Default: %(default)s]")
	parser.add_argument("--default", required=False, action="store_true", default=False, help = "Set to let HiggsPlotter take care of binning and skip custom configs.")

	args = parser.parse_args()
	logger.initLogger(args)
	configs = []
	isocut = not args.no_iso_cut
	decay_mode=str(args.decaymode)
	if decay_mode not in ["0","1","10","split","all"]:
		print "Decay mode "+decay_mode+" not supported. Options: all, 0, 1, 10 ,split"
		exit()
	web_dir = args.www
	output_dir = args.output_dir
	input_dir = args.input_dir
	peakwidth = args.peakwidth+" GeV"
	if args.binarea == "1":
		binarea="[0.01,0.02]"
	elif args.binarea == "2":
		binarea="[0.21,0.22]"


	data_trackcleaned_cleaned_legend = [0.43,0.60,0.96,0.85] 
	data_trackcleaned_cleaned_noratio_legend = [0.43,0.75,0.94,0.90]
	data_embedded_mirrored_cleaned_legend = [0.53,0.40,0.90,0.85]
	data_embedded_mirrored_legend = [0.53,0.50,0.90,0.85]
	data_embedded_mirrored_random_legend_upper_left = [0.21,0.55,0.60,0.90]
	data_embedded_mirrored_random_legend_upper_right = [0.52,0.55,0.91,0.90]
	data_embedded_mirrored_random_legend_lower_right = [0.52,0.20,0.91,0.55]
	data_embedded_mirrored_random_legend_lower_left = [0.21,0.20,0.60,0.55]

	### Vertex Refitting Check for Muon Embedding
	'''
	vtx_check_dx_MM = pltcl.single_plot(
		name = "vtx_check_dx_MM",
		x_expression = "vtx_dx",
		x_label = "#Deltax [cm]",
		y_lims = [0,500000],
		wwwfolder = web_dir
		title = "",
		plot_type = "absolute",
		plotlines = [vtx_corrected_MM],
	)

	configs.extend(vtx_check_dx_MM.return_json_with_changed_x_and_weight(
		x_expressions = ["vtx_dx"],
		))

	vtx_check_dy_MM = vtx_check_dx_MM.clone(
		name = "vtx_check_dy_MM",
		x_expression = "vtx_dy",
		x_label = "#Deltay [cm]"
	)

	configs.extend(vtx_check_dy_MM.return_json_with_changed_x_and_weight(
		x_expressions = ["vtx_dy"],
		))

	vtx_check_dz_MM = vtx_check_dx_MM.clone(
		name = "vtx_check_dz_MM",
		x_expression = "vtx_dz",
		y_lims = [0,350000],
		x_label = "#Deltaz [cm]"
	)

	configs.extend(vtx_check_dz_MM.return_json_with_changed_x_and_weight(
		x_expressions = ["vtx_dz"],
		))


	### Merging and Cleaning Check for Muon Embedding


	# Loose Electrons Merging
	merging_check_NE = pltcl.single_plot(
		name = "merging_check_NE",
		title = "electrons: loose ID",
		x_expression = "NLooseElectrons",
		y_lims = [10, 1000000000],
		x_bins = "3,0,3",
		normalized_by_binwidth = False,
		x_label = "N(electrons)",
		y_label = "Events",
		y_log = True,
		legend = data_embedded_mirrored_cleaned_legend,
		plot_type = "absolute",
		subplot_denominator = 0,
		subplot_numerators = [1,2,3],
		y_subplot_lims = [0.8,1.2],
		y_subplot_label = "Ratio",
		plotlines = [DoubleMuonSelected, DoubleMuonEmbedded, DoubleMuonMirrored, DoubleMuonCleaned]
	)

	configs.extend(merging_check_NE.return_json_with_changed_x_and_weight(
		x_expressions = ["NLooseElectrons"]
		))

	# Loose Electrons Cleaning
	cleaning_check_NE = merging_check_NE.clone(
		name = "cleaning_check_NE",
		legend = data_trackcleaned_cleaned_legend,
		subplot_numerators = [1,2],
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NE.return_json_with_changed_x_and_weight(
		x_expressions = ["NLooseElectrons"]
		))

	# Loose Electrons Cleaning without Vertex Criteria
	cleaning_check_NE_noVtx = merging_check_NE.clone(
		name = "cleaning_check_NE_noVtx",
		title = "electrons: loose ID without vertex criteria",
		legend = data_trackcleaned_cleaned_legend,
		subplot_numerators = [1,2],
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NE_noVtx.return_json_with_changed_x_and_weight(
		x_expressions = ["NLooseElectronsRelaxedVtxCriteria"]
		))

	# Particle Flow Electrons Merging
	merging_check_NPFE = merging_check_NE.clone(
		name = "merging_check_NPFE",
		title = "electrons: particle flow",
		x_bins = "7,0,7",
		y_subplot_lims = [0.7,1.3],
		x_expression = "NPFElectrons"
	)

	configs.extend(merging_check_NPFE.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFElectrons"]
		))

	# Particle Flow Electrons Cleaning
	cleaning_check_NPFE = merging_check_NPFE.clone(
		name = "cleaning_check_NPFE",
		subplot_numerators = [1,2],
		legend = data_trackcleaned_cleaned_legend,
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NPFE.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFElectrons"]
		))

	# Muons Merging
	merging_check_NMu = merging_check_NE.clone(
		name = "merging_check_NMu",
		title = "muons: global & particle flow",
		x_expression = "NEmbeddingMuons",
		x_bins = "7,0,7",
		x_label = "N(muons)",
		y_lims = [5,1000000000],
		legend = data_embedded_mirrored_legend,
		subplot_numerators = [1,2],
		y_subplot_lims = [0.9,1.1],
		plotlines = [DoubleMuonSelected, DoubleMuonEmbedded, DoubleMuonMirrored]
	)

	configs.extend(merging_check_NMu.return_json_with_changed_x_and_weight(
		x_expressions = ["NEmbeddingMuons"]
		))

	# Muons Cleaning
	cleaning_check_NMu = merging_check_NMu.clone(
		name = "cleaning_check_NMu",
		subplot_numerators = [],
		legend = data_trackcleaned_cleaned_noratio_legend,
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NMu.return_json_with_changed_x_and_weight(
		x_expressions = ["NEmbeddingMuons"]
		))

	# Particle Flow Muons Merging
	merging_check_NPFMu = merging_check_NMu.clone(
		name = "merging_check_NPFMu",
		title = "muons: particle flow",
		x_bins = "9,0,9",
		x_expression = "NPFMuons"
	)

	configs.extend(merging_check_NPFMu.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFMuons"]
		))

	# Particle Flow Muons Cleaning
	cleaning_check_NPFMu = merging_check_NPFMu.clone(
		name = "cleaning_check_NPFMu",
		legend = data_trackcleaned_cleaned_noratio_legend,
		subplot_numerators = [],
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NPFMu.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFMuons"]
		))

	merging_check_NPFC = merging_check_NE.clone(
		name = "merging_check_NPFC",
		x_expression = "NPFCandidates",
		x_bins = "20,300,2000",
		title = "",
		y_lims = [0,780000],
		y_log = False,
		y_subplot_lims = [0.95,1.05],
		x_label = "N(all)"
	)

	configs.extend(merging_check_NPFC.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFCandidates"]
		))

	cleaning_check_NPFC = merging_check_NPFC.clone(
		name = "cleaning_check_NPFC",
		y_lims = [0,580000],
		legend = data_trackcleaned_cleaned_legend,
		subplot_numerators = [1,2],
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NPFC.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFCandidates"]
		))	

	merging_check_NPFPh = merging_check_NE.clone(
		name = "merging_check_NPFPh",
		x_expression = "NPFPhotons",
		x_bins = "60,0,300",
		title = "",
		y_lims = [0,170000],
		y_log = False,
		y_subplot_lims = [0.95,1.05],
		x_label = "N(photons)"
	)

	configs.extend(merging_check_NPFPh.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFPhotons"]
		))

	cleaning_check_NPFPh = merging_check_NPFPh.clone(
		name = "cleaning_check_NPFPh",
		legend = data_trackcleaned_cleaned_legend,
		subplot_numerators = [1,2],
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NPFPh.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFPhotons"]
		))

	merging_check_NPFCH = merging_check_NE.clone(
		name = "merging_check_NPFCH",
		x_expression = "NPFChargedHadrons",
		y_subplot_lims = [0.95,1.05],
		x_bins = "160,0,800",
		title = "",
		y_lims = [0,66000],
		y_log = False,
		x_label = "N(charged hadrons)"
	)

	configs.extend(merging_check_NPFCH.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFChargedHadrons"]
		))

	cleaning_check_NPFCH = merging_check_NPFCH.clone(
		name = "cleaning_check_NPFCH",
		legend = data_trackcleaned_cleaned_legend,
		subplot_numerators = [1,2],
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NPFCH.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFChargedHadrons"]
		))


	merging_check_NPFNH = merging_check_NE.clone(
		name = "merging_check_NPFNH",
		x_expression = "NPFNeutralHadrons",
		x_bins = "20,0,100",
		title = "",
		y_lims = [0,880000],
		y_log = False,
		y_subplot_lims = [0.85,1.15],
		x_label = "N(neutral hadrons)"
	)

	configs.extend(merging_check_NPFNH.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFNeutralHadrons"]
		))

	cleaning_check_NPFNH = merging_check_NPFNH.clone(
		name = "cleaning_check_NPFNH",
		y_lims = [0,780000],
		legend = data_trackcleaned_cleaned_legend,
		subplot_numerators = [1,2],
		plotlines = [DoubleMuonSelected, DoubleMuonTrackcleaned, DoubleMuonCleaned]
	)

	configs.extend(cleaning_check_NPFNH.return_json_with_changed_x_and_weight(
		x_expressions = ["NPFNeutralHadrons"]
		))

	merging_check_NJets = merging_check_NE.clone(
		name = "merging_check_NJets",
		x_expression = "nJets",
		title = "",
		x_bins = "6,0,6",
		y_subplot_lims = [0.5,1.5],
		legend = data_embedded_mirrored_cleaned_legend,
		subplot_numerators = [1,2,3],
		plotlines = [DoubleMuonSelected, DoubleMuonEmbedded, DoubleMuonMirrored, DoubleMuonCleaned],
		x_label = "N(jets)"
	)

	configs.extend(merging_check_NJets.return_json_with_changed_x_and_weight(
		x_expressions = ["nJets"]
		))

	merging_check_LeadingJetPt = merging_check_NE.clone(
		name = "merging_check_LeadingJetPt",
		title = "",
		x_expression = "LeadingTaggedJetPt",
		x_bins = "70,30,100",
		y_lims = [0,34000],
		y_log = False,
		legend = data_embedded_mirrored_cleaned_legend,
		subplot_numerators = [1,2,3],
		y_subplot_lims = [0.75,1.25],
		plotlines = [DoubleMuonSelected, DoubleMuonEmbedded, DoubleMuonMirrored, DoubleMuonCleaned],
		x_label = "p_{T}(leading jet) [GeV]"
	)

	configs.extend(merging_check_LeadingJetPt.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingJetPt"]
		))


	merging_check_sumPt = merging_check_NE.clone(
		name = "merging_check_sumPt",
		title = "",
		x_expression = "PFSumPt",
		x_bins = "50,0,100",
		y_lims = [0,210000],
		y_log = False,
		legend = data_embedded_mirrored_legend,
		subplot_numerators = [1,2],
		y_subplot_lims = [0.75,1.25],
		plotlines = [DoubleMuonSelectedValidation, DoubleMuonEmbeddedValidation, DoubleMuonMirroredValidation],
		x_label = "E_{T} [GeV]"
	)

	configs.extend(merging_check_sumPt.return_json_with_changed_x_and_weight(
		x_expressions = ["PFSumPt"]
		))

	merging_check_sumPt_noMuMu = merging_check_sumPt.clone(
		name = "merging_check_sumPt_noMuMu",
		title = "Z#rightarrow#mu#mu contribution neglected",
		x_expression = "PFSumPtWithoutZMuMu"
	)

	configs.extend(merging_check_sumPt_noMuMu.return_json_with_changed_x_and_weight(
			x_expressions = ["PFSumPtWithoutZMuMu"]
			))

	merging_check_PFMet = merging_check_NE.clone(
		name = "merging_check_PFMet",
		title = "",
		x_expression = "PFMet",
		x_bins = "50,0,100",
		y_lims = [0,210000],
		y_log = False,	
		legend = data_embedded_mirrored_legend,
		subplot_numerators = [1,2],
		y_subplot_lims = [0.75,1.25],
		plotlines = [DoubleMuonSelectedValidation, DoubleMuonEmbeddedValidation, DoubleMuonMirroredValidation],
		x_label = "#slash{E}_{T} [GeV]"
	)

	configs.extend(merging_check_PFMet.return_json_with_changed_x_and_weight(
		x_expressions = ["PFMet"]
		))

	merging_check_sumHt = merging_check_NE.clone(
		name = "merging_check_sumHt",
		title = "",
		x_expression = "PFSumHt",
		x_bins = "50,0,2000",
		y_lims = [0,210000],
		y_log = False,
		legend = data_embedded_mirrored_legend,
		subplot_numerators = [1,2],
		y_subplot_lims = [0.75,1.25],
		plotlines = [DoubleMuonSelectedValidation, DoubleMuonEmbeddedValidation, DoubleMuonMirroredValidation],
		x_label = "H_{T} [GeV]"
	)

	configs.extend(merging_check_sumHt.return_json_with_changed_x_and_weight(
		x_expressions = ["PFSumHt"]
		))

	merging_check_sumHt_noMuMu = merging_check_sumHt.clone(
		name = "merging_check_sumHt_noMuMu",
		title = "Z#rightarrow#mu#mu contribution neglected",
		x_expression = "PFSumHtWithoutZMuMu"
	)

	configs.extend(merging_check_sumHt_noMuMu.return_json_with_changed_x_and_weight(
			x_expressions = ["PFSumHtWithoutZMuMu"]
			))
	'''
	# Zmumu selection Check for Muon Embedding

	selection_check_ZMass = pltcl.single_plot(
		name = "selection_check_ZMass",
		title = "",
		x_expression = "ZMass",
		x_bins = "50,20,120",
		normalized_by_binwidth = False,
		x_label = "m(#mu#mu) [GeV]",
		y_label = "Events",
		wwwfolder = web_dir,
		legend =[0.3,0.3,0.65,0.7],
		plot_type = "absolute",
		subplot_denominator = 0,
		subplot_numerators = [1,2],
		y_subplot_lims = [0.85,1.15],
		y_subplot_label = "Ratio",
		plotlines = [DoubleMuonSelectedValidation, DoubleMuonEmbeddedValidation, DoubleMuonMirroredValidation]
	)
	'''
	#configs.extend(selection_check_ZMass.return_json_with_changed_x_and_weight(x_expressions = ["ZMass"]))

	fsr_ZMass = selection_check_ZMass.clone(
		name = "fsr_ZMass",
		normalized_to_unity = True,
		x_bins = "60,60,120",
		y_label = "arbitary units",
		y_subplot_lims = [0.4,1.5],
		subplot_denominator = 2,
		subplot_numerators = [0,1],
		plotlines = [DoubleMuonFSRsimMuons, DoubleMuonFSRfsrMuons, DoubleMuonFSRrecoMuons]
	)

	#configs.extend(fsr_ZMass.return_json_with_changed_x_and_weight(x_expressions = ["ZMass"]))

	selection_check_leadingMuPt = selection_check_ZMass.clone(
		name = "selection_check_leadingMuPt",
		x_bins = "70,0,140",
		legend =[0.55,0.45,0.9,0.85],
		x_expression = "leadingLeptonFromZPt",
		x_label = "p_{T}(leading #mu) [GeV]"
	)

	#configs.extend(selection_check_leadingMuPt.return_json_with_changed_x_and_weight(	x_expressions = ["leadingLeptonFromZPt"]	))

	selection_check_ThetaZMuMinus = selection_check_ZMass.clone(
		name = "selection_check_ThetaZMuMinus",
		x_bins = "50,0,3.15",
		legend = [0.4,0.15,0.75,0.55],
		x_expression = "thetaZLepMinus",
		x_label = "#theta(#mu^{-}, Z)"
	)

	#configs.extend(selection_check_ThetaZMuMinus.return_json_with_changed_x_and_weight(x_expressions = ["thetaZLepMinus"]	))
		
	selection_check_leadingMuEta = selection_check_ZMass.clone(
		name = "selection_check_leadingMuEta",
		x_expression = "leadingLeptonFromZEta",
		legend =[0.4,0.15,0.75,0.55],
		x_bins = "50,-3,3",
		x_label = "#eta(leading #mu)"
	)

	#configs.extend(selection_check_leadingMuEta.return_json_with_changed_x_and_weight(	x_expressions = ["leadingLeptonFromZEta"]	))

	selection_check_leadingMuPhi = selection_check_ZMass.clone(
		name = "selection_check_leadingMuPhi",
		x_expression = "leadingLeptonFromZPhi",
		legend =[0.4,0.15,0.75,0.55],
		x_bins = "50,-3.5,3.5",
		x_label = "#phi(leading #mu)"
	)

	#configs.extend(selection_check_leadingMuPhi.return_json_with_changed_x_and_weight(	x_expressions = ["leadingLeptonFromZPhi"]	))

	selection_check_trailingMuPt = selection_check_ZMass.clone(
		name = "selection_check_trailingMuPt",
		x_bins = "50,0,100",
		legend =[0.55,0.45,0.9,0.85],
		x_expression = "trailingLeptonFromZPt",
		x_label = "p_{T}(trailing #mu) [GeV]"
	)

	#configs.extend(selection_check_trailingMuPt.return_json_with_changed_x_and_weight(	x_expressions = ["trailingLeptonFromZPt"]	))
		
	selection_check_trailingMuEta = selection_check_ZMass.clone(
		name = "selection_check_trailingMuEta",
		x_expression = "trailingLeptonFromZEta",
		legend =[0.4,0.15,0.75,0.55],
		x_bins = "50,-3,3",
		x_label = "#eta(trailing #mu)"
	)

	#configs.extend(selection_check_trailingMuEta.return_json_with_changed_x_and_weight(	x_expressions = ["trailingLeptonFromZEta"]	))

	selection_check_trailingMuPhi = selection_check_ZMass.clone(
		name = "selection_check_trailingMuPhi",
		x_expression = "trailingLeptonFromZPhi",
		legend =[0.4,0.15,0.75,0.55],
		x_bins = "50,-3.5,3.5",
		x_label = "#phi(trailing #mu)"
	)

	#configs.extend(selection_check_trailingMuPhi.return_json_with_changed_x_and_weight(	x_expressions = ["trailingLeptonFromZPhi"]	))

	## Muon isolation

	# Charged hadrons from PV
	selection_check_lMu_CHPV = selection_check_ZMass.clone(
		name = "selection_check_lMu_CHPV",
		title = "general selection",
		x_expression = "leadingMuon_ChargedFromFirstPVPtFlow_full",
		legend = data_embedded_mirrored_random_legend_upper_right,
		y_lims = [0,0.035],
		subplot_numerators = [],
		x_bins = "100,0.0,0.4",
		plotlines = [DoubleMuonSelectedPtFlowHistograms, DoubleMuonEmbeddedPtFlowHistograms, DoubleMuonMirroredPtFlowHistograms, DoubleMuonRandomPtFlowHistograms],
		y_label = "p_{T}-flow per bin width [GeV]",
		x_label = "#DeltaR(leading #mu, charged hadrons (PV))"
	)

	configs.extend(selection_check_lMu_CHPV.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_ChargedFromFirstPVPtFlow_full"]
		))

	selection_check_lMu_CHPV_peak = selection_check_lMu_CHPV.clone(
		name = "selection_check_lMu_CHPV_peak",
		y_lims = [0,0.0115],
		legend = data_embedded_mirrored_random_legend_upper_left,
		title = "general selection & peak region"
	)

	configs.extend(selection_check_lMu_CHPV_peak.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_ChargedFromFirstPVPtFlow_peak"]
		))

	selection_check_lMu_CHPV_sideband = selection_check_lMu_CHPV.clone(
		name = "selection_check_lMu_CHPV_sideband",
		y_lims = [0,0.026],
		title = "general selection & sideband region"
	)

	configs.extend(selection_check_lMu_CHPV_sideband.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_ChargedFromFirstPVPtFlow_sideband"]
		))

	# Charged hadrons from PU
	selection_check_lMu_CHNPV = selection_check_ZMass.clone(
		name = "selection_check_lMu_CHNPV",
		title = "general selection",
		x_expression = "leadingMuon_ChargedNotFromFirstPVPtFlow_full",
		legend = data_embedded_mirrored_random_legend_upper_left,
		subplot_numerators = [],
		x_bins = "100,0.0,0.4",
		plotlines = [DoubleMuonSelectedPtFlowHistograms, DoubleMuonEmbeddedPtFlowHistograms, DoubleMuonMirroredPtFlowHistograms, DoubleMuonRandomPtFlowHistograms],
		y_label = "p_{T}-flow per bin width [GeV]",
		x_label = "#DeltaR(leading #mu, charged hadrons (PU))"
	)

	configs.extend(selection_check_lMu_CHNPV.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_ChargedNotFromFirstPVPtFlow_full"]
		))

	selection_check_lMu_CHNPV_peak = selection_check_lMu_CHNPV.clone(
		name = "selection_check_lMu_CHNPV_peak",
		legend = data_embedded_mirrored_random_legend_upper_left,
		title = "general selection & peak region"
	)

	configs.extend(selection_check_lMu_CHNPV_peak.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_ChargedNotFromFirstPVPtFlow_peak"]
		))

	selection_check_lMu_CHNPV_sideband = selection_check_lMu_CHNPV.clone(
		name = "selection_check_lMu_CHNPV_sideband",
		y_lims = [0,0.028],
		title = "general selection & sideband region"
	)

	configs.extend(selection_check_lMu_CHNPV_sideband.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_ChargedNotFromFirstPVPtFlow_sideband"]
		))

	# Neutral Hadrons
	selection_check_lMu_NHPV = selection_check_ZMass.clone(
		name = "selection_check_lMu_NHPV",
		title = "general selection",
		x_expression = "leadingMuon_NeutralFromFirstPVPtFlow_full",
		legend = data_embedded_mirrored_random_legend_upper_right,
		subplot_numerators = [],
		x_bins = "100,0.0,0.4",
		y_lims = [0,0.024],
		plotlines = [DoubleMuonSelectedPtFlowHistograms, DoubleMuonEmbeddedPtFlowHistograms, DoubleMuonMirroredPtFlowHistograms, DoubleMuonRandomPtFlowHistograms],
		y_label = "p_{T}-flow per bin width [GeV]",
		x_label = "#DeltaR(leading #mu, neutral hadrons)"
	)

	configs.extend(selection_check_lMu_NHPV.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_NeutralFromFirstPVPtFlow_full"]
		))

	selection_check_lMu_NHPV_peak = selection_check_lMu_NHPV.clone(
		name = "selection_check_lMu_NHPV_peak",
		y_lims = [0,0.013],
		legend = data_embedded_mirrored_random_legend_upper_left,
		title = "general selection & peak region"
	)

	configs.extend(selection_check_lMu_NHPV_peak.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_NeutralFromFirstPVPtFlow_peak"]
		))

	selection_check_lMu_NHPV_sideband = selection_check_lMu_NHPV.clone(
		name = "selection_check_lMu_NHPV_sideband",
		y_lims = [0,0.012],
		legend = data_embedded_mirrored_random_legend_upper_right,
		title = "general selection & sideband region"
	)

	configs.extend(selection_check_lMu_NHPV_sideband.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_NeutralFromFirstPVPtFlow_sideband"]
		))
	'''
	# Photons
	'''
	selection_check_lMu_PPV = selection_check_ZMass.clone(
		name = "selection_check_lMu_PPV",
		title = "general selection",
		x_expression = "leadingMuon_PhotonsFromFirstPVPtFlow_full",
		legend = data_embedded_mirrored_random_legend_lower_right,
		y_lims = [0,0.062],
		subplot_numerators = [],
		x_bins = "40,0.0,0.4",
		plotlines = [DoubleMuonSelectedPtFlowHistograms, DoubleMuonEmbeddedPtFlowHistograms, DoubleMuonMirroredPtFlowHistograms, DoubleMuonRandomPtFlowHistograms],
		y_label = "p_{T}-flow per bin width [GeV]",
		x_label = "#DeltaR(leading #mu, photons)"
	)

	configs.extend(selection_check_lMu_PPV.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_full"]
		))

	selection_check_lMu_PPV_peak = selection_check_lMu_PPV.clone(
		name = "selection_check_lMu_PPV_peak",
		y_lims = [0,0.04],
		legend = data_embedded_mirrored_random_legend_upper_left,
		title = "general selection & peak region (#pm 10 GeV)"
	)

	configs.extend(selection_check_lMu_PPV_peak.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_peak"]
		))

	selection_check_lMu_PPV_sideband = selection_check_lMu_PPV.clone(
		name = "selection_check_lMu_PPV_sideband",
		y_lims = [0,0.06],
		legend = data_embedded_mirrored_random_legend_upper_right,
		title = "general selection & sideband region (#pm 10 GeV)"
	)

	configs.extend(selection_check_lMu_PPV_sideband.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_sideband"]
		))


	ptflow_photon_histograms(binarea=binarea,peakwidth=peakwidth)


	### Tau Embedding Studies


	# Acceptance efficiencies as function of Pt

	MuTauAccEfficiency2D = pltcl.single_plot(
		name = "MuTauAccEfficiency2D",
		title = "#scale[1.3]{#mu#tau_{h}: #varepsilon per bin}",
		x_expression = "MuTau_accEff",
		y_expression = "MuTau_accEff",
		x_label = "p_{T}(#tau, #tau#rightarrow#mu) [GeV]",
		y_label = "p_{T}(#tau, #tau#rightarrow#tau_{h}) [GeV]",
		z_label = "",
		z_lims = [0,0.23],
		plot_type = "absolute",
		wwwfolder = web_dir
		plotlines = [AccEfficiency2D])

	#configs.extend(MuTauAccEfficiency2D.return_json_with_changed_x_and_weight(x_expressions = ["MuTau_accEff"]))


	ElTauAccEfficiency2D = MuTauAccEfficiency2D.clone(
		name = "ElTauAccEfficiency2D",
		title = "#scale[1.3]{e#tau_{h}: #varepsilon per bin}",
		x_expression = "ElTau_accEff",
		y_expression = "ElTau_accEff",
		x_label = "p_{T}(#tau, #tau#rightarrow e) [GeV]",
		y_label = "p_{T}(#tau, #tau#rightarrow#tau_{h}) [GeV]",
		z_lims = [0,0.24]
		)

	#configs.extend(ElTauAccEfficiency2D.return_json_with_changed_x_and_weight(x_expressions = ["ElTau_accEff"]))

	TauTauAccEfficiency2D = MuTauAccEfficiency2D.clone(
		name = "TauTauAccEfficiency2D",
		title = "#scale[1.3]{#tau_{h}#tau_{h}: #varepsilon per bin}",
		x_expression = "TauTau_accEff",
		y_expression = "TauTau_accEff",
		x_label = "p_{T}(#tau^{-}) [GeV]",
		y_label = "p_{T}(#tau^{+}) [GeV]",
		z_lims = [0,0.42]
		)

	#configs.extend(TauTauAccEfficiency2D.return_json_with_changed_x_and_weight(x_expressions = ["TauTau_accEff"]))

	ElMuAccEfficiency2D = MuTauAccEfficiency2D.clone(
		name = "ElMuAccEfficiency2D",
		title = "#scale[1.3]{e#mu: #varepsilon per bin}",
		x_expression = "ElMu_accEff",
		y_expression = "ElMu_accEff",
		x_label = "p_{T}(#tau, #tau#rightarrow e) [GeV]",
		y_label = "p_{T}(#tau, #tau#rightarrow #mu) [GeV]",
		z_lims = [0,0.065]
		)

	#configs.extend(ElMuAccEfficiency2D.return_json_with_changed_x_and_weight(x_expressions = ["ElMu_accEff"]))

	# Number of events as function of Pt

	MuTauNEvents2D = MuTauAccEfficiency2D.clone(
		name = "MuTauNEvents2D",
		title = "#scale[1.3]{#mu#tau_{h}: Events per bin}",
		x_expression = "number_of_entries_hist",
		y_expression = "number_of_entries_hist",
		z_log = True,
		z_lims = [0.9,5000000],
		plotlines = [NEntries2DMuTau])

	#configs.extend(MuTauNEvents2D.return_json_with_changed_x_and_weight(x_expressions = ["number_of_entries_hist"]))

	ElTauNEvents2D = MuTauNEvents2D.clone(
		name = "ElTauNEvents2D",
		title = "#scale[1.3]{e#tau_{h}: Events per bin}",
		x_label = "p_{T}(#tau, #tau#rightarrow e) [GeV]",
		y_label = "p_{T}(#tau, #tau#rightarrow#tau_{h}) [GeV]",
		plotlines = [NEntries2DElTau])

	#configs.extend(ElTauNEvents2D.return_json_with_changed_x_and_weight(x_expressions = ["number_of_entries_hist"]))

	TauTauNEvents2D = MuTauNEvents2D.clone(
		name = "TauTauNEvents2D",
		title = "#scale[1.3]{#tau_{h}#tau_{h}: Events per bin}",
		x_label = "p_{T}(#tau^{-}) [GeV]",
		y_label = "p_{T}(#tau^{+}) [GeV]",
		plotlines = [NEntries2DTauTau])

	#configs.extend(TauTauNEvents2D.return_json_with_changed_x_and_weight(x_expressions = ["number_of_entries_hist"]))

	ElMuNEvents2D = MuTauNEvents2D.clone(
		name = "ElMuNEvents2D",
		title = "#scale[1.3]{e#mu: Events per bin}",
		x_label = "p_{T}(#tau, #tau#rightarrow e) [GeV]",
		y_label = "p_{T}(#tau, #tau#rightarrow #mu) [GeV]",
		plotlines = [NEntries2DElMu])

	#configs.extend(ElMuNEvents2D.return_json_with_changed_x_and_weight(x_expressions = ["number_of_entries_hist"]))

	# Acceptance efficiency distributions

	AccEfficiencyMuTau = pltcl.single_plot(
		name = "AccEfficiencyMuTau",
		title = "#scale[1.3]{#mu#tau_{h}}",
		x_expression = "accEfficiency",
		y_lims = [0.5,10000000],
		x_bins = "25,0,0.25",
		normalized_by_binwidth = False,
		x_label = "#varepsilon",
		y_label = "Events",
		y_log = True,
		plot_type = "absolute",
		vertical_lines = [0.2255],
		plotlines = [AccEfficiencyMuTauFile]
	)

	#configs.extend(AccEfficiencyMuTau.return_json_with_changed_x_and_weight(x_expressions = ["accEfficiency"]))

	AccEfficiencyElTau = AccEfficiencyMuTau.clone(
		name = "AccEfficiencyElTau",
		title = "#scale[1.3]{e#tau_{h}}",
		x_bins = "25,0,0.25",
		vertical_lines = [0.2309],
		plotlines = [AccEfficiencyElTauFile]
	)

	#configs.extend(AccEfficiencyElTau.return_json_with_changed_x_and_weight(x_expressions = ["accEfficiency"]))

	AccEfficiencyTauTau = AccEfficiencyMuTau.clone(
		name = "AccEfficiencyTauTau",
		title = "#scale[1.3]{#tau_{h}#tau_{h}}",
		x_bins = "25,0,0.48",
		vertical_lines = [0.4194],
		plotlines = [AccEfficiencyTauTauFile]
	)

	#configs.extend(AccEfficiencyTauTau.return_json_with_changed_x_and_weight(x_expressions = ["accEfficiency"]))

	AccEfficiencyElMu = AccEfficiencyMuTau.clone(
		name = "AccEfficiencyElMu",
		title = "#scale[1.3]{e#mu}",
		x_bins = "25,0,0.07",
		vertical_lines = [0.0621],
		plotlines = [AccEfficiencyElMuFile]
	)

	#configs.extend(AccEfficiencyElMu.return_json_with_changed_x_and_weight(x_expressions = ["accEfficiency"]))


	# visible Mass comparisons

	stitching_weight = "(((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.25449124172134e-6) + ((genbosonmass >= 150.0 && npartons == 1)*1.17272893569016e-6) + ((genbosonmass >= 150.0 && npartons == 2)*1.17926755938344e-6) + ((genbosonmass >= 150.0 && npartons == 3)*1.18242445124698e-6) + ((genbosonmass >= 150.0 && npartons == 4)*1.16077776187804e-6)+((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*1.15592e-4) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.5569730365e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.68069486078868e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.74717616341537e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.3697397756176e-5)+((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"

	selection_weight_mt = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(mt_1<40.0)*(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.15)*((q_1*q_2)<0.0)"

	selection_weight_et = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(againstElectronTightMVA6_2 > 0.5)*(mt_1<40.0)*(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(iso_1 < 0.1)*((q_1*q_2)<0.0)"

	selection_weight_tt = "(pt_1 > 42.0 && pt_2 > 42.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((q_1*q_2)<0.0)"

	#selection_weight_em = "(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"
	selection_weight_em = "(pt_1 > 24.0 && pt_2 > 24.0)*(pZetaMissVis > -20.0)*(iso_1 < 0.15)*(iso_2 < 0.2)*((q_1*q_2)<0.0)"

	genmatching_weight_xt = "*(gen_match_2 == 5)"
	genmatching_weight_tt = "*(gen_match_1 == 5 && gen_match_2 == 5)"
	genmatching_weight_em = "*(gen_match_1 > 2 && gen_match_2 > 3)"

	visibleMassMuTau = pltcl.single_plot(
		name = "visibleMassMuTau",
		title = "#scale[1.3]{#mu#tau_{h}: shape comparison}",
		x_expression = "m_vis",
		x_bins = "30,30,120",
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		x_label = "m_{vis}(#tau#tau) [GeV]",
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_mt,
		y_label = "1/dm_{vis} [GeV^{-1}]",
		y_lims = [0,0.058],
		plot_type = "absolute",
		legend = [0.53,0.44,0.92,0.88],
		subplot_denominator = 0,
		subplot_numerators = [1,2,3],
		y_subplot_lims = [0.5,1.5],
		y_subplot_label = "Ratio",
		print_infos = True,
		plotlines = [EmbeddingMuTauFileNominal, EmbeddingMuTauFileUp, EmbeddingMuTauFileDown, DYFileMuTauFile, HToTauTauMuTauFile]
	)

	#configs.extend(visibleMassMuTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassElTau = visibleMassMuTau.clone(
		name = "visibleMassElTau",
		title = "#scale[1.3]{e#tau_{h}: shape comparison}",
		weight = stitching_weight + genmatching_weight_xt + "*eventWeight*(eventWeight<=1)*" + selection_weight_et,
		plotlines = [EmbeddingElTauFileNominal, EmbeddingElTauFileUp, EmbeddingElTauFileDown, DYFileElTauFile, HToTauTauElTauFile]
	)

	#configs.extend(visibleMassElTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassTauTau = visibleMassMuTau.clone(
		name = "visibleMassTauTau",
		title = "#scale[1.3]{#tau_{h}#tau_{h}: shape comparison}",
		x_bins = "11,30,250",
		y_lims = [0,0.026],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + "*eventWeight*(eventWeight<=1)*" + selection_weight_tt,
		plotlines = [EmbeddingTauTauFileNominal, EmbeddingTauTauFileUp, EmbeddingTauTauFileDown, DYFileTauTauFile, HToTauTauTauTauFile]
	)

	#configs.extend(visibleMassTauTau.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	visibleMassElMu = visibleMassMuTau.clone(
		name = "visibleMassElMu",
		title = "#scale[1.3]{e#mu: shape comparison}",
		subplot_denominator = 0,
		x_bins = "30,30,120",
		y_lims = [0,0.062],
	#	x_bins = "1,0,13000",
		normalized_by_binwidth = True,
	#	normalized_by_binwidth = False,
		weight = stitching_weight + genmatching_weight_em + "*eventWeight*(eventWeight<=1)*" + selection_weight_em,
		plotlines = [EmbeddingElMuFileNominal, EmbeddingElMuFileUp, EmbeddingElMuFileDown, DYFileElMuFile, HToTauTauElMuFile]
	)

	#configs.extend(visibleMassElMu.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))


	## Integrals for Decay channel migration

	MuTauIntegrals = pltcl.single_plot(
		name = "MuTauIntegrals",
		title = "#mu#tau_{h}",
		x_expression = "m_vis",
		x_bins = "1,0,13000",
		normalized_by_binwidth = False,
		x_label = "Integral",
		weight = "generatorWeight*(generatorWeight<=1)*" + selection_weight_mt,
	#	weight = "generatorWeight*(generatorWeight<=1)",
		y_label = "",
		wwwfolder ="integrals",
		plot_type = "absolute",
		print_infos = True,
		plotlines = [EmbeddingMuTauIntegralMuTauFile, EmbeddingElTauIntegralMuTauFile, EmbeddingTauTauIntegralMuTauFile, EmbeddingElMuIntegralMuTauFile]
	)

	#configs.extend(MuTauIntegrals.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	ElTauIntegrals = MuTauIntegrals.clone(
		name = "ElTauIntegrals",
		title = "e#tau_{h}",
		x_expression = "m_vis",
		x_bins = "1,0,13000",
		normalized_by_binwidth = False,
		x_label = "Integral",
		weight = "generatorWeight*(generatorWeight<=1)*" + selection_weight_et,
	#	weight = "generatorWeight*(generatorWeight<=1)",
		y_label = "",
		wwwfolder ="integrals",
		plot_type = "absolute",
		print_infos = True,
		plotlines = [EmbeddingMuTauIntegralElTauFile, EmbeddingElTauIntegralElTauFile, EmbeddingTauTauIntegralElTauFile, EmbeddingElMuIntegralElTauFile]
	)

	#configs.extend(ElTauIntegrals.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))

	TauTauIntegrals = MuTauIntegrals.clone(
		name = "TauTauIntegrals",
		title = "#tau_{h}#tau_{h}",
		x_expression = "m_vis",
		x_bins = "1,0,13000",
		normalized_by_binwidth = False,
		x_label = "Integral",
		weight = "generatorWeight*(generatorWeight<=1)*" + selection_weight_tt,
	#	weight = "generatorWeight*(generatorWeight<=1)",
		y_label = "",
		wwwfolder ="integrals",
		plot_type = "absolute",
		print_infos = True,
		plotlines = [EmbeddingMuTauIntegralTauTauFile, EmbeddingElTauIntegralTauTauFile, EmbeddingTauTauIntegralTauTauFile, EmbeddingElMuIntegralTauTauFile]
	)

	#configs.extend(TauTauIntegrals.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))


	ElMuIntegrals = MuTauIntegrals.clone(
		name = "TauTauIntegrals",
		title = "e#mu",
		x_expression = "m_vis",
		x_bins = "1,0,13000",
		normalized_by_binwidth = False,
		x_label = "Integral",
		weight = "generatorWeight*(generatorWeight<=1)*" + selection_weight_em,
	#	weight = "generatorWeight*(generatorWeight<=1)",
		y_label = "",
		wwwfolder ="integrals",
		plot_type = "absolute",
		print_infos = True,
		plotlines = [EmbeddingMuTauIntegralElMuFile, EmbeddingElTauIntegralElMuFile, EmbeddingTauTauIntegralElMuFile, EmbeddingElMuIntegralElMuFile]
	)

	#configs.extend(ElMuIntegrals.return_json_with_changed_x_and_weight(x_expressions = ["m_vis"]))
	'''
 
	default_variables=[
			"integral",
			"pt_1", "eta_1", "phi_1", "m_1", "iso_1", "mt_1",
			"pt_2", "eta_2", "phi_2", "m_2", "iso_2", "mt_2",
			"pt_sv", "eta_sv", "phi_sv", "m_sv", "m_vis", "ptvis",
			"met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
			"mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
			"pZetaMissVis", "pzetamiss", "pzetavis",
			"jpt_1", "jeta_1", "jphi_1",
			"jpt_2", "jeta_2", "jphi_2",
			"njetspt30", "mjj", "jdeta", "njetingap20", "njetingap",
			"trigweight_1", "trigweight_2", "puweight",
			"npv", "npu", "rho","nbtag",'genMatchedLep1LV.fCoordinates.fPt','genMatchedLep2LV.fCoordinates.fPt','genMatchedLep2LV.fCoordinates.fEta','genMatchedLep1LV.fCoordinates.fEta','genMatchedLep2LV.fCoordinates.fPhi','genMatchedLep1LV.fCoordinates.fPhi','triggerWeight_1','identificationWeight_1','trigweight_1'
	]
	iso_variables = [
	"againstElectronLooseMVA6_1",
		"againstElectronLooseMVA6_2",

		"iso_1",
		"iso_2",
		"decayDistX_1",
		"decayDistX_2",
		"decayDistY_1",
		"decayDistY_2",
		"decayDistZ_1",
		"decayDistZ_2",
		"decayDistM_1",
		"decayDistM_2",
		"nPhoton_1",
		"nPhoton_2",
		"ptWeightedDetaStrip_1",
		"ptWeightedDetaStrip_2",
		"ptWeightedDphiStrip_1",
		"ptWeightedDphiStrip_2",
		"ptWeightedDrSignal_1",
		"ptWeightedDrSignal_2",
		"ptWeightedDrIsolation_1",
		"ptWeightedDrIsolation_2",
		"leadingTrackChi2_1",
		"leadingTrackChi2_2",
		"eRatio_1",
		"eRatio_2",
		"MVAdxy_sign_1",
		"MVAdxy_sign_2",
		"MVAdxy_abs_1",	 
		"MVAdxy_abs_2",
		"MVAdxy_signal_1",
		"MVAdxy_signal_2",
		"MVAdxy_ip3d_sign_1",
		"MVAdxy_ip3d_sign_2",
		"MVAdxy_ip3d_abs_1",
		"MVAdxy_ip3d_abs_2",
		"MVAdxy_ip3d_signal_1",
		"MVAdxy_ip3d_signal_2",
		"hasSecondaryVertex_1",
		"hasSecondaryVertex_2",
		"flightLengthSig_1",
		"flightLengthSig_2","byCombinedIsolationDeltaBetaCorrRaw3Hits_2","byCombinedIsolationDeltaBetaCorrRaw3Hits_2","photonPtSumOutsideSignalCone_2","chargedIsoPtSum_2","neutralIsoPtSum_2","footprintCorrection_2","puCorrPtSum_2"]
	
	tau_iso_variables = [x for x in iso_variables if x[-2:]=="_2"]
	plotting_dict={}
	for v in default_variables:
		plotting_dict.setdefault(v,[])
		plotting_dict[v]={}
		plotting_dict[v].setdefault("x_label",v)
		if 'eta' in v or 'Eta' in v:
			plotting_dict[v].setdefault("x_bins","25,-2.5,2.5")
		if 'phi' in v or 'Phi' in v:
			plotting_dict[v].setdefault("x_bins","30,-3.2,3.2")
		if 'njet' in v:
			plotting_dict[v].setdefault("x_bins","7,0,7")	
		if 'Weight' in v or 'weight' in v:
			plotting_dict[v].setdefault("x_bins","24,0,1.2")
		
		plotting_dict[v].setdefault("x_bins","50,0,100")
	plotting_dict['genMatchedLep1LV.fCoordinates.fPt']["x_bins"]="50,0,100"

	plotting_dict["integral"]["x_bins"]="1,0,1"
	plotting_dict["m_1"]["x_bins"]="10,0,0.5"
	plotting_dict["m_1"]["x_label"]="Muon Mass / GeV"
	plotting_dict["m_2"]["x_bins"]="30,0,1.5"
	plotting_dict["mt_1"]["x_bins"]="25,0,120"
	plotting_dict["mt_2"]["x_bins"]="25,0,120"
	plotting_dict["m_vis"]["x_bins"]="25,20,120"
	plotting_dict["npu"]["x_bins"]="30,0,60"
	plotting_dict["npv"]["x_bins"]="30,0,60"
	plotting_dict["npv"]["x_bins"]="30,0,60"
	plotting_dict["iso_1"]["x_bins"]="25,0.,1."
	plotting_dict["nbtag"]["x_bins"]="5,0,5"
	plotting_dict["pzetamiss"]["x_bins"]="12,-150.0,100.0"
	plotting_dict["pZetaMissVis"]["x_bins"] = "12,-150.0,100.0"
	plotting_dict["pzetavis"]["x_bins"]="10,0.0,100.0"
	plotting_dict["met"]["x_bins"]="10,0,100"

	plotting_dict["mt_2"]["x_bins"]="25,0,120"
	plotting_dict["mt_2"]["x_bins"]="25,0,120"
		
	plotting_dict["m_2"]["x_label"]="Tau Mass / GeV"
	plotting_dict["mt_1"]["x_label"]="m_{T} / GeV"
	plotting_dict["m_vis"]["x_label"]="m_{vis} / GeV"
	plotting_dict["npu"]["x_label"]="Number Pileup"
	plotting_dict["npv"]["x_label"]="NPV"
	plotting_dict["iso_1"]["x_label"]="Muon Isolation"
	plotting_dict["nbtag"]["x_label"]="Number of b-tags"
	plotting_dict["njetspt30"]["x_label"]="Number of Jets (p_{T} 30)"
	plotting_dict["pt_1"]["x_label"]="Muon p_{T} / GeV"
	plotting_dict["pt_2"]["x_label"]="Tau p_{T} / GeV"

	for v in iso_variables:
		plotting_dict.setdefault(v,[])
		plotting_dict[v]={}
		plotting_dict[v].setdefault("x_label",v)
		if "sign_" in v:
			plotting_dict[v].setdefault("x_bins","15,-1.5,1.5")
		elif "ptWeightedD" in v:
			plotting_dict[v].setdefault("x_bins","30,0,0.6")
		else:
			plotting_dict[v].setdefault("x_bins","20,0,10")
	plotting_dict["decayDistX_2"]["x_bins"]="20,-2,2"
	plotting_dict["decayDistY_2"]["x_bins"]="20,-2,2"
	plotting_dict["decayDistZ_2"]["x_bins"]="20,-2,2"
	plotting_dict["MVAdxy_abs_2"]["x_bins"]="30,0,0.3"
	plotting_dict["eRatio_2"]["x_bins"]="20,0,2"
	plotting_dict["hasSecondaryVertex_2"]["x_bins"]="10,-0.5,1.5"
	#plotting_dict["MVAdxy_abs_2"]["x_bins"]="30,0,0.3"
	#plotting_dict["MVAdxy_abs_2"]["x_bins"]="30,0,0.3"
	plotting_dict["againstElectronLooseMVA6_2"]["x_bins"]="2,-0.5,1.5"
	plotting_dict["MVAdxy_ip3d_abs_2"]["x_bins"]="30,0,0.3"
	plotting_dict["decayDistM_2"]["x_bins"]="15,0,3"
	plotting_dict["byCombinedIsolationDeltaBetaCorrRaw3Hits_2"]["x_bins"]="20,0,10"
	plotting_dict["photonPtSumOutsideSignalCone_2"]["x_bins"]="20,0,10"
	plotting_dict["chargedIsoPtSum_2"]["x_bins"]="20,0,1"
	plotting_dict["neutralIsoPtSum_2"]["x_bins"]="20,0,20"
	plotting_dict["footprintCorrection_2"]["x_bins"]="25,0,25"
	plotting_dict["puCorrPtSum_2"]["x_bins"]="20,0,80"
	plotting_dict["decayDistM_2"]["x_bins"]="20,0,1"
	plotting_dict["flightLengthSig_2"]["x_bins"]="24,-6,6"
	
	plotting_dict["iso_2"]["x_bins"]="50,0.5,1"
	plotting_dict["iso_1"]["x_bins"]="20,0.,0.2"
	variables_to_plot = ["pt_1"]
	#variables_to_plot = tau_iso_variables
	#variables_to_plot = ["MVAdxy_abs_2","MVAdxy_ip3d_abs_2"]

#	variables_to_plot=["flightLengthSig_2"]
	variables_to_plot=default_variables
	
	if args.quantities is not None:
		variables_to_plot=args.quantities
	for v in variables_to_plot:
		if not args.default:
			if decay_mode=="split":
				for dm in ["0","1","10","all"]:
					if True:	
						plot_root_variable(variable=v,xlabel=plotting_dict[v]["x_label"],x_bins=plotting_dict[v]["x_bins"],decay_mode=dm, isocut=isocut,channel=args.channel)
			else:
				plot_root_variable(variable=v,xlabel=plotting_dict[v]["x_label"],x_bins=plotting_dict[v]["x_bins"],decay_mode=decay_mode,isocut=isocut,channel=args.channel)
		else:
			default_plot_root_variable(variable=v)
	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""],n_processes=args.n_processes)
