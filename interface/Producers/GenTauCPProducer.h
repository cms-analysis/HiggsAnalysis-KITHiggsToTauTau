#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "TauSpinner/SimpleParticle.h"
#include "TauSpinner/tau_reweight_lib.h"

#include "../HttTypes.h"

/**
   \brief GlobalProducer, for CP studies of tau decays. Following quantities are calculated from the input of GenTauDecayProducer :
   
   -Phi* : this is a variable, with which one can say, whether the considered Higgs-Boson is a scalar (CP even) or a pseudoscalar (CP odd)
   -Psi*CP : this is a variable, with which one can figure out, whether the have a CP-mixture or not
*/

class GenTauCPProducer : public HttProducerBase {
public:
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "gen_cp";
	}
	
	GenTauCPProducer() : HttProducerBase() {};

	virtual void ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE;
	void PhiPsiStarCalc(RMDataLV tau1, RMDataLV tau2, RMDataLV pion1, RMDataLV pion2, HttProduct& product) const;
	void PhiCalc(RMDataLV higgs, RMDataLV tau1, RMDataLV tau2, RMDataLV pion1, RMDataLV pion2, HttProduct& product) const;
};
