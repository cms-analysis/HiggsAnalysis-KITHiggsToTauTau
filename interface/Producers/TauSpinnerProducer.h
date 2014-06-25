
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

class TauSpinnerProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tauspinner";
	}

	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
	

private:
	virtual TauSpinner::SimpleParticle getSimpleParticle(KGenParticle*& in) const;
	virtual std::vector<TauSpinner::SimpleParticle> *GetFinalStates(MotherDaughterBundle& mother,
                                        std::vector<TauSpinner::SimpleParticle> *resultVector) const;
	virtual double GetMass(std::vector<TauSpinner::SimpleParticle> in) const;
	virtual void LogSimpleParticle(std::string particleName, TauSpinner::SimpleParticle in) const;
	virtual void LogSimpleParticle(std::string particleName, std::vector<TauSpinner::SimpleParticle> in) const;

};


