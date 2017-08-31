
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "boost/functional/hash.hpp"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producer for the MET
*/


template<class TMet>
class MetSelectorBase: public ProducerBase<HttTypes>
{
public:

	MetSelectorBase(TMet* event_type::*met, std::vector<TMet>* event_type::*mets) :
		ProducerBase<HttTypes>(),
		m_metMember(met),
		m_metsMember(mets)
	{
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metSumEt", [](event_type const& event, product_type const& product)
		{
			return product.m_met.sumEt;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metPt", [](event_type const& event, product_type const& product)
		{
			return product.m_met.p4.Pt();
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metPhi", [](event_type const& event, product_type const& product)
		{
			return product.m_met.p4.Phi();
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metCov00", [](event_type const& event, product_type const& product)
		{
			return product.m_met.significance.At(0, 0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metCov01", [](event_type const& event, product_type const& product)
		{
			return product.m_met.significance.At(0, 1);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metCov10", [](event_type const& event, product_type const& product)
		{
			return product.m_met.significance.At(1, 0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metCov11", [](event_type const& event, product_type const& product)
		{
			return product.m_met.significance.At(1, 1);
		});

		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetSumEt", [](event_type const& event, product_type const& product)
		{
			return product.m_pfmet.sumEt;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetPt", [](event_type const& event, product_type const& product)
		{
			return product.m_pfmet.p4.Pt();
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetPhi", [](event_type const& event, product_type const& product)
		{
			return product.m_pfmet.p4.Phi();
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetCov00", [](event_type const& event, product_type const& product)
		{
			return product.m_pfmet.significance.At(0, 0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetCov01", [](event_type const& event, product_type const& product)
		{
			return product.m_pfmet.significance.At(0, 1);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetCov10", [](event_type const& event, product_type const& product)
		{
			return product.m_pfmet.significance.At(1, 0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetCov11", [](event_type const& event, product_type const& product)
		{
			return product.m_pfmet.significance.At(1, 1);
		});
	
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetSumEt", [](event_type const& event, product_type const& product)
		{
			return product.m_mvamet.sumEt;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetPt", [](event_type const& event, product_type const& product)
		{
			return product.m_mvamet.p4.Pt();
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetPhi", [](event_type const& event, product_type const& product)
		{
			return product.m_mvamet.p4.Phi();
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCov00", [](event_type const& event, product_type const& product)
		{
			return product.m_mvamet.significance.At(0, 0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCov01", [](event_type const& event, product_type const& product)
		{
			return product.m_mvamet.significance.At(0, 1);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCov10", [](event_type const& event, product_type const& product)
		{
			return product.m_mvamet.significance.At(1, 0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCov11", [](event_type const& event, product_type const& product)
		{
			return product.m_mvamet.significance.At(1, 1);
		});
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override
	{
		if ((m_metsMember != nullptr) && ((event.*m_metsMember) != nullptr))
		{
			assert(product.m_ptOrderedLeptons.size() > 0);
			
			// create hashes from lepton selection. Any number of leptons is possible 
			std::vector<KLepton*> leptons = product.m_ptOrderedLeptons;
			std::vector<size_t> hashes;
			if (leptons.size() == 2 && (leptons[0]->p4.Pt() < leptons[1]->p4.Pt()))
			{
				do
				{
					size_t hash = 0;
					for (std::vector<KLepton*>::iterator lepton = leptons.begin(); lepton != leptons.end(); ++lepton)
					{
						boost::hash_combine(hash,(*lepton)->internalId);
					}
					hashes.push_back(hash);
				}
				while (std::prev_permutation(leptons.begin(), leptons.end(), [](KLepton const* lepton1, KLepton const* lepton2) -> bool { return lepton1->p4.Pt() < lepton2->p4.Pt(); }));
			}
			else
			{
				// in case both pt's are equal the results of before does not include both permutations.
				// Comupte the hashes for both permutations.
				size_t hash = 0;
				for (std::vector<KLepton*>::iterator lepton = leptons.begin(); lepton != leptons.end(); ++lepton)
				{
					boost::hash_combine(hash,(*lepton)->internalId);
				}
				hashes.push_back(hash);
				// permutate both leptons and calculate the second one
				std::swap(leptons[0],leptons[1]);
				hash = 0;
				for (std::vector<KLepton*>::iterator lepton = leptons.begin(); lepton != leptons.end(); ++lepton)
				{
					boost::hash_combine(hash,(*lepton)->internalId);
				}
				hashes.push_back(hash);
			}

			
			bool foundMvaMet = false;
			for (typename std::vector<TMet>::iterator met = (event.*m_metsMember)->begin(); met != (event.*m_metsMember)->end(); ++met)
			{
				if (std::find(hashes.begin(), hashes.end(), met->leptonSelectionHash)!= hashes.end())
				{
					product.m_mvametUncorr = &(*met);
					foundMvaMet = true;
					break;
				} 
			}
			
			// Make sure we found a corresponding MVAMET, this is to ensure we do not fall back to the PFMet
			assert(foundMvaMet && (product.m_mvametUncorr != nullptr));
			// If this assertion fails, one might have to consider running the MetSelector before this producer
			// in order to have the (PF) MET as a fallback solution
			
			// Copy the MET object, for possible future corrections
			product.m_mvamet = *(product.m_mvametUncorr);
			if (settings.GetChooseMvaMet())
			{
				product.m_metUncorr = product.m_mvametUncorr;
				product.m_met = product.m_mvamet;
			}
		}
		else if ((m_metMember != nullptr) && ((event.*m_metMember) != nullptr))
		{
			product.m_pfmetUncorr = (event.*m_metMember);
			
			// Copy the MET object, for possible future corrections
			product.m_pfmet = *(product.m_pfmetUncorr);
			if (!settings.GetChooseMvaMet())
			{
				product.m_metUncorr = product.m_pfmetUncorr;
				product.m_met = product.m_pfmet;
			}
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
	                     setting_type const& settings, metadata_type const& metadata) const override;
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
