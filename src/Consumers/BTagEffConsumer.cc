#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/BTagEffConsumer.h"

//#include "Kappa/DataFormats/interface/Kappa.h"


void BTagEffConsumer::Init(setting_type const& settings, metadata_type& metadata)
{
	ConsumerBase<HttTypes>::Init(settings, metadata);
	//Histograms initialization for different muons and Pt Flow per DeltaR.
	//Format of the histograms: PtFlow per DeltaR on y-axis and DeltaR on x-axis.
	//nDeltaRBins = settings.GetDeltaRBinning();
	//DeltaRMax = settings.GetDeltaRMaximum();

	//btag efficiency measurement -> possible to get binning by cfgs settings
	int  ptNBins = 20;
	double ptBins[ptNBins] = {20, 30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 600, 700, 800, 900, 1000}; 

	int etaNBins = 5;
	double etaBins[etaNBins] = {0.0, 0.9, 1.2, 2.1, 2.4};//, etaBins[4] =  5.0;
	m_BTaggingEff_Denom_b     = new TH2D("BTaggingEff_Denom_b",     ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Denom_c     = new TH2D("BTaggingEff_Denom_c",     ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Denom_udsg  = new TH2D("BTaggingEff_Denom_udsg",  ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Denom_undef = new TH2D("BTaggingEff_Denom_undef", ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Num_b       = new TH2D("bTaggingEff_Num_b",       ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Num_c       = new TH2D("bTaggingEff_Num_c",       ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Num_udsg    = new TH2D("bTaggingEff_Num_udsg",    ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Num_undef   = new TH2D("bTaggingEff_Num_undef",   ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
}

//void ValidBTaggedJetsProducer::Produce(event_type const& event, product_type& product,
//                                       setting_type const& settings, metadata_type const& metadata) const
//{

void BTagEffConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
{
	assert(event.m_jetMetadata);

	std::map<std::string, std::vector<float>> bTagWorkingPoints = Utility::ParseMapTypes<std::string,float>(Utility::ParseVectorToMap(settings.GetBTaggerWorkingPoints()));
	float bTaggingWorkingPoint = bTagWorkingPoints.at(settings.GetBTagWPs().at(0)).at(0);
	
	for (auto jet = product.m_validJets.begin(); jet != product.m_validJets.end(); ++jet)
	{
		KJet* tjet = static_cast<KJet*>(*jet);
		float combinedSecondaryVertex = tjet->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
		// more info: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools
		// int jetflavor = tjet->flavour;
		int jetHadronFlavor = tjet->hadronFlavour;
		int jetPartonFlavor = tjet->partonFlavour;
		if (jetHadronFlavor == 5 || (jetHadronFlavor == 0 && jetPartonFlavor == 5)) // b jet
		{
			m_BTaggingEff_Denom_b->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
			if (combinedSecondaryVertex > bTaggingWorkingPoint) m_BTaggingEff_Num_b->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
		}
		else if (jetHadronFlavor == 4 || (jetHadronFlavor == 0 && jetPartonFlavor == 5)) // c jet
		{
			m_BTaggingEff_Denom_c->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
			if (combinedSecondaryVertex > bTaggingWorkingPoint) m_BTaggingEff_Num_c->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
		}
		else if (jetPartonFlavor == 1 ||  jetPartonFlavor == 2 || jetPartonFlavor ==  3 || jetPartonFlavor ==  21) // light-flavour jets: partonFlavour=1, 2, 3, or 21
		{
			m_BTaggingEff_Denom_udsg->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
			if (combinedSecondaryVertex > bTaggingWorkingPoint) m_BTaggingEff_Num_udsg->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
		}
		else // undefined jets
		{
			m_BTaggingEff_Denom_undef->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
			if (combinedSecondaryVertex > bTaggingWorkingPoint) m_BTaggingEff_Num_undef->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
		}
	}
}

void BTagEffConsumer::Finish(setting_type const& settings, metadata_type const& metadata)
{
	RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
	m_BTaggingEff_Denom_b->Write(m_BTaggingEff_Denom_b->GetName());
	m_BTaggingEff_Denom_c->Write(m_BTaggingEff_Denom_c->GetName());
	m_BTaggingEff_Denom_udsg->Write(m_BTaggingEff_Denom_udsg->GetName());
	m_BTaggingEff_Denom_undef->Write(m_BTaggingEff_Denom_undef->GetName());
	m_BTaggingEff_Num_b->Write(m_BTaggingEff_Num_b->GetName());
	m_BTaggingEff_Num_c->Write(m_BTaggingEff_Num_c->GetName());
	m_BTaggingEff_Num_udsg->Write(m_BTaggingEff_Num_udsg->GetName());
	m_BTaggingEff_Num_undef->Write(m_BTaggingEff_Num_undef->GetName());
}

std::string BTagEffConsumer::GetConsumerId() const
{
	return "BTagEffConsumer";
}
