
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "../HttTypes.h"


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
	
	enum class TauTauRestFrameReco : int
	{
		NONE  = -1,
		VISIBLE_LEPTONS = 0,
		VISIBLE_LEPTONS_MET = 1,
		COLLINEAR_APPROXIMATION  = 2,
		SVFIT  = 3,
	};
	static TauTauRestFrameReco ToTauTauRestFrameReco(std::string const& tauTauRestFrameReco)
	{
		if (tauTauRestFrameReco == "visible_leptons") return TauTauRestFrameReco::VISIBLE_LEPTONS;
		else if (tauTauRestFrameReco == "visible_leptons_met") return TauTauRestFrameReco::VISIBLE_LEPTONS_MET;
		else if (tauTauRestFrameReco == "collinear_approximation") return TauTauRestFrameReco::COLLINEAR_APPROXIMATION;
		else if (tauTauRestFrameReco == "svfit") return TauTauRestFrameReco::SVFIT;
		else return TauTauRestFrameReco::NONE;
	}
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tautau_restframe";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;


private:
	TauTauRestFrameReco tauTauRestFrameReco;

};

