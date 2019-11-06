
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenHiggsCPProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"


std::string GenHiggsCPProducer::GetProducerId() const
{
	return "GenHiggsCPProducer";
}

void GenHiggsCPProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	// add possible quantities for the lambda ntuples consumers
	
	for (size_t particleIndex = 0; particleIndex < 9; ++particleIndex)
	{
		std::string particleIndexStr = std::to_string(particleIndex+1);
		
		LambdaNtupleConsumer<HttTypes>::AddCartesianRMFLVQuantity(metadata, "lheParticle"+particleIndexStr+"LV", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return event.m_lheParticles->particles.size() > particleIndex ? event.m_lheParticles->particles.at(particleIndex).p4 : DefaultValues::UndefinedCartesianRMFLV;
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lheParticle"+particleIndexStr+"PdgId", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return event.m_lheParticles->particles.size() > particleIndex ? event.m_lheParticles->particles.at(particleIndex).pdgId : DefaultValues::UndefinedInt;
		});
		
		LambdaNtupleConsumer<HttTypes>::AddCartesianRMFLVQuantity(metadata, "lheParticleIn"+particleIndexStr+"LV", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return product.m_lheParticlesIn.size() > particleIndex ? product.m_lheParticlesIn.at(particleIndex)->p4 : DefaultValues::UndefinedCartesianRMFLV;
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lheParticleIn"+particleIndexStr+"PdgId", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return product.m_lheParticlesIn.size() > particleIndex ? product.m_lheParticlesIn.at(particleIndex)->pdgId : DefaultValues::UndefinedInt;
		});
		
		LambdaNtupleConsumer<HttTypes>::AddCartesianRMFLVQuantity(metadata, "lheParticleOut"+particleIndexStr+"LV", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return product.m_lheParticlesOut.size() > particleIndex ? product.m_lheParticlesOut.at(particleIndex)->p4 : DefaultValues::UndefinedCartesianRMFLV;
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lheParticleOut"+particleIndexStr+"PdgId", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return product.m_lheParticlesOut.size() > particleIndex ? product.m_lheParticlesOut.at(particleIndex)->pdgId : DefaultValues::UndefinedInt;
		});
		
		LambdaNtupleConsumer<HttTypes>::AddCartesianRMFLVQuantity(metadata, "lheParticleBoson"+particleIndexStr+"LV", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return product.m_lheParticlesBoson.size() > particleIndex ? product.m_lheParticlesBoson.at(particleIndex)->p4 : DefaultValues::UndefinedCartesianRMFLV;
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lheParticleBoson"+particleIndexStr+"PdgId", [this, particleIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return product.m_lheParticlesBoson.size() > particleIndex ? product.m_lheParticlesBoson.at(particleIndex)->pdgId : DefaultValues::UndefinedInt;
		});
	}
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lheSignedDiJetDeltaPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_lheParticlesOut.size() > 1 ? ROOT::Math::VectorUtil::DeltaPhi(product.m_lheParticlesOut[0]->p4, product.m_lheParticlesOut[1]->p4) * (product.m_lheParticlesOut[0]->p4.Eta() > 0.0 ? 1.0 : -1.0) :
		                                              DefaultValues::UndefinedDouble;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lheDiJetAbsDeltaEta", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_lheParticlesOut.size() > 1 ? std::abs(product.m_lheParticlesOut[0]->p4.Eta() - product.m_lheParticlesOut[1]->p4.Eta()) :
		                                              DefaultValues::UndefinedDouble;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lheDiJetMass", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_lheParticlesOut.size() > 1 ? (product.m_lheParticlesOut[0]->p4 + product.m_lheParticlesOut[1]->p4).mass() :
		                                              DefaultValues::UndefinedDouble;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lheNJets", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_lheParticlesOut.size();
	});
}

void GenHiggsCPProducer::Produce(event_type const& event, product_type& product,
                                 setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_lheParticles);
	
	product.m_lheParticlesIn.clear();
	product.m_lheParticlesOut.clear();
	product.m_lheParticlesBoson.clear();
	
	for (std::vector<KLHEParticle>::iterator lheParticle = event.m_lheParticles->particles.begin(); lheParticle != event.m_lheParticles->particles.end(); ++lheParticle)
	{
		if (lheParticle->status < 0)
		{
			product.m_lheParticlesIn.push_back(&(*lheParticle));
		}
		else
		{
			if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(lheParticle->pdgId)))
			{
				product.m_lheParticlesBoson.push_back(&(*lheParticle));
			}
			else if ((std::abs(lheParticle->pdgId) <= DefaultValues::pdgIdTop) || (lheParticle->pdgId == DefaultValues::pdgIdGluon))
			{
				product.m_lheParticlesOut.push_back(&(*lheParticle));
			}
			else
			{
				// TODO: save outgoing particles if not quark or gluon separately? This currently does not happen in H->tautau samples
			}
		}
	}
}

