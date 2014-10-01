
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

protected:

	virtual void Init(KappaSettings const& settings) ARTUS_CPP11_OVERRIDE {
	
		ValidTausProducer::Init(settings);
		
		HttSettings const& specSettings = static_cast<HttSettings const&>(settings);
		MvaIsolationCutsByIndex = Utility::ParseMapTypes<size_t, float>(Utility::ParseVectorToMap(specSettings.GetTauDiscriminatorMvaIsolation()), MvaIsolationCutsByName);
	}
	
	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataPFTau* tau, KappaEvent const& event,
	                                KappaProduct& product, KappaSettings const& settings) const  ARTUS_CPP11_OVERRIDE;


private:
	bool ApplyCustomMvaIsolationCut(KDataPFTau* tau, KappaEvent const& event,
	                                  std::vector<float>) const;
	bool ApplyCustomElectronRejection(KDataPFTau* tau, KappaEvent const& event,
	                                  HttSettings const& settings) const;

	std::map<size_t, std::vector<float> > MvaIsolationCutsByIndex;
	std::map<std::string, std::vector<float> > MvaIsolationCutsByName;

};

