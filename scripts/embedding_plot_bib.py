#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
from HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib import *

configs = []

'''# npu efficiency plots
muon_full_run2 = pltcl.single_plot(
	name = "muon_full_run2",
	title = "Run II",
	x_expression = "npv",
	x_bins = "1 5 9 13 17 21 25 29 33 38 43 50 61",
	wwwfolder="Efficiencies",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID & Iso)}{#mu(genMatched))}}",
	plot_type = "efficiency",
	subplot_denominator = 0,
	subplot_numerators = [1],
	plotlines = [run2_MC_full,run2_RH_full]
)
configs.extend(muon_full_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"npv"
		]
))


muon_iso_run2 = muon_full_run2.clone(
	plotlines = [run2_MC_iso,run2_RH_iso],
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & Iso)}{#mu(genMatched))}}"
)
configs.extend(muon_iso_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"npv"
		]
))

muon_id_run2 = muon_full_run2.clone(
	plotlines = [run2_MC_id,run2_RH_id],
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID)}{#mu(genMatched))}}"
)
configs.extend(muon_id_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"npv"
		]
))



# PtFlow plots

ptFlow_run2 = pltcl.single_plot(
	name = "ptFlow_run2",
	title = "Run II",
	x_expression = "leadingMuon_NeutralNoPUPtFlow",
	x_label = "#Delta R",
	y_label = "#Sigma p_{T} / #DeltaR ",
	y_subplot_label = "Embedding/MC",
	plot_type = "absolute",
	legend =[0.25,0.55,0.55,0.9],
	normalized_to_nevents = True,
	wwwfolder = "PtFlow",
	subplot_denominator = 0,
	subplot_numerators = [1],
	plotlines = [run2_MC_PtFlow,run2_RH_PtFlow]
)
configs.extend(ptFlow_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"leadingMuon_NeutralNoPUPtFlow",
#		"leadingMuon_ChargedNoPUPtFlow",
#		"leadingMuon_ChargedPUPtFlow",
#		"leadingMuon_PhotonsNoPUPtFlow",

#		"trailingMuon_NeutralNoPUPtFlow",
#		"trailingMuon_ChargedNoPUPtFlow",
#		"trailingMuon_ChargedPUPtFlow",
#		"trailingMuon_PhotonsNoPUPtFlow"
		]
))



### Plots for Zmumu selection of CMSSW skim

#Pt
zmumu_all_pt = pltcl.single_plot(
        name = "zmumu_all_pt",
        title = "Z#rightarrow#mu#mu MC (Run II): all Muons",
        x_expression = "ptMuons",
        x_label = "p^{#mu}_{T}",
        y_label = "Muons / bin width [GeV^{-1}]",
        y_subplot_label = "#frac{selection}{gen. filter}",
        wwwfolder = "",
        plot_type = "absolute",
        legend =[0.6,0.4,0.9,0.8],
        subplot_denominator = 0,
        subplot_numerators = [1,2,3],
        y_subplot_lims = [0.8,1.1],
        plotlines = [zmumu_genfilter_all,zmumu_baseline_all,zmumu_id_all,zmumu_id_and_trigger_all]
)
configs.extend(zmumu_all_pt.return_json_with_changed_x_and_weight(
        x_expressions=["ptMuons"]
))

zmumu_MC_matched_pt = zmumu_all_pt.clone(name = "zmumu_MC_matched_pt",
                                       title = "Z#rightarrow#mu#mu MC (Run II): MC matched Muons",
                                      plotlines = [zmumu_genfilter_MC_matched,
                                                   zmumu_baseline_MC_matched,
                                                   zmumu_id_MC_matched,
                                                   zmumu_id_and_trigger_MC_matched])
configs.extend(zmumu_MC_matched_pt.return_json_with_changed_x_and_weight(
        x_expressions=["ptMuons"]
))

zmumu_not_MC_matched_pt = zmumu_all_pt.clone(name = "zmumu_not_MC_matched_pt",
                                       title = "Z#rightarrow#mu#mu MC (Run II): not MC matched Muons",
                                          plotlines = [zmumu_genfilter_not_MC_matched,
                                                       zmumu_baseline_not_MC_matched,
                                                       zmumu_id_not_MC_matched,
                                                       zmumu_id_and_trigger_not_MC_matched])
configs.extend(zmumu_not_MC_matched_pt.return_json_with_changed_x_and_weight(
        x_expressions=["ptMuons"]
))

#Eta
zmumu_all_eta = pltcl.single_plot(
        name = "zmumu_all_eta",
        title = "Z#rightarrow#mu#mu MC (Run II): all Muons",
        x_expression = "etaMuons",
        x_label = "#eta^{#mu}",
        y_label = "Muons",
        y_subplot_label = "#frac{selection}{gen. filter}",
        wwwfolder = "",
        plot_type = "absolute",
        legend =[0.4,0.15,0.7,0.55],
        subplot_denominator = 0,
        subplot_numerators = [1,2,3],
        y_subplot_lims = [0.8,1.1],
        plotlines = [zmumu_genfilter_all,zmumu_baseline_all,zmumu_id_all,zmumu_id_and_trigger_all]
)
configs.extend(zmumu_all_eta.return_json_with_changed_x_and_weight(
        x_expressions=["etaMuons"]
))

zmumu_MC_matched_eta = zmumu_all_eta.clone(name = "zmumu_MC_matched_eta",
                                       title = "Z#rightarrow#mu#mu MC (Run II): MC matched Muons",
                                       plotlines = [zmumu_genfilter_MC_matched,
                                                    zmumu_baseline_MC_matched,
                                                    zmumu_id_MC_matched,
                                                    zmumu_id_and_trigger_MC_matched])
configs.extend(zmumu_MC_matched_eta.return_json_with_changed_x_and_weight(
        x_expressions=["etaMuons"]
))

zmumu_not_MC_matched_eta = zmumu_all_eta.clone(name = "zmumu_not_MC_matched_eta",
                                       title = "Z#rightarrow#mu#mu MC (Run II): not MC matched Muons",
                                           plotlines = [zmumu_genfilter_not_MC_matched,
                                                        zmumu_baseline_not_MC_matched,
                                                        zmumu_id_not_MC_matched,
                                                        zmumu_id_and_trigger_not_MC_matched],
                                           legend = [0.2,0.45,0.5,0.85])
configs.extend(zmumu_not_MC_matched_eta.return_json_with_changed_x_and_weight(
        x_expressions=["etaMuons"]
))


#nMuons
zmumu_all_n = pltcl.single_plot(
        name = "zmumu_all_n",
        title = "Z#rightarrow#mu#mu MC (Run II): all Muons",
        x_expression = "nMuons",
        x_label = "N^{#mu}",
        y_label = "Events",
        y_log = True,
        y_lims = [10000, 10000000],
        wwwfolder = "",
        plot_type = "absolute",
        legend =[0.65,0.75,0.95,0.9],
        plotlines = [zmumu_genfilter_all,zmumu_id_and_trigger_all]
)
configs.extend(zmumu_all_n.return_json_with_changed_x_and_weight(
        x_expressions=["nMuons"]
))


zmumu_MC_matched_n = zmumu_all_n.clone(name = "zmumu_MC_matched_n",
                                       title = "Z#rightarrow#mu#mu MC (Run II): MC matched Muons",
                                       plotlines = [zmumu_genfilter_MC_matched,
                                                    zmumu_id_and_trigger_MC_matched])
configs.extend(zmumu_MC_matched_n.return_json_with_changed_x_and_weight(
        x_expressions=["nMuons"]
))

zmumu_not_MC_matched_n = zmumu_all_n.clone(name = "zmumu_not_MC_matched_n",
                                       title = "Z#rightarrow#mu#mu MC (Run II): not MC matched Muons",
                                           plotlines = [zmumu_genfilter_not_MC_matched,
                                                        zmumu_id_and_trigger_not_MC_matched])
configs.extend(zmumu_not_MC_matched_n.return_json_with_changed_x_and_weight(
        x_expressions=["nMuons"]
))


### Acceptance efficiencies

#eMinusmuPlus
eMinusmuPlus_PtTauPlus = pltcl.single_plot(
	name = "eMinusmuPlus_PtTauPlus",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu",
	x_expression = "PtTauPlus",
	x_bins = "50,0,200",
	y_expression = "accEfficiency",
	x_label = "p^{#tau^{+}(gen)}_{T} [GeV]",
	y_label = "#scale[0.75]{#epsilon_{acc.} = #frac{passed}{attempted} per bin width [GeV^{-1}]}",
	wwwfolder = "",
	profiled = True,
	plot_type = "absolute",
	legend =[0.73,0.65,0.93,0.85],
	subplot_denominator = 1,
	subplot_numerators = [0],
	y_subplot_lims = [0.5,2],
	y_subplot_label = "#frac{pythia8}{tauola}",
	plotlines = [eMinusmuPlus_pythia, eMinusmuPlus_tauola]
	)

configs.extend(eMinusmuPlus_PtTauPlus.return_json_with_changed_x_and_weight(x_expressions = ["PtTauPlus"]))

eMinusmuPlus_PtTauMinus = eMinusmuPlus_PtTauPlus.clone(
	name = "eMinusmuPlus_PtTauMinus",
	x_expression = "PtTauMinus",
	x_label = "p^{#tau^{-}(gen)}_{T} [GeV]")

configs.extend(eMinusmuPlus_PtTauMinus.return_json_with_changed_x_and_weight(x_expressions = ["PtTauMinus"]))

eMinusmuPlus_pythia_2D = pltcl.single_plot(
	name = "eMinusmuPlus_pythia_2D",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu: pythia8",
	x_expression = "acc_eff_hist",
	y_expression = "acc_eff_hist",
	x_label = "p^{#tau^{-}(gen)}_{T} [GeV]",
	y_label = "p^{#tau^{+}(gen)}_{T} [GeV]",
	z_label = "#epsilon_{acceptance} per bin [GeV^{-2}]",
	z_lims = [0,1],
	plot_type = "absolute",
	wwwfolder = "",
	plotlines = [eMinusmuPlus_pythia_2D])

configs.extend(eMinusmuPlus_pythia_2D.return_json_with_changed_x_and_weight(x_expressions = ["acc_eff_hist"]))

eMinusmuPlus_tauola_2D = eMinusmuPlus_pythia_2D.clone(
	name = "eMinusmuPlus_tauola_2D",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu: tauola",
	plotlines = [eMinusmuPlus_tauola_2D])

configs.extend(eMinusmuPlus_tauola_2D.return_json_with_changed_x_and_weight(x_expressions = ["acc_eff_hist"]))


#ePlusmuMinus
ePlusmuMinus_PtTauPlus = pltcl.single_plot(
	name = "ePlusmuMinus_PtTauPlus",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrowe^{+}#mu^{-}+4#nu",
	x_expression = "PtTauPlus",
	x_bins = "50,0,200",
	y_expression = "accEfficiency",
	x_label = "p^{#tau^{+}(gen)}_{T} [GeV]",
	y_label = "#scale[0.75]{#epsilon_{acc.} = #frac{passed}{attempted} per bin width [GeV^{-1}]}",
	wwwfolder = "",
	profiled = True,
	plot_type = "absolute",
	legend =[0.73,0.65,0.93,0.85],
	subplot_denominator = 1,
	subplot_numerators = [0],
	y_subplot_lims = [0.5,2],
	y_subplot_label = "#frac{pythia8}{tauola}",
	plotlines = [ePlusmuMinus_pythia, ePlusmuMinus_tauola]
	)

configs.extend(ePlusmuMinus_PtTauPlus.return_json_with_changed_x_and_weight(x_expressions = ["PtTauPlus"]))

ePlusmuMinus_PtTauMinus = ePlusmuMinus_PtTauPlus.clone(
	name = "ePlusmuMinus_PtTauMinus",
	x_expression = "PtTauMinus",
	x_label = "p^{#tau^{-}(gen)}_{T} [GeV]")

configs.extend(ePlusmuMinus_PtTauMinus.return_json_with_changed_x_and_weight(x_expressions = ["PtTauMinus"]))


ePlusmuMinus_pythia_2D = pltcl.single_plot(
	name = "ePlusmuMinus_pythia_2D",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrowe^{+}#mu^{-}+4#nu: pythia8",
	x_expression = "acc_eff_hist",
	y_expression = "acc_eff_hist",
	x_label = "p^{#tau^{-}(gen)}_{T} [GeV]",
	y_label = "p^{#tau^{+}(gen)}_{T} [GeV]",
	z_label = "#epsilon_{acceptance} per bin [GeV^{-2}]",
	z_lims = [0,1],
	plot_type = "absolute",
	wwwfolder = "",
	plotlines = [ePlusmuMinus_pythia_2D])

configs.extend(ePlusmuMinus_pythia_2D.return_json_with_changed_x_and_weight(x_expressions = ["acc_eff_hist"]))

ePlusmuMinus_tauola_2D = ePlusmuMinus_pythia_2D.clone(
	name = "ePlusmuMinus_tauola_2D",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrowe^{+}#mu^{-}+4#nu: tauola",
	plotlines = [ePlusmuMinus_tauola_2D])

configs.extend(ePlusmuMinus_tauola_2D.return_json_with_changed_x_and_weight(x_expressions = ["acc_eff_hist"]))

#ePlusmuMinus Path1

ePlusmuMinus_PtTauPlus_path1 = pltcl.single_plot(
	name = "ePlusmuMinus_PtTauPlus_path1",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrowe^{+}#mu^{-}+4#nu (Path1 only)",
	x_expression = "PtTauPlus",
	x_bins = "50,0,200",
	y_expression = "accEfficiency",
	x_label = "p^{#tau^{+}(gen)}_{T} [GeV]",
	y_label = "#scale[0.75]{#epsilon_{acc.} = #frac{passed}{attempted} per bin width [GeV^{-1}]}",
	wwwfolder = "",
	profiled = True,
	plot_type = "absolute",
	legend =[0.73,0.65,0.93,0.85],
	plotlines = [ePlusmuMinus_tauola_path1]
	)

configs.extend(ePlusmuMinus_PtTauPlus_path1.return_json_with_changed_x_and_weight(x_expressions = ["PtTauPlus"]))

ePlusmuMinus_PtTauMinus_path1 = ePlusmuMinus_PtTauPlus_path1.clone(
	name = "ePlusmuMinus_PtTauMinus_path1",
	x_expression = "PtTauMinus",
	x_label = "p^{#tau^{-}(gen)}_{T} [GeV]")

configs.extend(ePlusmuMinus_PtTauMinus_path1.return_json_with_changed_x_and_weight(x_expressions = ["PtTauMinus"]))

'''
'''
### CP and spin quantities

# for eMinusmuPlus

eMinusmuPlus_PhiCP = pltcl.single_plot(
	name = "eMinusmuPlus_PhiCP",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu, E_{l^{#pm}}^{rest frame} > 0.44 GeV",
	x_expression = "genPhiCP",
	x_bins = "50,-0.2,6.5",
	y_label = "arbitary units",
	x_label = "#phi_{CP} [rad]",
	weight = "TauMProngEnergy > 0.44 && TauPProngEnergy > 0.44",
	wwwfolder = "",
	normalized_to_hist1 = True,
	plot_type = "absolute",
	legend =[0.73,0.7,0.93,0.9],
	plotlines = [eMinusmuPlus_CP_spin_pythia, eMinusmuPlus_CP_spin_tauola]
	)

configs.extend(eMinusmuPlus_PhiCP.return_json_with_changed_x_and_weight(x_expressions = ["genPhiCP"]))


eMinusmuPlus_Zs = eMinusmuPlus_PhiCP.clone(
	name = "eMinusmuPlus_Zs",
	weight = "1",
	x_expression = "genZs",
	x_bins = "50,-0.5,0.5",
	x_label = "z_{s}")

configs.extend(eMinusmuPlus_Zs.return_json_with_changed_x_and_weight(x_expressions = ["genZs"]))


eMinusmuPlus_Zp_vs_Zm_pythia = pltcl.single_plot(
	name = "eMinusmuPlus_Zp_vs_Zm_pythia",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu: pythia8",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [eMinusmuPlus_CP_spin_pythia_2D]
	)

configs.extend(eMinusmuPlus_Zp_vs_Zm_pythia.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))

eMinusmuPlus_Zp_vs_Zm_tauola = pltcl.single_plot(
	name = "eMinusmuPlus_Zp_vs_Zm_tauola",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu: tauola",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [eMinusmuPlus_CP_spin_tauola_2D]
	)

configs.extend(eMinusmuPlus_Zp_vs_Zm_tauola.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))


# for eMinusmuPlus (no cut)

eMinusmuPlus_PhiStarCP_nocut = pltcl.single_plot(
	name = "ePlusmuMinus_PhiStarCP_nocut",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu, E_{l^{#pm}}^{rest frame} > 0.44 GeV",
	x_expression = "genPhiStarCP",
	x_bins = "50,-0.2,6.5",
	y_label = "arbitary units",
	x_label = "#phi^{*}_{CP} [rad]",
	weight = "TauMProngEnergy > 0.44 && TauPProngEnergy > 0.44",
	wwwfolder = "",
	plot_type = "absolute",
	legend =[0.73,0.7,0.93,0.9],
	plotlines = [eMinusmuPlus_CP_spin_pythia_nocut, eMinusmuPlus_CP_spin_tauola_nocut]
	)

configs.extend(eMinusmuPlus_PhiStarCP_nocut.return_json_with_changed_x_and_weight(x_expressions = ["genPhiStarCP"]))


eMinusmuPlus_Zs_nocut = eMinusmuPlus_PhiStarCP_nocut.clone(
	name = "ePlusmuMinus_Zs_nocut",
	weight = "1",
	x_expression = "genZs",
	x_bins = "50,-0.5,0.5",
	x_label = "z_{s}")

configs.extend(eMinusmuPlus_Zs_nocut.return_json_with_changed_x_and_weight(x_expressions = ["genZs"]))


eMinusmuPlus_Zp_vs_Zm_pythia_nocut = pltcl.single_plot(
	name = "ePlusmuMinus_Zp_vs_Zm_pythia_nocut",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu: pythia8",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [eMinusmuPlus_CP_spin_pythia_2D_nocut]
	)

configs.extend(eMinusmuPlus_Zp_vs_Zm_pythia_nocut.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))

eMinusmuPlus_Zp_vs_Zm_tauola_nocut = pltcl.single_plot(
	name = "ePlusmuMinus_Zp_vs_Zm_tauola_nocut",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu: tauola",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [eMinusmuPlus_CP_spin_tauola_2D_nocut]
	)

configs.extend(eMinusmuPlus_Zp_vs_Zm_tauola_nocut.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))


# for PiPlusPiMinus

PiPlusPiMinus_PhiStarCP = pltcl.single_plot(
	name = "PiPlusPiMinus_PhiStarCP",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu",
	x_expression = "genPhiStarCP",
	x_bins = "50,-0.2,6.5",
	y_label = "arbitary units",
	x_label = "#phi^{*}_{CP} [rad]",
	wwwfolder = "",
	plot_type = "absolute",
	legend =[0.73,0.7,0.93,0.9],
	normalized_to_hist1 = True,
	plotlines = [PiPlusPiMinus_CP_spin_pythia, PiPlusPiMinus_CP_spin_tauola]
	)

configs.extend(PiPlusPiMinus_PhiStarCP.return_json_with_changed_x_and_weight(x_expressions = ["genPhiStarCP"]))


PiPlusPiMinus_Zs = PiPlusPiMinus_PhiStarCP.clone(
	name = "PiPlusPiMinus_Zs",
	x_expression = "genZs",
	x_bins = "50,-0.5,0.5",
	x_label = "z_{s}")

configs.extend(PiPlusPiMinus_Zs.return_json_with_changed_x_and_weight(x_expressions = ["genZs"]))


PiPlusPiMinus_Zp_vs_Zm_pythia = pltcl.single_plot(
	name = "PiPlusPiMinus_Zp_vs_Zm_pythia",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu: pythia8",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [PiPlusPiMinus_CP_spin_pythia_2D]
	)

configs.extend(PiPlusPiMinus_Zp_vs_Zm_pythia.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))

PiPlusPiMinus_Zp_vs_Zm_tauola = pltcl.single_plot(
	name = "PiPlusPiMinus_Zp_vs_Zm_tauola",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu: tauola",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [PiPlusPiMinus_CP_spin_tauola_2D]
	)

configs.extend(PiPlusPiMinus_Zp_vs_Zm_tauola.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))

PiPlusPiMinus_PtTauPlus = pltcl.single_plot(
	name = "PiPlusPiMinus_PtTauPlus",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu",
	x_expression = "PtTauPlus",
	x_bins = "50,0,200",
	y_lims = [0,0.6],
	y_expression = "accEfficiency",
	x_label = "p^{#tau^{+}(gen)}_{T} [GeV]",
	y_label = "#scale[0.75]{#epsilon_{acc.} = #frac{passed}{attempted} per bin width [GeV^{-1}]}",
	wwwfolder = "",
	profiled = True,
	plot_type = "absolute",
	legend =[0.73,0.65,0.93,0.85],
	subplot_denominator = 1,
	subplot_numerators = [0],
	y_subplot_lims = [0.5,2],
	y_subplot_label = "#frac{pythia8}{tauola}",
	plotlines = [PiPlusPiMinus_CP_spin_pythia, PiPlusPiMinus_CP_spin_tauola]
	)

configs.extend(PiPlusPiMinus_PtTauPlus.return_json_with_changed_x_and_weight(x_expressions = ["PtTauPlus"]))

PiPlusPiMinus_PtTauMinus = PiPlusPiMinus_PtTauPlus.clone(
	name = "PiPlusPiMinus_PtTauMinus",
	x_expression = "PtTauMinus",
	x_label = "p^{#tau^{-}(gen)}_{T} [GeV]")

configs.extend(PiPlusPiMinus_PtTauMinus.return_json_with_changed_x_and_weight(x_expressions = ["PtTauMinus"]))


# for PiPlusPiMinus (no cut)

PiPlusPiMinus_nocut_PhiStarCP = pltcl.single_plot(
	name = "PiPlusPiMinus_nocut_PhiStarCP",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu",
	x_expression = "genPhiStarCP",
	x_bins = "50,-0.2,6.5",
	y_label = "arbitary units",
	x_label = "#phi^{*}_{CP} [rad]",
	wwwfolder = "",
	plot_type = "absolute",
	legend =[0.73,0.7,0.93,0.9],
	normalized_to_hist1 = True,
	plotlines = [PiPlusPiMinus_CP_spin_pythia_nocut, PiPlusPiMinus_CP_spin_tauola_nocut]
	)

configs.extend(PiPlusPiMinus_nocut_PhiStarCP.return_json_with_changed_x_and_weight(x_expressions = ["genPhiStarCP"]))


PiPlusPiMinus_nocut_Zs = PiPlusPiMinus_nocut_PhiStarCP.clone(
	name = "PiPlusPiMinus_nocut_Zs",
	x_expression = "genZs",
	x_bins = "50,-0.5,0.5",
	x_label = "z_{s}")

configs.extend(PiPlusPiMinus_nocut_Zs.return_json_with_changed_x_and_weight(x_expressions = ["genZs"]))


PiPlusPiMinus_nocut_Zp_vs_Zm_pythia = pltcl.single_plot(
	name = "PiPlusPiMinus_nocut_Zp_vs_Zm_pythia",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu: pythia8",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [PiPlusPiMinus_CP_spin_pythia_2D_nocut]
	)

configs.extend(PiPlusPiMinus_nocut_Zp_vs_Zm_pythia.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))

PiPlusPiMinus_nocut_Zp_vs_Zm_tauola = pltcl.single_plot(
	name = "PiPlusPiMinus_nocut_Zp_vs_Zm_tauola",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu: tauola",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [PiPlusPiMinus_CP_spin_tauola_2D_nocut]
	)

configs.extend(PiPlusPiMinus_nocut_Zp_vs_Zm_tauola.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))


# for PiPlusPiMinus (no cut long)

PiPlusPiMinus_nocut_long_PhiStarCP = pltcl.single_plot(
	name = "PiPlusPiMinus_nocut_long_PhiStarCP",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu",
	x_expression = "genPhiStarCP",
	x_bins = "50,-0.2,6.5",
	y_label = "arbitary units",
	x_label = "#phi^{*}_{CP} [rad]",
	wwwfolder = "",
	plot_type = "absolute",
	legend =[0.73,0.7,0.93,0.9],
	normalized_to_hist1 = True,
	plotlines = [PiPlusPiMinus_CP_spin_pythia_nocut_long, PiPlusPiMinus_CP_spin_tauola_nocut_long]
	)

configs.extend(PiPlusPiMinus_nocut_long_PhiStarCP.return_json_with_changed_x_and_weight(x_expressions = ["genPhiStarCP"]))


PiPlusPiMinus_nocut_long_Zs = PiPlusPiMinus_nocut_long_PhiStarCP.clone(
	name = "PiPlusPiMinus_nocut_long_Zs",
	x_expression = "genZs",
	x_bins = "50,-0.5,0.5",
	x_label = "z_{s}")

configs.extend(PiPlusPiMinus_nocut_long_Zs.return_json_with_changed_x_and_weight(x_expressions = ["genZs"]))


PiPlusPiMinus_nocut_long_Zp_vs_Zm_pythia = pltcl.single_plot(
	name = "PiPlusPiMinus_nocut_long_Zp_vs_Zm_pythia",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu: pythia8",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [PiPlusPiMinus_CP_spin_pythia_2D_nocut_long]
	)

configs.extend(PiPlusPiMinus_nocut_long_Zp_vs_Zm_pythia.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))

PiPlusPiMinus_nocut_long_Zp_vs_Zm_tauola = pltcl.single_plot(
	name = "PiPlusPiMinus_nocut_long_Zp_vs_Zm_tauola",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#pi^{+}#pi^{-}+2#nu: tauola",
	x_expression = "genZPlus",
	y_expression = "genZMinus",
	x_bins = "50,0,1",
	y_bins = "50,0,1",
	x_label = "z_{+}",
	y_label = "z_{-}",
	wwwfolder = "",
	plot_type = "absolute",
	plotlines = [PiPlusPiMinus_CP_spin_tauola_2D_nocut_long]
	)

configs.extend(PiPlusPiMinus_nocut_long_Zp_vs_Zm_tauola.return_json_with_changed_x_and_weight(x_expressions = ["genZPlus"]))

# bare vs. dressed (emu channel)

FSR_pythia_diLepMass = pltcl.single_plot(
	name = "FSR_pythia_diLepMass",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu (pythia8): normalized to reco",
	x_expression = "diLepMass",
	x_bins = "50,0,150",
	x_label = "m_{#tau#tau}^{vis}",
	wwwfolder = "",
	legend =[0.68,0.65,0.93,0.85],
	plot_type = "absolute",
	normalized_to_hist1 = True,
	subplot_denominator = 1,
	subplot_numerators = [0,2],
	y_subplot_lims = [0.9,1.1],
	y_subplot_label = "#frac{dressed or reco}{bare}",
	plotlines = [Normal_pythia, Bare_pythia, Dressed_pythia]
	)

configs.extend(FSR_pythia_diLepMass.return_json_with_changed_x_and_weight(x_expressions = ["diLepMass"]))




FSRstudies_EM = pltcl.single_plot(
	name = "FSRstudies_EM",
	title = "",
	x_expression = "diLepMass",
	x_bins = "40 45 50 55 60 65 70 75 80 90 100 120 140",
	normalized_by_binwidth = True,
	x_label = "m_{#tau#tau}^{vis}",
	y_label = "#frac{dN}{dm} [GeV^{-1}]",
	wwwfolder = "",
	legend =[0.4,0.55,0.93,0.85],
	plot_type = "absolute",
	normalize_reference = 1,
	normalize_targets = [0,4],
	subplot_denominator = 1,
	subplot_numerators = [0,2,3],
	y_subplot_lims = [0.6,1.4],
	y_subplot_label = "#frac{Z#rightarrow#tau#tau sim.}{#mu#rightarrow#tau emb.}",
	plotlines = [FSRstudies_EM, FSRstudies_EM_emb_afterFSR, FSRstudies_EM_emb_afterFSR_up, FSRstudies_EM_emb_afterFSR_down, FSRstudies_EM_higgs],
	)

configs.extend(FSRstudies_EM.return_json_with_changed_x_and_weight(
	x_expressions = ["diLepMass"],
	weights = ["eventWeight"]
	))

FSRstudies_ET = FSRstudies_EM.clone(
	name = "FSRstudies_ET",
	title = "",
	legend =[0.4,0.55,0.9,0.85],
	plotlines = [FSRstudies_ET, FSRstudies_ET_emb_afterFSR, FSRstudies_ET_emb_afterFSR_up, FSRstudies_ET_emb_afterFSR_down, FSRstudies_ET_higgs]
	)

configs.extend(FSRstudies_ET.return_json_with_changed_x_and_weight(
	x_expressions = ["diLepMass"],
	weights = ["eventWeight"]
	))

FSRstudies_MT = FSRstudies_EM.clone(
	name = "FSRstudies_MT",
	title = "",
	legend =[0.4,0.55,0.9,0.85],
	plotlines = [FSRstudies_MT, FSRstudies_MT_emb_afterFSR, FSRstudies_MT_emb_afterFSR_up, FSRstudies_MT_emb_afterFSR_down, FSRstudies_MT_higgs]
	)

configs.extend(FSRstudies_MT.return_json_with_changed_x_and_weight(
	x_expressions = ["diLepMass"],
	weights = ["eventWeight"]
	))

FSRstudies_TT = FSRstudies_EM.clone(
	name = "FSRstudies_TT",
	title = "",
	legend =[0.4,0.55,0.9,0.85],
	plotlines = [FSRstudies_TT, FSRstudies_TT_emb_afterFSR, FSRstudies_TT_emb_afterFSR_up, FSRstudies_TT_emb_afterFSR_down, FSRstudies_TT_higgs]
	)

configs.extend(FSRstudies_TT.return_json_with_changed_x_and_weight(
	x_expressions = ["diLepMass"],
	weights = ["eventWeight"]
	))

### Embedding Cleaning Check

emb_clean_check_NE = pltcl.single_plot(
	name = "emb_clean_check_NE",
	title = "",
	x_expression = "NKappaElectrons",
	x_bins = "7,0,7",
	normalized_by_binwidth = False,
	x_label = "N_{e}",
	y_label = "Events",
	wwwfolder = "",
	legend =[0.6,0.55,0.95,0.85],
	plot_type = "absolute",
	subplot_denominator = 0,
	subplot_numerators = [1,2,3],
	y_subplot_lims = [0.85,1.15],
	y_subplot_label = "#frac{own work}{Run2015D}",
	plotlines = [DoubleMuonMINIAOD, DoubleMuonMINIAODonfly, DoubleMuonCleaned, DoubleMuonFullyCleaned],
)

configs.extend(emb_clean_check_NE.return_json_with_changed_x_and_weight(
	x_expressions = ["NKappaElectrons", "NKappaElectronsWithEtaCut", "NKappaElectronsWithPtCut","nElectrons","NKappaPackedPFCandidatesElectrons"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_NMu = emb_clean_check_NE.clone(
	name = "emb_clean_check_NMu",
	x_expression = "NKappaMuons",
	x_bins = "5,2,7",
	x_label = "N_{#mu}",
	y_subplot_lims = [0.9,1.1],
)

configs.extend(emb_clean_check_NMu.return_json_with_changed_x_and_weight(
	x_expressions = ["NKappaMuons","NKappaGlobalMuons", "NKappaGlobalMuonsWithPtCut", "NKappaPackedPFCandidatesMuons"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)", "(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_NPFC = emb_clean_check_NE.clone(
	name = "emb_clean_check_NPFC",
	x_expression = "NKappaPackedPFCandidates",
	x_bins = "20,300,2000",
	y_subplot_lims = [0.95,1.05],
	x_label = "N_{PF cand.}"
)

configs.extend(emb_clean_check_NPFC.return_json_with_changed_x_and_weight(
	x_expressions = ["NKappaPackedPFCandidates"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_NPFCPh = emb_clean_check_NE.clone(
	name = "emb_clean_check_NPFC",
	x_expression = "NKappaPackedPFCandidatesPhotons",
	x_bins = "60,0,300",
	y_subplot_lims = [0.95,1.05],
	x_label = "N_{PF cand.}"
)

configs.extend(emb_clean_check_NPFCPh.return_json_with_changed_x_and_weight(
	x_expressions = ["NKappaPackedPFCandidatesPhotons"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_NPFCCH = emb_clean_check_NE.clone(
	name = "emb_clean_check_NPFC",
	x_expression = "NKappaPackedPFCandidatesChargedHadrons",
	y_subplot_lims = [0.95,1.05],
	x_bins = "160,0,800",
	x_label = "N_{PF cand.}"
)

configs.extend(emb_clean_check_NPFCCH.return_json_with_changed_x_and_weight(
	x_expressions = ["NKappaPackedPFCandidatesChargedHadrons"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_NPFCNH = emb_clean_check_NE.clone(
	name = "emb_clean_check_NPFC",
	x_expression = "NKappaPackedPFCandidatesNeutralHadrons",
	x_bins = "20,0,100",
	y_subplot_lims = [0.85,1.15],
	x_label = "N_{PF cand.}"
)

configs.extend(emb_clean_check_NPFCNH.return_json_with_changed_x_and_weight(
	x_expressions = ["NKappaPackedPFCandidatesNeutralHadrons"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_NPFCR = emb_clean_check_NE.clone(
	name = "emb_clean_check_NPFC",
	x_expression = "NKappaPackedPFCandidatesNeutralRemaining",
	x_bins = "70,100,800",
	x_label = "N_{PF cand.}",
	legend =[0.2,0.25,0.55,0.55],
)

configs.extend(emb_clean_check_NPFCR.return_json_with_changed_x_and_weight(
	x_expressions = ["NKappaPackedPFCandidatesRemaining"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))


emb_clean_check_RunNumber = emb_clean_check_NE.clone(
	name = "emb_clean_check_RunNumber",
	x_expression = "RunNumber",
	x_bins = "50,256600,260800",
	normalized_to_nevents = False,
	x_label = "Run Number",
	y_label = "Events",
	y_subplot_lims = [0.98,1.02]
)

configs.extend(emb_clean_check_RunNumber.return_json_with_changed_x_and_weight(
	x_expressions = ["run"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_EventCounter = emb_clean_check_NE.clone(
	name = "emb_clean_check_EventCounter",
	x_expression = "EventCounter",
	x_bins = "1,1,2",
	x_label = "EventCounter",
	y_label = "Events",
	y_subplot_lims = [0.98,1.02],
	normalized_to_nevents = False
)

configs.extend(emb_clean_check_EventCounter.return_json_with_changed_x_and_weight(
	x_expressions = ["EventCounter"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_MuonPt = emb_clean_check_NE.clone(
	name = "emb_clean_check_MuonPt",
	x_expression = "leadingMuonPt",
	x_bins = "50,0,160",
	x_label = "p_{T}^{#mu}"
)

configs.extend(emb_clean_check_MuonPt.return_json_with_changed_x_and_weight(
	x_expressions = ["leadingMuonPt", "trailingMuonPt"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)", "(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_electronsPt = emb_clean_check_NE.clone(
	name = "emb_clean_check_electronsPt",
	x_expression = "electronPts",
	y_label = "electrons/bin width [GeV^{-1}]",
	x_bins = "70,0,70",
	x_label = "p_{T}^{e}"
)

configs.extend(emb_clean_check_electronsPt.return_json_with_changed_x_and_weight(
	x_expressions = ["electronPts","looseElectronPts"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)", "(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_MET = emb_clean_check_NE.clone(
	name = "emb_clean_check_MET",
	x_expression = "PFCandidatesMET",
	x_bins = "50,0,100",
	y_subplot_lims = [0.75,1.25],
	x_label = "missing E_{T}"
)

configs.extend(emb_clean_check_MET.return_json_with_changed_x_and_weight(
	x_expressions = ["PFCandidatesMET", "SumPtPFChargedHadrons", "SumPtPFNeutralHadrons", "SumPtPFPhotons", "SumPtPFElectrons", "SumPtPFMuons"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))

emb_clean_check_sumPT = emb_clean_check_NE.clone(
	name = "emb_clean_check_sumPT",
	x_expression = "PFCandidatesMET",
	x_bins = "50,0,100",
	y_subplot_lims = [0.75,1.25],
	x_label = "|#sum#vec{p_{T}}|"
)

configs.extend(emb_clean_check_sumPT.return_json_with_changed_x_and_weight(
	x_expressions = ["SumPtPFChargedHadrons", "SumPtPFNeutralHadrons", "SumPtPFPhotons", "SumPtPFElectrons"],
#	weights = ["(RunNumber != 257613)*(RunNumber < 258500)"]
	))


emb_clean_check_deltaR = emb_clean_check_NE.clone(
	name = "emb_clean_check_deltaR",
	x_expression = "deltaRsElectronMuon",
	y_label = "electrons/bin width",
	y_subplot_lims = [0.8,1.2],
	x_bins = "40,0,4",
	x_label = "min_{#mu}#DeltaR_{e,#mu}"
)

configs.extend(emb_clean_check_deltaR.return_json_with_changed_x_and_weight(
	x_expressions = ["deltaRsElectronMuon", "deltaRslooseElectronMuon"],
#	weights = ["deltaRsElectronMuon>0"]
	))

emb_clean_check_deltaEta = emb_clean_check_NE.clone(
	name = "emb_clean_check_deltaEta",
	x_expression = "deltaEtasElectronMuon",
	y_label = "electrons/bin width",
	y_subplot_lims = [0.8,1.2],
	x_bins = "40,0,4",
	x_label = "min_{#mu}#Delta#eta_{e,#mu}"
)

configs.extend(emb_clean_check_deltaEta.return_json_with_changed_x_and_weight(
	x_expressions = ["deltaEtasElectronMuon", "deltaEtaslooseElectronMuon"],
#	weights = ["deltaEtasElectronMuon>0"]
	))

emb_clean_check_deltaPhi = emb_clean_check_NE.clone(
	name = "emb_clean_check_deltaPhi",
	x_expression = "deltaPhisElectronMuon",
	y_label = "electrons/bin width",
	y_subplot_lims = [0.8,1.2],
	x_bins = "40,0,4",
	x_label = "min_{#mu}#Delta#phi_{e,#mu}"
)

configs.extend(emb_clean_check_deltaPhi.return_json_with_changed_x_and_weight(
	x_expressions = ["deltaPhisElectronMuon", "deltaPhislooseElectronMuon"],
#	weights = ["deltaPhisElectronMuon>0"]
	))


'''
vtx_check_dxy_MM = pltcl.single_plot(
	name = "vtx_check_dxy_MM",
	x_expression = "vtx_dxy",
	x_label = "#Deltaxy [cm]",
	y_lims = [0,900000],
	wwwfolder = "",
	title = "Z#rightarrow#mu#mu: MC vs. Embedded",
	plot_type = "absolute",
	plotlines = [vtx_corrected_MM],
)

