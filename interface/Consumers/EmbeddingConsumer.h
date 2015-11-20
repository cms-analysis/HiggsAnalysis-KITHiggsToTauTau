
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

	virtual void FillHistogram(TH1F* hist, KPFCandidates* pf_collection, KMuon* muon); 

private:
	unsigned int nDeltaRBins = 0;
	float DeltaRMax = 0.0;
	std::vector<TH1F*> histograms;

	KMuon* leadingMuon = nullptr;
	KMuon* trailingMuon = nullptr;
	KMuon* positiveMuon = nullptr;
	KMuon* negativeMuon = nullptr;

	TH1F* leadingMuon_ChargedNoPUPtFlow = nullptr;
	TH1F* trailingMuon_ChargedNoPUPtFlow = nullptr;
	TH1F* positiveMuon_ChargedNoPUPtFlow = nullptr;
	TH1F* negativeMuon_ChargedNoPUPtFlow = nullptr;

	TH1F* leadingMuon_ChargedPUPtFlow = nullptr;
	TH1F* trailingMuon_ChargedPUPtFlow = nullptr;
	TH1F* positiveMuon_ChargedPUPtFlow = nullptr;
	TH1F* negativeMuon_ChargedPUPtFlow = nullptr;

	TH1F* leadingMuon_NeutralNoPUPtFlow = nullptr;
	TH1F* trailingMuon_NeutralNoPUPtFlow = nullptr;
	TH1F* positiveMuon_NeutralNoPUPtFlow = nullptr;
	TH1F* negativeMuon_NeutralNoPUPtFlow = nullptr;

	TH1F* leadingMuon_PhotonsNoPUPtFlow = nullptr;
	TH1F* trailingMuon_PhotonsNoPUPtFlow = nullptr;
	TH1F* positiveMuon_PhotonsNoPUPtFlow = nullptr;
	TH1F* negativeMuon_PhotonsNoPUPtFlow = nullptr;
};
