
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/KappaAnalysis/interface/KappaFactory.h"

#include "HttTypes.h"


class HttFactory: public KappaFactory<HttTypes> {
public:

	HttFactory() : KappaFactory<HttTypes>() {  };
	virtual ~HttFactory() {  };

	virtual HttProducerBase * createProducer ( std::string const& id ) ARTUS_CPP11_OVERRIDE;
	virtual HttFilterBase * createFilter ( std::string const& id ) ARTUS_CPP11_OVERRIDE;
	virtual HttConsumerBase * createConsumer ( std::string const& id ) ARTUS_CPP11_OVERRIDE;

};
