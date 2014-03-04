
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/KappaAnalysis/interface/KappaEventProvider.h"

#include "HttTypes.h"

/**
   \brief class to connect the analysis specific event content to the pipelines.

   This is a plain copy of the KappaEventProvider. 
*/

class HttEventProvider: public KappaEventProvider<HttTypes> {
public:
	
	typedef typename HttTypes::global_setting_type global_setting_type;
	
	HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType) :
			KappaEventProvider<HttTypes>(fileInterface, inpType)
	{

	}

	virtual void WireEvent(global_setting_type const& globalSettings) ARTUS_CPP11_OVERRIDE
	{
		KappaEventProvider::WireEvent(globalSettings);
	}
};
