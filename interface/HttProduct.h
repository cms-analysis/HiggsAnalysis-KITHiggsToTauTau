
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"
#include "HttComputedObjects.h"


class HttProduct : public KappaProduct
{
public:

	enum class DecayChannel : int
	{
		NONE = -1,
		TT   = 0,
		MT   = 1,
		ET   = 2,
		EM   = 3,
		MM   = 4,
		EE   = 5
	};
	static DecayChannel ToDecayChannel(std::string const& decayChannelString)
	{
		if (decayChannelString == "TT") return DecayChannel::TT;
		else if (decayChannelString == "MT") return DecayChannel::MT;
		else if (decayChannelString == "ET") return DecayChannel::ET;
		else if (decayChannelString == "EM") return DecayChannel::EM;
		else if (decayChannelString == "MM") return DecayChannel::MM;
		else if (decayChannelString == "EE") return DecayChannel::EE;
		return DecayChannel::NONE;
	}

	// TODO: to be extended
	enum class EventCategory : int
	{
		NONE      = -1,
		INCLUSIVE = 0,
		ZERO_JET  = 1,
		BOOST     = 2,
		VBF       = 3
	};
	static EventCategory ToEventCategory(std::string const& eventCategoryString)
	{
		if (eventCategoryString == "INCLUSIVE") return EventCategory::INCLUSIVE;
		else if (eventCategoryString == "ZERO_JET") return EventCategory::ZERO_JET;
		else if (eventCategoryString == "BOOST") return EventCategory::BOOST;
		else if (eventCategoryString == "VBF") return EventCategory::VBF;
		return EventCategory::NONE;
	}

	DecayChannel m_decayChannel;
	std::vector<EventCategory> m_eventCategories;
	
	// filled by DecayChannelProducer
	std::vector<KLepton*> m_ptOrderedLeptons;
	std::vector<KLepton*> m_flavourOrderedLeptons;

	// filled by HttValid<Leptons>Producer
	std::map<KLepton*, double> m_leptonIsolation;
	std::map<KLepton*, double> m_leptonIsolationOverPt;
	
	KDataPFMET* m_met = 0;

	double m_genMassRoundOff1;
	double m_genMassRoundOff2;
	double m_genPhi;
	double m_genPhiStar;
	double m_genPsiStarCP;
	std::pair <double,double> m_genChargedProngEnergys;
	std::pair <double,double> m_genChargedPionEnergysApprox;
	double m_genThetaNuHadron;
	double m_genAlphaTauNeutrinos;
	double PhiDet;
	double PhiStarDet;
	double PhiOnePion;
	double PhiStarOnePion;

	KGenParticle* m_genOneProngCharged1 = 0;
	KGenParticle* m_genOneProngCharged2 = 0;

};
