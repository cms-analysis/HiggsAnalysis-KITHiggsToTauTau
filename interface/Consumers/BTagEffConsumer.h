
#pragma once

#include <TH1.h>
#include <TH2.h>
#include "TROOT.h"

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

class BTagEffConsumer : public ConsumerBase<HttTypes> {
public:

	virtual std::string GetConsumerId() const override;
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) override;
	virtual void Finish(setting_type const& settings, metadata_type const& metadata) override;

private:
	TH2D* m_BTaggingEff_Denom_b;
	TH2D* m_BTaggingEff_Denom_c;
	TH2D* m_BTaggingEff_Denom_udsg;
	TH2D* m_BTaggingEff_Num_b;
	TH2D* m_BTaggingEff_Num_c;
	TH2D* m_BTaggingEff_Num_udsg;
	TH2D* m_BTaggingEff_Denom_undef;
	TH2D* m_BTaggingEff_Num_undef;
};
