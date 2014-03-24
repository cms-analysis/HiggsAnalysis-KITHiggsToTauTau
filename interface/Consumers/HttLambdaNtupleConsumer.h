
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/GlobalInclude.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumerBase.h"

#include "../HttTypes.h"


class HttLambdaNtupleConsumer: public LambdaNtupleConsumerBase<HttTypes> {
public:

	typedef std::function<float(HttEvent const&, HttProduct const&)> float_extractor_lambda;

	HttLambdaNtupleConsumer();
};
