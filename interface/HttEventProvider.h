
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Provider/interface/KappaEventProvider.h"
#include "Artus/KappaLeptonAnalysis/interface/KappaLeptonEventProvider.h"

#include "HttTypes.h"

class HttEventProvider: public KappaLeptonEventProvider<HttTypes> {
public:
	
	typedef typename HttTypes::global_setting_type global_setting_type;
	
	HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType) :
			KappaLeptonEventProvider<HttTypes>(fileInterface, inpType)
	{

	}

	virtual void WireEvent(global_setting_type const& globalSettings) {
		KappaLeptonEventProvider::WireEvent(globalSettings);
	}
};
