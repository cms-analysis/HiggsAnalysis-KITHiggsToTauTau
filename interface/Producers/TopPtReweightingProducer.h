
#pragma once

#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include <boost/regex.hpp>

/**
   \brief TopPtReweightingProducer
   Config tags:
   - Fill me with something meaningful

*/

class TopPtReweightingProducer : public KappaProducerBase {
public:

	std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings) override;
	void Produce( KappaEvent const& event,
			KappaProduct & product,
			KappaSettings const& settings) const override;
private:
	bool m_isTTbar;
};