configs.extend(vtx_check_dxy_MM.return_json_with_changed_x_and_weight(
	x_expressions = ["vtx_dxy"],
	))

vtx_check_dz_MM = vtx_check_dxy_MM.clone(
	name = "vtx_check_dz_MM",
	x_expression = "vtx_dz",
	x_label = "#Deltaz [cm]"
)

configs.extend(vtx_check_dz_MM.return_json_with_changed_x_and_weight(
	x_expressions = ["vtx_dz"],
	))

# Merging Check for Muon Embedding

merging_check_NPFE = pltcl.single_plot(
	name = "merging_check_NPFE",
	title = "",
	x_expression = "NPFElectrons",
	x_bins = "7,0,7",
	normalized_by_binwidth = False,
	x_label = "N_{e}",
	y_label = "Events",
	wwwfolder = "",
	legend =[0.6,0.55,0.95,0.85],
	plot_type = "absolute",
	subplot_denominator = 0,
	subplot_numerators = [1,2],
	y_subplot_lims = [0.85,1.15],
	y_subplot_label = "#frac{own work}{Run2015D}",
	plotlines = [DoubleMuonSelected, DoubleMuonMerged, DoubleMuonCleaned]
)

configs.extend(merging_check_NPFE.return_json_with_changed_x_and_weight(
	x_expressions = ["NPFElectrons"]
	))

