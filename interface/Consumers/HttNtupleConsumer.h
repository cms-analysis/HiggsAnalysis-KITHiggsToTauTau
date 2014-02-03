
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/Consumer/interface/NtupleConsumerBase.h"

#include "../HttTypes.h"


class HttNtupleConsumer: public NtupleConsumerBase<HttTypes> {
public:

	virtual std::string GetConsumerId() {
		return "ntuple";
	}

private:

	float returnvalue(std::string string, HttEvent const& event,
			HttProduct const& product ) ARTUS_CPP11_OVERRIDE
	{
	
		/*for(auto muon = event.m_muons->begin(); muon != event.m_muons->end(); muon++) {
			double pt = muon->p4()->Pt();
		}*/
		
		if(event.m_muons->size() > 1) {
			if (string == "hardLepPt") return event.m_muons->at(0).p4.Pt();
			else if (string == "hardLepEta") return event.m_muons->at(0).p4.Eta();
			else if (string == "softLepPt") return event.m_muons->at(1).p4.Pt();
			else if (string == "softLepEta") return event.m_muons->at(1).p4.Eta();
			else if (string == "diLepMass") return (event.m_muons->at(0).p4 + event.m_muons->at(1).p4).mass();
			else {
				LOG_FATAL("The quantity " << string << " could not be added to the Ntuple")
			
			}
		}
		
		return -999.0;
	}


};
