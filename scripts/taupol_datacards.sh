#!/bin/sh

# Mandatory options
# $1: artus output directory
# $2: datacards output base directory


# ===== omegaBarSvfit =============================================================================

# polarisationOmegaBarSvfit_1 (em, et, mt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/omegaBarSvfit_1 -c em --categories em_oneprong_1 -c et --categories et_oneprong_1 -c mt --categories mt_oneprong_1 --clear-output-dir --use-asimov-dataset

# polarisationOmegaBarSvfit_1 (em, et, mt), polarisationOmegaBarSvfit_1/2 (tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/omegaBarSvfit_2 -c em --categories em_oneprong_2 -c et --categories et_a1 et_rho et_oneprong -c mt --categories mt_a1 mt_rho mt_oneprong -c tt --categories tt_a1 tt_rho tt_oneprong --clear-output-dir --use-asimov-dataset

# polarisationCombinedOmegaBarSvfit (em, et, mt, tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/polarisationCombinedOmegaBarSvfit -c em --categories em_combined_oneprong_oneprong -c et --categories et_combined_a1_oneprong et_combined_rho_oneprong et_combined_oneprong_oneprong -c mt --categories mt_combined_a1_oneprong mt_combined_rho_oneprong mt_combined_oneprong_oneprong -c tt --categories tt_combined_a1_a1 tt_combined_a1_rho tt_combined_a1_oneprong tt_combined_rho_rho tt_combined_rho_oneprong tt_combined_oneprong_oneprong --clear-output-dir --use-asimov-dataset


# ===== omegaBarSvfitM91 ==========================================================================

# polarisationOmegaBarSvfitM91_1 (em, et, mt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/omegaBarSvfitM91_1 -c em --categories em_oneprong_1 -c et --categories et_oneprong_1 -c mt --categories mt_oneprong_1 --clear-output-dir --use-asimov-dataset --omega-version BarSvfitM91

# polarisationOmegaBarSvfitM91_1 (em, et, mt), polarisationOmegaBarSvfit_1/2 (tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/omegaBarSvfitM91_2 -c em --categories em_oneprong_2 -c et --categories et_a1 et_rho et_oneprong -c mt --categories mt_a1 mt_rho mt_oneprong -c tt --categories tt_a1 tt_rho tt_oneprong --clear-output-dir --use-asimov-dataset --omega-version BarSvfitM91

# polarisationCombinedOmegaBarSvfitM91 (em, et, mt, tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/polarisationCombinedOmegaBarSvfitM91 -c em --categories em_combined_oneprong_oneprong -c et --categories et_combined_a1_oneprong et_combined_rho_oneprong et_combined_oneprong_oneprong -c mt --categories mt_combined_a1_oneprong mt_combined_rho_oneprong mt_combined_oneprong_oneprong -c tt --categories tt_combined_a1_a1 tt_combined_a1_rho tt_combined_a1_oneprong tt_combined_rho_rho tt_combined_rho_oneprong tt_combined_oneprong_oneprong --clear-output-dir --use-asimov-dataset --omega-version BarSvfitM91


# ===== omegaVisible(Svfit) =======================================================================

# polarisationOmegaVisibleSvfit_1 (et, mt), polarisationOmegaBarSvfit_1/2 (tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/omegaVisible_2 -c et --categories et_rho -c mt --categories mt_rho -c tt --categories tt_rho --clear-output-dir --use-asimov-dataset --omega-version VisibleSvfit

# polarisationCombinedOmegaVisibleSvfit (tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/polarisationCombinedOmegaVisible -c tt --categories tt_combined_rho_rho --clear-output-dir --use-asimov-dataset --omega-version VisibleSvfit


# ===== visible mass ==============================================================================

# m_vis, inclusive (em, et, mt, tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/m_vis_inclusive -c em --categories em_oneprong_1 -c et --categories et_oneprong_1 -c mt --categories mt_oneprong_1 -c tt --categories inclusive --clear-output-dir --use-asimov-dataset -x m_vis

# m_vis, omega categorisation (em, et, mt, tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/m_vis_omegaCategories -c em --categories em_oneprong_2 -c et --categories et_a1 et_rho et_oneprong -c mt --categories mt_a1 mt_rho mt_oneprong -c tt --categories tt_a1 tt_rho tt_oneprong --clear-output-dir --use-asimov-dataset -x m_vis

# m_vis, combinedOmega categorisation (em, et, mt, tt)
$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation_shared.py -i $1 -n 8 -o $2/m_vis_combinedOmegaCategories -c em --categories em_combined_oneprong_oneprong -c et --categories et_combined_a1_oneprong et_combined_rho_oneprong et_combined_oneprong_oneprong -c mt --categories mt_combined_a1_oneprong mt_combined_rho_oneprong mt_combined_oneprong_oneprong -c tt --categories tt_combined_a1_a1 tt_combined_a1_rho tt_combined_a1_oneprong tt_combined_rho_rho tt_combined_rho_oneprong tt_combined_oneprong_oneprong --clear-output-dir --use-asimov-dataset -x m_vis


# ===== text2workspace ============================================================================

combineTool.py -M T2W -o workspace.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol -m 0 -i $2/*/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt --parallel 8

