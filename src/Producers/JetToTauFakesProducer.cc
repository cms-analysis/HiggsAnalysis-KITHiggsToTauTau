#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/JetToTauFakesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"


JetToTauFakesProducer::~JetToTauFakesProducer()
{
}

std::string JetToTauFakesProducer::GetProducerId() const
{
	return "JetToTauFakesProducer";
}

void JetToTauFakesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	std::map<std::string,std::vector<std::string>> ffFiles = Utility::ParseMapTypes<std::string,std::string>(Utility::ParseVectorToMap(settings.GetFakeFaktorFiles()));

	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);

	// Save some time by excluding not needed samples (e.g. HTauTau)
	m_applyFakeFactors = boost::regex_search(settings.GetNickname(), boost::regex("^(Single|MuonEG|Tau|Double|DY|TT|ST|WW|WZ|ZZ|VV)", boost::regex::icase | boost::regex::extended));
	
	#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
	gROOT->ProcessLine("#include <map>");
	#endif

	for(auto ffFile: ffFiles)
	{
		TFile ffTFile(ffFile.second.at(0).c_str(), "READ");
		
		m_ffComb[ffFile.first] = (FakeFactor*)ffTFile.Get("ff_comb");
		
		ffTFile.Close();
	}
	gDirectory = savedir;
	gFile = savefile;
}

void JetToTauFakesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{
	// Fill inputs
	// to see input vector needs visit:
	// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L9-L15
	std::vector<double> inputs(6);

	// Tau pT 
	inputs[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
	
	// For this quantity one has to be sure that the second lepton really is a tau
	inputs[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;


	// Number of Jets
	inputs[2] = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.1);
	
	// Visible mass
	inputs[3] = product.m_diLeptonSystem.mass();
	
	// Transverse Mass calculated from lepton and MET - needs Quantities to compute
	inputs[4] = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
	
	// Using lepton isolation over pT
	inputs[5] = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());
	
	for(auto  ff_comb: m_ffComb)
	{
		// Retrieve nominal fake factors
		// To see the way to call each factor/systematic visit:
		// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766
		product.m_optionalWeights["jetToTauFakeWeight_comb_"+ff_comb.first] = ff_comb.second->value(inputs);
		// Retrieve uncertainties
		// Total systematic uncertainties on the QCD fake factor
		product.m_optionalWeights["jetToTauFakeWeight_qcd_syst_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_syst_up");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_syst_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_syst_down");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet0_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet0_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet0_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet0_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet1_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet1_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet1_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet1_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet0_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet0_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet0_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet0_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet1_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet1_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet1_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet1_stat_down");
		// Total systematic uncertainties on the W fake factor
		product.m_optionalWeights["jetToTauFakeWeight_w_syst_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_syst_up");
		product.m_optionalWeights["jetToTauFakeWeight_w_syst_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_syst_down");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm0_njet0_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm0_njet0_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm0_njet0_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm0_njet0_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm0_njet1_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm0_njet1_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm0_njet1_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm0_njet1_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm1_njet0_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm1_njet0_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm1_njet0_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm1_njet0_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm1_njet1_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm1_njet1_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_w_dm1_njet1_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_w_dm1_njet1_stat_down");
		// Total systematic uncertainties on the tt fake factor
		product.m_optionalWeights["jetToTauFakeWeight_tt_syst_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_syst_up");
		product.m_optionalWeights["jetToTauFakeWeight_tt_syst_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_syst_down");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm0_njet0_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm0_njet0_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm0_njet0_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm0_njet0_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm0_njet1_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm0_njet1_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm0_njet1_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm0_njet1_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm1_njet0_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm1_njet0_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm1_njet0_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm1_njet0_stat_down");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm1_njet1_stat_up_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm1_njet1_stat_up");
		product.m_optionalWeights["jetToTauFakeWeight_tt_dm1_njet1_stat_down_"+ff_comb.first] = ff_comb.second->value(inputs, "ff_tt_dm1_njet1_stat_down");
	}
}
