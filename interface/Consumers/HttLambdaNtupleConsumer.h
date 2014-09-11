
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "../HttTypes.h"


class HttLambdaNtupleConsumer: public KappaLambdaNtupleConsumer<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
};