merging_check_NPFMu = merging_check_NPFE.clone(
	name = "emb_clean_check_NPFMu",
	x_expression = "NPFMuons",
	x_bins = "7,0,7",
	x_label = "N_{#mu}",
	subplot_numerators = [1],
	y_subplot_lims = [0.9,1.1],
	plotlines = [DoubleMuonSelected, DoubleMuonMerged]
)

configs.extend(merging_check_NPFMu.return_json_with_changed_x_and_weight(
	x_expressions = ["NPFMuons"]
	))

merging_check_NPFC = merging_check_NPFE.clone(
	name = "merging_check_NPFC",
	x_expression = "NPFCandidates",
	x_bins = "20,300,2000",
	y_subplot_lims = [0.95,1.05],
	x_label = "N_{PF}"
)

configs.extend(merging_check_NPFC.return_json_with_changed_x_and_weight(
	x_expressions = ["NPFCandidates"]
	))

merging_check_NPFPh = merging_check_NPFE.clone(
	name = "merging_check_NPFPh",
	x_expression = "NPFPhotons",
	x_bins = "60,0,300",
	y_subplot_lims = [0.95,1.05],
	x_label = "N_{ph}"
)

configs.extend(merging_check_NPFPh.return_json_with_changed_x_and_weight(
	x_expressions = ["NPFPhotons"]
	))

