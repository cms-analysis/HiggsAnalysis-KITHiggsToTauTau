
#include <Math/VectorUtil.h>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTmvaClassificationReaders.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/Quantities.h"
#include "Artus/Utility/interface/DefaultValues.h"

	
AntiTtbarDiscriminatorTmvaReader::AntiTtbarDiscriminatorTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&spec_setting_type::GetAntiTtbarTmvaInputQuantities,
	                                       &spec_setting_type::GetAntiTtbarTmvaMethods,
	                                       &spec_setting_type::GetAntiTtbarTmvaWeights,
	                                       &spec_product_type::m_antiTtbarDiscriminators)
{
}

void AntiTtbarDiscriminatorTmvaReader::Init(spec_setting_type const& settings)
{
	// register variables needed for the MVA evaluation
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pzetavis", [](spec_event_type const& event, spec_product_type const& product)
	{
		return product.pZetaVis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pzetamiss", [](spec_event_type const& event, spec_product_type const& product)
	{
		return product.pZetaMissVis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dphi", [](spec_event_type const& event, spec_product_type const& product)
	{
		return std::abs(ROOT::Math::VectorUtil::DeltaPhi(product.m_flavourOrderedLeptons[0]->p4,
		                                                 product.m_flavourOrderedLeptons[1]->p4));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvamet", [](spec_event_type const& event, spec_product_type const& product)
	{
		return product.m_met->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mtll", [](spec_event_type const& event, spec_product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4,
		                               product.m_flavourOrderedLeptons[1]->p4);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("csv", [](spec_event_type const& event, spec_product_type const& product)
	{
		float csv = -1.0;
		for (std::vector<KDataPFJet*>::const_iterator jet = product.m_validJets.begin();
		     ((jet != product.m_validJets.end()) && ((*jet)->p4.Pt() > 20.0)); ++jet)
		{
			if (((*jet)->p4.Pt() > 20.0) && (std::abs((*jet)->p4.Eta()) < 2.4))
			{
				csv = static_cast<KDataPFTaggedJet const*>(*jet)->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggerMetadata);
				csv = ((csv > 0.244) ? csv : -1.0);
				break;
			}
		}
		return csv;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d01", [](spec_event_type const& event, spec_product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->track.getDxy(&(event.m_vertexSummary->pv));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva", [](spec_event_type const& event, spec_product_type const& product)
	{
		return ((product.m_antiTtbarDiscriminators.size() > 0) ? product.m_antiTtbarDiscriminators[0] : DefaultValues::UndefinedFloat);
	});
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Init(settings);
}

void AntiTtbarDiscriminatorTmvaReader::Produce(spec_event_type const& event,
                                               spec_product_type& product,
                                               spec_setting_type const& settings) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_tjets);
	assert(event.m_taggerMetadata);
	assert(event.m_mvaMetEM);
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Produce(event, product, settings);
}

