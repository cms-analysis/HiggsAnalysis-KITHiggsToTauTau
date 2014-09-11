
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

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataPFTau* tau, KappaEvent const& event,
	                                KappaProduct& product, KappaSettings const& settings) const  ARTUS_CPP11_OVERRIDE;


private:
	bool ApplyCustomElectronRejection(KDataPFTau* tau, KappaEvent const& event,
	                                  HttSettings const& settings) const;

};

