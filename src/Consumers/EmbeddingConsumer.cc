#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/EmbeddingConsumer.h"


void EmbeddingConsumer::Init(setting_type const& settings)
{
	ConsumerBase<HttTypes>::Init(settings);
	//Histograms initialization for different muons and Pt Flow per DeltaR.
	//Format of the histograms: PtFlow per DeltaR on y-axis and DeltaR on x-axis.
	nDeltaRBins = settings.GetDeltaRBinning();
	DeltaRMax = settings.GetDeltaRMaximum();

	for(unsigned int i = 0;i<muonTypeVector.size();i++)
	{
		// PtFlow for charged hadrons (not from PU)
		TString histname = muonTypeVector[i] + TString("Muon_ChargedNoPUPtFlow");
		Muon_ChargedNoPUPtFlow[(const char*) muonTypeVector[i]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
		histograms.push_back(Muon_ChargedNoPUPtFlow[(const char*) muonTypeVector[i]]);

		// PtFlow for charged hadrons (from PU)
		histname = muonTypeVector[i] + TString("Muon_ChargedPUPtFlow");
		Muon_ChargedPUPtFlow[(const char*) muonTypeVector[i]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
		histograms.push_back(Muon_ChargedPUPtFlow[(const char*) muonTypeVector[i]]);

		// PtFlow for neutral hadrons (not from PU)
		histname = muonTypeVector[i] + TString("Muon_NeutralNoPUPtFlow");
		Muon_NeutralNoPUPtFlow[(const char*) muonTypeVector[i]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
		histograms.push_back(Muon_NeutralNoPUPtFlow[(const char*) muonTypeVector[i]]);

		// PtFlow for photons (not from PU)
		histname = muonTypeVector[i] + TString("Muon_PhotonsNoPUPtFlow");
		Muon_PhotonsNoPUPtFlow[(const char*) muonTypeVector[i]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
		histograms.push_back(Muon_PhotonsNoPUPtFlow[(const char*) muonTypeVector[i]]);
	}

	//2D histograms to analyze the correlation between Photon, Neutral and ChargedPU isolations.
	//Format of the histograms: Number of events on z-axis, Iso_ph or Iso_nh on y-axis, Iso_ch on x-axis.
	nIsoPtSumBins = settings.GetIsoPtSumBinning();
	IsoPtSumMax = settings.GetIsoPtSumMaximum();
	IsoPtSumOverPtMax = settings.GetIsoPtSumOverPtMaximum();

	for(unsigned int i = 0;i<muonTypeVector.size();i++)
	{
		// absolute IsoPtSum for photons
		TString histname = muonTypeVector[i]+ TString("Muon_absIsoPhotonsOverChargedPU");
		Muon_absIsoPhotonsOverChargedPU[(const char*) muonTypeVector[i]] = new TH2F((const char*) histname, (const char*) histname, nIsoPtSumBins, 0., IsoPtSumMax, nIsoPtSumBins, 0., IsoPtSumMax);
		histograms2D.push_back(Muon_absIsoPhotonsOverChargedPU[(const char*) muonTypeVector[i]]);

		// absolute IsoPtSum for neutral hadrons
		histname = muonTypeVector[i]+ TString("Muon_absIsoNeutralOverChargedPU");
		Muon_absIsoNeutralOverChargedPU[(const char*) muonTypeVector[i]] = new TH2F((const char*) histname, (const char*) histname, nIsoPtSumBins, 0., IsoPtSumMax, nIsoPtSumBins, 0., IsoPtSumMax);
		histograms2D.push_back(Muon_absIsoNeutralOverChargedPU[(const char*) muonTypeVector[i]]);

		// relative IsoPtSum for photons
		histname = muonTypeVector[i]+ TString("Muon_relIsoPhotonsOverChargedPU");
		Muon_relIsoPhotonsOverChargedPU[(const char*) muonTypeVector[i]] = new TH2F((const char*) histname, (const char*) histname, nIsoPtSumBins, 0., IsoPtSumOverPtMax, nIsoPtSumBins, 0., IsoPtSumOverPtMax);
		histograms2D.push_back(Muon_relIsoPhotonsOverChargedPU[(const char*) muonTypeVector[i]]);

		// relative IsoPtSum for neutral hadrons
		histname = muonTypeVector[i]+ TString("Muon_relIsoNeutralOverChargedPU");
		Muon_relIsoNeutralOverChargedPU[(const char*) muonTypeVector[i]] = new TH2F((const char*) histname, (const char*) histname, nIsoPtSumBins, 0., IsoPtSumOverPtMax, nIsoPtSumBins, 0., IsoPtSumOverPtMax);
		histograms2D.push_back(Muon_relIsoNeutralOverChargedPU[(const char*) muonTypeVector[i]]);

		// absolute IsoPtSum for neutral hadrons + photons
		histname = muonTypeVector[i]+ TString("Muon_absIsoNeutandPhoOverChargedPU");
		Muon_absIsoNeutandPhoOverChargedPU[(const char*) muonTypeVector[i]] = new TH2F((const char*) histname, (const char*) histname, nIsoPtSumBins, 0., IsoPtSumMax, nIsoPtSumBins, 0., IsoPtSumMax);
		histograms2D.push_back(Muon_absIsoNeutandPhoOverChargedPU[(const char*) muonTypeVector[i]]);


		// relative IsoPtSum for neutral hadrons+ phosnon
		histname = muonTypeVector[i]+ TString("Muon_relIsoNeutandPhoOverChargedPU");
		Muon_relIsoNeutandPhoOverChargedPU[(const char*) muonTypeVector[i]] = new TH2F((const char*) histname, (const char*) histname, nIsoPtSumBins, 0., IsoPtSumOverPtMax, nIsoPtSumBins, 0., IsoPtSumOverPtMax);
		histograms2D.push_back(Muon_relIsoNeutandPhoOverChargedPU[(const char*) muonTypeVector[i]]);


	}
}


void EmbeddingConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings)
{
	// Here is assumed, that validMuons are Pt ordered
	Muon["leading"] = product.m_validMuons[0];
	Muon["trailing"] = product.m_validMuons[1];


	// Looking for positively and negatively charged Muons with highest Pt. Again, Pt ordering is assumed
	bool foundPositiveMuon = false;
	bool foundNegativeMuon = false;
	for(std::vector<KMuon*>::const_iterator validMuon = product.m_validMuons.begin();validMuon!=product.m_validMuons.end();++validMuon)
	{
		if(((*validMuon)->charge() == +1) && !foundPositiveMuon)
		{
			Muon["positive"] = (*validMuon);
			foundPositiveMuon = true;
		}
		else if(((*validMuon)->charge() == -1) && !foundNegativeMuon)
		{
			Muon["negative"] = (*validMuon);
			foundNegativeMuon = true;
		}
		else if(foundPositiveMuon && foundNegativeMuon) break;
	}

	// Filling histograms for all muons defined above

	for(unsigned int i = 0;i<muonTypeVector.size();i++)
	{
		std::string muontype = (const char*) muonTypeVector[i];
		KMuon* muon = Muon[muontype];

		// Filling PtFlow histograms
		EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedNoPUPtFlow[muontype], event.m_pfChargedHadronsNoPileUp, muon);
		EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedPUPtFlow[muontype], event.m_pfChargedHadronsPileUp, muon);
		EmbeddingConsumer::FillPtFlowHistogram(Muon_NeutralNoPUPtFlow[muontype], event.m_pfNeutralHadronsNoPileUp, muon);
		EmbeddingConsumer::FillPtFlowHistogram(Muon_PhotonsNoPUPtFlow[muontype], event.m_pfPhotonsNoPileUp, muon);

		// Filling 2D IsoPtSum histograms
		if (product.m_muonPhotonIsolation.at(muon)>0) Muon_absIsoPhotonsOverChargedPU[muontype]->Fill(product.m_muonDeltaBetaIsolation.at(muon), product.m_muonPhotonIsolation.at(muon));
		if (product.m_muonNeutralIsolation.at(muon)>0) Muon_absIsoNeutralOverChargedPU[muontype]->Fill(product.m_muonDeltaBetaIsolation.at(muon), product.m_muonNeutralIsolation.at(muon));
		if (product.m_muonPhotonIsolationOverPt.at(muon)>0) Muon_relIsoPhotonsOverChargedPU[muontype]->Fill(product.m_muonDeltaBetaIsolationOverPt.at(muon), product.m_muonPhotonIsolationOverPt.at(muon));
		if (product.m_muonNeutralIsolationOverPt.at(muon)>0) Muon_relIsoNeutralOverChargedPU[muontype]->Fill(product.m_muonDeltaBetaIsolationOverPt.at(muon), product.m_muonNeutralIsolationOverPt.at(muon));

		double sum_neut_and_phot = product.m_muonNeutralIsolation.at(muon) + product.m_muonPhotonIsolation.at(muon);
		if (sum_neut_and_phot>0) Muon_absIsoNeutandPhoOverChargedPU[muontype]->Fill(product.m_muonDeltaBetaIsolationOverPt.at(muon), sum_neut_and_phot);

		double sum_neut_and_phot_rel = product.m_muonNeutralIsolationOverPt.at(muon) + product.m_muonPhotonIsolationOverPt.at(muon);
		if (sum_neut_and_phot_rel>0) Muon_relIsoNeutandPhoOverChargedPU[muontype]->Fill(product.m_muonDeltaBetaIsolationOverPt.at(muon), sum_neut_and_phot_rel);


	}

}

void EmbeddingConsumer::Finish(setting_type const& settings)
{
	for(unsigned int i=0;i<histograms.size();i++)
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		histograms[i]->Write(histograms[i]->GetName());
	}

	for(unsigned int i=0;i<histograms2D.size();i++)
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		histograms2D[i]->Write(histograms2D[i]->GetName());
	}
}

std::string EmbeddingConsumer::GetConsumerId() const
{
	return "EmbeddingConsumer";
}

void EmbeddingConsumer::FillPtFlowHistogram(TH1F* hist, KPFCandidates* pf_collection, KMuon* muon)
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
