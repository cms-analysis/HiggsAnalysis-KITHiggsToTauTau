
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"
#include <boost/regex.hpp>

#include "RooWorkspace.h"
#include "RooFunctor.h"


#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
#include <TROOT.h>
#endif

/**
   \brief JetToTauFakesProducer
   Config tags:
   
    Run this producer after the Run2DecayModeProducer

*/

class JetToTauFakesProducer : public ProducerBase<HttTypes> {
public:

	virtual ~JetToTauFakesProducer();
	
	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	void Produce(event_type const& event, product_type& product,
                 setting_type const& settings, metadata_type const& metadata) const override;
private:

	std::map<std::string,std::shared_ptr<FakeFactor>> m_ffComb;
	bool m_applyFakeFactors;
	std::string fakefactormethod;
	std::string ff_function_variables;


protected:
	RooWorkspace *m_workspace;
	std::map<std::string,std::shared_ptr<RooFunctor>> fns_fractions;
	//std::map<std::string,std::string> ff_functions;
};