merging_check_NPFCH = merging_check_NPFE.clone(
	name = "merging_check_NPFCH",
	x_expression = "NPFChargedHadrons",
	y_subplot_lims = [0.95,1.05],
	x_bins = "160,0,800",
	x_label = "N_{ch}"
)

configs.extend(merging_check_NPFCH.return_json_with_changed_x_and_weight(
	x_expressions = ["NPFChargedHadrons"]
	))

merging_check_NPFNH = merging_check_NPFE.clone(
	name = "merging_check_NPFNH",
	x_expression = "NPFNeutralHadrons",
	x_bins = "20,0,100",
	y_subplot_lims = [0.85,1.15],
	x_label = "N_{nh}"
)

configs.extend(merging_check_NPFNH.return_json_with_changed_x_and_weight(
	x_expressions = ["NPFNeutralHadrons"]
	))

merging_check_sumPt = merging_check_NPFE.clone(
	name = "merging_check_sumPt",
	x_expression = "PFSumPt",
	x_bins = "50,0,100",
	subplot_numerators = [1],
	y_subplot_lims = [0.75,1.25],
	plotlines = [DoubleMuonSelected, DoubleMuonMerged],
	x_label = "|#sum#vec{p_{T}}|"
)

configs.extend(merging_check_sumPt.return_json_with_changed_x_and_weight(
	x_expressions = ["PFSumPt"]
	))

