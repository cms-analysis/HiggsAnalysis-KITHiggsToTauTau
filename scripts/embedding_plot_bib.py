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

### CP and spin quantities

# for eMinusmuPlus

eMinusmuPlus_PhiStarCP = pltcl.single_plot(
	name = "ePlusmuMinus_PhiStarCP",
	title = "Z#rightarrow#tau^{+}#tau^{-}#rightarrow#mu^{+}e^{-}+4#nu, E_{l^{#pm}}^{rest frame} > 0.44 GeV",
	x_expression = "genPhiStarCP",
	x_bins = "50,-0.2,6.5",
	y_label = "arbitary units",
	x_label = "#phi^{*}_{CP} [rad]",
	weight = "TauMProngEnergy > 0.44 && TauPProngEnergy > 0.44",
	wwwfolder = "",
	plot_type = "absolute",
	legend =[0.73,0.7,0.93,0.9],
	plotlines = [eMinusmuPlus_CP_spin_pythia, eMinusmuPlus_CP_spin_tauola]
	)

configs.extend(eMinusmuPlus_PhiStarCP.return_json_with_changed_x_and_weight(x_expressions = ["genPhiStarCP"]))


eMinusmuPlus_Zs = eMinusmuPlus_PhiStarCP.clone(
	name = "ePlusmuMinus_Zs",
	weight = "1",
	x_expression = "genZs",
	x_bins = "50,-0.5,0.5",
	x_label = "z_{s}")

configs.extend(eMinusmuPlus_Zs.return_json_with_changed_x_and_weight(x_expressions = ["genZs"]))


eMinusmuPlus_Zp_vs_Zm_pythia = pltcl.single_plot(
	name = "ePlusmuMinus_Zp_vs_Zm_pythia",
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
	name = "ePlusmuMinus_Zp_vs_Zm_tauola",
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

higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
