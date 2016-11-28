
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ZReweightingProducer.h"

std::string ZReweightingProducer::GetProducerId() const
{
	return "ZReweightingProducer";
}

void ZReweightingProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{
	float genPt = 0.;  // generator Z pt
	float genMass = 0.;  // generator Z mass
	float genEta = 0.;  // generator Z eta
	RMFLV genMomentum;
	if (m_applyReweighting && m_isDY)
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
		genEta = genMomentum.Eta();
		float zRwWeight = m_zReweightingHist->GetBinContent(m_zReweightingHist->GetXaxis()->FindBin(genPt), m_zReweightingHist->GetYaxis()->FindBin(genMass), m_zReweightingHist->GetZaxis()->FindBin(genEta));
		product.m_optionalWeights["zReweightingWeight"] = zRwWeight;
	}
}
