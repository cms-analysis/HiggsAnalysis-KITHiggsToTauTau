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
    if(m_applyFakeFactors)
    {


    // Input names
    // Currently: tau_pt, tau_decayMode, njets, mvis, mt, muon_iso
    //const std::vector<std::string>& inputNames = ff->inputs();    
    
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
     
    // Retrieve nominal fake factors
    // To see the way to call each factor/systematic visit:
    // https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766



//----------------- ET -------------------
	if(m_isET)
	{
    // Initiate FaceFactor object
    // For now only ff_comb to be used, individual factors saved for later
    FakeFactor* ff_comb_et_incl = (FakeFactor*)ff_file_et_incl->Get("ff_comb");
    FakeFactor* ff_comb_et_0jet = (FakeFactor*)ff_file_et_0jet->Get("ff_comb");
    FakeFactor* ff_comb_et_1jet = (FakeFactor*)ff_file_et_1jet->Get("ff_comb");
    FakeFactor* ff_comb_et_1jetZ050 = (FakeFactor*)ff_file_et_1jetZ050->Get("ff_comb");
    FakeFactor* ff_comb_et_1jetZ50100 = (FakeFactor*)ff_file_et_1jetZ50100->Get("ff_comb");
    FakeFactor* ff_comb_et_1jetZ100 = (FakeFactor*)ff_file_et_1jetZ100->Get("ff_comb");
    FakeFactor* ff_comb_et_2jet = (FakeFactor*)ff_file_et_2jet->Get("ff_comb");
    FakeFactor* ff_comb_et_2jetVBF = (FakeFactor*)ff_file_et_2jetVBF->Get("ff_comb");
    FakeFactor* ff_comb_et_anyb = (FakeFactor*)ff_file_et_anyb->Get("ff_comb");


    //ET channel weights (incl)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl"] = ff_comb_et_incl->value(inputs);
    //Retrieve uncertainties (incl)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_qcd_syst_up"] = ff_comb_et_incl->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_qcd_syst_down"] = ff_comb_et_incl->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_qcd_stat_up"] = ff_comb_et_incl->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_qcd_stat_down"] = ff_comb_et_incl->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_w_syst_up"] = ff_comb_et_incl->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_w_syst_down"] = ff_comb_et_incl->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_w_stat_up"] = ff_comb_et_incl->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_w_stat_down"] = ff_comb_et_incl->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_tt_syst_up"] = ff_comb_et_incl->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_tt_syst_down"] = ff_comb_et_incl->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_tt_stat_up"] = ff_comb_et_incl->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_incl_tt_stat_down"] = ff_comb_et_incl->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (0jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet"] = ff_comb_et_0jet->value(inputs);
    //Retrieve uncertainties (0jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_qcd_syst_up"] = ff_comb_et_0jet->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_qcd_syst_down"] = ff_comb_et_0jet->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_qcd_stat_up"] = ff_comb_et_0jet->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_qcd_stat_down"] = ff_comb_et_0jet->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_w_syst_up"] = ff_comb_et_0jet->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_w_syst_down"] = ff_comb_et_0jet->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_w_stat_up"] = ff_comb_et_0jet->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_w_stat_down"] = ff_comb_et_0jet->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_tt_syst_up"] = ff_comb_et_0jet->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_tt_syst_down"] = ff_comb_et_0jet->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_tt_stat_up"] = ff_comb_et_0jet->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_0jet_tt_stat_down"] = ff_comb_et_0jet->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (1jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet"] = ff_comb_et_1jet->value(inputs);
    //Retrieve uncertainties (1jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_qcd_syst_up"] = ff_comb_et_1jet->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_qcd_syst_down"] = ff_comb_et_1jet->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_qcd_stat_up"] = ff_comb_et_1jet->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_qcd_stat_down"] = ff_comb_et_1jet->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_w_syst_up"] = ff_comb_et_1jet->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_w_syst_down"] = ff_comb_et_1jet->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_w_stat_up"] = ff_comb_et_1jet->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_w_stat_down"] = ff_comb_et_1jet->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_tt_syst_up"] = ff_comb_et_1jet->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_tt_syst_down"] = ff_comb_et_1jet->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_tt_stat_up"] = ff_comb_et_1jet->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jet_tt_stat_down"] = ff_comb_et_1jet->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (1jetZ050)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050"] = ff_comb_et_1jetZ050->value(inputs);
    //Retrieve uncertainties (1jetZ050)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_qcd_syst_up"] = ff_comb_et_1jetZ050->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_qcd_syst_down"] = ff_comb_et_1jetZ050->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_qcd_stat_up"] = ff_comb_et_1jetZ050->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_qcd_stat_down"] = ff_comb_et_1jetZ050->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_w_syst_up"] = ff_comb_et_1jetZ050->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_w_syst_down"] = ff_comb_et_1jetZ050->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_w_stat_up"] = ff_comb_et_1jetZ050->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_w_stat_down"] = ff_comb_et_1jetZ050->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_tt_syst_up"] = ff_comb_et_1jetZ050->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_tt_syst_down"] = ff_comb_et_1jetZ050->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_tt_stat_up"] = ff_comb_et_1jetZ050->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ050_tt_stat_down"] = ff_comb_et_1jetZ050->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (1jetZ50100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100"] = ff_comb_et_1jetZ50100->value(inputs);
    //Retrieve uncertainties (1jetZ50100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_qcd_syst_up"] = ff_comb_et_1jetZ50100->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_qcd_syst_down"] = ff_comb_et_1jetZ50100->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_qcd_stat_up"] = ff_comb_et_1jetZ50100->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_qcd_stat_down"] = ff_comb_et_1jetZ50100->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_w_syst_up"] = ff_comb_et_1jetZ50100->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_w_syst_down"] = ff_comb_et_1jetZ50100->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_w_stat_up"] = ff_comb_et_1jetZ50100->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_w_stat_down"] = ff_comb_et_1jetZ50100->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_tt_syst_up"] = ff_comb_et_1jetZ50100->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_tt_syst_down"] = ff_comb_et_1jetZ50100->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_tt_stat_up"] = ff_comb_et_1jetZ50100->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ50100_tt_stat_down"] = ff_comb_et_1jetZ50100->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (1jetZ100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100"] = ff_comb_et_1jetZ100->value(inputs);
    //Retrieve uncertainties (1jetZ100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_qcd_syst_up"] = ff_comb_et_1jetZ100->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_qcd_syst_down"] = ff_comb_et_1jetZ100->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_qcd_stat_up"] = ff_comb_et_1jetZ100->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_qcd_stat_down"] = ff_comb_et_1jetZ100->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_w_syst_up"] = ff_comb_et_1jetZ100->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_w_syst_down"] = ff_comb_et_1jetZ100->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_w_stat_up"] = ff_comb_et_1jetZ100->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_w_stat_down"] = ff_comb_et_1jetZ100->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_tt_syst_up"] = ff_comb_et_1jetZ100->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_tt_syst_down"] = ff_comb_et_1jetZ100->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_tt_stat_up"] = ff_comb_et_1jetZ100->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_1jetZ100_tt_stat_down"] = ff_comb_et_1jetZ100->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (2jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet"] = ff_comb_et_2jet->value(inputs);
    //Retrieve uncertainties (2jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_qcd_syst_up"] = ff_comb_et_2jet->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_qcd_syst_down"] = ff_comb_et_2jet->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_qcd_stat_up"] = ff_comb_et_2jet->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_qcd_stat_down"] = ff_comb_et_2jet->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_w_syst_up"] = ff_comb_et_2jet->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_w_syst_down"] = ff_comb_et_2jet->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_w_stat_up"] = ff_comb_et_2jet->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_w_stat_down"] = ff_comb_et_2jet->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_tt_syst_up"] = ff_comb_et_2jet->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_tt_syst_down"] = ff_comb_et_2jet->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_tt_stat_up"] = ff_comb_et_2jet->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jet_tt_stat_down"] = ff_comb_et_2jet->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (2jetVBF)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF"] = ff_comb_et_2jetVBF->value(inputs);
    //Retrieve uncertainties (2jetVBF)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_qcd_syst_up"] = ff_comb_et_2jetVBF->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_qcd_syst_down"] = ff_comb_et_2jetVBF->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_qcd_stat_up"] = ff_comb_et_2jetVBF->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_qcd_stat_down"] = ff_comb_et_2jetVBF->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_w_syst_up"] = ff_comb_et_2jetVBF->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_w_syst_down"] = ff_comb_et_2jetVBF->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_w_stat_up"] = ff_comb_et_2jetVBF->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_w_stat_down"] = ff_comb_et_2jetVBF->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_tt_syst_up"] = ff_comb_et_2jetVBF->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_tt_syst_down"] = ff_comb_et_2jetVBF->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_tt_stat_up"] = ff_comb_et_2jetVBF->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_2jetVBF_tt_stat_down"] = ff_comb_et_2jetVBF->value(inputs, "ff_tt_stat_down");
    
    //ET channel weights (anyb)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb"] = ff_comb_et_anyb->value(inputs);
    //Retrieve uncertainties (anyb)
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_qcd_syst_up"] = ff_comb_et_anyb->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_qcd_syst_down"] = ff_comb_et_anyb->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_qcd_stat_up"] = ff_comb_et_anyb->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_qcd_stat_down"] = ff_comb_et_anyb->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_w_syst_up"] = ff_comb_et_anyb->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_w_syst_down"] = ff_comb_et_anyb->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_w_stat_up"] = ff_comb_et_anyb->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_w_stat_down"] = ff_comb_et_anyb->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_tt_syst_up"] = ff_comb_et_anyb->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_tt_syst_down"] = ff_comb_et_anyb->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_tt_stat_up"] = ff_comb_et_anyb->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_et_anyb_tt_stat_down"] = ff_comb_et_anyb->value(inputs, "ff_tt_stat_down");


    //delete ET objects
    delete ff_comb_et_incl;
    delete ff_comb_et_0jet;
    delete ff_comb_et_1jet;
    delete ff_comb_et_1jetZ050;
    delete ff_comb_et_1jetZ50100;
    delete ff_comb_et_1jetZ100;
    delete ff_comb_et_2jet;
    delete ff_comb_et_2jetVBF;
    delete ff_comb_et_anyb;
	}




