
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producers for candidates of di-tau pairs
*/


template<class TLepton1, class TLepton2>
class DiTauPairCandidatesProducerBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	DiTauPairCandidatesProducerBase(std::vector<TLepton1*> product_type::*validLeptonsMember1,
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
			return static_cast<int>(product.diTauPairCandidates.size());
		});
	}
	
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		product.diTauPairCandidates.clear();
		
		for (typename std::vector<TLepton1*>::iterator lepton1 = (product.*m_validLeptonsMember1).begin();
		     lepton1 != (product.*m_validLeptonsMember1).end(); ++lepton1)
		{
			for (typename std::vector<TLepton2*>::iterator lepton2 = (product.*m_validLeptonsMember2).begin();
			     lepton2 != (product.*m_validLeptonsMember2).end(); ++lepton2)
			{
				product.diTauPairCandidates.push_back(DiTauPair(*lepton1, *lepton2));
			}
		}
		
		std::sort(product.diTauPairCandidates.begin(), product.diTauPairCandidates.end(),
		          DiTauPairIsoPtComparator(&(product.m_leptonIsolationOverPt)));
	}

private:
	std::vector<TLepton1*> product_type::*m_validLeptonsMember1;
	std::vector<TLepton2*> product_type::*m_validLeptonsMember2;

};


class TTPairCandidatesProducer: public DiTauPairCandidatesProducerBase<KTau, KTau>
{
public:
	TTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class MTPairCandidatesProducer: public DiTauPairCandidatesProducerBase<KMuon, KTau>
{
public:
	MTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class ETPairCandidatesProducer: public DiTauPairCandidatesProducerBase<KElectron, KTau>
{
public:
	ETPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class EMPairCandidatesProducer: public DiTauPairCandidatesProducerBase<KMuon, KElectron>
{
public:
	EMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class MMPairCandidatesProducer: public DiTauPairCandidatesProducerBase<KMuon, KMuon>
{
public:
	MMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class EEPairCandidatesProducer: public DiTauPairCandidatesProducerBase<KElectron, KElectron>
{
public:
	EEPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

