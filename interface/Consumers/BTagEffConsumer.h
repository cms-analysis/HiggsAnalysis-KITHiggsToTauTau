
#pragma once

#include <TH1.h>
#include <TH2.h>
#include "TROOT.h"

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

class BTagEffConsumer : public ConsumerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetConsumerId() const override;
	virtual void Init(setting_type const& settings) override;
	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings) override;
	virtual void Finish(setting_type const& settings) override;

private:
	TH2D* m_BTaggingEff_Denom_b;
	TH2D* m_BTaggingEff_Denom_c;
	TH2D* m_BTaggingEff_Denom_udsg;
	TH2D* m_BTaggingEff_Num_b;
	TH2D* m_BTaggingEff_Num_c;
	TH2D* m_BTaggingEff_Num_udsg;
};
