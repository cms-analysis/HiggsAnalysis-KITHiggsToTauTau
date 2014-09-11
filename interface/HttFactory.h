
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/KappaAnalysis/interface/KappaFactory.h"

#include "HttTypes.h"


class HttFactory: public KappaFactory {
public:

	HttFactory() : KappaFactory() {  };
	virtual ~HttFactory() {  };

	virtual ProducerBaseUntemplated * createProducer(std::string const& id) ARTUS_CPP11_OVERRIDE;
	virtual FilterBaseUntemplated * createFilter(std::string const& id) ARTUS_CPP11_OVERRIDE;
	virtual ConsumerBaseUntemplated * createConsumer(std::string const& id) ARTUS_CPP11_OVERRIDE;

};
