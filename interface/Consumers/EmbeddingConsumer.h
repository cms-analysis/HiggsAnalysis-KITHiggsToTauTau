
#pragma once

#include <TH1.h>
#include "TROOT.h"

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

class EmbeddingConsumer : public ConsumerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetConsumerId() const override;
	virtual void Init(setting_type const& settings) override;
	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings) override;
	virtual void Finish(setting_type const& settings) override;

private:
	std::vector<TH1F*> histograms;
	KMuon* leadingMuon = nullptr;
	KMuon* trailingMuon = nullptr;
	KMuon* positiveMuon = nullptr;
	KMuon* negativeMuon = nullptr;

protected:
	TH1F* leadingMuon_absChargedIso = nullptr;
	TH1F* trailingMuon_absChargedIso = nullptr;
	TH1F* positiveMuon_absChargedIso = nullptr;
	TH1F* negativeMuon_ansChargedIso = nullptr;
};