merging_check_sumHt = merging_check_NPFE.clone(
	name = "merging_check_sumHt",
	x_expression = "PFSumHt",
	x_bins = "50,0,2000",
	subplot_numerators = [1],
	y_subplot_lims = [0.75,1.25],
	plotlines = [DoubleMuonSelected, DoubleMuonMerged],
	x_label = "|#sump_{T}|"
)

configs.extend(merging_check_sumHt.return_json_with_changed_x_and_weight(
	x_expressions = ["PFSumHt"]
	))

# Zmumu selection Check for Muon Embedding
selection_check_ZMass = pltcl.single_plot(
	name = "selection_check_ZMass",
	title = "",
	x_expression = "ZMass",
	x_bins = "50,20,120",
	normalized_by_binwidth = False,
	x_label = "m(#mu#mu)",
	y_label = "Events",
	wwwfolder = "",
	legend =[0.4,0.4,0.75,0.7],
	plot_type = "absolute",
	subplot_denominator = 0,
	subplot_numerators = [1,2],
	y_subplot_lims = [0.85,1.15],
	y_subplot_label = "#frac{own work}{Run2015D}",
	plotlines = [DoubleMuonSelectedValidation, DoubleMuonMergedValidation, DoubleMuonMirroredValidation]
)

configs.extend(selection_check_ZMass.return_json_with_changed_x_and_weight(
	x_expressions = ["ZMass"]
	))

