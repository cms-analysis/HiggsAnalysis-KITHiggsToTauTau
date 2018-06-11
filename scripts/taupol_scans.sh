#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# ===== r floating ================================================================================

# combine

# total uncertainty + saving best fit values for each parameter in a workspace
combineTool.py -M MultiDimFit --points 200 --redefineSignalPOIs pol --algo grid --there -n .pol.tot_unc.scan --saveWorkspace -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

# statistical uncertainty
combineTool.py -M MultiDimFit --points 200 --redefineSignalPOIs pol --algo grid --there -n .pol.stat_unc.scan --freezeNuisanceGroups syst_plus_bbb -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root --parallel 8

# plotting

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root; do
	
	# full range
	echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol.stat_unc.scan.MultiDimFit.mH0.root@g"` \
		-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -1 1 --y-lims 0 100 \
		--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r floating\"" -m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
		--labels \"Stat. + Syst.\" \"\" \"\" \"\" \"Stat.\" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol.scan.MultiDimFit.mH0 --formats pdf png \
		--no-cache
	
	# zoomed
	echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol.stat_unc.scan.MultiDimFit.mH0.root@g"` \
		-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -0.3 0 --y-lims 0 10 \
		--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r floating\"" -m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
		--labels "\"Stat. + Syst.\"" \"\" \"\" \"\" "\"Stat.\"" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol.scan.MultiDimFit.mH0_zoom --formats pdf png \
		--no-cache

done | runParallel.py -n 8


# ===== r=1 fixed =================================================================================

# combine

# total uncertainty + saving best fit values for each parameter in a workspace
combineTool.py -M MultiDimFit --points 200 --redefineSignalPOIs pol --freezeParameters r --algo grid --there -n .pol_r1.tot_unc.scan --saveWorkspace -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

# statistical uncertainty
combineTool.py -M MultiDimFit --points 200 --redefineSignalPOIs pol --freezeParameters r --algo grid --there -n .pol_r1.stat_unc.scan --freezeNuisanceGroups syst_plus_bbb -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root --parallel 8

# plotting

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root; do
	
	# full range
	echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol_r1.stat_unc.scan.MultiDimFit.mH0.root@g"` \
		-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -1 1 --y-lims 0 100 \
		--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r=1 fixed\"" -m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
		--labels \"Stat. + Syst.\" \"\" \"\" \"\" \"Stat.\" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol_r1.scan.MultiDimFit.mH0 --formats pdf png \
		--no-cache
	
	# zoomed
	echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol_r1.stat_unc.scan.MultiDimFit.mH0.root@g"` \
		-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -0.3 0 --y-lims 0 10 \
		--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r=1 fixed\"" -m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
		--labels "\"Stat. + Syst.\"" \"\" \"\" \"\" "\"Stat.\"" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
		--www $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol_r1.scan.MultiDimFit.mH0_zoom --formats pdf png \
		--no-cache

done | runParallel.py -n 8

