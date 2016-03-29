
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/SafeMap.h"

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
	
	MetSelectorBase(TMet* event_type::*met, std::vector<TMet>* event_type::*mets) :
		ProducerBase<HttTypes>(),
		m_metMember(met),
		m_metsMember(mets)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_pfmet.significance.At(1, 1);
		});
	
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met.significance.At(1, 1);
		});
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		if ((m_metsMember != nullptr) && ((event.*m_metsMember) != nullptr))
		{
			assert(product.m_ptOrderedLeptons.size() > 0);
			
			// create hashes from lepton selection. Any number of leptons is possible 
			std::vector<KLepton*> leptons = product.m_ptOrderedLeptons;
			std::vector<unsigned int> hashes;
			do
			{
				unsigned int hash = 0;
				for (std::vector<KLepton*>::iterator lepton = leptons.begin(); lepton != leptons.end(); ++lepton)
				{
					hash = bitShift(hash, 3);
					hash = hash ^ SafeMap::GetWithDefault(
							product.m_originalLeptons,
							static_cast<const KLepton*>(*lepton),
							static_cast<const KLepton*>(*lepton)
					)->getHash();
				}
				hashes.push_back(hash);
			}
			while (std::prev_permutation(leptons.begin(), leptons.end(), [](KLepton const* lepton1, KLepton const* lepton2) -> bool { return lepton1->p4.Pt() < lepton2->p4.Pt(); }));
			
			for (typename std::vector<TMet>::iterator met = (event.*m_metsMember)->begin(); met != (event.*m_metsMember)->end(); ++met)
			{
				if (std::find(hashes.begin(), hashes.end(), met->leptonSelectionHash)!= hashes.end())
				{
					product.m_metUncorr = &(*met);
					break;
				} 
			}
			
			assert(product.m_metUncorr != nullptr);
			// If this assertion fails, one might have to consider running the MetSelector before this producer
			// in order to have the (PF) MET as a fallback solution
			
			// Copy the MET object, for possible future corrections
			product.m_met = *(product.m_metUncorr);
		}
		else if ((m_metMember != nullptr) && ((event.*m_metMember) != nullptr))
		{
			product.m_metUncorr = (event.*m_metMember);
			product.m_pfmetUncorr = (event.*m_metMember);
			
			// Copy the MET object, for possible future corrections
			product.m_met = *(product.m_metUncorr);
			product.m_pfmet = *(product.m_pfmetUncorr);
		}
		else
		{
			assert(((m_metsMember != nullptr) && ((event.*m_metsMember) != nullptr)) ||
			       ((m_metMember != nullptr) && ((event.*m_metMember) != nullptr)));
		}
	}
	

protected:
	TMet* event_type::*m_metMember;
	std::vector<TMet>* event_type::*m_metsMember;
};



/**
   \brief Producer for (PF) MET
*/
class MetSelector: public MetSelectorBase<KMET>
{
public:
	MetSelector();
	virtual std::string GetProducerId() const override;
};


/**
   \brief Producer for Puppi MET
*/
class MetSelectorPuppi: public MetSelectorBase<KMET>
{
public:
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
	MetSelectorPuppi();
	virtual std::string GetProducerId() const override;
};

/**
   \brief Producer for MVAMET (TT channel)
*/
class MvaMetTTSelector: public MetSelectorBase<KMET>
{
public:
	MvaMetTTSelector();
	virtual std::string GetProducerId() const override;
};



/**
   \brief Producer for MVAMET (MT channel)
*/
class MvaMetMTSelector: public MetSelectorBase<KMET>
{
public:
	MvaMetMTSelector();
	virtual std::string GetProducerId() const override;
};



/**
   \brief Producer for MVAMET (ET channel)
*/
class MvaMetETSelector: public MetSelectorBase<KMET>
{
public:
	MvaMetETSelector();
	virtual std::string GetProducerId() const override;
};



/**
   \brief Producer for MVAMET (EM channel)
*/
class MvaMetEMSelector: public MetSelectorBase<KMET>
{
public:
	MvaMetEMSelector();
	virtual std::string GetProducerId() const override;
};

/**
   \brief Producer for MVAMET (EM channel)
*/
class MvaMetSelector: public MetSelectorBase<KMET>
{
public:
	MvaMetSelector();
	virtual std::string GetProducerId() const override;
};
