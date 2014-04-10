
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"


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

	HttProduct() : KappaProduct() {};
	//~HttProduct() : ~KappaProduct() {};

	// all weights are collected in a map
	// and multiplied into one "eventWeight" by the EventWeightProducer
	std::map<std::string, double> m_weights;

	DecayChannel m_decayChannel;
	std::vector<EventCategory> m_eventCategories;

	std::vector<RMDataLV*> m_ptOrderedLeptons;
	std::vector<RMDataLV*> m_flavourOrderedLeptons;

	double m_MassRoundOff1;
	double m_MassRoundOff2;
	double m_Phi;
	double m_PhiStar;
	double m_PsiStarCP;

};

