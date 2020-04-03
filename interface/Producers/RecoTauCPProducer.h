#pragma once

#include "Artus/Utility/interface/Utility.h"


#include "Kappa/DataFormats/interface/Kappa.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/Utility/interface/DefaultValues.h"

/**
   \brief
*/

class RecoTauCPProducer : public ProducerBase<HttTypes> {
	private:
		bool m_isData;
		RMFLV alternativePiZeroMomentum(const KTau* tau);

	public:

		virtual std::string GetProducerId() const override;
		
		virtual void Init(setting_type const& settings, metadata_type& metadata)  override;
	
		virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;
};
