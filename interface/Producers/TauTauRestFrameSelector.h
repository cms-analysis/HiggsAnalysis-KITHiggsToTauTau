
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

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const override {
		return "TauTauRestFrameSelector";
	}
	
	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;


private:
	HttEnumTypes::TauTauRestFrameReco tauTauRestFrameReco;

};

