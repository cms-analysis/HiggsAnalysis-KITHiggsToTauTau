
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiTauPair.h"


DiTauPair::DiTauPair(KLepton* lepton1, KLepton* lepton2) :
	std::pair<KLepton*, KLepton*>(lepton1, lepton2)
{
}


DiTauPairIsoPtComparator::DiTauPairIsoPtComparator(const std::map<KLepton*, double>* leptonIsolationOverPt):
	m_leptonIsolationOverPt(leptonIsolationOverPt)
{
}

bool DiTauPairIsoPtComparator::operator() (DiTauPair const& diTauPair1, DiTauPair const& diTauPair2) const
{
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Pair_Selection_Algorithm
	
	double isoPair1Lepton1 = SafeMap::Get(*m_leptonIsolationOverPt, diTauPair1.first);
	double isoPair2Lepton1 = SafeMap::Get(*m_leptonIsolationOverPt, diTauPair2.first);
	
	if (! Utility::ApproxEqual(isoPair1Lepton1, isoPair2Lepton1))
	{
		return (isoPair1Lepton1 < isoPair2Lepton1);
	}
	else
	{
		if (! Utility::ApproxEqual(diTauPair1.first->p4.Pt(), diTauPair2.first->p4.Pt()))
		{
			return (diTauPair1.first->p4.Pt() > diTauPair2.first->p4.Pt());
		}
		else
		{
			double isoPair1Lepton2 = SafeMap::Get(*m_leptonIsolationOverPt, diTauPair1.second);
			double isoPair2Lepton2 = SafeMap::Get(*m_leptonIsolationOverPt, diTauPair2.second);
			
			if (! Utility::ApproxEqual(isoPair1Lepton2, isoPair2Lepton2))
			{
				return (isoPair1Lepton2 < isoPair2Lepton2);
			}
			else
			{
				return (diTauPair1.second->p4.Pt() > diTauPair2.second->p4.Pt());
			}
		}
	}
}

