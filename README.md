# KITHiggsToTauTau Analysis Code

## Dependencies
- Kappa: git clone https://github.com/KappaAnalysis/Kappa.git
- KappaTools: git clone https://github.com/KappaAnalysis/KappaTools.git
- Artus+HarryPlotter: git clone https://github.com/artus-analysis/Artus.git
- More documentation and recipes: [TWiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/KITHiggsAnalysisWorkflow#AnalYsisARTUS)

## Location of Files

For the [Artus repository](https://github.com/artus-analysis/Artus) a similar understanding of the directories applies.

### C++
- [interface](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/interface) and [src](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/src): code that is compiled in libraries
	- No subdirectory: code that is derived from [Artus core](https://github.com/artus-analysis/Artus/tree/master/Core/interface) classes
	- Producers subdirectory: Artus producers
	- Filters subdirectory: Artus filters
	- Consumers subdirectory: Artus consumers
	- Utility subdirectory: Other code
- [bin](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/bin): code that is compiled into executables. Every executable needs an entry in the [BuildFile.xml](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/bin/BuildFile.xml)

### Python
- [python](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/python): files that need to be included in other files/scripts
	- [plotting](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/python/plotting): Modules and Python configurations for HarryPlotter

### Scripts
- [scripts](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/scripts): no subdirectories, files should be marked as executable

### Configuration
- [data](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/data): small/text-based configuration files
  - [ArtusConfigs](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/data/ArtusConfigs): JSON files for C++ code
  - [ArtusWrapperConfigs](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/data/ArtusWrapperConfigs): Config files for the Python wrapper (HiggsToTauTauAnalysis.py)
  - [Samples](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/data/Samples): File lists for Artus
  - [plots/configs](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/data/plots/configs): JSON files for HarryPlotter
  - [gc](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/data/gc): Grid-Control configurations needed for the Python wrapper
- [auxiliaries](https://ekptrac.physik.uni-karlsruhe.de/svn/KITHiggsToTauTau-auxiliaries/trunk): larger configuration files (e.g. ROOT files) and additional small data to keep tracked. Dedicated SVN repository.


## Workflow

The following code fragments are meant as examples. All scripts offer meaningfull help via -h/--help (or sometimes without arguments).

### Skimming
If you want to skim a new Dataset, use [registerDataset.py](https://github.com/KappaAnalysis/Kappa/blob/CMSSW_7_6_X/Skimming/scripts/registerDataset.py) from the Kappa repository. It autmatically fills meta information of each sample, including the number of generated events for each dataset.

Skimming with crab3:

	source /cvmfs/cms.cern.ch/crab3/crab.sh
	cd $CMSSW_BASE/src/Kappa/Skimming/higgsTauTau/
	python crabConfig.py submit

Outputs are written in your personal DESY dCache directory:

	se path = srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/%USERNAME%/higgs-kit/skimming/<date>_<campaign>`


In case not all skims of a MC sample have been skimmed succesfully, you can manually check how many have been processed with [getNumberOfGeneratedEvents.py](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/getNumberOfGeneratedEvents.py).


File lists for Artus need to be created by [createInputFilelists.py](https://github.com/artus-analysis/Artus/blob/master/Configuration/scripts/createInputFilelists.py):

	createInputFilelists.py -s /pnfs/desy.de/cms/tier2/store/user/tmuller/higgs-kit/skimming/<date>_<campaign> -d <date> [-r]


When using NLO samples, the proper normalization has to be applied. This can be done with [getGeneratorWeight.py](https://github.com/artus-analysis/Artus/blob/Kappa_2_1/KappaAnalysis/scripts/getGeneratorWeight.py). Do e.g.

	for folder in /pnfs/desy.de/cms/tier2/store/user/$USER/higgs-kit/skimming/<date>/*; do ./getGeneratorWeight.py $folder/*/*/*/*.root; done

to update all entries in the Kappa database. Remember to commit your changes afterwards.


JEC parameters can be downloaded using [getJecParameters.py](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/getJecParameters.py):

	getJecParameters.py

The retrieved files have to be configured in Artus.

Pile-up weights are determined using [puWeightCalc.py](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/puWeightCalc.py):

	puWeightCalc.py -h

#### Kappa file helpers

- Print electron MVAs in Kappa skim: [`availableKappaElectronMvaIds.py <Kappa file(s)>`](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/availableKappaElectronMvaIds.py)
- Print HLT triggers in Kappa skim: [`availableKappaHltTriggers.py <Kappa file(s)>`](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/availableKappaHltTriggers.py)
- Print jet taggers in Kappa skim: [`availableKappaJetTaggers.py <Kappa file(s)>`](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/availableKappaJetTaggers.py)
- Print tau discriminators in Kappa skim: [`availableKappaTauDiscriminators.py <Kappa file(s)>`](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/availableKappaTauDiscriminators.python)
- Print user info in Kappa skim: [`availableKappaUserInfo.py <Kappa file(s)>`](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/availableKappaUserInfo.py)
- Find Kappa skim containing certain events: [`findKappaFiles.py -h`](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/findKappaFiles.py)
- Remove empty fileslists: [deleteEmptyFilelists.sh](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/Kappa_2_1/scripts/deleteEmptyFilelists.sh)

### Running Artus

The C++ executable ([HiggsToTauTauAnalysis](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/bin/HiggsToTauTauAnalysis.cc)) is called by a python wrapper ([HiggsToTauTauAnalysis.py](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/HiggsToTauTauAnalysis.py)) for convenience reasons.

The 8TeV SM analysis can be run with by stepping back to the "8TeVFinal" Tag in Artus, Kappa and KITHiggs repositories.

The new SM analysis can be run with by stepping back to the "8TeVFinal" Tag in Artus, Kappa and KITHiggs repositories.

	HiggsToTauTauAnalysis.py @HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/Run2Analysis.cfg -i HiggsAnalysis/KITHiggsToTauTau/data/Samples/DCAP_collection_SM_Analysis_CompletePlus_HToTauTau_13TeV_recent.txt [-b --project-name <project name>]

Beware that the above example runs on a (very!) large number of input files and has a complicated structure, which is driven by the complexity of the analysis. A more didactic example, which runs locally on a Kappa skim and applies only a very basic selection on electrons and muons, can be executed with:

	HiggsToTauTauAnalysis.py -i /afs/cern.ch/user/f/fcolombo/public/kappa_VBFHToTauTauM125_Phys14DR_PU20bx25_13TeV_MINIAODSIM.root @HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/exampleConfig.cfg

Especially for beginners, it is advisable to look carefully into the content of the above exemplary configs and json files, in order to get familiar with the way in which the Producers, Consumers and Filters are organized and called in Artus and how settings such as cut thresholds are defined.

For beeing able to use the --batch mode, go.py from grid-control (release 1499) needs to be in the $PATH. Default configurations, log files and outputs are written to `$ARTUS_WORK_BASE/<date>_<project name>`

To speed up the post-processing of the outputs, they can be merged (per nick name) by [artusMergeOutputs.py](https://github.com/artus-analysis/Artus/blob/master/Configuration/scripts/artusMergeOutputs.py):

	artusMergeOutputs.py <project directory>

In case some jobs fail, they can be collected by [getFailedJobOutputs.py](https://github.com/artus-analysis/Artus/blob/master/Configuration/scripts/getFailedJobOutputs.py) into a single directory to ease digesting the errors:

	getFailedJobOutputs.py <project directory>

JSON configurations (\*.json, \*.root, "{...}") can be compared by [artusConfigDiff.py](https://github.com/artus-analysis/Artus/blob/master/Configuration/scripts/artusConfigDiff.py):

	artusConfigDiff.py <config 1> <config 2>

The (committed) status of two different Artus runs can be compared using [artusRepositoryDiff.py](https://github.com/artus-analysis/Artus/blob/master/Configuration/scripts/artusRepositoryDiff.py):

	cd <repository to compare>
	artusRepositoryDiff.py <config 1> <config 2>

### Svfit

There are several possibilites to access the reconstructe di-tau mass in the framework.

##### Calculation of Svfit within the Artus run

The most easy, but computing intensive way is to run Svfit within the `producer:SvfitProducer` and directly use the results in the output.

The behaviour is configured in [data/ArtusConfigs/Includes/settingsSvfit.json](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/Kappa_2_1/data/ArtusConfigs/Includes/settingsSvfit.json). 
##### Reading in Cache files with pre-calculated Svfit values

By specifying a "SvfitCacheFile", usually sample-dependent, the SvfitProducer first tries to retrieve the result of the Svfit calculation from this cache file. In case of cache misses, there are three options

1) Stop the job and throw an assert, setting "SvfitCacheMissBehaviour" : "assert" 
2) Calculate the Svfit value within the job as explained in the previous section, "SvfitCacheMissBehaviour" : "recalculate"
3) Fill the Svfit result with dummy values, "SvfitCacheMissBehaviour" : "undefined"

##### Filling the caches within the Artus run

If the Svfit values are calculated within the job, the `SvfitCacheConsumer` can write them to the job output files.

To achieve this, use

	"GenerateSvfitInput" : false
	"SvfitCacheMissBehaviour" : "recalculate"

Depending on if you want to fill only events from cache misses, set "UpdateSvfitCache" to either true or false.
These results can be collected by [svfitCacheTreeMerge.py](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/svfitCacheTreeMerge.py):

	for dir in <Artus project directory>/[output|merged]/*; do echo $dir; svfitCacheTreeMerge.py -i $dir/*.root -o `echo "HiggsAnalysis/KITHiggsToTauTau/auxiliaries/svfit/svfitCache_${dir}.root" | sed -e 's@<Artus project directory>/[output|merged]/@@g'`; done

If you only have to update a few cached values, this approach is fine and does not affect runtime too much. For a complete calculation of a full dataset, use the following settings.

	HiggsToTauTauAnalysis.py -b --files-per-job 1 --wall-time 48:00:00 ...

It is recommended to store the cached results on dCache.

#### Filling the caches standalone on the grid

This approach has one step more to solve the balancing-problem by splitting the Svfit calculation on any user-defined number of events and use the WLCG for the calculation itself. 

The first step is to run the SvfitProducer and fill only dummy values. The SvfitConsumer writes one output file per pipeline containing at most the number of events specified in "SvfitInputCutOff". This can by done by specifying in the config

	"SvfitCacheMissBehaviour" : "undefined"
	"SvfitOutFile" : "SvfitCache.root",
	"GenerateSvFitInput" : true,
	"SvFitInputCutOff" : 10000,

To minimize the runtime spread and unnecessary overhead, run Artus with as man files per job as reasonable. Also, do the stageout directly to dCache to make it accessible from anywhere.

	HiggsToTauTauAnalysis.py -b --files-per-job 40 --wall-time 12:00:00 --se-path srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=//pnfs/desy.de/cms/tier2/store/user/$USER/higgs-kit/svfitinputs/

Once the Artus run is finished, you can submit the jobs to the grid with

	python HiggsAnalysis/KITHiggsToTauTau/scripts/submitCrabSvfitJobs.py /pnfs/desy.de/cms/tier2/store/user/$USER/higgs-kit/svfitinputs/

This script creates for each Sample an executable that is sent with the jobs. The output path is specified automatically in the parameter config.Data.outLFNDirBase.

Once the jobs are all done, you can merge the outputs for each sample and upload them again to dCache by e.g.

python HiggsAnalysis/KITHiggsToTauTau/scripts/svfitCacheTreeMerge.py --dcache True --input /pnfs/desy.de/cms/tier2/store/user/$USER/higgs-kit/Svfit/2016-04-12/\* -o srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=//pnfs/desy.de/cms/tier2/store/user/$USER/higgs-kit/MergedCaches/

Make sure not to miss the '\*' in the path or specify a single directory by hand. The macro prints out the new configuration settings you can copy&paste to settingsSvfit.json.

### Post-processing

The postprocessing is done based on [HarryPlotter](https://github.com/artus-analysis/Artus/tree/master/HarryPlotter):

	higgsplot.py [--plot-modules PlotRootHtt] [-h] ...

It does not only offer the possibility to create plots but also centralises the functions to read in (and scale/re-weight) histograms from Artus (or any other) outputs. It can also write out ROOT histograms for further processing.

All pipelines are listed by the script [artusPipelines.py](https://github.com/artus-analysis/Artus/blob/master/Configuration/scripts/artusPipelines.py):

	artusPipelines.py <ROOT file|JSON config>

They usually correspond to possible folders in [HarryPlotter](https://github.com/artus-analysis/Artus/tree/master/HarryPlotter). The possible quantities and modules are printed using [higgsplot.py](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/higgsplot.py):

	higgsplot.py -i <ROOT file> -f <pipeline>[/<ntuple name>] --quantities
	higgsplot.py --list-available-modules

The modules have to be registered centrally in case they are not located in the usual places ([python/plotting](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/python/plotting) or ([Artus/HarryPlotter/python](https://github.com/artus-analysis/Artus/tree/master/HarryPlotter/python)).

Sets of plots are created by the scripts

	makePlots_*.py [-h]

Example for control plots:

	makePlots_controlPlots.py -i <Artus project directory>/[merged|output]

It is recommended to produce sets of plots following the structure in these scripts.

### Statistical Inference

Inputs for combine are created by the plotting script [makePlots\_limitInputs.py](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/makePlots_limitInputs.py) using the `--plot-modules ExportRoot`:

	makePlots_limitInputs.py -i <Artus project directory>/[merged|output] [-o <limit inputs>.root]

Prefit plots are created by [makePlots\_limitInputsPrefitPlots.py](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/makePlots_limitInputsPrefitPlots.py):

	makePlots_limitInputsPrefitPlots.py -i <limit inputs>.root

Datacards are created by [SMLegacyDatacards.cc](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/bin/SMLegacyDatacards.cc) or [SMDatacards.cc](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/bin/SMDatacards.cc):

	SMLegacyDatacards [--help]
	SMDatacards [--help]

These tools are based on [CombineHarvester/CombineTools](https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau/blob/master/CombineHarvester/docs/Main.md) and require `scram b` after changes. Migration to Python is possible but not done yet. These scripts provide the configuration for the datacards.

The statistics tools (e.g. combine) of the [HiggsToTauTau repository](https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau/tree/master/scripts) are then applied on the datacards. Take [sm-protocol.txt](https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau/blob/development/data/sm-protocol.txt) as a starting point.

Postfit (and prefit) plots are created by [makePlots\_datacardsPostfitPlots.py](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/makePlots_datacardsPostfitPlots.py) after the max-likelihood fit has been run:

	makePlots_datacardsPostfitPlots.py -d <datacards> [-f <ml fit results>] [-m 125]

JSON configurations for further plots can be found in [plots/configs/combine](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/tree/master/data/plots/configs/combine).

### Utilities

#### General ROOT file helpers

- Compare ROOT files recursively: [`compareRootFiles.py -h`](https://github.com/artus-analysis/Artus/blob/master/Utility/scripts/compareRootFiles.py)
- Print content of ROOT files recursively: [`get_root_file_content.py -h`](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/scripts/get_root_file_content.py)
- Get binning of ROOT histograms: [`get_binning.py -h`](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/scripts/get_binning.py)

- Create friend trees with additional branches containing constant values: [`annotate-trees.py -h`](https://github.com/artus-analysis/Artus/blob/master/Utility/scripts/annotate-trees.py)

#### TMVA training
- Classifications: [`tmvaClassification.py -h`](https://github.com/artus-analysis/Artus/blob/master/KappaAnalysis/scripts/tmvaClassification.py)
- tmvaWrapper (recommended): [`tmvaWrapper.py -h`](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/tmvaWrapper.py)
	- -i and -o are mandatory and you will be reminded if one is missing
	- -S and -n are not mandatory but one of them must be specified for a  proper training
	- -S is the SplitValue: if this is specified you will do a regular training with a splitting of your sample defined by this variable
	- -n is the number of N-Fold: with this you will do a N-Fold training and splitting is done accordingly
	- --modify  and --modificatioin: those parameters give you access to predefined training routines, those are defined below the argparse part
	- use those parameters to use already predefined sequences or define your own in the code.
	- You should write all trainings that belong together in one folder!

#### TMVA post training duties
- Overtraining: [`plot_overtraining.py -h`](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/plot_overtraining.py)
- ConfigWriter: [`mvaConfigWriter.py -h`](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/mvaConfigWriter.py)
	- store all trainings that belong together in the same folder
	- use the Producer MVATestMethodsProducer to run all of your trainings with Artus, the config for this is contained in the output of ConfigWriter
- Correlations
	- Producer: [`correlation_SampleProducer.py -h`](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/correlation_SampleProducer.py)
	- Collector: [`correlation_SampleCollector.py -h`](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/correlation_SampleCollector.py)
	- use the Producer to calculate correlations for an Artus run, there must be a merged folder within the directory of the run
	- use the Collector to add Correlations of different channels and plot them
	- Producer: if run for the first time you have to use -P to produce a set of rootfiles, that are the base for correlation calculation, as of now the options for BDT bin correlations and multiprocess are there but not implemented
	- Collector: Per default the collector never adds MC Sample correlations and data correlations but you can add all MC Samples and compare it to data

#### Plotlevel Filtering
- ArtusRunFilter: [`MinimalPlotlevelFilter.h`](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/interface/Filters/MinimalPlotlevelFilter.h)
	-general instructions for the setup are in the source code
- PostRunFilter: [`reduce_mergedFiles.py -h`](https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/scripts/reduce_mergedFiles.py)
	-this filter reduces the merged output from an Artus run to a reduced set, which is enough for plotting etc.

#### JSON tools

Manipulation of all sorts of JSON configurations can be done using the Artus wrapper:

	HiggsToTauTauAnalysis.py -P --no-run ...

- Print JSON configs: [`jsonTools.py <JSON configs>`](https://github.com/artus-analysis/Artus/blob/master/Utility/scripts/jsonTools.py)
- Compare JSON configs: [`artusConfigDiff.py -h`](https://github.com/artus-analysis/Artus/blob/master/Configuration/scripts/artusConfigDiff.py)

