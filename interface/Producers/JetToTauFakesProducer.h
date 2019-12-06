
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string.hpp>

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
	std::map<std::string,std::shared_ptr<RooFunctor>> fns_fractions;
	std::string ff_function_variables;
	std::string fakefactormethod;

protected:
	RooWorkspace *m_workspace;
	//std::map<std::string,std::string> ff_functions;
};

class LegacyJetToTauFakesProducer: public JetToTauFakesProducer {
public:
	LegacyJetToTauFakesProducer();
	virtual ~LegacyJetToTauFakesProducer();

	virtual std::string GetProducerId() const override {
		return "LegacyJetToTauFakesProducer";
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type & product,
						 setting_type const& settings, metadata_type const& metadata) const override;

private:
		std::map<std::string,std::shared_ptr<RooFunctor>> m_fns;
		std::map<std::string,std::vector<std::string>> m_ff_functions;
};
