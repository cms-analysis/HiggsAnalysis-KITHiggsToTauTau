
#pragma once

#include <boost/regex.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/KappaAnalysis/interface/Producers/TriggerMatchingProducers.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producers for candidates of di-tau pairs
*/


template<class TObject>
class TriggerTagAndProbeProducerBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	TriggerTagAndProbeProducerBase(
			std::vector<TObject*> product_type::*validObjectsMember,
			std::map<TObject*, std::map<std::string, std::map<std::string, std::vector<KLV*> > >* > product_type::*detailedTriggerMatchedObjects,
			std::vector<std::string>& (setting_type::*GetTagObjectHltPaths)(void) const,
			std::vector<std::string>& (setting_type::*GetProbeObjectHltPaths)(void) const,
			//std::vector<std::string>& (setting_type::*GetTagObjectTriggerFilterNames)(void) const,
			//std::vector<std::string>& (setting_type::*GetProbeObjectTriggerFilterNames)(void) const,
			bool product_type::*triggerTagObjectAvailable,
			bool product_type::*triggerProbeObjectAvailable,
			TObject* product_type::*triggerTagObject,
			TObject* product_type::*triggerProbeObject
	) :
		ProducerBase<HttTypes>(),
		m_validObjectsMember(validObjectsMember),
		m_detailedTriggerMatchedObjects(detailedTriggerMatchedObjects),
		GetTagObjectHltPaths(GetTagObjectHltPaths),
		GetProbeObjectHltPaths(GetProbeObjectHltPaths),
		//GetTagObjectTriggerFilterNames(GetTagObjectTriggerFilterNames),
		//GetProbeObjectTriggerFilterNames(GetProbeObjectTriggerFilterNames),
		m_triggerTagObjectAvailable(triggerTagObjectAvailable),
		m_triggerProbeObjectAvailable(triggerProbeObjectAvailable),
		m_triggerTagObject(triggerTagObject),
		m_triggerProbeObject(triggerProbeObject)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
	}
	
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		assert((product.*m_validObjectsMember).size() >= 2);
		
		(product.*m_triggerTagObjectAvailable) = false;
		(product.*m_triggerProbeObjectAvailable) = false;
		(product.*m_triggerTagObject) = nullptr;
		(product.*m_triggerProbeObject) = nullptr;
		
		// TODO: swapping the loops over TObject and std::string can speed up this producer significantly
		for (typename std::vector<TObject*>::iterator validObject = (product.*m_validObjectsMember).begin();
		     validObject != (product.*m_validObjectsMember).end(); ++validObject)
		{
			std::vector<std::string> hltPaths = TriggerMatchingProducerBase<TObject>::GetHltNamesWhereAllFiltersMatched(*SafeMap::GetWithDefault(
					(product.*m_detailedTriggerMatchedObjects),
					(*validObject),
					new std::map<std::string, std::map<std::string, std::vector<KLV*> > >()
			));
			
			for (std::vector<std::string>::iterator hltPath = hltPaths.begin();
			     (hltPath != hltPaths.end()) && (! (product.*m_triggerTagObjectAvailable));
			     ++hltPath)
			{
				for (std::vector<std::string>::iterator tagObjectHltPath = (settings.*GetTagObjectHltPaths)().begin();
				     (tagObjectHltPath != (settings.*GetTagObjectHltPaths)().end()) && (! (product.*m_triggerTagObjectAvailable));
				     ++tagObjectHltPath)
				{
					if (boost::regex_search(*hltPath, boost::regex(*tagObjectHltPath, boost::regex::icase | boost::regex::extended)))
					{
						(product.*m_triggerTagObjectAvailable) = true;
						(product.*m_triggerTagObject) = (*validObject);
					}
				}
			}
			
			if (! (product.*m_triggerTagObjectAvailable))
			{
				for (std::vector<std::string>::iterator hltPath = hltPaths.begin();
				    (hltPath != hltPaths.end()) && (! (product.*m_triggerProbeObjectAvailable));
				    ++hltPath)
				{
					for (std::vector<std::string>::iterator probeObjectHltPath = (settings.*GetProbeObjectHltPaths)().begin();
					     (probeObjectHltPath != (settings.*GetProbeObjectHltPaths)().end()) && (! (product.*m_triggerProbeObjectAvailable));
					     ++probeObjectHltPath)
					{
						if (boost::regex_search(*hltPath, boost::regex(*probeObjectHltPath, boost::regex::icase | boost::regex::extended)))
						{
							(product.*m_triggerProbeObjectAvailable) = true;
							(product.*m_triggerProbeObject) = (*validObject);
						}
					}
				}
			}
		}
	}


private:
	std::vector<TObject*> product_type::*m_validObjectsMember;
	std::map<TObject*, std::map<std::string, std::map<std::string, std::vector<KLV*> > >*> product_type::*m_detailedTriggerMatchedObjects; // TODO: for jets this would be a slighly different type
	std::vector<std::string>& (setting_type::*GetTagObjectHltPaths)(void) const;
	std::vector<std::string>& (setting_type::*GetProbeObjectHltPaths)(void) const;
	//std::vector<std::string>& (setting_type::*GetTagObjectTriggerFilterNames)(void) const;
	//std::vector<std::string>& (setting_type::*GetProbeObjectTriggerFilterNames)(void) const;
	bool product_type::*m_triggerTagObjectAvailable;
	bool product_type::*m_triggerProbeObjectAvailable;
	TObject* product_type::*m_triggerTagObject;
	TObject* product_type::*m_triggerProbeObject;

};



class LeptonTriggerTagAndProbeProducer: public TriggerTagAndProbeProducerBase<KLepton>
{
public:
	LeptonTriggerTagAndProbeProducer();
	virtual std::string GetProducerId() const override;
	virtual void Init(setting_type const& settings) override;
};
