
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTriggerEfficiency2017Producer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/Utility.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/TauTriggerSFs2017.h"

std::string TauTriggerEfficiency2017Producer::GetProducerId() const
{
	return "TauTriggerEfficiency2017Producer";
}

void TauTriggerEfficiency2017Producer::Init(setting_type const& settings, metadata_type& metadata)
	{
	ProducerBase<HttTypes>::Init(settings, metadata);
	std::string decay_channel = "NONE";
	// string wp_type = "NONE";
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
	for(std::string TauTrigger2017WorkingPoint:settings.GetTauTrigger2017WorkingPoints())
	{
	        std::string tauIDType = settings.GetTauIDType();
		if(tauIDType!="MVAv2")
		{
			LOG(WARNING) << "tauIDType = "<<tauIDType<<" is not supported by TauTriggerSF. Using MVAv2 instead.";
		  tauIDType = "MVAv2";
		}
		std::shared_ptr<TauTriggerSFs2017> TauTriggerSF(new TauTriggerSFs2017(settings.GetTauTrigger2017Input(), decay_channel, "2017", TauTrigger2017WorkingPoint, tauIDType));
		TauSFs.push_back(TauTriggerSF);
		HttEnumTypes::TauIDWP tauidwp = HttEnumTypes::ToTauIDWP(TauTrigger2017WorkingPoint);
		for(unsigned int tauindex = 0; tauindex < 2; tauindex++)
		{
			std::string tautriggerefficiencyData = std::string("tautriggerefficiencyData_") + std::to_string(tauindex+1) + std::string("_") + TauTrigger2017WorkingPoint;
			std::string tautriggerefficiencyMC = std::string("tautriggerefficiencyMC_") + std::to_string(tauindex+1) + std::string("_") + TauTrigger2017WorkingPoint;
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, tautriggerefficiencyData, [tauindex, tauidwp](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
			{
				return product.m_tautriggerefficienciesData.at(tauidwp).at(tauindex);
			});

			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, tautriggerefficiencyMC, [tauindex, tauidwp](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
			{
				return product.m_tautriggerefficienciesMC.at(tauidwp).at(tauindex);
			});
		}
	}
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyData_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyMC_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyData_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).at(1); //only used in Embedding2017 e tau final state
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tautriggerefficiencyMC_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).at(1); //only used in Embedding2017 e tau final state
	});
	}

void TauTriggerEfficiency2017Producer::Produce(event_type const& event, product_type& product,
                                          setting_type const& settings, metadata_type const& metadata) const
{
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
			if(decayMode==11||decayMode==5||decayMode==6){
			  LOG(WARNING) << "WARNING: decayMode = "<<decayMode<<" is not supported by TauTriggerSF. Using 10 instead.";
			  decayMode=10;
			}
			tautriggerefficienciesMC.push_back(TauSFs.at(i)->getTriggerEfficiencyMC(tau->p4.Pt(),tau->p4.Eta(),tau->p4.Phi(),decayMode));
			tautriggerefficienciesData.push_back(TauSFs.at(i)->getTriggerEfficiencyData(tau->p4.Pt(),tau->p4.Eta(),tau->p4.Phi(),decayMode));

			LOG(DEBUG) << "Lepton 1 Pt: " << tau->p4.Pt() << " Eta: " <<  tau->p4.Eta() << std::endl;
			LOG(DEBUG) << "MC: " << tautriggerefficienciesMC[0] << " DATA: " << tautriggerefficienciesData[0] << std::endl;
		}
		else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::TT)
		{
			KTau* tau0 = static_cast<KTau*>(product.m_flavourOrderedLeptons[0]);
			KTau* tau1 = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);
			int decayMode0 = tau0->decayMode;
			if(decayMode0==11||decayMode0==5||decayMode0==6){
			  LOG(WARNING) << "WARNING: decayMode = "<<decayMode0<<" is not supported by TauTriggerSF. Using 10 instead.";
			  decayMode0=10;
                        }
			int decayMode1 = tau1->decayMode;
			if(decayMode1==11||decayMode1==5||decayMode1==6){
			  LOG(WARNING) << "WARNING: decayMode = "<<decayMode1<<" is not supported by TauTriggerSF. Using 10 instead.";
                          decayMode1=10;
                        }
			tautriggerefficienciesMC.push_back(TauSFs.at(i)->getTriggerEfficiencyMC(tau0->p4.Pt(),tau0->p4.Eta(),tau0->p4.Phi(),decayMode0));
			tautriggerefficienciesMC.push_back(TauSFs.at(i)->getTriggerEfficiencyMC(tau1->p4.Pt(),tau1->p4.Eta(),tau1->p4.Phi(),decayMode1));

			tautriggerefficienciesData.push_back(TauSFs.at(i)->getTriggerEfficiencyData(tau0->p4.Pt(),tau0->p4.Eta(),tau0->p4.Phi(),decayMode0));
			tautriggerefficienciesData.push_back(TauSFs.at(i)->getTriggerEfficiencyData(tau1->p4.Pt(),tau1->p4.Eta(),tau1->p4.Phi(),decayMode1));
		}
		product.m_tautriggerefficienciesMC[Utility::ToEnum<HttEnumTypes::TauIDWP>(i)] = tautriggerefficienciesMC;
		product.m_tautriggerefficienciesData[Utility::ToEnum<HttEnumTypes::TauIDWP>(i)] = tautriggerefficienciesData;
	}
}
