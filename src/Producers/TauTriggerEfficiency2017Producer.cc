
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTriggerEfficiency2017Producer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "TauTriggerSFs2017/TauTriggerSFs2017/interface/TauTriggerSFs2017.h"

std::string TauTriggerEfficiency2017Producer::GetProducerId() const
{
	return "TauTriggerEfficiency2017Producer";
}

void TauTriggerEfficiency2017Producer::Init(setting_type const& settings, metadata_type& metadata)
	{
	ProducerBase<HttTypes>::Init(settings, metadata);
        //TauSFs = new TauTriggerSFs2017("$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root","tight");
	TauSFs = new TauTriggerSFs2017(settings.GetTauTrigger2017Input(), settings.GetTauTrigger2017WorkingPoint());
	}

void TauTriggerEfficiency2017Producer::Produce(event_type const& event, product_type& product,
                                          setting_type const& settings, metadata_type const& metadata) const
{
	//TODO for olena: loop over both leptons for tt channel, and put it in the triggerweight. for et and mt it is calculated in DataMCScaleFactorProducer.cc
	//if variable changes into vector please also change DataMCScaleFactorProducer.cc, feel free to improve.
	//https://github.com/truggles/TauTriggerSFs2017
	KLepton* lepton = product.m_flavourOrderedLeptons[1];
	
	if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::ET)
        {
		//if(mc_weight)
        	product.m_tautriggerefficienciesMC = TauSFs->getETauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()); 
		product.m_tautriggerefficienciesData = TauSFs->getETauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
	}
	else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::MT)
        {
		product.m_tautriggerefficienciesMC = TauSFs->getMuTauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
		product.m_tautriggerefficienciesData = TauSFs->getMuTauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
	}
}
