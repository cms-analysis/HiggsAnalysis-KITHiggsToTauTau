
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTriggerEfficiency2017Producer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/TauTriggerSFs2017.h"

std::string TauTriggerEfficiency2017Producer::GetProducerId() const
{
	return "TauTriggerEfficiency2017Producer";
}

void TauTriggerEfficiency2017Producer::Init(setting_type const& settings, metadata_type& metadata)
	{
	ProducerBase<HttTypes>::Init(settings, metadata);
	// TauSFs = new TauTriggerSFs2017("$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root","tight");
	// TauSFs = new TauTriggerSFs2017(settings.GetTauTrigger2017Input(), settings.GetTauTrigger2017InputOLD(), settings.GetTauTrigger2017WorkingPoint()); // TODO: , "MVA" not yet updated for c++ code
	string decay_channel = "NONE";
	string wp_type = "NONE";
	if(settings.GetChannel() == "ET")
	{
		decay_channel = "etau";
	}
	else if(settings.GetChannel() == "MT")
	{
		decay_channel = "mutau";
	}
	else if(settings.GetChannel() == "TT")
	{
		decay_channel = "ditau";
	}
	if(settings.GetTauDiscriminatorIsolationName() == "byIsolationMVArun2017v2DBoldDMwLTraw2017")
	{
		wp_type = "MVAv2";
	}
	
	TauSFs = new TauTriggerSFs2017(settings.GetTauTrigger2017Input(), decay_channel, "2017", settings.GetTauTrigger2017WorkingPoint(), wp_type);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyData", [](event_type const& event, product_type const& product)
	{
		return product.m_tautriggerefficienciesData.at(0); //only used in Embedding2017 e tau final state
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyMC", [](event_type const& event, product_type const& product)
	{
		return product.m_tautriggerefficienciesData.at(0); //only used in Embedding2017 e tau final state
	});

	}

void TauTriggerEfficiency2017Producer::Produce(event_type const& event, product_type& product,
                                          setting_type const& settings, metadata_type const& metadata) const
{
	//TODO loop over both leptons for tt channel, and put it in the triggerweight. for et and mt it is calculated in RooWorkspaceWeightProducer.cc
	//if variable changes into vector please also change DataMCScaleFactorProducer.cc, feel free to improve.
	//https://github.com/truggles/TauTriggerSFs2017
	// 
	// if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::ET)
  //       {
	// 	KLepton* lepton = product.m_flavourOrderedLeptons[1];
	// 	//if(mc_weight)
  //       	product.m_tautriggerefficienciesMC.push_back(TauSFs->getETauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
	// 	product.m_tautriggerefficienciesData.push_back(TauSFs->getETauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
	// 
	// 	LOG(DEBUG) << "Lepton 1     Pt: " << lepton->p4.Pt() << "Eta: " <<  lepton->p4.Eta() << std::endl;
	// 	LOG(DEBUG) << "MC:  " << product.m_tautriggerefficienciesMC[0] << "DATA: " << product.m_tautriggerefficienciesData[0] << std::endl;
	// }
	// else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::MT)
  //       {
	// 	KLepton* lepton = product.m_flavourOrderedLeptons[1];
	// 	product.m_tautriggerefficienciesMC.push_back(TauSFs->getMuTauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
	// 	product.m_tautriggerefficienciesData.push_back(TauSFs->getMuTauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi()));
	// }
	// else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::TT)
	// {
	// 	KLepton* lepton0 = product.m_flavourOrderedLeptons[0];
	// 	KLepton* lepton1 = product.m_flavourOrderedLeptons[1];
	// 	product.m_tautriggerefficienciesMC.push_back(TauSFs->getDiTauEfficiencyMC(lepton0->p4.Pt(),lepton0->p4.Eta(),lepton0->p4.Phi()));
	// 	product.m_tautriggerefficienciesMC.push_back(TauSFs->getDiTauEfficiencyMC(lepton1->p4.Pt(),lepton1->p4.Eta(),lepton1->p4.Phi()));
	// 
	// 	product.m_tautriggerefficienciesData.push_back(TauSFs->getDiTauEfficiencyData(lepton0->p4.Pt(),lepton0->p4.Eta(),lepton0->p4.Phi()));
	// 	product.m_tautriggerefficienciesData.push_back(TauSFs->getDiTauEfficiencyData(lepton1->p4.Pt(),lepton1->p4.Eta(),lepton1->p4.Phi()));
	// }

	if((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) || (product.m_decayChannel ==  HttEnumTypes::DecayChannel::MT))
	{
		KTau* tau = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);
		product.m_tautriggerefficienciesMC.push_back(TauSFs->getTriggerEfficiencyMC(tau->p4.Pt(),tau->p4.Eta(),tau->p4.Phi(),tau->decayMode));
		product.m_tautriggerefficienciesData.push_back(TauSFs->getTriggerEfficiencyData(tau->p4.Pt(),tau->p4.Eta(),tau->p4.Phi(),tau->decayMode));

		LOG(DEBUG) << "Lepton 1 Pt: " << tau->p4.Pt() << " Eta: " <<  tau->p4.Eta() << std::endl;
		LOG(DEBUG) << "MC: " << product.m_tautriggerefficienciesMC[0] << " DATA: " << product.m_tautriggerefficienciesData[0] << std::endl;
	}
	else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::TT)
	{
		KTau* tau0 = static_cast<KTau*>(product.m_flavourOrderedLeptons[0]);
		KTau* tau1 = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);
		product.m_tautriggerefficienciesMC.push_back(TauSFs->getTriggerEfficiencyMC(tau0->p4.Pt(),tau0->p4.Eta(),tau0->p4.Phi(),tau0->decayMode));
		product.m_tautriggerefficienciesMC.push_back(TauSFs->getTriggerEfficiencyMC(tau1->p4.Pt(),tau1->p4.Eta(),tau1->p4.Phi(),tau1->decayMode));

		product.m_tautriggerefficienciesData.push_back(TauSFs->getTriggerEfficiencyData(tau0->p4.Pt(),tau0->p4.Eta(),tau0->p4.Phi(),tau0->decayMode));
		product.m_tautriggerefficienciesData.push_back(TauSFs->getTriggerEfficiencyData(tau1->p4.Pt(),tau1->p4.Eta(),tau1->p4.Phi(),tau1->decayMode));
	}
}
