#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory

# em/em_combined_oneprong_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/em/em_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/em/em_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/em/em_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"e#mu, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/em/em_combined_oneprong_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# et/et_combined_a1_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/et/et_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/et/et_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/et/et_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"ea_{1}, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/et/et_combined_a1_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# et/et_combined_rho_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/et/et_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/et/et_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/et/et_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/omegaVisible_2/datacards/individual/et/et_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"e#rho, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				"\"#omega^{vis}\"" \"\" \"\" \"\" \
				--legend 0.45 0.5 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 kOrange-3 kOrange-3 kOrange-3 kOrange-3 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/et/et_combined_rho_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# et/et_combined_oneprong_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/et/et_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/et/et_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/et/et_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"e#pi, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/et/et_combined_oneprong_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# mt/mt_combined_a1_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/mt/mt_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/mt/mt_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/mt/mt_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"#mua_{1}, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/mt/mt_combined_a1_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# mt/mt_combined_rho_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/mt/mt_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/mt/mt_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/mt/mt_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/omegaVisible_2/datacards/individual/mt/mt_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"#mu#rho, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				"\"#omega^{vis}\"" \"\" \"\" \"\" \
				--legend 0.45 0.5 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 kOrange-3 kOrange-3 kOrange-3 kOrange-3 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/mt/mt_combined_rho_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# mt/mt_combined_oneprong_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/mt/mt_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/mt/mt_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/mt/mt_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"#mu#pi, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/mt/mt_combined_oneprong_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# tt/tt_combined_a1_a1
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/tt/tt_combined_a1_a1/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/tt/tt_combined_a1_a1/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/tt/tt_combined_a1_a1/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"a_{1}a_{1}, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/tt/tt_combined_a1_a1 --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# tt/tt_combined_a1_rho
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/tt/tt_combined_a1_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/tt/tt_combined_a1_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/tt/tt_combined_a1_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"a_{1}#rho+#rhoa_{1}, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/tt/tt_combined_a1_rho --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# tt/tt_combined_a1_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/tt/tt_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/tt/tt_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/tt/tt_combined_a1_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"a_{1}#pi+#pia_{1}, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/tt/tt_combined_a1_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# tt/tt_combined_rho_rho
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/tt/tt_combined_rho_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/tt/tt_combined_rho_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/tt/tt_combined_rho_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaVisible/datacards/individual/tt/tt_combined_rho_rho/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"#rho#rho, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				"\"#Omega^{vis}\"" \"\" \"\" \"\" \
				--legend 0.45 0.5 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 kOrange-3 kOrange-3 kOrange-3 kOrange-3 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/tt/tt_combined_rho_rho --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# tt/tt_combined_rho_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/tt/tt_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/tt/tt_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/tt/tt_combined_rho_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"#rho#pi+#pi#rho, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/tt/tt_combined_rho_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8

# tt/tt_combined_oneprong_oneprong
for POL_OPTION in "pol" "pol_r1"
do
	for UNC_OPTION in "tot_unc" "stat_unc"
	do
		for ZOOM_OPTION in " --x-lims -1 1 --y-lims 0 100" "_zoom --x-lims -0.3 0 --y-lims 0 10"
		do
			echo higgsplot.py -f limit -x pol -y "\"2*deltaNLL\"" --tree-draw-options TGraph --analysis-modules LikelihoodScan -i \
				$1/m_vis_combinedOmegaCategories/datacards/individual/tt/tt_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfit/datacards/individual/tt/tt_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				$1/combinedOmegaBarSvfitM91/datacards/individual/tt/tt_combined_oneprong_oneprong/higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0.root \
				--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				--title \"#pi#pi, `[[ ${UNC_OPTION} = "tot_unc" ]] && echo "tot. unc." || echo "stat. unc."`, `[[ ${POL_OPTION} = "pol" ]] && echo "r floating" || echo "r=1 fixed"`\" --labels \
				"\"m_{vis}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}\"" \"\" \"\" \"\" \
				"\"#bar{#Omega}_{m_{Z}}\"" \"\" \"\" \"\" \
				--legend 0.45 0.6 0.65 0.9 --legend-markers LP -m LP L L L LP L L L LP L L L -C 2 2 2 2 3 3 3 3 4 4 4 4 --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 1 1 2 3 \
				--formats pdf png --www $2/datacards/individual/tt/tt_combined_oneprong_oneprong --filename higgsCombine.${POL_OPTION}.${UNC_OPTION}.scan.MultiDimFit.mH0${ZOOM_OPTION} \
				--no-cache
		done
	done
done | runParallel.py -n 8
