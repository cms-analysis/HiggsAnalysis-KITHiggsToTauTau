
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/KappaAnalysis/interface/KappaEventProvider.h"

#include "HttTypes.h"

/**
   \brief class to connect the analysis specific event content to the pipelines.
*/


class HttEventProvider: public KappaEventProvider<HttTypes> {
public:
	
	typedef typename HttTypes::setting_type setting_type;
	
	HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType);

	virtual void WireEvent(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
};

