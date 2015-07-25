
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producers for candidates of di-tau pairs
*/


template<class TLepton1, class TLepton2>
class ValidDiTauPairCandidatesProducerBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	ValidDiTauPairCandidatesProducerBase(std::vector<TLepton1*> product_type::*validLeptonsMember1,
	                                std::vector<TLepton2*> product_type::*validLeptonsMember2) :
		ProducerBase<HttTypes>(),
		m_validLeptonsMember1(validLeptonsMember1),
		m_validLeptonsMember2(validLeptonsMember2)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiTauPairCandidates", [](event_type const& event, product_type const& product)
		{
			return static_cast<int>(product.m_validDiTauPairCandidates.size());
		});
	}
	
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		product.m_validDiTauPairCandidates.clear();
		
		// build pairs for all combinations
		for (typename std::vector<TLepton1*>::iterator lepton1 = (product.*m_validLeptonsMember1).begin();
		     lepton1 != (product.*m_validLeptonsMember1).end(); ++lepton1)
		{
			for (typename std::vector<TLepton2*>::iterator lepton2 = (product.*m_validLeptonsMember2).begin();
			     lepton2 != (product.*m_validLeptonsMember2).end(); ++lepton2)
			{
				DiTauPair diTauPair(*lepton1, *lepton2);
				
				// pair selections
				bool validDiTauPair = true;
				
				// check possible additional criteria from subclasses
				validDiTauPair = validDiTauPair && AdditionalCriteria(diTauPair, event, product, settings);
			
				if (validDiTauPair)
				{
					product.m_validDiTauPairCandidates.push_back(diTauPair);
				}
				else
				{
					product.m_invalidDiTauPairCandidates.push_back(diTauPair);
				}
			}
		}
		
		// sort pairs
		std::sort(product.m_validDiTauPairCandidates.begin(), product.m_validDiTauPairCandidates.end(),
		          DiTauPairIsoPtComparator(&(product.m_leptonIsolationOverPt)));
		std::sort(product.m_invalidDiTauPairCandidates.begin(), product.m_invalidDiTauPairCandidates.end(),
		          DiTauPairIsoPtComparator(&(product.m_leptonIsolationOverPt)));
	}
	

protected:
	// Can be overwritten for special use cases
	virtual bool AdditionalCriteria(DiTauPair const& diTauPair, event_type const& event,
	                                product_type& product, setting_type const& settings) const
	{
		bool validDiTauPair = true;
		return validDiTauPair;
	}


private:
	std::vector<TLepton1*> product_type::*m_validLeptonsMember1;
	std::vector<TLepton2*> product_type::*m_validLeptonsMember2;

};


class ValidTTPairCandidatesProducer: public ValidDiTauPairCandidatesProducerBase<KTau, KTau>
{
public:
	ValidTTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class ValidMTPairCandidatesProducer: public ValidDiTauPairCandidatesProducerBase<KMuon, KTau>
{
public:
	ValidMTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class ValidETPairCandidatesProducer: public ValidDiTauPairCandidatesProducerBase<KElectron, KTau>
{
public:
	ValidETPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class ValidEMPairCandidatesProducer: public ValidDiTauPairCandidatesProducerBase<KMuon, KElectron>
{
public:
	ValidEMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class ValidMMPairCandidatesProducer: public ValidDiTauPairCandidatesProducerBase<KMuon, KMuon>
{
public:
	ValidMMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class ValidEEPairCandidatesProducer: public ValidDiTauPairCandidatesProducerBase<KElectron, KElectron>
{
public:
	ValidEEPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

