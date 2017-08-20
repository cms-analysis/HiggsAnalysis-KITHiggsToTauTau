
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

	typedef typename KappaTypes::event_type event_type;
	typedef typename KappaTypes::product_type product_type;
	typedef typename KappaTypes::setting_type setting_type;
	typedef typename KappaTypes::metadata_type metadata_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;
	typedef typename HttTypes::metadata_type spec_metadata_type;

protected:

	virtual void Init(setting_type const& settings, metadata_type& metadata) override {
	
		ValidTausProducer::Init(settings, metadata);
		
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
	virtual bool AdditionalCriteria(KTau* tau, event_type const& event,
	                                product_type& product, setting_type const& settings, metadata_type const& metadata) const  override;


private:
	bool ApplyCustomMvaIsolationCut(KTau* tau, event_type const& event,
	                                  std::vector<float>) const;
	bool ApplyCustomElectronRejection(KTau* tau, event_type const& event,
	                                  HttSettings const& settings) const;

	std::map<size_t, std::vector<float> > MvaIsolationCutsByIndex;
	std::map<std::string, std::vector<float> > MvaIsolationCutsByName;

};

