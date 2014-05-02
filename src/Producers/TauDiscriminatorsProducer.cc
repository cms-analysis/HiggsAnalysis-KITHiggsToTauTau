
#include <string>

#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauDiscriminatorsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"


void TauDiscriminatorsProducer::ProduceGlobal(event_type const& event,
                                              product_type& product,
                                              global_setting_type const& globalSettings) const
{
	Produce(event, product, globalSettings.GetTauDiscriminators());
}

void TauDiscriminatorsProducer::ProduceLocal(event_type const& event,
                                             product_type& product,
                                             setting_type const& settings) const
{
	TauDiscriminatorsProducer::Produce(event, product, settings.GetTauDiscriminators());
}

void TauDiscriminatorsProducer::Produce(event_type const& event, product_type& product, stringvector discriminatorNames) const
{
	// parse configuration to define pt-dependent discriminators
	std::map<int, std::vector<std::string> > discriminators = HttValidTausProducer::ParseTauDiscriminators(discriminatorNames);
	
	int index = 0;
	for (std::vector<KDataPFTau*>::iterator tau = product.m_validTaus.begin(); tau != product.m_validTaus.end(); )
	{
		// get pt-dependent discriminators
		stringvector tmpDiscriminatorNames = SafeMap::GetWithDefault(discriminators, index,
		                                     SafeMap::GetWithDefault(discriminators, -1, std::vector<std::string>()));
		
		// filter on discriminators
		bool validTau = true;
		for (stringvector::iterator discriminatorName = tmpDiscriminatorNames.begin();
		     discriminatorName != tmpDiscriminatorNames.end(); ++discriminatorName)
		{
			validTau = validTau && (*tau)->hasID(*discriminatorName, event.m_tauDiscriminatorMetadata);
			if (! validTau)
				break;
		}
		
		if (validTau)
			++tau;
		else {
			product.m_invalidTaus.push_back(*tau);
			tau = product.m_validTaus.erase(tau);
		}
		++index;
	}
	
	// resort invalid taus list
	std::sort(product.m_invalidTaus.begin(), product.m_invalidTaus.end(),
	          [](KDataPFTau* tau1, KDataPFTau* tau2) { return tau1->p4.Pt() > tau2->p4.Pt(); });
}

