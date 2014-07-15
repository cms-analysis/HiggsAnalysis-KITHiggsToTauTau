
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/TauEnergyCorrectionProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for tau energy scale corrections (Htt version).
   
   Required config tags
   - TauEnergyCorrection (possible value: summer2013)
*/
class HttTauEnergyCorrectionProducer: public TauEnergyCorrectionProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	enum class TauEnergyCorrection : int
	{
		NONE  = -1,
		SUMMER2013 = 0,
	};
	static TauEnergyCorrection ToTauEnergyCorrection(std::string const& tauEnergyCorrection)
	{
		if (tauEnergyCorrection == "summer2013") return TauEnergyCorrection::SUMMER2013;
		else return TauEnergyCorrection::NONE;
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;


protected:

	// Htt type tau energy corrections
	virtual void AdditionalCorrections(KDataPFTau* tau, event_type const& event,
	                                   product_type& product, setting_type const& settings) const ARTUS_CPP11_OVERRIDE;


private:
	TauEnergyCorrection tauEnergyCorrection;

};

