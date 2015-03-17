#include <string>
#include <map>
#include <set>
#include <iostream>
#include <vector>
#include <utility>
#include <cstdlib>
#include "boost/filesystem.hpp"
#include "boost/program_options.hpp"
#include "CombineTools/interface/CombineHarvester.h"
#include "CombineTools/interface/Utilities.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/CombineTools/HttSystematics.h"
#include "CombineTools/interface/MakeUnique.h"
#include "Artus/Utility/interface/Utility.h"

using namespace std;

int main(int argc, char* argv[]) {
	string higgsAuxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
	string aux_pruning  = higgsAuxiliaries +"pruning/";
	
	string kitAuxiliaries  = string(getenv("CMSSW_BASE")) + "/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/combine/";
	string aux_shapes   = kitAuxiliaries +"shapes/";
	
	vector<string> eras = {"8TeV"}; // {"7TeV", "8TeV"}
	vector<string> chns = {"mt"}; // {"et", "mt", "em", "ee", "mm", "tt"}
	vector<string> masses = ch::MassesFromRange("110-145:5");
	float lumi = 0.0;
	string energy = "8";
	bool asimovDataset = false;
	string asimovDatasetMass = "125";
	string outputDirectory = kitAuxiliaries +"datacards/";

	boost::program_options::options_description help_config("Help");
	help_config.add_options()
		("help,h", "produce help message");
	boost::program_options::options_description config("Configuration");
	config.add_options()
		("eras", boost::program_options::value<std::vector<string> >(&eras)->default_value(eras, ""),
		"Eras")
		("channels,c", boost::program_options::value<std::vector<string> >(&chns)->default_value(chns, ""),
		"Channels")
		("masses,m", boost::program_options::value<std::vector<string> >(&masses)->default_value(masses, ""),
		"Higgs masses")
		("lumi,l", boost::program_options::value<float>(&lumi)->default_value(lumi),
		"Scale integrated luminosity to specified value [Default: no scaling]")
		("energy,e", boost::program_options::value<string>(&energy)->default_value(energy),
		"Center-of-mass energy (in TeV) to scale cross sections to [Default: \"8\"]")
		("asimov,a", boost::program_options::value<bool>(&asimovDataset)->default_value(asimovDataset)->implicit_value(true),
		"Replace observation by an asimov dataset [Default: False]")
		("asimov-mass", boost::program_options::value<string>(&asimovDatasetMass)->default_value(asimovDatasetMass),
		"Mass for the signal used in asimov dataset [Default: \"125\"]")
		("output,o", boost::program_options::value<string>(&outputDirectory)->default_value(outputDirectory),
		"Output directory [Default: \"datacards/sm\"]");

	boost::program_options::variables_map vm;
	boost::program_options::store(
			boost::program_options::command_line_parser(argc, argv).options(help_config).allow_unregistered().run(),
			vm
	);
	boost::program_options::notify(vm);
	if (vm.count("help")) {
		cout << config << endl;
		return 1;
	}
	boost::program_options::store(boost::program_options::command_line_parser(argc, argv).options(config).run(), vm);
	boost::program_options::notify(vm);
	cout << ">> Choosen program arguments:" << endl;
	cout << ">>>> eras: ";
	for (string era : eras) {
		cout << era << " ";
	}
	cout << endl;
	cout << ">>>> channels: ";
	for (string chn : chns) {
		cout << chn << " ";
	}
	cout << endl;
	cout << ">>>> Higgs masses: ";
	for (string m : masses) {
		cout << m << " ";
	}
	cout << endl;
	cout << ">>>> lumi: " << lumi << endl;
	cout << ">>>> energy: " << energy << endl;
	cout << ">>>> asimovDataset: " << (asimovDataset ? "true" : "false") << endl;
	cout << ">>>> asimovDatasetMass: " << asimovDatasetMass << endl;
	cout << ">>>> output: " << outputDirectory << endl;
	
	ch::CombineHarvester cb;

	// cb.SetVerbosity(1);

	typedef vector<pair<int, string>> Categories;
	typedef vector<string> VString;

	map<string, float> lumis8TeV = {
			{"et", 19.7},
			{"mt", 19.7},
			{"em", 19.7},
			{"ee", 19.7},
			{"mm", 19.7},
			{"tt", 18.4}
	};
	
	map<string, string> input_folders = {
			{"et", "et"},
			{"mt", "mt"},
			{"em", "em"},
			{"ee", "ee"},
			{"mm", "mm"},
			{"tt", "tt"}
	};

	map<string, VString> bkg_procs;
	bkg_procs["et"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
	bkg_procs["mt"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};
	bkg_procs["em"] = {"Ztt", "EWK", "Fakes", "ttbar", "ggH_hww125", "qqH_hww125"};
	bkg_procs["ee"] = {"ZTT", "WJets", "QCD", "ZEE", "TTJ", "Dibosons", "ggH_hww125", "qqH_hww125"};
	bkg_procs["mm"] = {"ZTT", "WJets", "QCD", "ZMM", "TTJ", "Dibosons", "ggH_hww125", "qqH_hww125"};
	bkg_procs["tt"] = {"ZTT", "W", "QCD", "ZL", "ZJ", "TT", "VV"};

	VString sig_procs = {"ggH", "qqH", "WH", "ZH"};

	map<string, Categories> cats;
	cats["et_7TeV"] = {
			{1, "et_0jet_medium"}, {2, "et_0jet_high"},
			{3, "et_1jet_medium"}, {5, "et_1jet_high_mediumhiggs"},
			{6, "et_vbf"}};

	cats["et_8TeV"] = {
			{1, "et_0jet_medium"}, {2, "et_0jet_high"},
			{3, "et_1jet_medium"}, {5, "et_1jet_high_mediumhiggs"},
			{6, "et_vbf_loose"}, {7, "et_vbf_tight"}};

	cats["mt_7TeV"] = {
			{1, "mt_0jet_medium"}, {2, "mt_0jet_high"},
			{3, "mt_1jet_medium"}, {4, "mt_1jet_high_lowhiggs"}, {5, "mt_1jet_high_mediumhiggs"},
			{6, "mt_vbf"}};

	cats["mt_8TeV"] = {
			{1, "mt_0jet_medium"}, {2, "mt_0jet_high"},
			{3, "mt_1jet_medium"}, {4, "mt_1jet_high_lowhiggs"}, {5, "mt_1jet_high_mediumhiggs"},
			{6, "mt_vbf_loose"}, {7, "mt_vbf_tight"}};

	cats["em_7TeV"] = {
			{0, "em_0jet_low"}, {1, "em_0jet_high"},
			{2, "em_1jet_low"}, {3, "em_1jet_high"},
			{4, "em_vbf_loose"}};

	cats["em_8TeV"] = {
			{0, "em_0jet_low"}, {1, "em_0jet_high"},
			{2, "em_1jet_low"}, {3, "em_1jet_high"},
			{4, "em_vbf_loose"}, {5, "em_vbf_tight"}};

	cats["ee_7TeV"] = {
			{0, "ee_0jet_low"}, {1, "ee_0jet_high"},
			{2, "ee_1jet_low"}, {3, "ee_1jet_high"},
			{4, "ee_vbf"}};
	cats["ee_8TeV"] = cats["ee_7TeV"];

	cats["mm_7TeV"] = {
			{0, "mm_0jet_low"}, {1, "mm_0jet_high"},
			{2, "mm_1jet_low"}, {3, "mm_1jet_high"},
			{4, "mm_vbf"}};
	cats["mm_8TeV"] = cats["mm_7TeV"];

	cats["tt_8TeV"] = {
			{0, "tt_1jet_high_mediumhiggs"}, {1, "tt_1jet_high_highhiggs"},
			{2, "tt_vbf"}};

	cout << ">> Creating processes and observations...\n";
	for (string era : eras) {
		for (auto chn : chns) {
			cb.AddObservations(
				{"*"}, {"htt"}, {era}, {chn}, cats[chn+"_"+era]);
			cb.AddProcesses(
				{"*"}, {"htt"}, {era}, {chn}, bkg_procs[chn], cats[chn+"_"+era], false);
			cb.AddProcesses(
				masses, {"htt"}, {era}, {chn}, sig_procs, cats[chn+"_"+era], true);
		}
	}
	// Have to drop ZL from tt_vbf category
	cb.FilterProcs([](ch::Process const* p) {
		return p->bin() == "tt_vbf" && p->process() == "ZL";
	});

	cout << ">> Adding systematic uncertainties...\n";
	if (Utility::Contains(chns, string("et")) || Utility::Contains(chns, string("mt")))
	{
		HttSystematics::AddSystematicsETMT(cb);
	}
	if (Utility::Contains(chns, string("em")))
	{
		HttSystematics::AddSystematicsEM(cb);
	}
	if (Utility::Contains(chns, string("ee")) || Utility::Contains(chns, string("mm")))
	{
		HttSystematics::AddSystematicsEEMM(cb);
	}
	if (Utility::Contains(chns, string("tt")))
	{
		HttSystematics::AddSystematicsTT(cb);
	}

	cout << ">> Extracting histograms from input root files...\n";
	for (string era : eras) {
		for (string chn : chns) {
			// Skip 7TeV tt:
			if (chn == "tt" && era == "7TeV") continue;
			string file = aux_shapes + input_folders[chn] + "/htt_" + chn +
										".inputs-sm-" + era + ".root";
			cb.cp().channel({chn}).era({era}).backgrounds().ExtractShapes(
					file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
			cb.cp().channel({chn}).era({era}).signals().ExtractShapes(
					file, "$BIN/$PROCESS$MASS", "$BIN/$PROCESS$MASS_$SYSTEMATIC");
		}
	}

	cout << ">> Scaling signal process rates...\n";
	map<string, TGraph> xs;
	// Get the table of H->tau tau BRs vs mass
	string xsecs_dir = string(getenv("CMSSW_BASE")) + "/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/input/xsecs_brs/";
	ch::ParseTable(&xs, xsecs_dir+"htt_YR3.txt", {"htt"});
	for (string const& e : eras) {
		for (string const& p : sig_procs) {
			string dstEra = e;
			if (e != "7TeV") {
				dstEra = energy+"TeV";
			}
			
			// Get the table of xsecs vs mass for process "p" and era "e":
			ch::ParseTable(&xs, xsecs_dir+p+"_"+dstEra+"_YR3.txt", {p+"_"+dstEra});
			cout << ">>>> Scaling for process " << p << " and era " << dstEra << "\n";
			cb.cp().process({p}).era({e}).ForEachProc([&](ch::Process *proc) {
				ch::ScaleProcessRate(proc, &xs, p+"_"+dstEra, "htt");
			});
		}
	}
	ch::ParseTable(&xs, xsecs_dir+"hww_over_htt.txt", {"hww_over_htt"});
	for (string const& e : eras) {
		string dstEra = e;
		if (e != "7TeV") {
			dstEra = energy+"TeV";
		}
		for (string const& p : {"ggH", "qqH"}) {
		 cb.cp().channel({"em"}).process({p+"_hww125"}).era({dstEra})
			 .ForEachProc([&](ch::Process *proc) {
				 ch::ScaleProcessRate(proc, &xs, p+"_"+dstEra, "htt", "125");
				 ch::ScaleProcessRate(proc, &xs, "hww_over_htt", "", "125");
			});
		}
	}
	
	if (boost::lexical_cast<float>(energy) > 8.0) {
		cout << ">> Scaling 8TeV background process rates to " << energy << "TeV cross sections...\n";
		//map<string, double> xsRatios;
		//ch::ParseTable(&xsRatios, xsecs_dir+"sm_"+energy+"TeV_over_8TeV.txt");
		// scale factors taken from https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau/blob/master/scripts/scaleTo14TeV.py#L18-L30
		cb.cp().era({"8TeV"}).process({"ZTT", "ZL", "ZJ", "Ztt", "ZEE", "ZMM"}).ForEachProc([&](ch::Process *proc) {
			proc->set_rate(proc->rate() * 2.02904/1.14951);
		});
		cb.cp().era({"8TeV"}).process({"TT", "ttbar", "TTJ"}).ForEachProc([&](ch::Process *proc) {
			proc->set_rate(proc->rate() * 5.59001/1.42982);
		});
		cb.cp().era({"8TeV"}).process({"W", "WJets"}).ForEachProc([&](ch::Process *proc) {
			proc->set_rate(proc->rate() * 2.09545/1.15786);
		});
		cb.cp().era({"8TeV"}).process({"VV", "EWK", "Dibosons"}).ForEachProc([&](ch::Process *proc) {
			proc->set_rate(proc->rate() * (2.79381/1.23344+2.62549/1.21510+2.64949/1.21944) / 3.0);
		});
		cb.cp().era({"8TeV"}).process({"QCD", "Fakes"}).ForEachProc([&](ch::Process *proc) {
			proc->set_rate(proc->rate() * 3.0);
		});
	}
	
	if (lumi > 0.0) {
		cout << ">> Scaling luminosity for all 8TeV signal and background processes ...\n";
		for (string const& era : eras) {
			if (era == "7TeV") {
				continue;
			}
			for (string const& chn : chns) {
				cb.cp().channel({chn}).era({era}).backgrounds().ForEachProc([&](ch::Process *proc) {
					proc->set_rate(proc->rate() * lumi / lumis8TeV[chn]);
				});
			}
			for (string const& chn : chns) {
				cb.cp().channel({chn}).era({era}).signals().ForEachProc([&](ch::Process *proc) {
					proc->set_rate(proc->rate() * lumi / lumis8TeV[chn]);
				});
			}
		}
	}
	
	if (asimovDataset) {
		cout << ">> Replacing observation by an asimov dataset ...\n";
		cb.ForEachObs([&](ch::Observation *observation) {
			observation->set_shape(ch::make_unique<TH1F>(
					cb.cp().bin({observation->bin()}).backgrounds().GetShape() +
					cb.cp().bin({observation->bin()}).signals().mass({asimovDatasetMass}).GetShape()
			), true);
		});
	}

	cout << ">> Merging bin errors...\n";
	ch::CombineHarvester cb_et = move(cb.cp().channel({"et"}));
	for (string era : eras) {
		cb_et.cp().era({era}).bin_id({1, 2}).process({"ZL", "ZJ", "QCD", "W"})
				.MergeBinErrors(0.1, 0.5);
		cb_et.cp().era({era}).bin_id({3, 5}).process({"W"})
				.MergeBinErrors(0.1, 0.5);
	}
	cb_et.cp().era({"7TeV"}).bin_id({6}).process({"ZL", "ZJ", "W", "ZTT"})
			.MergeBinErrors(0.1, 0.5);
	cb_et.cp().era({"8TeV"}).bin_id({7}).process({"ZL", "ZJ", "W", "ZTT"})
			.MergeBinErrors(0.1, 0.5);
	cb_et.cp().era({"8TeV"}).bin_id({6}).process({"ZL", "ZJ", "W"})
			.MergeBinErrors(0.1, 0.5);

	ch::CombineHarvester cb_mt = move(cb.cp().channel({"mt"}));
	for (string era : eras) {
		cb_mt.cp().era({era}).bin_id({1, 2, 3, 4}).process({"W", "QCD"})
				.MergeBinErrors(0.1, 0.5);
	}
	cb_mt.cp().era({"7TeV"}).bin_id({5}).process({"W"})
			.MergeBinErrors(0.1, 0.5);
	cb_mt.cp().era({"7TeV"}).bin_id({6}).process({"W", "ZTT"})
			.MergeBinErrors(0.1, 0.5);
	cb_mt.cp().era({"8TeV"}).bin_id({5, 6}).process({"W"})
			.MergeBinErrors(0.1, 0.5);
	cb_mt.cp().era({"8TeV"}).bin_id({7}).process({"W", "ZTT"})
			.MergeBinErrors(0.1, 0.5);

	ch::CombineHarvester cb_em = move(cb.cp().channel({"em"}));
	for (string era : eras) {
		cb_em.cp().era({era}).bin_id({1, 3}).process({"Fakes"})
				.MergeBinErrors(0.1, 0.5);
	}
	cb_em.cp().era({"7TeV"}).bin_id({4}).process({"Fakes", "EWK", "Ztt"})
			.MergeBinErrors(0.1, 0.5);
	cb_em.cp().era({"8TeV"}).bin_id({5}).process({"Fakes", "EWK", "Ztt"})
			.MergeBinErrors(0.1, 0.5);
	cb_em.cp().era({"8TeV"}).bin_id({4}).process({"Fakes", "EWK"})
			.MergeBinErrors(0.1, 0.5);

	ch::CombineHarvester cb_ee_mm = move(cb.cp().channel({"ee", "mm"}));
	for (string era : eras) {
		cb_ee_mm.cp().era({era}).bin_id({1, 3, 4})
				.process({"ZTT", "ZEE", "ZMM", "TTJ"})
				.MergeBinErrors(0.0, 0.5);
	}

	ch::CombineHarvester cb_tt = move(cb.cp().channel({"tt"}));
	cb_tt.cp().bin_id({0, 1, 2}).era({"8TeV"}).process({"ZTT", "QCD"})
			.MergeBinErrors(0.1, 0.5);

	cout << ">> Generating bbb uncertainties...\n";
	cb_mt.cp().bin_id({0, 1, 2, 3, 4}).process({"W", "QCD"})
			.AddBinByBin(0.1, true, &cb);
	cb_mt.cp().era({"7TeV"}).bin_id({5}).process({"W"})
			.AddBinByBin(0.1, true, &cb);
	cb_mt.cp().era({"7TeV"}).bin_id({6}).process({"W", "ZTT"})
			.AddBinByBin(0.1, true, &cb);
	cb_mt.cp().era({"8TeV"}).bin_id({5, 6}).process({"W"})
			.AddBinByBin(0.1, true, &cb);
	cb_mt.cp().era({"8TeV"}).bin_id({7}).process({"W", "ZTT"})
			.AddBinByBin(0.1, true, &cb);

	cb_et.cp().bin_id({1, 2}).process({"ZL", "ZJ", "QCD", "W"})
			.AddBinByBin(0.1, true, &cb);
	cb_et.cp().bin_id({3, 5}).process({"W"})
			.AddBinByBin(0.1, true, &cb);
	cb_et.cp().era({"7TeV"}).bin_id({6}).process({"ZL", "ZJ", "W", "ZTT"})
			.AddBinByBin(0.1, true, &cb);
	cb_et.cp().era({"8TeV"}).bin_id({7}).process({"ZL", "ZJ", "W", "ZTT"})
			.AddBinByBin(0.1, true, &cb);
	cb_et.cp().era({"8TeV"}).bin_id({6}).process({"ZL", "ZJ", "W"})
			.AddBinByBin(0.1, true, &cb);

	cb_em.cp().bin_id({1, 3}).process({"Fakes"})
			.AddBinByBin(0.1, true, &cb);
	cb_em.cp().era({"7TeV"}).bin_id({4}).process({"Fakes", "EWK", "Ztt"})
			.AddBinByBin(0.1, true, &cb);
	cb_em.cp().era({"8TeV"}).bin_id({5}).process({"Fakes", "EWK", "Ztt"})
			.AddBinByBin(0.1, true, &cb);
	cb_em.cp().era({"8TeV"}).bin_id({4}).process({"Fakes", "EWK"})
			.AddBinByBin(0.1, true, &cb);

	cb_ee_mm.cp().bin_id({1, 3, 4}).process({"ZTT", "ZEE", "ZMM", "TTJ"})
			.AddBinByBin(0.0, true, &cb);

	cb_tt.cp().bin_id({0, 1, 2}).era({"8TeV"}).process({"QCD", "ZTT"})
			.AddBinByBin(0.1, true, &cb);

	cout << ">> Setting standardised bin names...\n";
	ch::SetStandardBinNames(cb);
	VString droplist = ch::ParseFileLines(
		aux_pruning + "uncertainty-pruning-drop-131128-sm.txt");
	cout << ">> Droplist contains " << droplist.size() << " entries\n";

	set<string> to_drop;
	for (auto x : droplist) to_drop.insert(x);

	auto pre_drop = cb.syst_name_set();
	cb.syst_name(droplist, false);
	auto post_drop = cb.syst_name_set();
	cout << ">> Systematics dropped: " << pre_drop.size() - post_drop.size()
						<< "\n";

	// set<string> dropped;
	// set_difference(pre_drop.begin(), pre_drop.end(), post_drop.begin(),
	//                post_drop.end(), inserter(dropped, dropped.end()));

	// set<string> undropped;
	// set_difference(to_drop.begin(), to_drop.end(), dropped.begin(),
	//                dropped.end(), inserter(undropped, undropped.end()));
	// cout << ">> Un-dropped:\n";
	// for (auto const& x : undropped) {
	//   cout << " - " << x << "\n";
	// }

	boost::filesystem::create_directories(outputDirectory);
	boost::filesystem::create_directories(outputDirectory+"/common");
	for (auto m : masses) {
		boost::filesystem::create_directories(outputDirectory+"/"+m);
	}

	for (string chn : chns) {
		TFile output((outputDirectory + "/common/htt_" + chn + ".input.root").c_str(), "RECREATE");
		auto bins = cb.cp().channel({chn}).bin_set();
		for (auto b : bins) {
			for (auto m : masses) {
				string dataCardPath = outputDirectory + "/" + m + "/" + b + ".txt";
				cout << ">> Writing datacard for bin: " << b << " and mass: " << m
									<< " to " << dataCardPath << endl;
				cb.cp().channel({chn}).bin({b}).mass({m, "*"}).WriteDatacard(
						dataCardPath, output);
			}
		}
		cb.cp().channel({chn}).mass({"125", "*"}).WriteDatacard(outputDirectory+"/htt_" + chn + "_125.txt", output);
		output.Close();
	}

	cout << "\n>> Done!\n";
}
