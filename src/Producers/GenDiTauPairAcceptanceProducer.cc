
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenDiTauPairAcceptanceProducer.h"


void GenDiTauPairAcceptanceProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nGenDiTauPairsInAcceptance", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return static_cast<int>(product.m_genDiTauPairInAcceptance.size());
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genDiTauPairMass", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return (product.m_genDiTauPairCandidates[0].first->p4 + product.m_genDiTauPairCandidates[0].second->p4).mass();
	});
}

void GenDiTauPairAcceptanceProducer::Produce(event_type const& event, product_type& product,
	                            setting_type const& settings, metadata_type const& metadata) const
{
	for (std::vector<DiGenTauPair>::iterator pair = product.m_genDiTauPairCandidates.begin();
	     pair != product.m_genDiTauPairCandidates.end(); ++pair)
	{
		bool passAcceptanceCuts = true;
		
		passAcceptanceCuts = passAcceptanceCuts && ((*pair).first->p4.Pt() > settings.GetLepton1AcceptancePtCut())
							&& (std::abs((*pair).first->p4.Eta()) < settings.GetLepton1AcceptanceEtaCut());
		
		passAcceptanceCuts = passAcceptanceCuts && ((*pair).second->p4.Pt() > settings.GetLepton2AcceptancePtCut())
							&& (std::abs((*pair).second->p4.Eta()) < settings.GetLepton2AcceptanceEtaCut());
		
		if (passAcceptanceCuts)
		{
			product.m_genDiTauPairInAcceptance.push_back(*pair);
		}
	}
}
