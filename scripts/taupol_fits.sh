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
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_tot_stat_unc --formats pdf png \
		--no-cache
	
	# zoomed
	echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_tot_stat_unc.json \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` \
		-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -0.3 0.0 --title \"r floating\" --y-grid \
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_tot_stat_unc_zoom --formats pdf png \
		--no-cache

done | runParallel.py -n 8


# ===== r=1 fixed =================================================================================

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
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_r1_tot_stat_unc --formats pdf png \
		--no-cache
	
	# zoomed
	echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_r1_tot_stat_unc.json \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` \
		-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -0.3 0.0 --title \"r=1 fixed\" --y-grid \
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` --filename best_fit_pol_r1_tot_stat_unc_zoom --formats pdf png \
		--no-cache

done | runParallel.py -n 8


# ===== comparisons ===============================================================================

# channel comparison
annotate-trees.py $1/*/datacards/combined/higgsCombine*.root -t limit -b channel --values 0
annotate-trees.py $1/*/datacards/channel/mt/higgsCombine*.root -t limit -b channel --values 1
annotate-trees.py $1/*/datacards/channel/et/higgsCombine*.root -t limit -b channel --values 2
annotate-trees.py $1/*/datacards/channel/em/higgsCombine*.root -t limit -b channel --values 3
annotate-trees.py $1/*/datacards/channel/tt/higgsCombine*.root -t limit -b channel --values 4

for DIRECTORY in $1/*/datacards
do
	for POL_OPTION in "pol" "pol_r1"
	do
		for ZOOM_OPTION in " --y-lims -1 1" "_zoom --y-lims -0.3 0"
		do
			echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_${POL_OPTION}_over_channel_tot_stat_unc.json \
				-d "\"${DIRECTORY}/combined ${DIRECTORY}/channel/mt ${DIRECTORY}/channel/et ${DIRECTORY}/channel/em ${DIRECTORY}/channel/tt\"" \
				--x-ticks 0 1 2 3 4 --x-tick-labels comb. channel_mt_large channel_et_large channel_em_large channel_tt_large --x-lims -0.5 4.5 \
				--www $2/`echo ${DIRECTORY} | sed -e "s@${1}/@@g"`/combined --formats pdf png --filename best_fit_${POL_OPTION}_over_channel_tot_stat_unc${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

