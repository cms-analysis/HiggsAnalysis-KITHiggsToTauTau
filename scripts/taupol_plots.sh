#!/bin/sh

for x in mvis omegabar; do

#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/mt/{1010,1020,1030}`" --filename best_fit_pol_over_individual_mt_rho_a1_oneprong --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{#mu#rho}" "" "" "#scale[2]{#mua_{1}}" "" "#scale[2]{#mu#pi}" --y-lims -0.5 0.3

#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/mt/{1012,1022,1032}`" --filename best_fit_pol_over_individual_mt_rho_2_a1_2_oneprong_2 --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{#mu#rho}" "" "" "#scale[2]{#mua_{1}}" "" "#scale[2]{#mu#pi}" --y-lims -0.5 0.3

#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/mt/1031`" --filename best_fit_pol_over_individual_mt_oneprong_1 --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "" "" "" "" "" "#scale[2]{#mu#tau_{h}}" --y-lims -0.5 0.3


#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/et/{1010,1020,1030}`" --filename best_fit_pol_over_individual_et_rho_a1_oneprong --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{e#rho}" "" "" "#scale[2]{ea_{1}}" "" "#scale[2]{e#pi}" --y-lims -0.5 0.3

#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/et/{1012,1021,1032}`" --filename best_fit_pol_over_individual_et_rho_2_a1_2_oneprong_2 --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{e#rho}" "" "" "#scale[2]{ea_{1}}" "" "#scale[2]{e#pi}" --y-lims -0.5 0.3

#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/et/1031`" --filename best_fit_pol_over_individual_et_oneprong_1 --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "" "" "" "" "" "#scale[2]{e#tau_{h}}" --y-lims -0.5 0.3


#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/tt/{1010,1020,1030}`" --filename best_fit_pol_over_individual_tt_rho_a1_oneprong --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{#rho+#tau_{h}}" "" "" "#scale[2]{a_{1}+#tau_{h}}" "" "#scale[2]{#pi+#tau_{h}}" --y-lims -0.5 0.3

#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/tt/{1012,1022,1032}`" --filename best_fit_pol_over_individual_tt_rho_2_a1_2_oneprong_2 --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{#tau_{h}#rho}" "" "" "#scale[2]{#tau_{h}a_{1}}" "" "#scale[2]{#tau_{h}#pi}" --y-lims -0.5 0.3

#	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/tt/{1011,1021,1031}`" --filename best_fit_pol_over_individual_tt_rho_1_a1_1_oneprong_1 --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{#rho#tau_{h}}" "" "" "#scale[2]{a_{1}#tau_{h}}" "" "#scale[2]{#pi#tau_{h}}" --y-lims -0.5 0.3




	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/mt/{1040,1050,1060}`" --filename best_fit_pol_over_individual_mt_combined --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{#mu#rho}" "" "" "#scale[2]{#mua_{1}}" "" "#scale[2]{#mu#pi}" --y-lims -0.5 0.3

	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/et/{1040,1050,1060}`" --filename best_fit_pol_over_individual_et_combined --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "" "" "#scale[2]{e#rho}" "" "" "#scale[2]{ea_{1}}" "" "#scale[2]{e#pi}" --y-lims -0.5 0.3

	higgsplot.py --www taupol/fits/$x --formats pdf png -C kRed --x-lims 0.5 8.5 -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_individual.json -d "`ls -1d plots/2018-05-14_ztt_polarisation_datacards_$x/datacards/individual/tt/{1040,1050,1060,1070,1080,1090}`" --filename best_fit_pol_over_individual_tt_combined --x-ticks 1 2 3 4 5 6 7 8 --x-tick-labels "#scale[2]{#rho+#rho}" "#scale[2]{#rho+a_{1}}" "#scale[2]{#rho+#pi}" "" "#scale[2]{a_{1}+a_{1}}" "#scale[2]{a_{1}+#pi}" "" "#scale[2]{#pi+#pi}" --y-lims -0.5 0.3


done
