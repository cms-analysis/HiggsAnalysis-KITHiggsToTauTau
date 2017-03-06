
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ZPtReweightProducer.h"


ZPtReweightProducer::~ZPtReweightProducer()
{
	if (m_zPtHist != nullptr)
	{
		delete m_zPtHist;
	}
}

std::string ZPtReweightProducer::GetProducerId() const
{
	return "ZPtReweightProducer";
}

void ZPtReweightProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	TFile zPtFile(settings.GetZptReweightProducerWeights().c_str(), "READ");
	m_zPtHist = (TH2D*)zPtFile.Get("zptmass_histo");
	m_zPtHist->SetDirectory(nullptr);
	zPtFile.Close();
	
	m_applyReweighting = boost::regex_search(settings.GetNickname(), boost::regex("DY.?JetsToLLM(50|150)", boost::regex::icase | boost::regex::extended));
}

void ZPtReweightProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{
	float genPt = 0.;  // generator Z(W) pt
	float genMass = 0.;  // generator Z(W) mass
	RMFLV genMomentum;
	if (m_applyReweighting)
	{
		for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
		genParticle != event.m_genParticles->end(); ++genParticle)
		{
			int pdgId = std::abs(genParticle->pdgId);
			
			if ( (pdgId >= DefaultValues::pdgIdElectron && pdgId <= DefaultValues::pdgIdNuTau && genParticle->fromHardProcessFinalState()) || (genParticle->isDirectHardProcessTauDecayProduct()) )
			{
				genMomentum += genParticle->p4;
			}
		}
		genPt = genMomentum.Pt();
		genMass = genMomentum.M();
		float zPtWeight = m_zPtHist->GetBinContent(m_zPtHist->GetXaxis()->FindBin(genMass),m_zPtHist->GetYaxis()->FindBin(genPt));
		product.m_optionalWeights["zPtReweightWeight"] = zPtWeight;
	}
}
