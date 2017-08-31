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
	double ptBins[ptNBins];
	ptBins[0] = 20, ptBins[1] = 30, ptBins[2] = 40, ptBins[3] = 50, ptBins[4] = 60, ptBins[5] = 70, ptBins[6] = 80, ptBins[7] = 100, ptBins[8] = 120;
	ptBins[9] = 160, ptBins[10] = 210, ptBins[11] = 260, ptBins[12] = 320, ptBins[13] = 400, ptBins[14] = 500, ptBins[15] = 600, ptBins[16] = 700, ptBins[17] = 800, ptBins[18] = 900, ptBins[19] = 1000;
	int etaNBins = 5;
	double etaBins[etaNBins];
	etaBins[0] = 0.0, etaBins[1] = 0.9, etaBins[2] = 1.2, etaBins[3] = 2.1, etaBins[4] = 2.4;//, etaBins[4] =  5.0;
	m_BTaggingEff_Denom_b   = new TH2D("BTaggingEff_Denom_b", ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Denom_c   = new TH2D("BTaggingEff_Denom_c", ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Denom_udsg = new TH2D("BTaggingEff_Denom_udsg", ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Num_b  = new TH2D("bTaggingEff_Num_b", ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Num_c  = new TH2D("bTaggingEff_Num_c", ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
	m_BTaggingEff_Num_udsg  = new TH2D("bTaggingEff_Num_udsg", ";p_{T} [GeV];#eta", ptNBins-1, ptBins, etaNBins-1, etaBins);
}

//void ValidBTaggedJetsProducer::Produce(event_type const& event, product_type& product,
//                                       setting_type const& settings, metadata_type const& metadata) const
//{

void BTagEffConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
{
  assert(event.m_jetMetadata);

  //for(std::vector<KMuon*>::const_iterator validMuon = product.m_validMuons.begin();validMuon!=product.m_validMuons.end();++validMuon)
  //for (std::vector<KBasicJet*>::cons_iterator jet = product.m_validJets.begin(); jet != product.m_validJets.end(); ++jet)
  std::map<std::string, std::vector<float>> bTagWorkingPoints = Utility::ParseMapTypes<std::string,float>(Utility::ParseVectorToMap(settings.GetBTaggerWorkingPoints()));
  float bTaggingWorkingPoint = bTagWorkingPoints.at(settings.GetBTagWPs().at(0)).at(0);
  for (auto jet = product.m_validJets.begin(); jet != product.m_validJets.end(); ++jet)
    {
      KJet* tjet = static_cast<KJet*>(*jet);
      float combinedSecondaryVertex = tjet->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
      
	      int jetflavor = tjet->flavour;
	      if(jetflavor==5){
		m_BTaggingEff_Denom_b->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
		if(combinedSecondaryVertex>bTaggingWorkingPoint){
		  m_BTaggingEff_Num_b->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));			    
		}
	      }
	      else if(jetflavor==4){
		m_BTaggingEff_Denom_c->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
		if(combinedSecondaryVertex>bTaggingWorkingPoint){
		  m_BTaggingEff_Num_c->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));			   
		}
	      }
	      else{
		m_BTaggingEff_Denom_udsg->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));
		if(combinedSecondaryVertex>bTaggingWorkingPoint){
		  m_BTaggingEff_Num_udsg->Fill(tjet->p4.pt(), std::fabs(tjet->p4.eta()));			   
		}
	      }
    }
}

void BTagEffConsumer::Finish(setting_type const& settings, metadata_type const& metadata)
{
	RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
  m_BTaggingEff_Denom_b->Write(m_BTaggingEff_Denom_b->GetName());
  m_BTaggingEff_Denom_c->Write(m_BTaggingEff_Denom_c->GetName());
  m_BTaggingEff_Denom_udsg->Write(m_BTaggingEff_Denom_udsg->GetName());
  m_BTaggingEff_Num_b->Write(m_BTaggingEff_Num_b->GetName());
  m_BTaggingEff_Num_c->Write(m_BTaggingEff_Num_c->GetName());
  m_BTaggingEff_Num_udsg->Write(m_BTaggingEff_Num_udsg->GetName());
}

std::string BTagEffConsumer::GetConsumerId() const
{
	return "BTagEffConsumer";
}
