
#pragma once

//#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "RooWorkspace.h"
#include "RooFunctor.h"
#include "TSystem.h"
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string.hpp>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

/**
   \brief RooWorkspaceWeightProducer
   Config tags:
   - Fill me with something meaningful

*/

class RooWorkspaceWeightProducer: public ProducerBase<HttTypes> {
public:

	RooWorkspaceWeightProducer();
	RooWorkspaceWeightProducer(bool (setting_type::*GetSaveRooWorkspaceTriggerWeightAsOptionalOnly)(void) const,
							   std::string (setting_type::*GetRooWorkspace)(void) const,
							   std::vector<std::string>& (setting_type::*GetRooWorkspaceWeightNames)(void) const,
							   std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectNames)(void) const,
							   std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectArguments)(void) const);

	virtual std::string GetProducerId() const override {
		return "RooWorkspaceWeightProducer";
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type & product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
private:
	bool (setting_type::*GetSaveRooWorkspaceTriggerWeightAsOptionalOnly)(void) const;
	std::string (setting_type::*GetRooWorkspace)(void) const;
	std::vector<std::string>& (setting_type::*GetRooWorkspaceWeightNames)(void) const;
	std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectNames)(void) const;
	std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectArguments)(void) const;

protected:
	bool m_saveTriggerWeightAsOptionalOnly;
	std::map<int,std::vector<std::string>> m_weightNames;
	std::map<int,std::vector<std::string>> m_functorArgs;
	std::map<int,std::vector<RooFunctor*>> m_functors;
	RooWorkspace *m_workspace;
	HttEnumTypes::DataMcScaleFactorProducerMode m_scaleFactorMode = HttEnumTypes::DataMcScaleFactorProducerMode::NONE;

};

class EETriggerWeightProducer: public RooWorkspaceWeightProducer {
public:
	EETriggerWeightProducer();

	virtual std::string GetProducerId() const override {
		return "EETriggerWeightProducer";
	}

	virtual void Produce(event_type const& event, product_type & product,
						 setting_type const& settings, metadata_type const& metadata) const override;
};

class MuMuTriggerWeightProducer: public RooWorkspaceWeightProducer {
public:
	MuMuTriggerWeightProducer();

	virtual std::string GetProducerId() const override {
		return "MuMuTriggerWeightProducer";
	}

	virtual void Produce(event_type const& event, product_type & product,
						 setting_type const& settings, metadata_type const& metadata) const override;
};

class TauTauTriggerWeightProducer: public RooWorkspaceWeightProducer {
public:
	TauTauTriggerWeightProducer();

	virtual std::string GetProducerId() const override {
		return "TauTauTriggerWeightProducer";
	}

	virtual void Produce(event_type const& event, product_type & product,
						 setting_type const& settings, metadata_type const& metadata) const override;
};

class MuTauTriggerWeightProducer: public RooWorkspaceWeightProducer {
public:
	MuTauTriggerWeightProducer();

	virtual std::string GetProducerId() const override {
		return "MuTauTriggerWeightProducer";
	}

	virtual void Produce(event_type const& event, product_type & product,
						 setting_type const& settings, metadata_type const& metadata) const override;
};

class EmbeddingWeightProducer: public RooWorkspaceWeightProducer {
public:
	EmbeddingWeightProducer();

	virtual std::string GetProducerId() const override {
		return "EmbeddingWeightProducer";
	}

	virtual void Produce(event_type const& event, product_type & product,
						 setting_type const& settings, metadata_type const& metadata) const override;
};

class LeptonTauTrigger2017WeightProducer: public RooWorkspaceWeightProducer {
public:
	LeptonTauTrigger2017WeightProducer();

	virtual std::string GetProducerId() const override {
		return "LeptonTauTrigger2017WeightProducer";
	}

	virtual void Produce(event_type const& event, product_type & product,
						 setting_type const& settings, metadata_type const& metadata) const override;
};

class LegacyWeightProducer: public RooWorkspaceWeightProducer {
public:
       LegacyWeightProducer();

       virtual std::string GetProducerId() const override {
               return "LegacyWeightProducer";
       }

       virtual void Produce(event_type const& event, product_type & product,
                                                setting_type const& settings, metadata_type const& metadata) const override;
};

class LegacyWeightUncProducer: public RooWorkspaceWeightProducer {
public:
       LegacyWeightUncProducer();

       virtual std::string GetProducerId() const override {
               return "LegacyWeightUncProducer";
       }

       virtual void Produce(event_type const& event, product_type & product,
                                                setting_type const& settings, metadata_type const& metadata) const override;
};
