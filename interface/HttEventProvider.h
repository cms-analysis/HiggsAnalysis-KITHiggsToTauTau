
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Provider/interface/KappaEventProvider.h"

#include "HttTypes.h"

class HttEventProvider: public KappaEventProvider<HttTypes::event_type> {
public:
	HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType) :
			KappaEventProvider<HttTypes::event_type>(fileInterface, inpType) {

		WireEvent();
	}

private:
	void WireEvent() {
		m_event.m_muons = m_fi.Get<KDataMuons>("muons", true);
	}
};
