#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/LFVJetCorrection2016Producer.h"

void LFVJetCorrection2016Producer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);		
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jetCorrectionWeight", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.lfvjetcorr;
	});
;
}


void LFVJetCorrection2016Producer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	std::vector<float> em_correction = {0.7746813893318176, 3.78820538520813, 7.594935417175293, 12.17646354, 17.546980964};
	std::vector<float> et_correction = {0.745861828327179, 4.280722141265869, 10.161121368408203, 18.6265464, 29.580584};
	std::vector<float> mt_correction = {0.7987861037254333, 3.5566015243530273, 7.512916088104248, 12.8207459, 19.4355435};

	int njet = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);

	if(product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::ELECTRON and product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::MUON)
	{	
		if(njet < 5)
		{
			product.lfvjetcorr = em_correction.at(njet);

		}
		
		else
		{
			product.lfvjetcorr = 1.0;
		}
		
						
	}	
	
		
	if(product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::ELECTRON and product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU)
	{	
		if(njet < 5)
		{
			product.lfvjetcorr = et_correction.at(njet);
		}
		
		else
		{
			product.lfvjetcorr = 1.0;
		}

						
	}
	if(product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::MUON and product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU)
	{	
		if(njet < 5)
		{
			product.lfvjetcorr = mt_correction.at(njet);
		}
		
		else
		{
			product.lfvjetcorr = 1.0;
		}
						
	}
}
