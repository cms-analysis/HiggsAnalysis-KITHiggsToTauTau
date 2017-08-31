
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


/** Producer to select the tautau restframe reconstruction method.
 *
 *  Required config tags:
 *  - TauTauRestFrameReco (possible valus: visible_leptons, visible_leptons_met, collinear_approximation, svfit)
 */
class TauTauRestFrameSelector: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "TauTauRestFrameSelector";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;


private:
	HttEnumTypes::TauTauRestFrameReco tauTauRestFrameReco;

};