selection_check_leadingMuPt = selection_check_ZMass.clone(
	name = "selection_check_leadingMuPt",
	x_bins = "70,0,140",
	legend =[0.6,0.55,0.95,0.85],
	x_expression = "leadingLeptonFromZPt",
	x_label = "p_{T}(leading #mu)"
)

configs.extend(selection_check_leadingMuPt.return_json_with_changed_x_and_weight(
	x_expressions = ["leadingLeptonFromZPt"]
	))
	
selection_check_leadingMuEta = selection_check_ZMass.clone(
	name = "selection_check_leadingMuEta",
	x_expression = "leadingLeptonFromZEta",
	legend =[0.4,0.25,0.75,0.55],
	x_bins = "50,-3,3",
	x_label = "#eta(leading #mu)"
)

configs.extend(selection_check_leadingMuEta.return_json_with_changed_x_and_weight(
	x_expressions = ["leadingLeptonFromZEta"]
	))

selection_check_leadingMuPhi = selection_check_ZMass.clone(
	name = "selection_check_leadingMuPhi",
	x_expression = "leadingLeptonFromZPhi",
	legend =[0.4,0.25,0.75,0.55],
	x_bins = "50,-3.5,3.5",
	x_label = "#phi(leading #mu)"
)

configs.extend(selection_check_leadingMuPhi.return_json_with_changed_x_and_weight(
	x_expressions = ["leadingLeptonFromZPhi"]
	))

