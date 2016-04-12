
#pragma once

#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"

/**
   \brief TopPtReweightingProducer
   Config tags:
   - Fill me with something meaningful

*/

class TopPtReweightingProducer : public KappaProducerBase {
public:

	std::string GetProducerId() const override;

	void Produce( KappaEvent const& event,
			KappaProduct & product,
			KappaSettings const& settings) const override;

};
