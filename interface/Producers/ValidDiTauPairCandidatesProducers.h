
#pragma once

#include <boost/regex.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/Utility.h"

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
		
		// configurations possible:
		// "cut" --> applied to all pairs
		// "<index in setting HltPaths>:<cut>" --> applied to pairs that fired and matched ONLY the indexed HLT path
		// "<HLT path regex>:<cut>" --> applied to pairs that fired and matched ONLY the given HLT path
		m_lepton1LowerPtCutsByIndex = Utility::ParseMapTypes<size_t, float>(
				Utility::ParseVectorToMap(settings.GetDiTauPairLepton1LowerPtCuts()), m_lepton1LowerPtCutsByHltName
		);
		m_lepton2LowerPtCutsByIndex = Utility::ParseMapTypes<size_t, float>(
				Utility::ParseVectorToMap(settings.GetDiTauPairLepton2LowerPtCuts()), m_lepton2LowerPtCutsByHltName
		);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiTauPairCandidates", [](event_type const& event, product_type const& product)
		{
			return static_cast<int>(product.m_validDiTauPairCandidates.size());
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nAllDiTauPairCandidates", [](event_type const& event, product_type const& product)
		{
			return static_cast<int>(product.m_validDiTauPairCandidates.size()+product.m_invalidDiTauPairCandidates.size());
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
				
				// OS charge requirement
				//validDiTauPair = validDiTauPair && diTauPair.IsOppositelyCharged();
				
				// delta R cut
				validDiTauPair = validDiTauPair && ((settings.GetDiTauPairMinDeltaRCut() < 0.0) || (diTauPair.GetDeltaR() > static_cast<double>(settings.GetDiTauPairMinDeltaRCut())));
				
				// require matchings with the same triggers
				if (!settings.GetDiTauPairNoHLT())
				{
					std::vector<std::string> commonHltPaths = diTauPair.GetCommonHltPaths(product.m_detailedTriggerMatchedLeptons, settings.GetDiTauPairHltPathsWithoutCommonMatchRequired());
					validDiTauPair = validDiTauPair && (commonHltPaths.size() > 0);
					
					// pt cuts in case one or more HLT paths are matched
					if (validDiTauPair)
					{
						//vector to hold the results for the individual HLTPaths, all results default to true
						std::vector<bool> hltValidDiTauPair(commonHltPaths.size(), true);
						for (std::vector<std::string>::size_type hltPathNumber = 0; hltPathNumber != commonHltPaths.size(); ++hltPathNumber)
						{
							// lepton 1
							for (std::map<size_t, std::vector<float> >::const_iterator lowerPtCutByIndex = m_lepton1LowerPtCutsByIndex.begin();
								lowerPtCutByIndex != m_lepton1LowerPtCutsByIndex.end() && hltValidDiTauPair.at(hltPathNumber); ++lowerPtCutByIndex)
							{
								if ((diTauPair.first->p4.Pt() <= *std::max_element(lowerPtCutByIndex->second.begin(), lowerPtCutByIndex->second.end())) &&
									boost::regex_search(commonHltPaths.at(hltPathNumber), boost::regex(settings.GetHltPaths().at(lowerPtCutByIndex->first), boost::regex::icase | boost::regex::extended)))
								{
									hltValidDiTauPair.at(hltPathNumber) = false;
								}
							}
						
							// lepton 1
							for (std::map<std::string, std::vector<float> >::const_iterator lowerPtCutByHltName = m_lepton1LowerPtCutsByHltName.begin();
								lowerPtCutByHltName != m_lepton1LowerPtCutsByHltName.end() && hltValidDiTauPair.at(hltPathNumber); ++lowerPtCutByHltName)
							{
								if ((diTauPair.first->p4.Pt() <= *std::max_element(lowerPtCutByHltName->second.begin(), lowerPtCutByHltName->second.end())) &&
									boost::regex_search(commonHltPaths.at(hltPathNumber), boost::regex(lowerPtCutByHltName->first, boost::regex::icase | boost::regex::extended)))
								{
									hltValidDiTauPair.at(hltPathNumber) = false;
								}
							}
						
							// lepton 2
							for (std::map<size_t, std::vector<float> >::const_iterator lowerPtCutByIndex = m_lepton2LowerPtCutsByIndex.begin();
								lowerPtCutByIndex != m_lepton2LowerPtCutsByIndex.end() && hltValidDiTauPair.at(hltPathNumber); ++lowerPtCutByIndex)
							{
								if ((diTauPair.second->p4.Pt() <= *std::max_element(lowerPtCutByIndex->second.begin(), lowerPtCutByIndex->second.end())) &&
									boost::regex_search(commonHltPaths.at(hltPathNumber), boost::regex(settings.GetHltPaths().at(lowerPtCutByIndex->first), boost::regex::icase | boost::regex::extended)))
								{
									hltValidDiTauPair.at(hltPathNumber) = false;
								}
							}
				
							// lepton 2
							for (std::map<std::string, std::vector<float> >::const_iterator lowerPtCutByHltName = m_lepton2LowerPtCutsByHltName.begin();
							lowerPtCutByHltName != m_lepton2LowerPtCutsByHltName.end() && hltValidDiTauPair.at(hltPathNumber); ++lowerPtCutByHltName)
							{
								if ((diTauPair.second->p4.Pt() <= *std::max_element(lowerPtCutByHltName->second.begin(), lowerPtCutByHltName->second.end())) &&
									boost::regex_search(commonHltPaths.at(hltPathNumber), boost::regex(lowerPtCutByHltName->first, boost::regex::icase | boost::regex::extended)))
								{
									hltValidDiTauPair.at(hltPathNumber) = false;
								}
							}
						}
						//default validity of ditaupair to false and set it to true in case it is a valid pair for at least one HLTPath
						validDiTauPair = false;
						for (std::vector<bool>::const_iterator hltPathResult = hltValidDiTauPair.begin(); hltPathResult != hltValidDiTauPair.end(); ++hltPathResult)
						{
							if(*hltPathResult)
							{
								validDiTauPair = true;
								break;
							}
						}
                        if (settings.GetRequireFirstTriggering())
                        {
                            bool hltFired = false;
                            auto trigger = product.m_detailedTriggerMatchedLeptons[diTauPair.first];
                            for (auto hltName : settings.GetHltPaths())
                            {
                                for (auto hlts: (*trigger))
                                {
                                    if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                    {
                                        for (auto matchedObjects: hlts.second)
                                        {
                                            if (matchedObjects.second.size() > 0) hltFired = true;
                                        }
                                    }
                                }
                            }
                            validDiTauPair = validDiTauPair && hltFired;
                            validDiTauPair = validDiTauPair && (diTauPair.first->p4.Pt() >= diTauPair.second->p4.Pt());
                        }

					}
				}
				else // will hopefully become obsolete towards the end of 2016 when the trigger is included in simulation
				{
					// this only gives sensible results for single-lepton triggers. for double-lepton or cross triggers please apply cuts at plotting level
					if (validDiTauPair)
					{
						// lepton 1
						for (std::map<size_t, std::vector<float> >::const_iterator lowerPtCutByIndex = m_lepton1LowerPtCutsByIndex.begin();
							lowerPtCutByIndex != m_lepton1LowerPtCutsByIndex.end(); ++lowerPtCutByIndex)
						{
							if (diTauPair.first->p4.Pt() <= *std::max_element(lowerPtCutByIndex->second.begin(), lowerPtCutByIndex->second.end()))
							{
								validDiTauPair = false;
							}
						}

						// lepton 1
						for (std::map<std::string, std::vector<float> >::const_iterator lowerPtCutByHltName = m_lepton1LowerPtCutsByHltName.begin();
							lowerPtCutByHltName != m_lepton1LowerPtCutsByHltName.end(); ++lowerPtCutByHltName)
						{
							if (diTauPair.first->p4.Pt() <= *std::max_element(lowerPtCutByHltName->second.begin(), lowerPtCutByHltName->second.end()))
							{
								validDiTauPair = false;
							}
						}

						// lepton 2
						for (std::map<size_t, std::vector<float> >::const_iterator lowerPtCutByIndex = m_lepton2LowerPtCutsByIndex.begin();
							lowerPtCutByIndex != m_lepton2LowerPtCutsByIndex.end(); ++lowerPtCutByIndex)
						{
							if (diTauPair.second->p4.Pt() <= *std::max_element(lowerPtCutByIndex->second.begin(), lowerPtCutByIndex->second.end()))
							{
								validDiTauPair = false;
							}
						}

						// lepton 2
						for (std::map<std::string, std::vector<float> >::const_iterator lowerPtCutByHltName = m_lepton2LowerPtCutsByHltName.begin();
						lowerPtCutByHltName != m_lepton2LowerPtCutsByHltName.end(); ++lowerPtCutByHltName)
						{
							if (diTauPair.second->p4.Pt() <= *std::max_element(lowerPtCutByHltName->second.begin(), lowerPtCutByHltName->second.end()))
							{
								validDiTauPair = false;
							}
						}
					}
				}
				
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
		          DiTauPairIsoPtComparator(&(product.m_leptonIsolationOverPt), settings.GetDiTauPairIsTauIsoMVA()));
		std::sort(product.m_invalidDiTauPairCandidates.begin(), product.m_invalidDiTauPairCandidates.end(),
		          DiTauPairIsoPtComparator(&(product.m_leptonIsolationOverPt), settings.GetDiTauPairIsTauIsoMVA()));
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

	std::map<size_t, std::vector<float> > m_lepton1LowerPtCutsByIndex;
	std::map<std::string, std::vector<float> > m_lepton1LowerPtCutsByHltName;
	std::map<size_t, std::vector<float> > m_lepton2LowerPtCutsByIndex;
	std::map<std::string, std::vector<float> > m_lepton2LowerPtCutsByHltName;

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

