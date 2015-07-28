
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/KappaAnalysis/interface/Producers/TriggerMatchingProducers.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiTauPair.h"


DiTauPair::DiTauPair(KLepton* lepton1, KLepton* lepton2) :
	std::pair<KLepton*, KLepton*>(lepton1, lepton2)
{
}

bool DiTauPair::IsOppositelyCharged()
{
	return (first->charge() * second->charge() < 0);
}

double DiTauPair::GetDeltaR()
{
	return ROOT::Math::VectorUtil::DeltaR(first->p4, second->p4);
}

// TODO: this function should probably get cached
std::vector<std::string> DiTauPair::GetCommonHltPaths(
		std::map<KLepton*, std::map<std::string, std::map<std::string, std::vector<KLV*> > >* > const& detailedTriggerMatchedLeptons,
		std::vector<std::string> const& hltPathsWithoutCommonMatchRequired
) {
	std::vector<std::string> hltPaths1 = TriggerMatchingProducerBase<KLepton>::GetHltNamesWhereAllFiltersMatched(*SafeMap::GetWithDefault(
			detailedTriggerMatchedLeptons,
			&(*first),
			new std::map<std::string, std::map<std::string, std::vector<KLV*> > >()
	));
	
	std::vector<std::string> hltPaths2 = TriggerMatchingProducerBase<KLepton>::GetHltNamesWhereAllFiltersMatched(*SafeMap::GetWithDefault(
			detailedTriggerMatchedLeptons,
			&(*second),
			new std::map<std::string, std::map<std::string, std::vector<KLV*> > >()
	));
	
	std::vector<std::string> commonHltPaths = Utility::Intersection(hltPaths1, hltPaths2);
	
	// in case no common triggers are found, use the fired ones of hltPathsWithoutCommonMatchRequired
	if (commonHltPaths.size() == 0)
	{
		for (std::vector<std::string>::const_iterator hltPathWithoutCommonMatchRequired = hltPathsWithoutCommonMatchRequired.begin();
		     hltPathWithoutCommonMatchRequired != hltPathsWithoutCommonMatchRequired.end(); ++hltPathWithoutCommonMatchRequired)
		{
			for (std::vector<std::string>::iterator hltPath1 = hltPaths1.begin(); hltPath1 != hltPaths1.end(); ++hltPath1)
			{
				if (boost::regex_search(*hltPath1, boost::regex(*hltPathWithoutCommonMatchRequired, boost::regex::icase | boost::regex::extended)))
				{
					commonHltPaths.push_back(*hltPath1);
				}
			}
			for (std::vector<std::string>::iterator hltPath2 = hltPaths2.begin(); hltPath2 != hltPaths2.end(); ++hltPath2)
			{
				if (boost::regex_search(*hltPath2, boost::regex(*hltPathWithoutCommonMatchRequired, boost::regex::icase | boost::regex::extended)))
				{
					commonHltPaths.push_back(*hltPath2);
				}
			}
		}
	}
	
	return commonHltPaths;
}

DiTauPairIsoPtComparator::DiTauPairIsoPtComparator(const std::map<KLepton*, double>* leptonIsolationOverPt):
	m_leptonIsolationOverPt(leptonIsolationOverPt)
{
}

bool DiTauPairIsoPtComparator::operator() (DiTauPair const& diTauPair1, DiTauPair const& diTauPair2) const
{
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Pair_Selection_Algorithm
	
	double isoPair1Lepton1 = SafeMap::GetWithDefault(*m_leptonIsolationOverPt, diTauPair1.first, static_cast<double>(diTauPair1.first->pfIso()));
	double isoPair2Lepton1 = SafeMap::GetWithDefault(*m_leptonIsolationOverPt, diTauPair2.first, static_cast<double>(diTauPair1.first->pfIso()));
	
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
			double isoPair1Lepton2 = SafeMap::GetWithDefault(*m_leptonIsolationOverPt, diTauPair1.second, static_cast<double>(diTauPair1.second->pfIso()));
			double isoPair2Lepton2 = SafeMap::GetWithDefault(*m_leptonIsolationOverPt, diTauPair2.second, static_cast<double>(diTauPair1.second->pfIso()));
			
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

