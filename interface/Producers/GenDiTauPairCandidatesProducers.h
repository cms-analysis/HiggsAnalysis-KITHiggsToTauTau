
#pragma once

#include <boost/regex.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producers for generator-level di-tau pairs candidates
*/


template<class TGenLepton1, class TGenLepton2>
class GenDiTauPairCandidatesProducerBase: public ProducerBase<HttTypes>
{
public:

	GenDiTauPairCandidatesProducerBase(std::vector<TGenLepton1*> product_type::*genLeptonsMember1,
	                                        std::vector<TGenLepton2*> product_type::*genLeptonsMember2) :
		ProducerBase<HttTypes>(),
		m_genLeptonsMember1(genLeptonsMember1),
		m_genLeptonsMember2(genLeptonsMember2)
	{
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nGenDiTauPairCandidates", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<int>(product.m_genDiTauPairCandidates.size());
		});
	}
	
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override
	{
		product.m_genDiTauPairCandidates.clear();
		
		// build pairs for all combinations
		for (typename std::vector<TGenLepton1*>::iterator lepton1 = (product.*m_genLeptonsMember1).begin();
		     lepton1 != (product.*m_genLeptonsMember1).end(); ++lepton1)
		{
			for (typename std::vector<TGenLepton2*>::iterator lepton2 = (product.*m_genLeptonsMember2).begin();
			     lepton2 != (product.*m_genLeptonsMember2).end(); ++lepton2)
			{
				DiGenTauPair diGenTauPair(*lepton1, *lepton2);
				
				// avoid self-pairs and combinatorics (pair 1-2 = pair 2-1)
				bool pairInVector = false;
				for (std::vector<DiGenTauPair>::iterator pair = product.m_genDiTauPairCandidates.begin();
				     pair != product.m_genDiTauPairCandidates.end() && !pairInVector; ++pair)
				{
					if ((diGenTauPair.first->p4 == (*pair).second->p4) && (diGenTauPair.second->p4 == (*pair).first->p4))
						pairInVector = true;
				}
				if ((diGenTauPair.GetDeltaR() > 0) && !pairInVector)
				{
					product.m_genDiTauPairCandidates.push_back(diGenTauPair);
				}
			}
		}
	}

private:
	std::vector<TGenLepton1*> product_type::*m_genLeptonsMember1;
	std::vector<TGenLepton2*> product_type::*m_genLeptonsMember2;

};


class GenTTPairCandidatesProducer: public GenDiTauPairCandidatesProducerBase<KGenJet, KGenJet>
{
public:
	GenTTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class GenMTPairCandidatesProducer: public GenDiTauPairCandidatesProducerBase<KGenParticle, KGenJet>
{
public:
	GenMTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class GenETPairCandidatesProducer: public GenDiTauPairCandidatesProducerBase<KGenParticle, KGenJet>
{
public:
	GenETPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class GenEMPairCandidatesProducer: public GenDiTauPairCandidatesProducerBase<KGenParticle, KGenParticle>
{
public:
	GenEMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class GenMMPairCandidatesProducer: public GenDiTauPairCandidatesProducerBase<KGenParticle, KGenParticle>
{
public:
	GenMMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class GenEEPairCandidatesProducer: public GenDiTauPairCandidatesProducerBase<KGenParticle, KGenParticle>
{
public:
	GenEEPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};
