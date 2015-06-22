
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidTausProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief GlobalProducer, for valid taus.
   Config tags:
   - TauDiscriminatorIsolationCut (optional)
   - TauDiscriminatorAntiElectronMvaCuts (optional)
*/

class HttValidTausProducer: public ValidTausProducer
{
public:
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "HttValidTausProducer";
	}


protected:

	virtual void Init(KappaSettings const& settings) ARTUS_CPP11_OVERRIDE {
	
		ValidTausProducer::Init(settings);
		
		HttSettings const& specSettings = static_cast<HttSettings const&>(settings);
		MvaIsolationCutsByIndex = Utility::ParseMapTypes<size_t, float>(Utility::ParseVectorToMap(specSettings.GetTauDiscriminatorMvaIsolation()), MvaIsolationCutsByName);

		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingTauIso", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
			return product.m_validTaus.size() >=1 ? SafeMap::GetWithDefault(product.m_tauIsolation, product.m_validTaus[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingTauIsoOverPt", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
			return product.m_validTaus.size() >=1 ? SafeMap::GetWithDefault(product.m_tauIsolationOverPt, product.m_validTaus[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingTauIso", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
			return product.m_validTaus.size() >=2 ? SafeMap::GetWithDefault(product.m_tauIsolation, product.m_validTaus[1], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingTauIsoOverPt", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
			return product.m_validTaus.size() >=2 ? SafeMap::GetWithDefault(product.m_tauIsolationOverPt, product.m_validTaus[1], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
		});
	}
	
	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KTau* tau, KappaEvent const& event,
	                                KappaProduct& product, KappaSettings const& settings) const  ARTUS_CPP11_OVERRIDE;


private:
	bool ApplyCustomMvaIsolationCut(KTau* tau, KappaEvent const& event,
	                                  std::vector<float>) const;
	bool ApplyCustomElectronRejection(KTau* tau, KappaEvent const& event,
	                                  HttSettings const& settings) const;

	std::map<size_t, std::vector<float> > MvaIsolationCutsByIndex;
	std::map<std::string, std::vector<float> > MvaIsolationCutsByName;

};

