#pragma once

#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief
   Produces impact parameter vector and related quantities.
   Formerly produced in RecoTauCPProducer
*/

class ImpactParameterProducer : public ProducerBase<HttTypes> {
	private:
		bool m_isData;

	public:

		virtual std::string GetProducerId() const override;

		virtual void Init(setting_type const& settings, metadata_type& metadata) override;

		virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;
};
