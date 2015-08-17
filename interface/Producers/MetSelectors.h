
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producer for the MET
*/


template<class TMet>
class MetSelectorBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	MetSelectorBase(TMet* event_type::*met) :
		ProducerBase<HttTypes>(),
		m_metMember(met)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(1, 1);
		});
	
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(1, 1);
		});
	}
	

protected:
	TMet* event_type::*m_metMember;
};



/**
   \brief Producer for MET (from event.m_met)
*/
class MetSelector: public MetSelectorBase<KMET>
{
public:
	MetSelector() : MetSelectorBase<KMET>(&HttTypes::event_type::m_met) {};
	
	virtual std::string GetProducerId() const override {
		return "MetSelector";
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		assert((event.*m_metMember));
		product.m_met = (event.*m_metMember);
	}
};

template<class TMet>
class MvaMetSelectorBase : public MetSelectorBase<KMETs>
{
public:
	MvaMetSelectorBase(TMet* event_type::*met) : MetSelectorBase<KMETs>(met) {};

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		//make sure product.m_met is already filled in case no MVA MET can be identified
		assert(product.m_met);

		// create hashes from lepton selection. Any number of leptons is possible 
		std::vector<KLepton*> leptons = product.m_ptOrderedLeptons;
		std::vector<int> hashes;
		do{
			int hash = 0;
			for(size_t i = 0; i < leptons.size(); ++i)
				hash = hash ^ leptons[i]->getHash();
			hashes.push_back(hash);
		}while(std::prev_permutation(leptons.begin(), leptons.end()));

		
		for(size_t i = 0; i < (event.*m_metMember)->size(); ++i)
		{
			if(std::find(hashes.begin(), hashes.end(), (event.*m_metMember)->at(i).leptonSelectionHash)!= hashes.end())
			{
				product.m_met = &(event.*m_metMember)->at(i);
				return;
			} 
		}
		LOG_N_TIMES(20, WARNING) << "Could not find MVA MET corresponding to lepton selection! Falling back to PFMet" << std::endl;
	}

};

/**
   \brief Producer for MVAMET (TT channel)
*/
class MvaMetTTSelector: public MvaMetSelectorBase<KMETs>
{
public:
	MvaMetTTSelector() : MvaMetSelectorBase(&HttTypes::event_type::m_mvaMetTT) {};
	
	virtual std::string GetProducerId() const override {
		return "MvaMetTTSelector";
	}
};



/**
   \brief Producer for MVAMET (MT channel)
*/
class MvaMetMTSelector: public MvaMetSelectorBase<KMETs>
{
public:
	MvaMetMTSelector() : MvaMetSelectorBase(&HttTypes::event_type::m_mvaMetMT) {};
	
	virtual std::string GetProducerId() const override {
		return "MvaMetMTSelector";
	}
};



/**
   \brief Producer for MVAMET (ET channel)
*/
class MvaMetETSelector: public MvaMetSelectorBase<KMETs>
{
public:
	MvaMetETSelector() : MvaMetSelectorBase(&HttTypes::event_type::m_mvaMetET) {};
	
	virtual std::string GetProducerId() const override {
		return "MvaMetETSelector";
	}
};



/**
   \brief Producer for MVAMET (EM channel)
*/
class MvaMetEMSelector: public MvaMetSelectorBase<KMETs>
{
public:
	MvaMetEMSelector() : MvaMetSelectorBase(&HttTypes::event_type::m_mvaMetEM) {};
	
	virtual std::string GetProducerId() const override {
		return "MvaMetEMSelector";
	}
};

