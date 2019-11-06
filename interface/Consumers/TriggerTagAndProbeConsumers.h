#pragma once

#include <TTree.h>

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Utility/interface/RootFileHelper.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

template<class TTag, class TProbe>
class TriggerTagAndProbeConsumerBase: public ConsumerBase<HttTypes>
{

public:

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

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ConsumerBase<HttTypes>::Init(settings, metadata);

		RootFileHelper::SafeCd(settings.GetRootOutFile(),
		                       settings.GetRootFileFolder());
		m_tree = new TTree(m_treeName.c_str(), m_treeName.c_str());
		
		m_tree->Branch("tag", &m_currentTagObject);
		m_tree->Branch("tagMatched", &m_currentTagObjectMatched, "tagMatched/O");
		m_tree->Branch("probe", &m_currentProbeObject);
		m_tree->Branch("probeMatched", &m_currentProbeObjectMatched, "probeMatched/O");
		m_tree->Branch("tagProbeSystem", &m_tagProbeSystem);
		

		LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "tagPt", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<float> tagPt;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				tagPt.push_back(tagProbePair->first->p4.Pt());
			}
			return tagPt;
		});
		LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "probePt", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<float> probePt;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				probePt.push_back(tagProbePair->second->p4.Pt());
			}
			return probePt;
		});
		LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "probeEta", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<float> probeEta;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				probeEta.push_back(tagProbePair->second->p4.Eta());
			}
			return probeEta;
		});
		LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "tagProbeDeltaR", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<float> tagProbeDeltaR;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				tagProbeDeltaR.push_back(ROOT::Math::VectorUtil::DeltaR(tagProbePair->first->p4, tagProbePair->second->p4));
			}
			return tagProbeDeltaR;
		});
		LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "tagProbeMass", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<float> tagProbeMass;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				tagProbeMass.push_back((tagProbePair->first->p4 + tagProbePair->second->p4).M());
			}
			return tagProbeMass;
		});
		LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "probeMatched", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<int> probeMatched;
			for (typename std::vector<std::pair<bool, bool> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectMatchedPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectMatchedPairsMember)).end(); ++tagProbePair)
			{
				probeMatched.push_back(tagProbePair->second);
			}
			return probeMatched;
		});
		LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "tagMatched", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<int> tagMatched;
			for (typename std::vector<std::pair<bool, bool> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectMatchedPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectMatchedPairsMember)).end(); ++tagProbePair)
			{
				tagMatched.push_back(tagProbePair->first);
			}
			return tagMatched;
		});
		LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "tagCharge", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<int> tagCharge;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				tagCharge.push_back(tagProbePair->first->charge());
			}
			return tagCharge;
		});
		LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "probeCharge", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<int> probeCharge;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				probeCharge.push_back(tagProbePair->second->charge());
			}
			return probeCharge;
		});
		LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "isOS", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<int> isOS;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				isOS.push_back(int((tagProbePair->first->charge()*tagProbePair->second->charge())<0));
			}
			return isOS;
		});
		LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "tagIsoOverPt", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<float> tagIsoOverPt;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				tagIsoOverPt.push_back(tagProbePair->first->pfIso() / tagProbePair->first->p4.Pt());
			}
			return tagIsoOverPt;
		});
		LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "tagIso", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			std::vector<float> tagIso;
			for (typename std::vector<std::pair<TTag*, TProbe*> >::const_iterator tagProbePair = (product.*(this->m_triggerTagProbeObjectPairsMember)).begin();
		       tagProbePair != (product.*(this->m_triggerTagProbeObjectPairsMember)).end(); ++tagProbePair)
			{
				tagIso.push_back(tagProbePair->first->pfIso() / tagProbePair->first->p4.Pt());
			}
			return tagIso;
		});
	}

	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product,
	                                  setting_type const& settings, metadata_type const& metadata) override
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
	
	virtual void Finish(setting_type const& settings, metadata_type const& metadata) override
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

