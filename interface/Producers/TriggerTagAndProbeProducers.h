
#pragma once

#include <algorithm>

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
		
		// loop over all permutations of valid objects
		std::vector<TObject*> validObjects = (product.*m_validObjectsMember);
		do
		{
			bool triggerTagObjectAvailable = false;
			bool triggerProbeObjectAvailable = false;
			TObject* triggerTagObject = nullptr;
			TObject* triggerProbeObject = nullptr;
			
			// TODO: swapping the loops over TObject and std::string can speed up this producer significantly
			for (typename std::vector<TObject*>::iterator validObject = validObjects.begin(); validObject != validObjects.end(); ++validObject)
			{
				bool objectIsUsedAsTag = false;
				
				std::vector<std::string> hltPaths = TriggerMatchingProducerBase<TObject>::GetHltNamesWhereAllFiltersMatched(*SafeMap::GetWithDefault(
						(product.*m_detailedTriggerMatchedObjects),
						(*validObject),
						new std::map<std::string, std::map<std::string, std::vector<KLV*> > >()
				));
				
				// search for tag matched first
				for (std::vector<std::string>::iterator hltPath = hltPaths.begin();
					 (hltPath != hltPaths.end()) && (! triggerTagObjectAvailable);
					 ++hltPath)
				{
					for (std::vector<std::string>::iterator tagObjectHltPath = (settings.*GetTagObjectHltPaths)().begin();
						 (tagObjectHltPath != (settings.*GetTagObjectHltPaths)().end()) && (! triggerTagObjectAvailable);
						 ++tagObjectHltPath)
					{
						if (boost::regex_search(*hltPath, boost::regex(*tagObjectHltPath, boost::regex::icase | boost::regex::extended)))
						{
							triggerTagObjectAvailable = true;
							triggerTagObject = *validObject;
							objectIsUsedAsTag = true;
						}
					}
				}
				
				// search for probe matched is object has no tag match
				if (! objectIsUsedAsTag)
				{
					triggerProbeObject = *validObject;
				
					for (std::vector<std::string>::iterator hltPath = hltPaths.begin();
						(hltPath != hltPaths.end()) && (! triggerProbeObjectAvailable);
						++hltPath)
					{
						for (std::vector<std::string>::iterator probeObjectHltPath = (settings.*GetProbeObjectHltPaths)().begin();
							 (probeObjectHltPath != (settings.*GetProbeObjectHltPaths)().end()) && (! triggerProbeObjectAvailable);
							 ++probeObjectHltPath)
						{
							if (boost::regex_search(*hltPath, boost::regex(*probeObjectHltPath, boost::regex::icase | boost::regex::extended)))
							{
								triggerProbeObjectAvailable = true;
							}
						}
					}
				}
			}
			
			if (triggerTagObjectAvailable || (! (product.*m_triggerTagObjectAvailable)))
			{
				(product.*m_triggerTagObjectAvailable) = triggerTagObjectAvailable;
				(product.*m_triggerProbeObjectAvailable) = triggerProbeObjectAvailable;
				(product.*m_triggerTagObject) = triggerTagObject;
				(product.*m_triggerProbeObject) = triggerProbeObject;
			}
			
			// quit searching if tag and probe are found in same permutation
			if ((product.*m_triggerTagObjectAvailable) && (product.*m_triggerProbeObjectAvailable))
			{
				break;
			}
		}
		while (std::next_permutation(validObjects.begin(), validObjects.end()));
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
