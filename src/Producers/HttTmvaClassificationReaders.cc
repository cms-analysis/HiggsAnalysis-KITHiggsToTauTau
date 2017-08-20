
#include <Math/VectorUtil.h>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTmvaClassificationReaders.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"
#include "Artus/Utility/interface/DefaultValues.h"

	
AntiTtbarDiscriminatorTmvaReader::AntiTtbarDiscriminatorTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&setting_type::GetAntiTtbarTmvaInputQuantities,
	                                       &setting_type::GetAntiTtbarTmvaMethods,
	                                       &setting_type::GetAntiTtbarTmvaWeights,
	                                       &product_type::m_antiTtbarDiscriminators)
{
}

void AntiTtbarDiscriminatorTmvaReader::Init(setting_type const& settings, metadata_type& metadata)
{
	// register variables needed for the MVA evaluation
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva_pzetavis", [](event_type const& event, product_type const& product)
	{
		return product.pZetaVis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva_pzetamiss", [](event_type const& event, product_type const& product)
	{
		return product.pZetaMissVis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva_dphi", [](event_type const& event, product_type const& product)
	{
		return std::abs(ROOT::Math::VectorUtil::DeltaPhi(product.m_flavourOrderedLeptons[0]->p4,
		                                                 product.m_flavourOrderedLeptons[1]->p4));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva_mvamet", [](event_type const& event, product_type const& product)
	{
		return product.m_met.p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva_mtll", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4,
		                               product.m_flavourOrderedLeptons[1]->p4);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva_csv", [](event_type const& event, product_type const& product)
	{
		float csv = -1.0;
		for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin();
		     ((jet != product.m_validJets.end()) && ((*jet)->p4.Pt() > 20.0)); ++jet)
		{
			if (((*jet)->p4.Pt() > 20.0) && (std::abs((*jet)->p4.Eta()) < 2.4))
			{
				csv = static_cast<KJet const*>(*jet)->getTag("CombinedSecondaryVertexBJetTags", event.m_jetMetadata);
				csv = ((csv > 0.244) ? csv : -1.0);
				break;
			}
		}
		return csv;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva_d01", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->track.getDxy(&(event.m_vertexSummary->pv));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("emAntiTTbarMva", [](event_type const& event, product_type const& product)
	{
		return ((product.m_antiTtbarDiscriminators.size() > 0) ? product.m_antiTtbarDiscriminators[0] : DefaultValues::UndefinedFloat);
	});
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Init(settings, metadata);
}

void AntiTtbarDiscriminatorTmvaReader::Produce(event_type const& event,
                                               product_type& product,
                                               setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_tjets);
	assert(event.m_jetMetadata);
	assert(product.m_metUncorr);
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Produce(event, product, settings, metadata);
}

// Tau polarisation MVA class:

TauPolarisationTmvaReader::TauPolarisationTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&setting_type::GetTauPolarisationTmvaInputQuantities,
	                                       &setting_type::GetTauPolarisationTmvaMethods,
	                                       &setting_type::GetTauPolarisationTmvaWeights,
	                                       &product_type::m_tauPolarisationDiscriminators)
{
}

void TauPolarisationTmvaReader::Init(setting_type const& settings, metadata_type& metadata)
{
	// register variables needed for the MVA evaluation
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauPolarisationTMVA", [](event_type const& event, product_type const& product)
	{
		return ((product.m_tauPolarisationDiscriminators.size() > 0) ? product.m_tauPolarisationDiscriminators[0] : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauPolarisationSKLEARN", [](event_type const& event, product_type const& product)
	{
		return ((product.m_tauPolarisationDiscriminators.size() > 0) ? product.m_tauPolarisationDiscriminators[1] : DefaultValues::UndefinedFloat);
	});
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Init(settings, metadata);
}

void TauPolarisationTmvaReader::Produce(event_type const& event,
                                               product_type& product,
                                               setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_tjets);
	assert(event.m_jetMetadata);
	assert(product.m_metUncorr);
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Produce(event, product, settings, metadata);
}

