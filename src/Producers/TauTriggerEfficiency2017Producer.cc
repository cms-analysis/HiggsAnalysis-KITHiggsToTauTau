
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
	TauSFs = new TauTriggerSFs2017(settings.GetTauTrigger2017Input(), settings.GetTauTrigger2017WorkingPoint()); // TODO: , "MVA" not yet updated for c++ code
	}

void TauTriggerEfficiency2017Producer::Produce(event_type const& event, product_type& product,
                                          setting_type const& settings, metadata_type const& metadata) const
{
	//TODO loop over both leptons for tt channel, and put it in the triggerweight. for et and mt it is calculated in RooWorkspaceWeightProducer.cc
	//if variable changes into vector please also change DataMCScaleFactorProducer.cc, feel free to improve.
	//https://github.com/truggles/TauTriggerSFs2017
	
	if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::ET)
        {
		KLepton* lepton = product.m_flavourOrderedLeptons[1];
		//if(mc_weight)
        	product.m_tautriggerefficienciesMC.push_back(TauSFs->getETauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
		product.m_tautriggerefficienciesData.push_back(TauSFs->getETauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
		
		LOG(DEBUG) << "Lepton 1     Pt: " << lepton->p4.Pt() << "Eta: " <<  lepton->p4.Eta() << std::endl;
		LOG(DEBUG) << "MC:  " << product.m_tautriggerefficienciesMC[0] << "DATA: " << product.m_tautriggerefficienciesData[0] << std::endl;
	}
	else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::MT)
        {
		KLepton* lepton = product.m_flavourOrderedLeptons[1];
		product.m_tautriggerefficienciesMC.push_back(TauSFs->getMuTauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
		product.m_tautriggerefficienciesData.push_back(TauSFs->getMuTauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
	}
	else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::TT)
	{
		KLepton* lepton0 = product.m_flavourOrderedLeptons[0];
		KLepton* lepton1 = product.m_flavourOrderedLeptons[1];
		product.m_tautriggerefficienciesMC.push_back(TauSFs->getDiTauEfficiencyMC(lepton0->p4.Pt(),lepton0->p4.Eta(),lepton0->p4.Phi()));
		product.m_tautriggerefficienciesMC.push_back(TauSFs->getDiTauEfficiencyMC(lepton1->p4.Pt(),lepton1->p4.Eta(),lepton1->p4.Phi()));

		product.m_tautriggerefficienciesData.push_back(TauSFs->getDiTauEfficiencyData(lepton0->p4.Pt(),lepton0->p4.Eta(),lepton0->p4.Phi()));
		product.m_tautriggerefficienciesData.push_back(TauSFs->getDiTauEfficiencyData(lepton1->p4.Pt(),lepton1->p4.Eta(),lepton1->p4.Phi()));
	}
}
