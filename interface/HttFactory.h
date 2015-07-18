
#pragma once

#include "Artus/KappaAnalysis/interface/KappaFactory.h"

#include "HttTypes.h"


class HttFactory: public KappaFactory {
public:

	HttFactory() : KappaFactory() {  };
	virtual ~HttFactory() {  };

	virtual ProducerBaseUntemplated * createProducer(std::string const& id) override;
	virtual FilterBaseUntemplated * createFilter(std::string const& id) override;
	virtual ConsumerBaseUntemplated * createConsumer(std::string const& id) override;

};
