
#pragma once

#include "Artus/KappaAnalysis/interface/KappaEvent.h"

/**
   HttEvent HiggsAnalysis/KITHiggsToTauTau/interface/HttEvent.h

   Defines the objects which are contained in a kappa ntuple, usually in use for a Htt analysis. 
   Members are usually pointer to the corresponding collections of objects in the input file. This 
   is a 1:1 copy of a usual KappaEvent.
*/

class HttEvent : public KappaEvent
{
public:
	HttEvent() : KappaEvent() {};
	//~HttEvent() : ~KappaEvent() {};

	/// pointer to (old) MVA MET collections
	KMET* m_mvaMetTT = 0;
	KMET* m_mvaMetMT = 0;
	KMET* m_mvaMetET = 0;
	KMET* m_mvaMetEM = 0;
	KMET* m_mvaMet = 0;

	/// pointer to (new) MVA MET collections
	KMETs* m_mvaMetsTT = 0;
	KMETs* m_mvaMetsMT = 0;
	KMETs* m_mvaMetsET = 0;
	KMETs* m_mvaMetsEM = 0;
	KMETs* m_mvaMets = 0;
	
};

