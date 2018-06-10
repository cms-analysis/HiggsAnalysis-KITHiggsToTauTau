#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# ===== r floating ================================================================================

# combine

# total uncertainty + saving best fit values for each parameter in a workspace
combineTool.py -M MultiDimFit --algo singles -P pol --redefineSignalPOIs pol --there -n .pol.tot_unc --saveWorkspace -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

# statistical uncertainty
combineTool.py -M MultiDimFit --algo singles -P pol --redefineSignalPOIs pol --there -n .pol.stat_unc --freezeNuisanceGroups syst_plus_bbb -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.tot_unc.MultiDimFit.mH0.root --parallel 8

# plotting

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.tot_unc.MultiDimFit.mH0.root; do

	# full range
	echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_tot_stat_unc.json \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` \
		-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -1.0 1.0 --title \"r floating\" --y-grid \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_tot_stat_unc --formats pdf png \
		--no-cache
	
	# zoomed
	echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_tot_stat_unc.json \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` \
		-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -0.3 0.0 --title \"r floating\" --y-grid \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_tot_stat_unc_zoom --formats pdf png \
		--no-cache

done | runParallel.py -n 8


## ===== r=1 fixed =================================================================================

# combine

# total uncertainty + saving best fit values for each parameter in a workspace
combineTool.py -M MultiDimFit --algo singles -P pol --redefineSignalPOIs pol --freezeParameters r --there -n .pol_r1.tot_unc --saveWorkspace -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

# statistical uncertainty
combineTool.py -M MultiDimFit --algo singles -P pol --redefineSignalPOIs pol --freezeParameters r --there -n .pol_r1.stat_unc --freezeNuisanceGroups syst_plus_bbb -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root --parallel 8

# plotting

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root; do

	# full range
	echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_r1_tot_stat_unc.json \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` \
		-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -1.0 1.0 --title \"r=1 fixed\" --y-grid \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_r1_tot_stat_unc --formats pdf png \
		--no-cache
	
	# zoomed
	echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_r1_tot_stat_unc.json \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` \
		-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -0.3 0.0 --title \"r=1 fixed\" --y-grid \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_r1_tot_stat_unc_zoom --formats pdf png \
		--no-cache

done | runParallel.py -n 8

