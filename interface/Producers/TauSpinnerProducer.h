
#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "TauSpinner/SimpleParticle.h"
#include "TauSpinner/tau_reweight_lib.h"

#include "../HttTypes.h"

/**
   \brief GlobalProducer, for tau decays on generator level. Following quantities are calculated:
   -This producer has the product of the GenTauDecayProducer as input and calculates the TauSpinnerWeight
   for these particles, where tau is the daughter of Higgs

*/

class TauSpinnerProducer: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	virtual std::string GetProducerId() const override
	{
		return "TauSpinnerProducer";
	}
	
	~TauSpinnerProducer();

	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings) const override;


private:
	virtual TauSpinner::SimpleParticle GetSimpleParticle(RMFLV const& particleLV, int particlePdgId) const;
	virtual std::vector<TauSpinner::SimpleParticle>* GetFinalStates(MotherDaughterBundle& mother,
			std::vector<TauSpinner::SimpleParticle>* resultVector) const;
	std::string GetLabelForWeightsMap(float mixingAngleOverPiHalf) const;
	
	std::vector<float> mixingAnglesOverPiHalf;
	
	std::string pipelineName;
	mutable int numberOfNanWeights = 0;
};

namespace std{
	string to_string(TauSpinner::SimpleParticle& particle);
	string to_string(std::vector<TauSpinner::SimpleParticle>& particleVector);
}
