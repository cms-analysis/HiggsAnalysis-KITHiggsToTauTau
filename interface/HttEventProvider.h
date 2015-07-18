
#pragma once

#include "Artus/KappaAnalysis/interface/KappaEventProvider.h"

#include "HttTypes.h"

/**
   \brief class to connect the analysis specific event content to the pipelines.
*/


class HttEventProvider: public KappaEventProvider<HttTypes> {
public:
	
	typedef typename HttTypes::setting_type setting_type;
	
	HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType, bool batchMode=false);

	virtual void WireEvent(setting_type const& settings) override;
};

