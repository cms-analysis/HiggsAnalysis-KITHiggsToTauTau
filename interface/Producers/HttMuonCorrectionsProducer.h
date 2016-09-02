
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/MuonCorrectionsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for muon energy scale corrections (Htt version).
   
   Required config tags
   - MuonEnergyCorrection (possible value: fall2015)
*/

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/RoccoR.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/rochcor2015.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/rochcor2016.h"

class HttMuonCorrectionsProducer: public MuonCorrectionsProducer
{

public:

	typedef KappaEvent event_type;
	typedef KappaProduct product_type;
	typedef KappaSettings setting_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;

	enum class MuonEnergyCorrection : int
	{
		NONE  = -1,
		FALL2015 = 0,
		ROCHCORR2015 = 1,
		ROCHCORR2016 = 2
	};
	static MuonEnergyCorrection ToMuonEnergyCorrection(std::string const& muonEnergyCorrection)
	{
		if (muonEnergyCorrection == "fall2015") return MuonEnergyCorrection::FALL2015;
		else if (muonEnergyCorrection == "rochcorr2015") return MuonEnergyCorrection::ROCHCORR2015;
		else if (muonEnergyCorrection == "rochcorr2016") return MuonEnergyCorrection::ROCHCORR2016;
		else return MuonEnergyCorrection::NONE;
	}
	
	virtual void Init(setting_type const& settings) override;


protected:

	// Htt type muon energy corrections
	virtual void AdditionalCorrections(KMuon* muon, event_type const& event,
	                                   product_type& product, setting_type const& settings) const override;


private:
	MuonEnergyCorrection muonEnergyCorrection;
	rochcor2015 *rmcor2015;
	rochcor2016 *rmcor2016;

};