selection_check_trailingMuPt = selection_check_ZMass.clone(
	name = "selection_check_trailingMuPt",
	x_bins = "50,0,100",
	legend =[0.6,0.55,0.95,0.85],
	x_expression = "trailingLeptonFromZPt",
	x_label = "p_{T}(trailing #mu)"
)

configs.extend(selection_check_trailingMuPt.return_json_with_changed_x_and_weight(
	x_expressions = ["trailingLeptonFromZPt"]
	))
	
selection_check_trailingMuEta = selection_check_ZMass.clone(
	name = "selection_check_trailingMuEta",
	x_expression = "trailingLeptonFromZEta",
	legend =[0.4,0.25,0.75,0.55],
	x_bins = "50,-3,3",
	x_label = "#eta(trailing #mu)"
)

configs.extend(selection_check_trailingMuEta.return_json_with_changed_x_and_weight(
	x_expressions = ["trailingLeptonFromZEta"]
	))

selection_check_trailingMuPhi = selection_check_ZMass.clone(
	name = "selection_check_trailingMuPhi",
	x_expression = "trailingLeptonFromZPhi",
	legend =[0.4,0.25,0.75,0.55],
	x_bins = "50,-3.5,3.5",
	x_label = "#phi(trailing #mu)"
)

configs.extend(selection_check_trailingMuPhi.return_json_with_changed_x_and_weight(
	x_expressions = ["trailingLeptonFromZPhi"]
	))

higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
