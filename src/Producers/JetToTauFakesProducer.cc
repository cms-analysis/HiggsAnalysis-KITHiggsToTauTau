#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/JetToTauFakesProducer.h"
//NOT NEEDED AS OF NOW	#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

//#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"


std::string JetToTauFakesProducer::GetProducerId() const
{
	return "JetToTauFakesProducer";
}

void JetToTauFakesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{
    // For now only ff_comb to be used, individual factors saved for later
    FakeFactor* ff_comb = (FakeFactor*)ff_file->Get("ff_comb");
    //FakeFactor* ff_qcd_ss = (FakeFactor*)ff_file->Get("ff_qcd_ss");
    //FakeFactor* ff_qcd_os = (FakeFactor*)ff_file->Get("ff_qcd_os");
    //FakeFactor* ff_w = (FakeFactor*)ff_file->Get("ff_w");
    //FakeFactor* ff_tt = (FakeFactor*)ff_file->Get("ff_tt");
    // Input names
    // Currently: tau_pt, tau_decayMode, mvis, mt, muon_iso
    //const std::vector<std::string>& inputNames = ff->inputs();
    
    
    // Fill inputs
    std::vector<double> inputs(4);
    
    inputs[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
    
    // For this quantity one has to be sure that the second lepton really is a tau
    inputs[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
    
    // Visible mass
    inputs[2] = product.m_diLeptonSystem.mass();
    
    // Transverse Mass calculated from Muon and MET - needs Quantities to compute
    //NOT NEEDED AS OF NOW	inputs[3] = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
    
    // Using Muon Isolation over pT
    inputs[3] = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());
    
    
    
    // Retrieve Fake Factors
    // double ff_nom = ff->value(inputs);
    // std::string sys(...);
    // Systematic shift
    // double ff_sys  = ff->value(inputs, sys);
    product.m_optionalWeights["jetToTauFakeWeight_comb"] = ff_comb->value(inputs);
    //product.m_optionalWeights["jetToTauFakeWeight_qcd_ss"] = ff_qcd_ss->value(inputs);
    //product.m_optionalWeights["jetToTauFakeWeight_qcd_os"] = ff_qcd_os->value(inputs);
    //product.m_optionalWeights["jetToTauFakeWeight_w"] = ff_w->value(inputs);
    //product.m_optionalWeights["jetToTauFakeWeight_tt"] = ff_tt->value(inputs);

    delete ff_comb;
    //delete ff_qcd_ss;
    //delete ff_qcd_os;
    //delete ff_w;
    //delete ff_tt;
}
