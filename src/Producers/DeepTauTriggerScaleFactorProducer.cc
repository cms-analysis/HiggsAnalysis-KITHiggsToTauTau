#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DeepTauTriggerScaleFactorProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/Utility.h"

std::string DeepTauTriggerScaleFactorProducer::GetProducerId() const
{
	return "DeepTauTriggerScaleFactorProducer";
}

void DeepTauTriggerScaleFactorProducer::Init(setting_type const& settings, metadata_type& metadata)
	{
	ProducerBase<HttTypes>::Init(settings, metadata);
	string decay_channel = "NONE";
	std::vector<std::string> DeepTauTriggerWorkingPoints = settings.GetDeepTauIDWorkingPoints();
	std::string DeepTauIDWorkingPoint = settings.GetDeepTauIDWorkingPoint();
	std::string_view DeepTauIDWorkingPoint_v(DeepTauIDWorkingPoint);
	std::string inputFile = settings.GetDeepTauTriggerInput();
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
	for(std::string DeepTauTriggerWorkingPoint:DeepTauTriggerWorkingPoints)
	{
		std::string_view DeepTauTriggerWorkingPoint_v(DeepTauTriggerWorkingPoint);
		std::shared_ptr<tau_trigger::SFProvider> TauTriggerSF(new tau_trigger::SFProvider(inputFile, decay_channel, DeepTauTriggerWorkingPoint_v));
		TauSFs.push_back(TauTriggerSF);
		HttEnumTypes::DeepTauIDWP tauidwp = HttEnumTypes::ToDeepTauIDWP(DeepTauTriggerWorkingPoint);
		for(unsigned int tauindex = 0; tauindex < 2; tauindex++)
		{
			std::string tautriggerefficiencyData = std::string("tautriggerefficiencyData_") + std::to_string(tauindex+1) + std::string("_") + DeepTauTriggerWorkingPoint;
			std::string tautriggerefficiencyMC = std::string("tautriggerefficiencyMC_") + std::to_string(tauindex+1) + std::string("_") + DeepTauTriggerWorkingPoint;
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, tautriggerefficiencyData, [tauindex, tauidwp](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
			{
				return product.m_deeptautriggerefficienciesData.at(tauidwp).at(tauindex);
			});

			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, tautriggerefficiencyMC, [tauindex, tauidwp](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
			{
				return product.m_deeptautriggerefficienciesMC.at(tauidwp).at(tauindex);
			});
		}
	}
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyData_1", [DeepTauIDWorkingPoint](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deeptautriggerefficienciesData.at(HttEnumTypes::ToDeepTauIDWP(DeepTauIDWorkingPoint)).at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyMC_1", [DeepTauIDWorkingPoint](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deeptautriggerefficienciesMC.at(HttEnumTypes::ToDeepTauIDWP(DeepTauIDWorkingPoint)).at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyData_2", [DeepTauIDWorkingPoint](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deeptautriggerefficienciesData.at(HttEnumTypes::ToDeepTauIDWP(DeepTauIDWorkingPoint)).at(1); //only used in Embedding2017 e tau final state
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyMC_2", [DeepTauIDWorkingPoint](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deeptautriggerefficienciesMC.at(HttEnumTypes::ToDeepTauIDWP(DeepTauIDWorkingPoint)).at(1); //only used in Embedding2017 e tau final state
	});
	}

void DeepTauTriggerScaleFactorProducer::Produce(event_type const& event, product_type& product,
																					setting_type const& settings, metadata_type const& metadata) const
{
	int unc_scale = 0;
	for(unsigned int i = 0; i < TauSFs.size(); i++)
	{
		std::vector<double> tautriggerefficienciesMC;
		std::vector<double> tautriggerefficienciesData;
		if((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) || (product.m_decayChannel ==  HttEnumTypes::DecayChannel::MT))
		{
			tautriggerefficienciesMC.push_back(1.0);
			tautriggerefficienciesData.push_back(1.0);

			KTau* tau = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);
			int decayMode = tau->decayMode;
			// if(decayMode==11||decayMode==5||decayMode==6){
			// 	LOG(WARNING) << "WARNING: decayMode = "<<decayMode<<" is not supported by TauTriggerSF. Using 10 instead.";
			// 	decayMode=10;
			// }
			tautriggerefficienciesMC.push_back(TauSFs.at(i)->getEfficiencyMC(tau->p4.Pt(), decayMode, unc_scale));
			tautriggerefficienciesData.push_back(TauSFs.at(i)->getEfficiencyData(tau->p4.Pt(), decayMode, unc_scale));

			LOG(DEBUG) << "Lepton 1 Pt: " << tau->p4.Pt() << " Eta: " <<  tau->p4.Eta() << std::endl;
			LOG(DEBUG) << "MC: " << tautriggerefficienciesMC[0] << " DATA: " << tautriggerefficienciesData[0] << std::endl;
		}
		else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::TT)
		{
			KTau* tau0 = static_cast<KTau*>(product.m_flavourOrderedLeptons[0]);
			KTau* tau1 = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);
			int decayMode0 = tau0->decayMode;
			// if(decayMode0==11||decayMode0==5||decayMode0==6){
			// 	LOG(WARNING) << "WARNING: decayMode = "<<decayMode0<<" is not supported by TauTriggerSF. Using 10 instead.";
			// 	decayMode0=10;
			// 									}
			int decayMode1 = tau1->decayMode;
			// if(decayMode1==11||decayMode1==5||decayMode1==6){
			// 	LOG(WARNING) << "WARNING: decayMode = "<<decayMode1<<" is not supported by TauTriggerSF. Using 10 instead.";
			// 										decayMode1=10;
			// 									}
			tautriggerefficienciesMC.push_back(TauSFs.at(i)->getEfficiencyMC(tau0->p4.Pt(), decayMode0, unc_scale));
			tautriggerefficienciesMC.push_back(TauSFs.at(i)->getEfficiencyMC(tau1->p4.Pt(), decayMode1, unc_scale));

			tautriggerefficienciesData.push_back(TauSFs.at(i)->getEfficiencyData(tau0->p4.Pt(), decayMode0, unc_scale));
			tautriggerefficienciesData.push_back(TauSFs.at(i)->getEfficiencyData(tau1->p4.Pt(), decayMode1, unc_scale));
		}
		product.m_deeptautriggerefficienciesMC[Utility::ToEnum<HttEnumTypes::DeepTauIDWP>(i)] = tautriggerefficienciesMC;
		product.m_deeptautriggerefficienciesData[Utility::ToEnum<HttEnumTypes::DeepTauIDWP>(i)] = tautriggerefficienciesData;
	}
}
