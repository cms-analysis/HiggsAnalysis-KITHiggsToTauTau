
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/TauCorrectionsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for tau energy scale corrections (Htt version).

   Required config tags
   - TauEnergyCorrection (possible value: summer2013)
*/
class HttTauCorrectionsProducer: public TauCorrectionsProducer
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

	enum class TauEnergyCorrection : int
	{
		NONE  = -1,
		SUMMER2013 = 0,
		NEWTAUID = 1,
		SMHTT2016,
		MSSMHTT2016,
		SMHTT2017,
		LEGACY2017,
	};
	static TauEnergyCorrection ToTauEnergyCorrection(std::string const& tauEnergyCorrection)
	{
		if (tauEnergyCorrection == "summer2013") return TauEnergyCorrection::SUMMER2013;
		else if (tauEnergyCorrection == "newtauid") return TauEnergyCorrection::NEWTAUID;
		else if (tauEnergyCorrection == "smhtt2016") return TauEnergyCorrection::SMHTT2016;
		else if (tauEnergyCorrection == "mssmhtt2016") return TauEnergyCorrection::MSSMHTT2016;
		else if (tauEnergyCorrection == "smhtt2017") return TauEnergyCorrection::SMHTT2017;
		else if (tauEnergyCorrection == "legacy2017") return TauEnergyCorrection::LEGACY2017;
		else return TauEnergyCorrection::NONE;
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;


protected:

	// Htt type tau energy corrections
	virtual void AdditionalCorrections(KTau* tau, event_type const& event,
	                                   product_type& product, setting_type const& settings, metadata_type const& metadata) const override;


private:
	TauEnergyCorrection tauEnergyCorrection;

};

