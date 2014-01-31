
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "HttTypes.h"

class PtCorrectionProducer: public HttGlobalProducerBase {
public:

	virtual bool ProduceGlobal(HttEvent const& event,
			HttProduct & product,
			HttGlobalSettings const& globalSettings) const
					ARTUS_CPP11_OVERRIDE {

		product.m_floatPtSim_corrected = event.m_floatPtSim
				* globalSettings.GetProducerPtCorrectionFactor();

		return true;
	}

};
