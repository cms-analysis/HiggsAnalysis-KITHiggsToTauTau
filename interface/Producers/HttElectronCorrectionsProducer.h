
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ElectronCorrectionsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for electron energy scale corrections (Htt version).
   
   Required config tags
   - ElectronEnergyCorrection (possible value: fall2015)
*/
class HttElectronCorrectionsProducer: public ElectronCorrectionsProducer
{

public:

	typedef KappaEvent event_type;
	typedef KappaProduct product_type;
	typedef KappaSettings setting_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;

	enum class ElectronEnergyCorrection : int
	{
		NONE  = -1,
		FALL2015 = 0,      
	};
	static ElectronEnergyCorrection ToElectronEnergyCorrection(std::string const& eleEnergyCorrection)
	{
		if (eleEnergyCorrection == "fall2015") return ElectronEnergyCorrection::FALL2015;
		else return ElectronEnergyCorrection::NONE;
	}
	
	virtual void Init(setting_type const& settings) override;


protected:

	// Htt type electron energy corrections
	virtual void AdditionalCorrections(KElectron* electron, event_type const& event,
	                                   product_type& product, setting_type const& settings) const override;


private:
	ElectronEnergyCorrection eleEnergyCorrection;

};

