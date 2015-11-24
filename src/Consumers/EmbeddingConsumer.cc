#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/EmbeddingConsumer.h"


void EmbeddingConsumer::Init(setting_type const& settings)
{
	ConsumerBase<HttTypes>::Init(settings);
	//TODO
	//Histograms initialization for different muons and Pt Flow per DeltaR.
	//Format of the histograms: PtFlow per DeltaR on y-axis and DeltaR on x-axis.
	nDeltaRBins = settings.GetDeltaRBinning();
	DeltaRMax = settings.GetDeltaRMaximum();

	// PtFlow for charged hadrons (not from PU)
	leadingMuon_ChargedNoPUPtFlow = new TH1F("leadingMuon_ChargedNoPUPtFlow", "leadingMuon_ChargedNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(leadingMuon_ChargedNoPUPtFlow);
	trailingMuon_ChargedNoPUPtFlow = new TH1F("trailingMuon_ChargedNoPUPtFlow", "trailingMuon_ChargedNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(trailingMuon_ChargedNoPUPtFlow);
	positiveMuon_ChargedNoPUPtFlow = new TH1F("positiveMuon_ChargedNoPUPtFlow", "positiveMuon_ChargedNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(positiveMuon_ChargedNoPUPtFlow);
	negativeMuon_ChargedNoPUPtFlow = new TH1F("negativeMuon_ChargedNoPUPtFlow", "negativeMuon_ChargedNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(negativeMuon_ChargedNoPUPtFlow);

	// PtFlow for charged hadrons (from PU)
	leadingMuon_ChargedPUPtFlow = new TH1F("leadingMuon_ChargedPUPtFlow", "leadingMuon_ChargedPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(leadingMuon_ChargedPUPtFlow);
	trailingMuon_ChargedPUPtFlow = new TH1F("trailingMuon_ChargedPUPtFlow", "trailingMuon_ChargedPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(trailingMuon_ChargedPUPtFlow);
	positiveMuon_ChargedPUPtFlow = new TH1F("positiveMuon_ChargedPUPtFlow", "positiveMuon_ChargedPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(positiveMuon_ChargedPUPtFlow);
	negativeMuon_ChargedPUPtFlow = new TH1F("negativeMuon_ChargedPUPtFlow", "negativeMuon_ChargedPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(negativeMuon_ChargedPUPtFlow);

	// PtFlow for neutral hadrons (not from PU)
	leadingMuon_NeutralNoPUPtFlow = new TH1F("leadingMuon_NeutralNoPUPtFlow", "leadingMuon_NeutralNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(leadingMuon_NeutralNoPUPtFlow);
	trailingMuon_NeutralNoPUPtFlow = new TH1F("trailingMuon_NeutralNoPUPtFlow", "trailingMuon_NeutralNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(trailingMuon_NeutralNoPUPtFlow);
	positiveMuon_NeutralNoPUPtFlow = new TH1F("positiveMuon_NeutralNoPUPtFlow", "positiveMuon_NeutralNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(positiveMuon_NeutralNoPUPtFlow);
	negativeMuon_NeutralNoPUPtFlow = new TH1F("negativeMuon_NeutralNoPUPtFlow", "negativeMuon_NeutralNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(negativeMuon_NeutralNoPUPtFlow);

	// PtFlow for photons (not from PU)
	leadingMuon_PhotonsNoPUPtFlow = new TH1F("leadingMuon_PhotonsNoPUPtFlow", "leadingMuon_PhotonsNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(leadingMuon_PhotonsNoPUPtFlow);
	trailingMuon_PhotonsNoPUPtFlow = new TH1F("trailingMuon_PhotonsNoPUPtFlow", "trailingMuon_PhotonsNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(trailingMuon_PhotonsNoPUPtFlow);
	positiveMuon_PhotonsNoPUPtFlow = new TH1F("positiveMuon_PhotonsNoPUPtFlow", "positiveMuon_PhotonsNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(positiveMuon_PhotonsNoPUPtFlow);
	negativeMuon_PhotonsNoPUPtFlow = new TH1F("negativeMuon_PhotonsNoPUPtFlow", "negativeMuon_PhotonsNoPUPtFlow", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(negativeMuon_PhotonsNoPUPtFlow);

}


void EmbeddingConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings)
{
	// Here is assumed, that validMuons are Pt ordered
	leadingMuon = product.m_validMuons[0];
	trailingMuon = product.m_validMuons[1];

	// Looking for positively and negatively charged Muons with highest Pt. Again, Pt ordering is assumed
	bool foundPositiveMuon = false;
	bool foundNegativeMuon = false;
	for(std::vector<KMuon*>::const_iterator validMuon = product.m_validMuons.begin();validMuon!=product.m_validMuons.end();++validMuon)
	{
		if(((*validMuon)->charge() == +1) && !foundPositiveMuon)
		{
			positiveMuon = (*validMuon);
			foundPositiveMuon = true;
		}
		else if(((*validMuon)->charge() == -1) && !foundNegativeMuon)
		{
			negativeMuon = (*validMuon);
			foundNegativeMuon = true;
		}
		else if(foundPositiveMuon && foundNegativeMuon) break;
	}

	// Filling histograms for all muons defined above

	// For charged hadrons (not from PU)
	EmbeddingConsumer::FillHistogram(leadingMuon_ChargedNoPUPtFlow, event.m_pfChargedHadronsNoPileUp, leadingMuon);
	EmbeddingConsumer::FillHistogram(trailingMuon_ChargedNoPUPtFlow, event.m_pfChargedHadronsNoPileUp, trailingMuon);
	EmbeddingConsumer::FillHistogram(positiveMuon_ChargedNoPUPtFlow, event.m_pfChargedHadronsNoPileUp, positiveMuon);
	EmbeddingConsumer::FillHistogram(negativeMuon_ChargedNoPUPtFlow, event.m_pfChargedHadronsNoPileUp, negativeMuon);

	// For charged hadrons (from PU)
	EmbeddingConsumer::FillHistogram(leadingMuon_ChargedPUPtFlow, event.m_pfChargedHadronsPileUp, leadingMuon);
	EmbeddingConsumer::FillHistogram(trailingMuon_ChargedPUPtFlow, event.m_pfChargedHadronsPileUp, trailingMuon);
	EmbeddingConsumer::FillHistogram(positiveMuon_ChargedPUPtFlow, event.m_pfChargedHadronsPileUp, positiveMuon);
	EmbeddingConsumer::FillHistogram(negativeMuon_ChargedPUPtFlow, event.m_pfChargedHadronsPileUp, negativeMuon);

	// For neutral hadrons (not from PU)
	EmbeddingConsumer::FillHistogram(leadingMuon_NeutralNoPUPtFlow, event.m_pfNeutralHadronsNoPileUp, leadingMuon);
	EmbeddingConsumer::FillHistogram(trailingMuon_NeutralNoPUPtFlow, event.m_pfNeutralHadronsNoPileUp, trailingMuon);
	EmbeddingConsumer::FillHistogram(positiveMuon_NeutralNoPUPtFlow, event.m_pfNeutralHadronsNoPileUp, positiveMuon);
	EmbeddingConsumer::FillHistogram(negativeMuon_NeutralNoPUPtFlow, event.m_pfNeutralHadronsNoPileUp, negativeMuon);

	// For photons (not from PU)
	EmbeddingConsumer::FillHistogram(leadingMuon_PhotonsNoPUPtFlow, event.m_pfPhotonsNoPileUp, leadingMuon);
	EmbeddingConsumer::FillHistogram(trailingMuon_PhotonsNoPUPtFlow, event.m_pfPhotonsNoPileUp, trailingMuon);
	EmbeddingConsumer::FillHistogram(positiveMuon_PhotonsNoPUPtFlow, event.m_pfPhotonsNoPileUp, positiveMuon);
	EmbeddingConsumer::FillHistogram(negativeMuon_PhotonsNoPUPtFlow, event.m_pfPhotonsNoPileUp, negativeMuon);

}

void EmbeddingConsumer::Finish(setting_type const& settings)
{
	for(unsigned int i=0;i<histograms.size();i++)
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		histograms[i]->Write(histograms[i]->GetName());
	}
}

std::string EmbeddingConsumer::GetConsumerId() const
{
	return "EmbeddingConsumer";
}

void EmbeddingConsumer::FillHistogram(TH1F* hist, KPFCandidates* pf_collection, KMuon* muon)
{
	if (pf_collection != nullptr)
	{
		for (std::vector<KPFCandidate>::const_iterator pfCandidate = pf_collection->begin();pfCandidate != pf_collection->end();++pfCandidate)
		{
			double deltaR = ROOT::Math::VectorUtil::DeltaR(muon->p4, pfCandidate->p4);
			if (deltaR < DeltaRMax)
			{
				hist->Fill(deltaR,pfCandidate->p4.Pt());
			}
		}
	}
}
