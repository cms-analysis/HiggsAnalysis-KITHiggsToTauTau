#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/JetToTauFakesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"


JetToTauFakesProducer::~JetToTauFakesProducer()
{
	if (ff_comb != nullptr)
	{
		delete ff_comb;
	}
	if (ff_qcd_ss != nullptr)
	{
		delete ff_qcd_ss;
	}
	if (ff_qcd_os != nullptr)
	{
		delete ff_qcd_os;
	}
	if (ff_w != nullptr)
	{
		delete ff_w;
	}
	if (ff_tt != nullptr)
	{
		delete ff_tt;
	}
}

std::string JetToTauFakesProducer::GetProducerId() const
{
	return "JetToTauFakesProducer";
}

void JetToTauFakesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
	gROOT->ProcessLine("#include <map>");
	#endif

	TFile ff_file(settings.GetJetToTauFakeFactorsFile().c_str(), "READ");
	
	ff_comb = (FakeFactor*)ff_file.Get("ff_comb");
	ff_qcd_ss = (FakeFactor*)ff_file.Get("ff_qcd_ss");
	ff_qcd_os = (FakeFactor*)ff_file.Get("ff_qcd_os");
	ff_w = (FakeFactor*)ff_file.Get("ff_w");
	ff_tt = (FakeFactor*)ff_file.Get("ff_tt");
	
	ff_file.Close();
}

void JetToTauFakesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{
	// Fill inputs
	// to see input vector needs visit:
	// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L9-L15
	std::vector<double> inputs(5);
	std::vector<double> inputs_qcd(4);
	std::vector<double> inputs_w(4);
	std::vector<double> inputs_tt(3);

	// Tau pT 
	inputs[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
	inputs_qcd[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
	inputs_w[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
	inputs_tt[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
	
	// For this quantity one has to be sure that the second lepton really is a tau
	inputs[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
	inputs_qcd[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
	inputs_w[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
	inputs_tt[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
	
	// Visible mass
	inputs[2] = product.m_diLeptonSystem.mass();
	inputs_qcd[2] = product.m_diLeptonSystem.mass();
	inputs_w[2] = product.m_diLeptonSystem.mass();
	inputs_tt[2] = product.m_diLeptonSystem.mass();
	
	// Transverse Mass calculated from lepton and MET - needs Quantities to compute
	inputs[3] = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
	inputs_w[3] = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
	
	// Using lepton isolation over pT
	inputs[4] = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());
	inputs_qcd[3] = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());
	
	// Retrieve nominal fake factors
	// To see the way to call each factor/systematic visit:
	// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766
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
	
	// Individual fake factos and their uncertainties
	// QCD same sign contribution
	product.m_optionalWeights["jetToTauFakeWeight_ff_qcd_ss"] = ff_qcd_ss->value(inputs);
	product.m_optionalWeights["jetToTauFakeWeight_ff_qcd_ss_up"] = ff_qcd_ss->value(inputs, "ff_qcd_up");
	product.m_optionalWeights["jetToTauFakeWeight_ff_qcd_ss_down"] = ff_qcd_ss->value(inputs, "ff_qcd_down");
	// QCD opposite sign contribution
	product.m_optionalWeights["jetToTauFakeWeight_ff_qcd_os"] = ff_qcd_os->value(inputs);
	product.m_optionalWeights["jetToTauFakeWeight_ff_qcd_os_up"] = ff_qcd_os->value(inputs, "ff_qcd_up");
	product.m_optionalWeights["jetToTauFakeWeight_ff_qcd_os_down"] = ff_qcd_os->value(inputs, "ff_qcd_down");
	// W contribution
	product.m_optionalWeights["jetToTauFakeWeight_ff_w"] = ff_w->value(inputs);
	product.m_optionalWeights["jetToTauFakeWeight_ff_w_up"] = ff_w->value(inputs, "ff_w_up");
	product.m_optionalWeights["jetToTauFakeWeight_ff_w_down"] = ff_w->value(inputs, "ff_w_down");
	// TTbar contribution
	product.m_optionalWeights["jetToTauFakeWeight_ff_tt"] = ff_tt->value(inputs);
	product.m_optionalWeights["jetToTauFakeWeight_ff_tt_corr_up"] = ff_tt->value(inputs, "ff_tt_corr_up");
	product.m_optionalWeights["jetToTauFakeWeight_ff_tt_corr_down"] = ff_tt->value(inputs, "ff_tt_corr_down");
	product.m_optionalWeights["jetToTauFakeWeight_ff_tt_stat_up"] = ff_tt->value(inputs, "ff_tt_stat_up");
	product.m_optionalWeights["jetToTauFakeWeight_ff_tt_stat_down"] = ff_tt->value(inputs, "ff_tt_stat_down");
}
