
#pragma once

#include "TauSpinner/SimpleParticle.h"
#include "TauSpinner/tau_reweight_lib.h"

#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief GlobalProducer, for tau decays on generator level. Following quantities are calculated:
   -This producer has the product of the GenTauDecayProducer as input and calculates the TauSpinnerWeight
   for these particles, where tau is the daughter of Higgs

*/

class TauSpinnerProducer: public ProducerBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override
	{
		return "TauSpinnerProducer";
	}
	
	~TauSpinnerProducer();

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

	static double CustomRandomGenerator();

private:
	virtual TauSpinner::SimpleParticle GetSimpleParticle(RMFLV const& particleLV, int particlePdgId) const;
	
	virtual GenParticleDecayTree* GetTau(GenParticleDecayTree* currentParticle) const;
	virtual std::vector<TauSpinner::SimpleParticle> GetFinalStates(
			GenParticleDecayTree& currentParticle,
			std::vector<TauSpinner::SimpleParticle>& resultVector
	) const;
	
	std::string GetLabelForWeightsMap(float mixingAngleOverPiHalf) const;
	
	std::map<int, std::vector<int> > m_validPdgIdsAndStatusCodes;
	std::map<std::string, std::vector<int> > m_validPdgIdsAndStatusCodesByString;
	
	std::vector<float> mixingAnglesOverPiHalf;
	
	std::string pipelineName;
	mutable int numberOfNanWeights = 0;
};

namespace std{
	string to_string(TauSpinner::SimpleParticle& particle);
	string to_string(std::vector<TauSpinner::SimpleParticle>& particleVector);
}
