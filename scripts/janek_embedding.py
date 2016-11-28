import argparse
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
from HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib import *
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


if __name__ == "__main__":
	configs = []

	data_trackcleaned_cleaned_legend = [0.43,0.60,0.96,0.85] 
	data_trackcleaned_cleaned_noratio_legend = [0.43,0.75,0.94,0.90]
	data_embedded_mirrored_cleaned_legend = [0.53,0.40,0.90,0.85]
	data_embedded_mirrored_legend = [0.53,0.50,0.90,0.85]
	data_embedded_mirrored_random_legend_upper_left = [0.21,0.55,0.60,0.90]
	data_embedded_mirrored_random_legend_upper_right = [0.52,0.55,0.91,0.90]
	data_embedded_mirrored_random_legend_lower_right = [0.52,0.20,0.91,0.55]
	data_embedded_mirrored_random_legend_lower_left = [0.21,0.20,0.60,0.55]

	#~ parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 #~ parents=[logger.loggingParser])

	#~ parser.add_argument("-i", "--input-file", required=True,
	                    #~ help="Input file.")
	                    
	                  
	#~ args = parser.parse_args()
	#~ print args.input_file
	selection_check_lMu_PPV = pltcl.single_plot(
		#num_file = args.input_file,
		name = "selection_check_lMu_PPV",
		title = "general selection",
		x_expression = "PtFlow",
		x_bins = "20,0.,4.",
		normalized_by_binwidth = False,
		wwwfolder = "",
		legend = data_embedded_mirrored_random_legend_lower_right,
		plot_type = "absolute",
		y_lims = [1,2e5],
		subplot_denominator = 0,
		subplot_numerators = [],
		y_subplot_lims = [0.85,1.15],
		y_subplot_label = "Ratio",
		y_label = "Events",
		x_label = "p_{T}-flow [GeV]",
		y_log = True,
		plotlines = [DoubleMuonEmbeddedPtFlowHistograms],
		)
	
	configs.extend(selection_check_lMu_PPV.return_json_with_changed_x_and_weight(
	x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_full"]
	))
	
	selection_check_lMu_PPV_peak = selection_check_lMu_PPV.clone(
		name = "selection_check_lMu_PPV_peak",
		legend = data_embedded_mirrored_random_legend_upper_left,
		title = "general selection & peak region"
		)
	
	configs.extend(selection_check_lMu_PPV_peak.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_peak"]
		))
	
	selection_check_lMu_PPV_sideband = selection_check_lMu_PPV.clone(
		name = "selection_check_lMu_PPV_sideband",
		legend = data_embedded_mirrored_random_legend_upper_left,
		title = "general selection & sideband region"
		)
	
	configs.extend(selection_check_lMu_PPV_sideband.return_json_with_changed_x_and_weight(
		x_expressions = ["leadingMuon_PhotonsFromFirstPVPtFlow_sideband"]
		))
	
	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
