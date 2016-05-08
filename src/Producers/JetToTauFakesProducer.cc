#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/JetToTauFakesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

//#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"


std::string JetToTauFakesProducer::GetProducerId() const
{
	return "JetToTauFakesProducer";
}

void JetToTauFakesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{
    
    // Load Fake Factor file    !!currently done in Init so following two lines commented!!
    //TFile* ff_file = TFile::Open("/afs/desy.de/user/g/gkoehler/CMSSW/Analysis_CMSSW804/CMSSW_8_0_4/src/HTTutilities/Jet2TauFakes/data/fakeFactors_20160425.root");
    //FakeFactor* ff = (FakeFactor*)ff_file->Get("ff_comb");
    FakeFactor* ff = (FakeFactor*)ff_file->Get("ff_comb");
    
    // Input names
    // Currently: tau_pt, tau_decayMode, mvis, mt, muon_iso
    //const std::vector<std::string>& inputNames = ff->inputs();
    
    
    // Fill inputs
    std::vector<double> inputs(5);
    
    inputs[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
    
    // For this quantity one has to be sure that the second lepton really is a tau
    inputs[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
    
    inputs[2] = product.m_diLeptonSystem.mass();
    
    // Transverse Mass calculated from Muon and MET - needs Quantities to compute
    inputs[3] = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
    
    // Using Muon Isolation over pT
    inputs[4] = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());
    
    
    
    // Retrieve Fake Factors
    // double ff_nom = ff->value(inputs);
    // std::string sys(...);
    // Systematic shift
    // double ff_sys  = ff->value(inputs, sys);
    product.m_optionalWeights["jetToTauFakeWeight"] = ff->value(inputs);

    delete ff;
    //ff_file->Close();
    
}
