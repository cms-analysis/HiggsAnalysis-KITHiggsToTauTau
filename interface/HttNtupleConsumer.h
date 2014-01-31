
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/Consumer/interface/NtupleConsumerBase.h"

#include "HttTypes.h"


class HttNtupleConsumer: public NtupleConsumerBase<HttTypes> {
private:
	
	float returnvalue(std::string string, HttEvent const& event,
			HttProduct const& product ) ARTUS_CPP11_OVERRIDE
	{
		if (string == "pt")
			return event.m_floatPtSim;
		else if (string == "pt_corr")
			return product.m_floatPtSim_corrected;
		else if (string == "theta")
			return event.m_floatTheSim;
		else
			LOG_FATAL("The quantity " << string << " could not be added to the Ntuple")
	}


};