//----------------- MT -------------------
	if(m_isMT)
	{
    FakeFactor* ff_comb_mt_incl = (FakeFactor*)ff_file_mt_incl->Get("ff_comb");
    FakeFactor* ff_comb_mt_0jet = (FakeFactor*)ff_file_mt_0jet->Get("ff_comb");
    FakeFactor* ff_comb_mt_1jet = (FakeFactor*)ff_file_mt_1jet->Get("ff_comb");
    FakeFactor* ff_comb_mt_1jetZ050 = (FakeFactor*)ff_file_mt_1jetZ050->Get("ff_comb");
    FakeFactor* ff_comb_mt_1jetZ50100 = (FakeFactor*)ff_file_mt_1jetZ50100->Get("ff_comb");
    FakeFactor* ff_comb_mt_1jetZ100 = (FakeFactor*)ff_file_mt_1jetZ100->Get("ff_comb");
    FakeFactor* ff_comb_mt_2jet = (FakeFactor*)ff_file_mt_2jet->Get("ff_comb");
    FakeFactor* ff_comb_mt_2jetVBF = (FakeFactor*)ff_file_mt_2jetVBF->Get("ff_comb");
    FakeFactor* ff_comb_mt_anyb = (FakeFactor*)ff_file_mt_anyb->Get("ff_comb");


    //MT channel weights (incl)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl"] = ff_comb_mt_incl->value(inputs);
    //Retrieve uncertainties (incl)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_qcd_syst_up"] = ff_comb_mt_incl->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_qcd_syst_down"] = ff_comb_mt_incl->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_qcd_stat_up"] = ff_comb_mt_incl->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_qcd_stat_down"] = ff_comb_mt_incl->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_w_syst_up"] = ff_comb_mt_incl->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_w_syst_down"] = ff_comb_mt_incl->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_w_stat_up"] = ff_comb_mt_incl->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_w_stat_down"] = ff_comb_mt_incl->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_tt_syst_up"] = ff_comb_mt_incl->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_tt_syst_down"] = ff_comb_mt_incl->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_tt_stat_up"] = ff_comb_mt_incl->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_incl_tt_stat_down"] = ff_comb_mt_incl->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (0jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet"] = ff_comb_mt_0jet->value(inputs);
    //Retrieve uncertainties (0jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_qcd_syst_up"] = ff_comb_mt_0jet->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_qcd_syst_down"] = ff_comb_mt_0jet->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_qcd_stat_up"] = ff_comb_mt_0jet->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_qcd_stat_down"] = ff_comb_mt_0jet->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_w_syst_up"] = ff_comb_mt_0jet->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_w_syst_down"] = ff_comb_mt_0jet->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_w_stat_up"] = ff_comb_mt_0jet->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_w_stat_down"] = ff_comb_mt_0jet->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_tt_syst_up"] = ff_comb_mt_0jet->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_tt_syst_down"] = ff_comb_mt_0jet->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_tt_stat_up"] = ff_comb_mt_0jet->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_0jet_tt_stat_down"] = ff_comb_mt_0jet->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (1jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet"] = ff_comb_mt_1jet->value(inputs);
    //Retrieve uncertainties (1jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_qcd_syst_up"] = ff_comb_mt_1jet->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_qcd_syst_down"] = ff_comb_mt_1jet->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_qcd_stat_up"] = ff_comb_mt_1jet->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_qcd_stat_down"] = ff_comb_mt_1jet->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_w_syst_up"] = ff_comb_mt_1jet->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_w_syst_down"] = ff_comb_mt_1jet->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_w_stat_up"] = ff_comb_mt_1jet->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_w_stat_down"] = ff_comb_mt_1jet->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_tt_syst_up"] = ff_comb_mt_1jet->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_tt_syst_down"] = ff_comb_mt_1jet->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_tt_stat_up"] = ff_comb_mt_1jet->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jet_tt_stat_down"] = ff_comb_mt_1jet->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (1jetZ050)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050"] = ff_comb_mt_1jetZ050->value(inputs);
    //Retrieve uncertainties (1jetZ050)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_qcd_syst_up"] = ff_comb_mt_1jetZ050->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_qcd_syst_down"] = ff_comb_mt_1jetZ050->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_qcd_stat_up"] = ff_comb_mt_1jetZ050->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_qcd_stat_down"] = ff_comb_mt_1jetZ050->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_w_syst_up"] = ff_comb_mt_1jetZ050->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_w_syst_down"] = ff_comb_mt_1jetZ050->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_w_stat_up"] = ff_comb_mt_1jetZ050->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_w_stat_down"] = ff_comb_mt_1jetZ050->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_tt_syst_up"] = ff_comb_mt_1jetZ050->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_tt_syst_down"] = ff_comb_mt_1jetZ050->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_tt_stat_up"] = ff_comb_mt_1jetZ050->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ050_tt_stat_down"] = ff_comb_mt_1jetZ050->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (1jetZ50100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100"] = ff_comb_mt_1jetZ50100->value(inputs);
    //Retrieve uncertainties (1jetZ50100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_qcd_syst_up"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_qcd_syst_down"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_qcd_stat_up"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_qcd_stat_down"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_w_syst_up"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_w_syst_down"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_w_stat_up"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_w_stat_down"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_tt_syst_up"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_tt_syst_down"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_tt_stat_up"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ50100_tt_stat_down"] = ff_comb_mt_1jetZ50100->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (1jetZ100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100"] = ff_comb_mt_1jetZ100->value(inputs);
    //Retrieve uncertainties (1jetZ100)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_qcd_syst_up"] = ff_comb_mt_1jetZ100->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_qcd_syst_down"] = ff_comb_mt_1jetZ100->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_qcd_stat_up"] = ff_comb_mt_1jetZ100->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_qcd_stat_down"] = ff_comb_mt_1jetZ100->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_w_syst_up"] = ff_comb_mt_1jetZ100->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_w_syst_down"] = ff_comb_mt_1jetZ100->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_w_stat_up"] = ff_comb_mt_1jetZ100->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_w_stat_down"] = ff_comb_mt_1jetZ100->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_tt_syst_up"] = ff_comb_mt_1jetZ100->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_tt_syst_down"] = ff_comb_mt_1jetZ100->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_tt_stat_up"] = ff_comb_mt_1jetZ100->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_1jetZ100_tt_stat_down"] = ff_comb_mt_1jetZ100->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (2jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet"] = ff_comb_mt_2jet->value(inputs);
    //Retrieve uncertainties (2jet)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_qcd_syst_up"] = ff_comb_mt_2jet->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_qcd_syst_down"] = ff_comb_mt_2jet->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_qcd_stat_up"] = ff_comb_mt_2jet->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_qcd_stat_down"] = ff_comb_mt_2jet->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_w_syst_up"] = ff_comb_mt_2jet->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_w_syst_down"] = ff_comb_mt_2jet->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_w_stat_up"] = ff_comb_mt_2jet->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_w_stat_down"] = ff_comb_mt_2jet->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_tt_syst_up"] = ff_comb_mt_2jet->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_tt_syst_down"] = ff_comb_mt_2jet->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_tt_stat_up"] = ff_comb_mt_2jet->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jet_tt_stat_down"] = ff_comb_mt_2jet->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (2jetVBF)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF"] = ff_comb_mt_2jetVBF->value(inputs);
    //Retrieve uncertainties (2jetVBF)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_qcd_syst_up"] = ff_comb_mt_2jetVBF->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_qcd_syst_down"] = ff_comb_mt_2jetVBF->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_qcd_stat_up"] = ff_comb_mt_2jetVBF->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_qcd_stat_down"] = ff_comb_mt_2jetVBF->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_w_syst_up"] = ff_comb_mt_2jetVBF->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_w_syst_down"] = ff_comb_mt_2jetVBF->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_w_stat_up"] = ff_comb_mt_2jetVBF->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_w_stat_down"] = ff_comb_mt_2jetVBF->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_tt_syst_up"] = ff_comb_mt_2jetVBF->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_tt_syst_down"] = ff_comb_mt_2jetVBF->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_tt_stat_up"] = ff_comb_mt_2jetVBF->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_2jetVBF_tt_stat_down"] = ff_comb_mt_2jetVBF->value(inputs, "ff_tt_stat_down");
    
    //MT channel weights (anyb)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb"] = ff_comb_mt_anyb->value(inputs);
    //Retrieve uncertainties (anyb)
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_qcd_syst_up"] = ff_comb_mt_anyb->value(inputs, "ff_qcd_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_qcd_syst_down"] = ff_comb_mt_anyb->value(inputs, "ff_qcd_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_qcd_stat_up"] = ff_comb_mt_anyb->value(inputs, "ff_qcd_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_qcd_stat_down"] = ff_comb_mt_anyb->value(inputs, "ff_qcd_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_w_syst_up"] = ff_comb_mt_anyb->value(inputs, "ff_w_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_w_syst_down"] = ff_comb_mt_anyb->value(inputs, "ff_w_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_w_stat_up"] = ff_comb_mt_anyb->value(inputs, "ff_w_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_w_stat_down"] = ff_comb_mt_anyb->value(inputs, "ff_w_stat_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_tt_syst_up"] = ff_comb_mt_anyb->value(inputs, "ff_tt_syst_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_tt_syst_down"] = ff_comb_mt_anyb->value(inputs, "ff_tt_syst_down");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_tt_stat_up"] = ff_comb_mt_anyb->value(inputs, "ff_tt_stat_up");
    product.m_optionalWeights["jetToTauFakeWeight_comb_mt_anyb_tt_stat_down"] = ff_comb_mt_anyb->value(inputs, "ff_tt_stat_down");
    

    //delete MT objects
    delete ff_comb_mt_incl;
    delete ff_comb_mt_0jet;
    delete ff_comb_mt_1jet;
    delete ff_comb_mt_1jetZ050;
    delete ff_comb_mt_1jetZ50100;
    delete ff_comb_mt_1jetZ100;
    delete ff_comb_mt_2jet;
    delete ff_comb_mt_2jetVBF;
    delete ff_comb_mt_anyb;
	}


    /*   //TT channel
    FakeFactor* ff_comb_tt_incl = (FakeFactor*)ff_file_tt_incl->Get("ff_comb");
    FakeFactor* ff_comb_tt_0jet = (FakeFactor*)ff_file_tt_0jet->Get("ff_comb");
    FakeFactor* ff_comb_tt_1jet = (FakeFactor*)ff_file_tt_1jet->Get("ff_comb");
    FakeFactor* ff_comb_tt_1jetZ050 = (FakeFactor*)ff_file_tt_1jetZ050->Get("ff_comb");
    FakeFactor* ff_comb_tt_1jetZ50100 = (FakeFactor*)ff_file_tt_1jetZ50100->Get("ff_comb");
    FakeFactor* ff_comb_tt_1jetZ100 = (FakeFactor*)ff_file_tt_1jetZ100->Get("ff_comb");
    FakeFactor* ff_comb_tt_2jet = (FakeFactor*)ff_file_tt_2jet->Get("ff_comb");
    FakeFactor* ff_comb_tt_2jetVBF = (FakeFactor*)ff_file_tt_2jetVBF->Get("ff_comb");
    FakeFactor* ff_comb_tt_anyb = (FakeFactor*)ff_file_tt_anyb->Get("ff_comb");
    */
    }
}
