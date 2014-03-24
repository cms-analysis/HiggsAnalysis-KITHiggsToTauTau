
#pragma once

#include "Artus/Consumer/interface/CutFlowHistogramConsumer.h"

#include "../HttTypes.h"


class HttCutFlowHistogramConsumer: public CutFlowHistogramConsumer<HttTypes> {
public:
	virtual void Init(HttPipeline * pipeline) ARTUS_CPP11_OVERRIDE;
	
};
