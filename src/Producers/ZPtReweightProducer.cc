
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ZPtReweightProducer.h"

std::string ZPtReweightProducer::GetProducerId() const
{
	return "ZPtReweightProducer";
}

void ZPtReweightProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{
		float genPt = 0.;  // generator Z(W) pt
		float genMass = 0.;  // generator Z(W) mass
		
		for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
		 genParticle != event.m_genParticles->end(); ++genParticle)
		{
			int pdgId = std::abs(genParticle->pdgId);
			
			if ( (pdgId >= DefaultValues::pdgIdElectron && pdgId <= DefaultValues::pdgIdNuTau && genParticle->fromHardProcessFinalState()) || (genParticle->isDirectHardProcessTauDecayProduct()) )
			{
				genPt += genParticle->p4.Pt();
				genMass += genParticle->p4.M();
			}
		}
		float zPtWeight = m_zPtHist->GetBinContent(m_zPtHist->GetXaxis()->FindBin(genMass),m_zPtHist->GetYaxis()->FindBin(genPt));
		product.m_optionalWeights["zPtReweightWeight"] = zPtWeight;
}
