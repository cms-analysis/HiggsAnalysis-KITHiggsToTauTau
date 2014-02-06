
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Provider/interface/KappaEventProvider.h"
#include "Artus/KappaLeptonAnalysis/interface/KappaLeptonEventProvider.h"

#include "HttTypes.h"

class HttEventProvider: public KappaLeptonEventProvider<HttTypes::event_type> {
public:
	HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType) :
			KappaLeptonEventProvider<HttTypes::event_type>(fileInterface, inpType)
	{

	}

	virtual void WireEvent() {
		
	}
};
