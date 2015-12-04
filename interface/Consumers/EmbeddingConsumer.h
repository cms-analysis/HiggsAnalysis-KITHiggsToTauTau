
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

	virtual void FillPtFlowHistogram(TH1F* hist, KPFCandidates* pf_collection, KMuon* muon);

private:
	unsigned int nDeltaRBins = 0;
	float DeltaRMax = 0.0;
	unsigned int nIsoPtSumBins = 0;
	float IsoPtSumMax = 0.0;
	float IsoPtSumOverPtMax = 0.0;

	std::vector<TH1F*> histograms;
	std::vector<TH2F*> histograms2D;

	std::map<std::string, KMuon*> Muon;

	std::vector<TString> muonTypeVector = {"leading", "trailing", "positive", "negative"};

	std::map<std::string, TH1F*> Muon_ChargedNoPUPtFlow;
	std::map<std::string, TH1F*> Muon_ChargedPUPtFlow;
	std::map<std::string, TH1F*> Muon_NeutralNoPUPtFlow;
	std::map<std::string, TH1F*> Muon_PhotonsNoPUPtFlow;

	std::map<std::string,TH2F*> Muon_absIsoPhotonsOverChargedPU;
	std::map<std::string, TH2F*> Muon_absIsoNeutralOverChargedPU;

	std::map<std::string,TH2F*> Muon_relIsoPhotonsOverChargedPU;
	std::map<std::string, TH2F*> Muon_relIsoNeutralOverChargedPU;

	std::map<std::string, TH2F*> Muon_absIsoNeutandPhoOverChargedPU; 
	std::map<std::string, TH2F*> Muon_relIsoNeutandPhoOverChargedPU;


};
