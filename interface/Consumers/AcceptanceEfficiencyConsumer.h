
#pragma once

#include <TH2.h>
#include "TROOT.h"

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

class AcceptanceEfficiencyConsumer : public LambdaNtupleConsumer<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetConsumerId() const override;
	virtual void Init(setting_type const& settings) override;
	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings) override;
	virtual void Finish(setting_type const& settings) override;

private:

	const unsigned int nAttempts = 1000;
	TH2F* acc_eff_hist;
	TH2F* number_of_passed_hist;
	TH2F* number_of_entries_hist;
};
