#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/EmbeddingConsumer.h"


void EmbeddingConsumer::Init(setting_type const& settings)
{
	ConsumerBase<HttTypes>::Init(settings);
	//TODO
	//Histograms initialization for different muons and Pt flows (abs. or rel. IsolationPtSum per DeltaR).
	//Format of the histograms: abs. or rel. IsolationPtSum per DeltaR on y-axis and DeltaR on x-axis.
	nDeltaRBins = settings.GetDeltaRBinning();
	DeltaRMax = settings.GetDeltaRMaximum();
	//abs. IsolationPtSum for charged Hadrons
	leadingMuon_absChargedIso = new TH1F("leadingMuon_absChargedIso", "leadingMuon_absChargedIso", nDeltaRBins, 0., DeltaRMax);
	histograms.push_back(leadingMuon_absChargedIso);

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
	// Filling the histograms for the chosen muons above.
	// Leading Muon
	// Charged Hadron Isolation from PV
	// Charged Hadron PF Candidates should be available in the sample
	if (event.m_pfChargedHadronsNoPileUp != nullptr)
	{
		for (std::vector<KPFCandidate>::const_iterator pfCandidate = event.m_pfChargedHadronsNoPileUp->begin();pfCandidate != event.m_pfChargedHadronsNoPileUp->end();++pfCandidate)
		{
			double deltaR = ROOT::Math::VectorUtil::DeltaR(leadingMuon->p4, pfCandidate->p4);
			if (deltaR < DeltaRMax)
			{
				leadingMuon_absChargedIso->Fill(deltaR,pfCandidate->p4.Pt());
			}
		}
	}
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
