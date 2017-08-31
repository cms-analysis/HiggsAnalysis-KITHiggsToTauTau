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

void JetToTauFakesProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	std::map<std::string,std::vector<std::string>> ffFiles = Utility::ParseMapTypes<std::string,std::string>(Utility::ParseVectorToMap(settings.GetFakeFaktorFiles()));

	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);

	// Save some time by excluding not needed samples (e.g. HTauTau)
	m_applyFakeFactors = boost::regex_search(settings.GetNickname(), boost::regex("^(Single|MuonEG|Tau|Double|DY|TT|ST|WW|WZ|ZZ|VV)", boost::regex::icase | boost::regex::extended));
	m_isET = boost::regex_search(settings.GetRootFileFolder(), boost::regex("^et", boost::regex::extended));
	m_isMT = boost::regex_search(settings.GetRootFileFolder(), boost::regex("^mt", boost::regex::extended));
	m_isTT = boost::regex_search(settings.GetRootFileFolder(), boost::regex("^tt", boost::regex::extended));

	
	#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
	gROOT->ProcessLine("#include <map>");
	#endif

    
	for(auto ffFile: ffFiles)
	{
		TFile* ffTFile = new TFile(ffFile.second.at(0).c_str(), "READ");
		FakeFactor* ff = (FakeFactor*)ffTFile->Get("ff_comb");
		m_ffComb[ffFile.first] = std::shared_ptr<FakeFactor>(ff);
		ffTFile->Close();
		delete ffTFile;
	}
	
	gDirectory = savedir;
	gFile = savefile;
}

void JetToTauFakesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings, metadata_type const& metadata) const
{
	// Fill inputs
	// to see input vector needs visit:
	// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L9-L15

    if (m_isMT || m_isET)
    {
        std::vector<double> inputs(6);
        // Tau pT 
        inputs[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
        
        // For this quantity one has to be sure that the second lepton really is a tau
        inputs[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;


        // Number of Jets
        inputs[2] = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);
        
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
    if (m_isTT)
    {
        std::vector<double> inputs1(6);
        std::vector<double> inputs2(6);
        // Tau pT 
        inputs1[0] = product.m_flavourOrderedLeptons[0]->p4.Pt();
        inputs2[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();

        inputs1[1] = product.m_flavourOrderedLeptons[1]->p4.Pt();
        inputs2[1] = product.m_flavourOrderedLeptons[0]->p4.Pt();
        
        // For this quantity one has to be sure that the second lepton really is a tau
        inputs1[2] = static_cast<KTau*>(product.m_flavourOrderedLeptons[0])->decayMode;
        inputs2[2] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;


        // Number of Jets
        inputs1[3] = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);
        inputs2[3] = inputs1[3];
        
        // Visible mass
        inputs1[4] = product.m_diLeptonSystem.mass();
        inputs2[4] = inputs1[4];
        
        // Total Transverse Mass  - needs Quantities to compute
        double mt_1 = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
        double mt_2 = Quantities::CalculateMt(product.m_flavourOrderedLeptons[1]->p4, product.m_met.p4);
        double mt_tt = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4);
        inputs1[5] = sqrt(pow(mt_tt,2)+pow(mt_1,2)+pow(mt_2,2));
        inputs2[5] = inputs1[5];
        for(auto  ff_comb: m_ffComb)
        {
            // Retrieve nominal fake factors
            // To see the way to call each factor/systematic visit:
            // https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766
            product.m_optionalWeights["jetToTauFakeWeight_comb_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1);
            product.m_optionalWeights["jetToTauFakeWeight_comb_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2);
            // Retrieve uncertainties
            // Total systematic uncertainties on the QCD fake factor
            product.m_optionalWeights["jetToTauFakeWeight_qcd_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet0_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet0_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet0_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet0_stat_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet1_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet1_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet1_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet1_stat_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet0_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet0_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet0_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet0_stat_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet1_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet1_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet1_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet1_stat_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet0_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet0_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet0_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet0_stat_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet1_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet1_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm0_njet1_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet1_stat_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet0_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet0_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet0_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet0_stat_down");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet1_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet1_stat_up");
            product.m_optionalWeights["jetToTauFakeWeight_qcd_dm1_njet1_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet1_stat_down");
            // Total systematic uncertainties on the W fake factor
            product.m_optionalWeights["jetToTauFakeWeight_w_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_w_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_w_frac_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_frac_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_w_frac_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_frac_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_w_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_w_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_w_frac_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_frac_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_w_frac_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_frac_syst_down");
            // Total systematic uncertainties on the tt fake factor
            product.m_optionalWeights["jetToTauFakeWeight_tt_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_tt_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_tt_frac_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_frac_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_tt_frac_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_frac_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_tt_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_tt_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_tt_frac_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_frac_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_tt_frac_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_frac_syst_down");
            // Uncertainties for the dy FF
            product.m_optionalWeights["jetToTauFakeWeight_dy_frac_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_dy_frac_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_dy_frac_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_dy_frac_syst_down");
            product.m_optionalWeights["jetToTauFakeWeight_dy_frac_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_dy_frac_syst_up");
            product.m_optionalWeights["jetToTauFakeWeight_dy_frac_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_dy_frac_syst_down");
	}
        
    }

	
}
