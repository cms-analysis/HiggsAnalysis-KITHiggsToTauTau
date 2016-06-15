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
    std::vector<double> inputs(5);
   
    // Tau pT 
    inputs[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
    
    // For this quantity one has to be sure that the second lepton really is a tau
    inputs[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
    
    // Visible mass
    inputs[2] = product.m_diLeptonSystem.mass();
    
    // Transverse Mass calculated from lepton and MET - needs Quantities to compute
    inputs[3] = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
    
    // Using lepton isolation over pT
    inputs[4] = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());
    
    
    
    // Retrieve nominal fake factors
    product.m_optionalWeights["jetToTauFakeWeight_comb"] = ff_comb->value(inputs);
    // Retrieve uncertainties
    // Total systematic uncertainties on the QCD fake factor
    product.m_optionalWeights["jetToTauFakeWeight_qcd_up"] = ff_comb->value(inputs, "ff_qcd_up");
    product.m_optionalWeights["jetToTauFakeWeight_qcd_down"] = ff_comb->value(inputs, "ff_qcd_down");
    // Total systematic uncertainties on the W fake factor
    product.m_optionalWeights["jetToTauFakeWeight_w_up"] = ff_comb->value(inputs, "ff_w_up");
    product.m_optionalWeights["jetToTauFakeWeight_w_down"] = ff_comb->value(inputs, "ff_w_down");
    // Systematic uncertainty du to the closure correction on the tt fake factor
    product.m_optionalWeights["jetToTauFakeWeight_tt_corr_up"] = ff_comb->value(inputs, "ff_tt_corr_up");
    product.m_optionalWeights["jetToTauFakeWeight_tt_corr_down"] = ff_comb->value(inputs, "ff_tt_corr_down");
    // Statistical uncertainty due to limited statistics in the tt control region on the tt fake factor
    product.m_optionalWeights["jetToTauFakeWeight_tt_stat_up"] = ff_comb->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_tt_stat_down"] = ff_comb->value(inputs, "ff_tt_stat_down");
    
    // Statistical uncertainty of the template fit on the estimated w fraction
    product.m_optionalWeights["jetToTauFakeWeight_frac_w_up"] = ff_comb->value(inputs, "frac_w_up");
    product.m_optionalWeights["jetToTauFakeWeight_frac_w_down"] = ff_comb->value(inputs, "frac_w_down");
    // Statistical uncertainty of the template fit on the estimated qcd fraction
    product.m_optionalWeights["jetToTauFakeWeight_frac_qcd_up"] = ff_comb->value(inputs, "frac_qcd_up");
    product.m_optionalWeights["jetToTauFakeWeight_frac_qcd_down"] = ff_comb->value(inputs, "frac_qcd_down");
    // Statistical uncertainty of the template fit on the estimated tt fraction
    product.m_optionalWeights["jetToTauFakeWeight_frac_tt_up"] = ff_comb->value(inputs, "frac_tt_up");
    product.m_optionalWeights["jetToTauFakeWeight_frac_tt_down"] = ff_comb->value(inputs, "frac_tt_down");
    // Statistical uncertainty of the template fit on the estimated dy fraction
    product.m_optionalWeights["jetToTauFakeWeight_frac_dy_up"] = ff_comb->value(inputs, "frac_dy_up");
    product.m_optionalWeights["jetToTauFakeWeight_frac_dy_down"] = ff_comb->value(inputs, "frac_dy_down");
    
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
