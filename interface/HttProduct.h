
#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"
#include "Artus/Utility/interface/EnumHelper.h"


#define DECAY_CHANNEL_BY_NAME(NAME) DecayChannel :: NAME
#define EVENT_CATEGORY_BY_NAME(NAME) EventCategory :: NAME

enum class DecayChannel : int {
	NONE = -1,
	TT   = 0,
	MT   = 1,
	ET   = 2,
	EM   = 3,
	MM   = 4,
	EE   = 5
};

// TODO: to be extended
enum class EventCategory : int {
	NONE      = -1,
	INCLUSIVE = 0,
	ZERO_JET  = 1,
	BOOST     = 2,
	VBF       = 3
};


class HttProduct : public KappaProduct {
public:
	HttProduct() : KappaProduct() {};
	//~HttProduct() : ~KappaProduct() {};
	
	DecayChannel m_decayChannel;
	std::vector<EventCategory> m_eventCategories;
	
	std::vector<RMDataLV*> m_ptOrderedLeptons;
	std::vector<RMDataLV*> m_flavourOrderedLeptons;
	
};

