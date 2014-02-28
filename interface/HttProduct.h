
#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"
#include "Artus/Utility/interface/EnumHelper.h"


#define DECAY_CHANNEL_BY_NAME(NAME) DecayChannel :: NAME
#define EVENT_CATEGORY_BY_NAME(NAME) EventCategory :: NAME


class HttProduct : public KappaProduct {
public:
	HttProduct() : KappaProduct()
	{
		/* tests
		decayChannel = DecayChannel::MT;
		std::cout << EnumHelper::toUnderlyingValue(decayChannel) << std::endl;
		decayChannel = DECAY_CHANNEL_BY_NAME(ET);
		std::cout << EnumHelper::toUnderlyingValue(decayChannel) << std::endl;
		decayChannel = EnumHelper::toEnum<DecayChannel>(3);
		std::cout << EnumHelper::toUnderlyingValue(decayChannel) << std::endl;
		*/
	};
	
	~HttProduct() : ~KappaProduct {};
	
	enum class DecayChannel : int {
		TT = 0,
		MT = 1,
		ET = 2,
		EM = 3,
		MM = 4,
		EE = 5
	} decayChannel;
	
	// TODO: extend
	enum class EventCategory : int {
		INCLUSIVE = 0,
		ZERO_JET  = 1,
		BOOST     = 2,
		VBF       = 3
	};
	std::vector<EventCategory> eventCategories;
	
};
