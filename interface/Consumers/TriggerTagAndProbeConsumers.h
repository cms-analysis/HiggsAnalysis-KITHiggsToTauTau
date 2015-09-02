#pragma once

#include <TTree.h>

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


template<class TTag, class TProbe>
class TriggerTagAndProbeConsumerBase: public ConsumerBase<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	TriggerTagAndProbeConsumerBase(
			std::string treeName,
			std::vector<std::pair<TTag*, TProbe*> > product_type::*triggerTagProbeObjectPairsMember,
			std::vector<std::pair<bool, bool> > product_type::*triggerTagProbeObjectMatchedPairsMember
	) :
		ConsumerBase<HttTypes>(),
		m_treeName(treeName),
		m_triggerTagProbeObjectPairsMember(triggerTagProbeObjectPairsMember),
		m_triggerTagProbeObjectMatchedPairsMember(triggerTagProbeObjectMatchedPairsMember)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ConsumerBase<HttTypes>::Init(settings);

		RootFileHelper::SafeCd(settings.GetRootOutFile(),
		                       settings.GetRootFileFolder());
		m_tree = new TTree(m_treeName.c_str(), m_treeName.c_str());
		
		m_tree->Branch("tag", &m_currentTagObject);
		m_tree->Branch("tagMatched", &m_currentTagObjectMatched, "tagMatched/O");
		m_tree->Branch("probe", &m_currentProbeObject);
		m_tree->Branch("probeMatched", &m_currentProbeObjectMatched, "probeMatched/O");
		m_tree->Branch("tagProbeSystem", &m_tagProbeSystem);
	}

	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product,
	                                  setting_type const& settings) override
	{
		size_t index = 0;
		for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*m_triggerTagProbeObjectPairsMember).begin();
		     tagProbePair != (product.*m_triggerTagProbeObjectPairsMember).end(); ++tagProbePair)
		{
			m_currentTagObject = *(tagProbePair->first);
			m_currentProbeObject = *(tagProbePair->second);
			
			m_currentTagObjectMatched = (product.*m_triggerTagProbeObjectMatchedPairsMember).at(index).first;
			m_currentProbeObjectMatched = (product.*m_triggerTagProbeObjectMatchedPairsMember).at(index).second;
			
			m_tagProbeSystem = tagProbePair->first->p4 + tagProbePair->second->p4;
			
			m_tree->Fill();
			++index;
		}
	}
	
	virtual void Finish(setting_type const& settings) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(),
		                       settings.GetRootFileFolder());
		
		m_tree->Write(m_tree->GetName());
	}


private:
	std::string m_treeName;
	std::vector<std::pair<TTag*, TProbe*> > product_type::*m_triggerTagProbeObjectPairsMember;
	std::vector<std::pair<bool, bool> > product_type::*m_triggerTagProbeObjectMatchedPairsMember;
	
	TTree* m_tree = nullptr;
	
	TTag m_currentTagObject;
	bool m_currentTagObjectMatched;
	TProbe m_currentProbeObject;
	bool m_currentProbeObjectMatched;
	RMFLV m_tagProbeSystem;
};



class MMTriggerTagAndProbeConsumer: public TriggerTagAndProbeConsumerBase<KMuon, KMuon>
{
public:
	MMTriggerTagAndProbeConsumer();
	virtual std::string GetConsumerId() const override;
};


class EETriggerTagAndProbeConsumer: public TriggerTagAndProbeConsumerBase<KElectron, KElectron>
{
public:
	EETriggerTagAndProbeConsumer();
	virtual std::string GetConsumerId() const override;
};


class MTTriggerTagAndProbeConsumer: public TriggerTagAndProbeConsumerBase<KMuon, KTau>
{
public:
	MTTriggerTagAndProbeConsumer();
	virtual std::string GetConsumerId() const override;
};


class ETTriggerTagAndProbeConsumer: public TriggerTagAndProbeConsumerBase<KElectron, KTau>
{
public:
	ETTriggerTagAndProbeConsumer();
	virtual std::string GetConsumerId() const override;
};

