
#pragma once

#include <TH2.h>
#include "TROOT.h"

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

class AcceptanceEfficiencyConsumer : public LambdaNtupleConsumer<HttTypes> {
public:

	virtual std::string GetConsumerId() const override;
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) override;
	virtual void Finish(setting_type const& settings, metadata_type const& metadata) override;

private:

	const unsigned int nAttempts = 1000;
	TH2D* acc_eff_hist;
	TH2D* number_of_passed_hist;
	TH2D* number_of_entries_hist;
	
	TH1D* PtTau1_hist;
	TH1D* PtVis1_hist;
	
	TH1D* PtTau2_hist;
	TH1D* PtVis2_hist;	

	unsigned int leadingTauDC = 0;
	unsigned int trailingTauDC = 0;
};
