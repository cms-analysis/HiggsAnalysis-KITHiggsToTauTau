#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/EmbeddingConsumer.h"


void EmbeddingConsumer::Init(setting_type const& settings, metadata_type& metadata)
{
	ConsumerBase<HttTypes>::Init(settings, metadata);
	//Histograms initialization for different muons and Pt Flow per DeltaR.
	//Format of the histograms: PtFlow per DeltaR on y-axis and DeltaR on x-axis.
	nDeltaRBins = settings.GetDeltaRBinning();
	DeltaRMax = settings.GetDeltaRMaximum();
	randomMuon = settings.GetRandomMuon();
	for(unsigned int i = 0;i<muonTypeVector.size();i++)
	{
		for(unsigned int j = 0; j < regionTypeVector.size();j++)
		{
			// PtFlow for charged hadrons (from first PV)
			TString histname = muonTypeVector[i] + TString("Muon_ChargedFromFirstPVPtFlow_") +  regionTypeVector[j];
			Muon_ChargedFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
			histograms.push_back(Muon_ChargedFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]]);

			// PtFlow for charged hadrons (not from first PV)
			histname = muonTypeVector[i] + TString("Muon_ChargedNotFromFirstPVPtFlow_") +  regionTypeVector[j];
			Muon_ChargedNotFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
			histograms.push_back(Muon_ChargedNotFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]]);

			// PtFlow for neutral hadrons (from first PV)
			histname = muonTypeVector[i] + TString("Muon_NeutralFromFirstPVPtFlow_") +  regionTypeVector[j];
			Muon_NeutralFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
			histograms.push_back(Muon_NeutralFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]]);

			// PtFlow for photons (from first PV)
			histname = muonTypeVector[i] + TString("Muon_PhotonsFromFirstPVPtFlow_") +  regionTypeVector[j];
			Muon_PhotonsFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]] = new TH1F((const char*) histname, (const char*) histname, nDeltaRBins, 0., DeltaRMax);
			histograms.push_back(Muon_PhotonsFromFirstPVPtFlow[(const char*) muonTypeVector[i]][(const char*) regionTypeVector[j]]);
		}
	}
}


void EmbeddingConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
{
	// Here is assumed, that validMuons are Pt ordered
	Muon["leading"] = static_cast<KMuon*>(product.m_zLeptons.first);
	Muon["trailing"] = static_cast<KMuon*>(product.m_zLeptons.second);

	if (product.m_zLeptons.first->charge() == +1)
	{
		Muon["positive"] = static_cast<KMuon*>(product.m_zLeptons.first);
		Muon["negative"] = static_cast<KMuon*>(product.m_zLeptons.second);
	}
	else
	{
		Muon["positive"] = static_cast<KMuon*>(product.m_zLeptons.second);
		Muon["negative"] = static_cast<KMuon*>(product.m_zLeptons.first);	
	}
	KMuon* rMuon = new KMuon();
	rMuon->p4.SetM(1.);
	rMuon->p4.SetPt(1.);
	double theta = randomnumbergenerator->Uniform(0,TMath::Pi());
	rMuon->p4.SetEta(-TMath::Log(TMath::Tan(theta/2)));
	rMuon->p4.SetPhi(randomnumbergenerator->Uniform(-TMath::Pi(),TMath::Pi()));
	// Filling histograms for all muons defined above
	for(unsigned int i = 0;i<muonTypeVector.size();i++)
	{
		std::string muontype = (const char*) muonTypeVector[i];
		KMuon* muon = randomMuon ? rMuon : Muon[muontype];

		// Filling PtFlow histograms
		EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedFromFirstPVPtFlow[muontype], product.m_pfChargedHadronsFromFirstPV, muon, "full");
		if(product.m_z.p4.M() < 100 && product.m_z.p4.M() > 80) EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedFromFirstPVPtFlow[muontype], product.m_pfChargedHadronsFromFirstPV, muon, "peak");
		else EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedFromFirstPVPtFlow[muontype], product.m_pfChargedHadronsFromFirstPV, muon, "sideband");
		
		EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedNotFromFirstPVPtFlow[muontype], product.m_pfChargedHadronsNotFromFirstPV, muon, "full");
		if(product.m_z.p4.M() < 100 && product.m_z.p4.M() > 80) EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedNotFromFirstPVPtFlow[muontype], product.m_pfChargedHadronsNotFromFirstPV, muon, "peak");
		else EmbeddingConsumer::FillPtFlowHistogram(Muon_ChargedNotFromFirstPVPtFlow[muontype], product.m_pfChargedHadronsNotFromFirstPV, muon, "sideband");
		
		EmbeddingConsumer::FillPtFlowHistogram(Muon_NeutralFromFirstPVPtFlow[muontype], product.m_pfNeutralHadronsFromFirstPV, muon, "full");
		if(product.m_z.p4.M() < 100 && product.m_z.p4.M() > 80) EmbeddingConsumer::FillPtFlowHistogram(Muon_NeutralFromFirstPVPtFlow[muontype], product.m_pfNeutralHadronsFromFirstPV, muon, "peak");
		else EmbeddingConsumer::FillPtFlowHistogram(Muon_NeutralFromFirstPVPtFlow[muontype], product.m_pfNeutralHadronsFromFirstPV, muon, "sideband");
		
		EmbeddingConsumer::FillPtFlowHistogram(Muon_PhotonsFromFirstPVPtFlow[muontype], product.m_pfPhotonsFromFirstPV, muon, "full");
		if(product.m_z.p4.M() < 100 && product.m_z.p4.M() > 80) EmbeddingConsumer::FillPtFlowHistogram(Muon_PhotonsFromFirstPVPtFlow[muontype], product.m_pfPhotonsFromFirstPV, muon, "peak");
		else EmbeddingConsumer::FillPtFlowHistogram(Muon_PhotonsFromFirstPVPtFlow[muontype], product.m_pfPhotonsFromFirstPV, muon, "sideband");

	}

}

void EmbeddingConsumer::Finish(setting_type const& settings, metadata_type const& metadata)
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

void EmbeddingConsumer::FillPtFlowHistogram(std::map<std::string, TH1F*> histmap, std::vector<const KPFCandidate*> pf_collection, KMuon* muon, std::string region)
{
	//double sumPt=0; //for PtFlow distribution

	for (std::vector<const KPFCandidate*>::const_iterator pfCandidate = pf_collection.begin();pfCandidate != pf_collection.end();++pfCandidate)
	{
		double deltaR = ROOT::Math::VectorUtil::DeltaR(muon->p4, (*pfCandidate)->p4);
		if (deltaR < DeltaRMax)
		{
			histmap[region]->Fill(deltaR,(*pfCandidate)->p4.Pt());
		}
	}
	//histmap[region]->Fill(sumPt); //for PtFlow distribution

}
