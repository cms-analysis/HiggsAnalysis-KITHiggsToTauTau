
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ParticleIsolation.h"
//#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/ParticleIsolation.h"
//#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

double ParticleIsolation::IsolationPtSumForParticleClass(RMFLV const& particle, KPFCandidates* pfCandidates,
                                                         float const& isoSignalConeSize,
                                                         float const& isoVetoConeSizeEB,
                                                         float const& isoVetoConeSizeEE,
                                                         float const& isoPtThreshold)
{
	double isolationPtSum = 0.0;
	for (std::vector<KPFCandidate>::const_iterator pfCandidate = pfCandidates->begin();
	     pfCandidate != pfCandidates->end(); ++pfCandidate)
	{
		double deltaR = ROOT::Math::VectorUtil::DeltaR(particle, pfCandidate->p4);
		if (
			(deltaR < isoSignalConeSize)
			&&
			(pfCandidate->p4.Pt() > isoPtThreshold)
			&&
			(
				(
					(std::abs(particle.Eta()) < DefaultValues::EtaBorderEB) && (deltaR > isoVetoConeSizeEB)
				)
				||
				(
					(std::abs(particle.Eta()) >= DefaultValues::EtaBorderEB) && (deltaR > isoVetoConeSizeEE)
				)
			)
		)
		{
			isolationPtSum += pfCandidate->p4.Pt();
		}
	}
	return isolationPtSum;
}


double ParticleIsolation::IsolationPtSum(RMFLV const& particle, HttEvent const& event,
                                         float const& isoSignalConeSize,
                                         float const& deltaBetaCorrectionFactor,
                                         float const& chargedIsoVetoConeSizeEB,
                                         float const& chargedIsoVetoConeSizeEE,
                                         float const& neutralIsoVetoConeSize,
                                         float const& photonIsoVetoConeSizeEB,
                                         float const& photonIsoVetoConeSizeEE,
                                         float const& deltaBetaIsoVetoConeSize,
                                         float const& chargedIsoPtThreshold,
                                         float const& neutralIsoPtThreshold,
                                         float const& photonIsoPtThreshold,
                                         float const& deltaBetaIsoPtThreshold)
{
	assert(event.m_pfChargedHadronsNoPileUp);
	assert(event.m_pfNeutralHadronsNoPileUp);
	assert(event.m_pfPhotonsNoPileUp);
	assert(event.m_pfChargedHadronsPileUp);
	
	double chargedIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
			particle,
			event.m_pfChargedHadronsNoPileUp,
			isoSignalConeSize,
			chargedIsoVetoConeSizeEB,
			chargedIsoVetoConeSizeEE,
			chargedIsoPtThreshold
	);

	double neutralIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
			particle,
			event.m_pfNeutralHadronsNoPileUp,
			isoSignalConeSize,
			neutralIsoVetoConeSize,
			neutralIsoVetoConeSize,
			neutralIsoPtThreshold
	);

	double photonIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
			particle,
			event.m_pfPhotonsNoPileUp,
			isoSignalConeSize,
			photonIsoVetoConeSizeEB,
			photonIsoVetoConeSizeEE,
			photonIsoPtThreshold
	);

	double deltaBetaIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
			particle,
			event.m_pfChargedHadronsPileUp,
			isoSignalConeSize,
			deltaBetaIsoVetoConeSize,
			deltaBetaIsoVetoConeSize,
			deltaBetaIsoPtThreshold
	);
	
	double isolationPtSum = chargedIsolationPtSum +
	                        std::max(0.0, neutralIsolationPtSum +
	                                      photonIsolationPtSum -
	                                      (deltaBetaCorrectionFactor * deltaBetaIsolationPtSum));
	                                      
	return isolationPtSum;
}
