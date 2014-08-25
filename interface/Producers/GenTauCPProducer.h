#pragma once

#include "Artus/Utility/interface/Utility.h"


#include "../HttTypes.h"

/**
   \brief GlobalProducer, for CP studies of tau decays. Following quantities are calculated from the input of GenTauDecayProducer :
   
   -Phi* : this is a variable, with which one can say, whether the considered Higgs-Boson is a scalar (CP even) or a pseudoscalar (CP odd)
   -Psi*CP : this is a variable, with which one can figure out, whether the have a CP-mixture or not
*/

class GenTauCPProducer : public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "GenTauCPProducer";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
};
