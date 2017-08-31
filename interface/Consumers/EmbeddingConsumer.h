
#pragma once

#include <TH1.h>
#include "TROOT.h"
#include "TRandom3.h"

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

class EmbeddingConsumer : public ConsumerBase<HttTypes> {
public:

	virtual std::string GetConsumerId() const override;
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) override;
	virtual void Finish(setting_type const& settings, metadata_type const& metadata) override;

	virtual void FillPtFlowHistogram(std::map<std::string, TH1F*> histmap, std::vector<const KPFCandidate*> pf_collection, KMuon* muon, std::string region);

private:
	TRandom3* randomnumbergenerator = new TRandom3(0);
	unsigned int nDeltaRBins = 0;
	float DeltaRMax = 0.0;
	unsigned int nIsoPtSumBins = 0;
	float IsoPtSumMax = 0.0;
	float IsoPtSumOverPtMax = 0.0;
	bool randomMuon = false;

	std::vector<TH1F*> histograms;

	std::map<std::string, KMuon*> Muon;

	std::vector<TString> muonTypeVector = {"leading", "trailing", "positive", "negative"};
	std::vector<TString> regionTypeVector = {"full", "peak", "sideband"};

	std::map<std::string, std::map<std::string, TH1F*>> Muon_ChargedFromFirstPVPtFlow;
	std::map<std::string, std::map<std::string, TH1F*>> Muon_ChargedNotFromFirstPVPtFlow;
	std::map<std::string, std::map<std::string, TH1F*>> Muon_NeutralFromFirstPVPtFlow;
	std::map<std::string, std::map<std::string, TH1F*>> Muon_PhotonsFromFirstPVPtFlow;
};
