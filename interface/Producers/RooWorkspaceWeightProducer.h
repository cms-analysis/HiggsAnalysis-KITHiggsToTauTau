
#pragma once

//#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "RooWorkspace.h"
#include "RooFunctor.h"
#include "TSystem.h"
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string.hpp>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief RooWorkspaceWeightProducer
   Config tags:
   - Fill me with something meaningful

*/

class RooWorkspaceWeightProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	RooWorkspaceWeightProducer();
	RooWorkspaceWeightProducer(std::string (setting_type::*GetRooWorkspace)(void) const,
							   std::vector<std::string>& (setting_type::*GetRooWorkspaceWeightNames)(void) const,
							   std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectNames)(void) const,
							   std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectArguments)(void) const);

	virtual std::string GetProducerId() const override {
		return "RooWorkspaceWeightProducer";
	}

	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
	std::string (setting_type::*GetRooWorkspace)(void) const;
	std::vector<std::string>& (setting_type::*GetRooWorkspaceWeightNames)(void) const;
	std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectNames)(void) const;
	std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectArguments)(void) const;

protected:
    std::map<int,std::vector<std::string>> m_weightNames;
    std::map<int,std::vector<std::string>> m_functorArgs;
    std::map<int,std::vector<RooFunctor*>> m_functors;
    RooWorkspace *m_workspace;

};

class MuMuTriggerWeightProducer: public RooWorkspaceWeightProducer {
public:
	MuMuTriggerWeightProducer();

	virtual std::string GetProducerId() const override {
		return "MuMuTriggerWeightProducer";
	}

	//virtual void Init(setting_type const& settings);

	virtual void Produce(event_type const& event, product_type & product,
	                     setting_type const& settings) const override;
};
