
#pragma once

#include <algorithm>
#include <utility>

#include <boost/regex.hpp>

#include <Math/VectorUtil.h>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/KappaAnalysis/interface/Producers/TriggerMatchingProducers.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"



template<class TTag, class TProbe>
class TriggerTagAndProbeProducerBase: public ProducerBase<HttTypes>
{
public:

	TriggerTagAndProbeProducerBase(
			std::vector<TTag*> product_type::*tagObjectsMember,
			std::vector<TProbe*> product_type::*probeObjectsMember,
			std::map<TTag*, std::map<std::string, std::map<std::string, std::vector<KLV*> > > > product_type::*detailedTriggerMatchedTagObjectsMember,
			std::map<TProbe*, std::map<std::string, std::map<std::string, std::vector<KLV*> > > > product_type::*detailedTriggerMatchedProbeObjectsMember,
			std::vector<std::string>& (setting_type::*GetTagObjectHltPaths)(void) const,
			std::vector<std::string>& (setting_type::*GetProbeObjectHltPaths)(void) const,
			//std::vector<std::string>& (setting_type::*GetTagObjectTriggerFilterNames)(void) const,
			//std::vector<std::string>& (setting_type::*GetProbeObjectTriggerFilterNames)(void) const,
			std::vector<std::pair<TTag*, TProbe*> > product_type::*triggerTagProbeObjectPairsMember,
			std::vector<std::pair<bool, bool> > product_type::*triggerTagProbeObjectMatchedPairsMember
	) :
		ProducerBase<HttTypes>(),
		m_tagObjectsMember(tagObjectsMember),
		m_probeObjectsMember(probeObjectsMember),
		m_detailedTriggerMatchedTagObjectsMember(detailedTriggerMatchedTagObjectsMember),
		m_detailedTriggerMatchedProbeObjectsMember(detailedTriggerMatchedProbeObjectsMember),
		GetTagObjectHltPaths(GetTagObjectHltPaths),
		GetProbeObjectHltPaths(GetProbeObjectHltPaths),
		//GetTagObjectTriggerFilterNames(GetTagObjectTriggerFilterNames),
		//GetProbeObjectTriggerFilterNames(GetProbeObjectTriggerFilterNames),
		m_triggerTagProbeObjectPairsMember(triggerTagProbeObjectPairsMember),
		m_triggerTagProbeObjectMatchedPairsMember(triggerTagProbeObjectMatchedPairsMember)
	{
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
	}
	
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override
	{
		assert((product.*m_tagObjectsMember).size() > 0);
		assert((product.*m_probeObjectsMember).size() > 0);
		
		for (typename std::vector<TTag*>::iterator tagObject = (product.*m_tagObjectsMember).begin();
		     tagObject != (product.*m_tagObjectsMember).end(); ++tagObject)
		{
			std::vector<std::string> tagFiredHltPaths = TriggerMatchingProducerBase<TObject>::GetHltNamesWhereAllFiltersMatched(SafeMap::GetWithDefault(
					(product.*m_detailedTriggerMatchedTagObjectsMember),
					(*tagObject),
					std::map<std::string, std::map<std::string, std::vector<KLV*> > >()
			));
			
			bool matchedTagObject = false;
			for (std::vector<std::string>::iterator tagFiredHltPath = tagFiredHltPaths.begin();
				 tagFiredHltPath != tagFiredHltPaths.end(); ++tagFiredHltPath)
			{
				for (std::vector<std::string>::iterator tagObjectHltPath = (settings.*GetTagObjectHltPaths)().begin();
					 tagObjectHltPath != (settings.*GetTagObjectHltPaths)().end(); ++tagObjectHltPath)
				{
					if (boost::regex_search(*tagFiredHltPath, boost::regex(*tagObjectHltPath, boost::regex::icase | boost::regex::extended)))
					{
						matchedTagObject = true;
						break;
					}
				}
			}
			
			for (typename std::vector<TProbe*>::iterator probeObject = (product.*m_probeObjectsMember).begin();
			     probeObject != (product.*m_probeObjectsMember).end(); ++probeObject)
			{
				if ((static_cast<void*>(*tagObject) != static_cast<void*>(*probeObject)) &&
				    ROOT::Math::VectorUtil::DeltaR((*tagObject)->p4, (*probeObject)->p4) > settings.GetDiTauPairMinDeltaRCut())
				{
					std::vector<std::string> probeFiredHltPaths = TriggerMatchingProducerBase<TObject>::GetHltNamesWhereAllFiltersMatched(SafeMap::GetWithDefault(
							(product.*m_detailedTriggerMatchedProbeObjectsMember),
							(*probeObject),
							std::map<std::string, std::map<std::string, std::vector<KLV*> > >()
					));
			
					bool matchedProbeObject = false;
					for (std::vector<std::string>::iterator probeFiredHltPath = probeFiredHltPaths.begin();
						 probeFiredHltPath != probeFiredHltPaths.end(); ++probeFiredHltPath)
					{
						for (std::vector<std::string>::iterator probeObjectHltPath = (settings.*GetProbeObjectHltPaths)().begin();
							 probeObjectHltPath != (settings.*GetProbeObjectHltPaths)().end(); ++probeObjectHltPath)
						{
							if (boost::regex_search(*probeFiredHltPath, boost::regex(*probeObjectHltPath, boost::regex::icase | boost::regex::extended)))
							{
								matchedProbeObject = true;
								break;
							}
						}
					}
				
					(product.*m_triggerTagProbeObjectPairsMember).push_back(std::pair<TTag*, TProbe*>(*tagObject, *probeObject));
					(product.*m_triggerTagProbeObjectMatchedPairsMember).push_back(std::pair<bool, bool>(matchedTagObject, matchedProbeObject));
				}
			}
		}
	}


private:
	std::vector<TTag*> product_type::*m_tagObjectsMember;
	std::vector<TProbe*> product_type::*m_probeObjectsMember;
	std::map<TTag*, std::map<std::string, std::map<std::string, std::vector<KLV*> > > > product_type::*m_detailedTriggerMatchedTagObjectsMember;
	std::map<TProbe*, std::map<std::string, std::map<std::string, std::vector<KLV*> > > > product_type::*m_detailedTriggerMatchedProbeObjectsMember;
	std::vector<std::string>& (setting_type::*GetTagObjectHltPaths)(void) const;
	std::vector<std::string>& (setting_type::*GetProbeObjectHltPaths)(void) const;
	//std::vector<std::string>& (setting_type::*GetTagObjectTriggerFilterNames)(void) const;
	//std::vector<std::string>& (setting_type::*GetProbeObjectTriggerFilterNames)(void) const;
	std::vector<std::pair<TTag*, TProbe*> > product_type::*m_triggerTagProbeObjectPairsMember;
	std::vector<std::pair<bool, bool> > product_type::*m_triggerTagProbeObjectMatchedPairsMember;

};



class MMTriggerTagAndProbeProducer: public TriggerTagAndProbeProducerBase<KMuon, KMuon>
{
public:
	MMTriggerTagAndProbeProducer();
	virtual std::string GetProducerId() const override;
};


class EETriggerTagAndProbeProducer: public TriggerTagAndProbeProducerBase<KElectron, KElectron>
{
public:
	EETriggerTagAndProbeProducer();
	virtual std::string GetProducerId() const override;
};


class MTTriggerTagAndProbeProducer: public TriggerTagAndProbeProducerBase<KMuon, KTau>
{
public:
	MTTriggerTagAndProbeProducer();
	virtual std::string GetProducerId() const override;
};


class ETTriggerTagAndProbeProducer: public TriggerTagAndProbeProducerBase<KElectron, KTau>
{
public:
	ETTriggerTagAndProbeProducer();
	virtual std::string GetProducerId() const override;
};

