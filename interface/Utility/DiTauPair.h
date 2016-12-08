
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiGenTauPair.h"


class DiTauPair : public DiGenTauPair
{
public:
	DiTauPair(KLepton* lepton1, KLepton* lepton2);
	
	bool IsOppositelyCharged();
	std::vector<std::string> GetCommonHltPaths(
			std::map<KLepton*, std::map<std::string, std::map<std::string, std::vector<KLV*> > >* > const& detailedTriggerMatchedLeptons,
			std::vector<std::string> const& hltPathsWithoutCommonMatchRequired
	);
    
};


class DiTauPairIsoPtComparator
{
public:
	DiTauPairIsoPtComparator(const std::map<KLepton*, double>* leptonIsolationOverPt, bool isTauIsoMVA);
	
	bool operator() (DiTauPair const& diTauPair1, DiTauPair const& diTauPair2) const;

private:
	const std::map<KLepton*, double>* m_leptonIsolationOverPt;
	bool m_isTauIsoMVA;
};

