
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"


class DiTauPair : public std::pair<KLepton*, KLepton*>
{
public:
	DiTauPair(KLepton* lepton1, KLepton* lepton2);
};


class DiTauPairIsoPtComparator
{
public:
	DiTauPairIsoPtComparator(const std::map<KLepton*, double>* leptonIsolationOverPt);
	
	bool operator() (DiTauPair const& diTauPair1, DiTauPair const& diTauPair2) const;

private:
	const std::map<KLepton*, double>* m_leptonIsolationOverPt;
};

