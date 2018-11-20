
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"

#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Kappa/DataFormats/interface/Kappa.h"

#include <boost/regex.hpp>

#include "Artus/Utility/interface/RootFileHelper.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/KappaAnalysis/interface/Utility/ValidPhysicsObjectTools.h"



#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
#include <TROOT.h>
#endif

class PrefiringWeightProducer : public ProducerBase<HttTypes> {
public:

	virtual ~PrefiringWeightProducer();
	
	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	void Produce(event_type const& event, product_type& product,
                 setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::string JetPrefireProbabilityFile;
	TH2F *jetPrefireProbabilityHist;
};

