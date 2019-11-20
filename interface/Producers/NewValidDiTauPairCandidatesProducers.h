
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
class NewValidDiTauPairCandidatesProducerBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	NewValidDiTauPairCandidatesProducerBase(std::vector<TLepton1*> product_type::*validLeptonsMember1,
	                                     std::vector<TLepton2*> product_type::*validLeptonsMember2) :
		ProducerBase<HttTypes>(),
		m_validLeptonsMember1(validLeptonsMember1),
		m_validLeptonsMember2(validLeptonsMember2)
	{
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);

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

		m_lepton1UpperEtaCutsByIndex = Utility::ParseMapTypes<size_t, float>(
				Utility::ParseVectorToMap(settings.GetDiTauPairLepton1UpperEtaCuts()), m_lepton1UpperEtaCutsByHltName
		);
		m_lepton2UpperEtaCutsByIndex = Utility::ParseMapTypes<size_t, float>(
				Utility::ParseVectorToMap(settings.GetDiTauPairLepton2UpperEtaCuts()), m_lepton2UpperEtaCutsByHltName
		);

		std::vector<std::string> lepton1CheckTriggerMatchByHltName = settings.GetCheckLepton1TriggerMatch();
		std::vector<std::string> lepton2CheckTriggerMatchByHltName = settings.GetCheckLepton2TriggerMatch();

		m_hltFiredBranchNames = Utility::ParseVectorToMap(settings.GetHLTBranchNames());

		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nDiTauPairCandidates", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<int>(product.m_validDiTauPairCandidates.size());
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata,"nAllDiTauPairCandidates", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<int>(product.m_validDiTauPairCandidates.size()+product.m_invalidDiTauPairCandidates.size());
		});

		// debug output in initialization step
		LOG(DEBUG) << "Settings for Lepton 1 Pt Cuts: ";
		for(unsigned int i = 0; i < settings.GetDiTauPairLepton1LowerPtCuts().size(); i++)
		{
			LOG(DEBUG) << settings.GetDiTauPairLepton1LowerPtCuts().at(i);
		}
		LOG(DEBUG) << "Settings for Lepton 2 Pt Cuts: ";
		for(unsigned int i = 0; i < settings.GetDiTauPairLepton2LowerPtCuts().size(); i++)
		{
			LOG(DEBUG) << settings.GetDiTauPairLepton2LowerPtCuts().at(i);
		}
		LOG(DEBUG) << "Amount of lepton 1 Pt Cuts by Hlt Name: " << m_lepton1LowerPtCutsByHltName.size();
		LOG(DEBUG) << "Amount of lepton 2 Pt Cuts by Hlt Name: " << m_lepton2LowerPtCutsByHltName.size();

		for(auto hltNames: m_hltFiredBranchNames)
		{
			std::map<std::string, std::vector<float>> lepton1LowerPtCutsByHltName = m_lepton1LowerPtCutsByHltName;
			std::map<std::string, std::vector<float>> lepton2LowerPtCutsByHltName = m_lepton2LowerPtCutsByHltName;
			std::map<std::string, std::vector<float>> lepton1UpperEtaCutsByHltName = m_lepton1UpperEtaCutsByHltName;
			std::map<std::string, std::vector<float>> lepton2UpperEtaCutsByHltName = m_lepton2UpperEtaCutsByHltName;
			bool lepton1CheckL1Match = settings.GetCheckL1MatchForDiTauPairLepton1();
			bool lepton2CheckL1Match = settings.GetCheckL1MatchForDiTauPairLepton2();
			LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, hltNames.first, [lepton1CheckL1Match, lepton2CheckL1Match, lepton1CheckTriggerMatchByHltName, lepton2CheckTriggerMatchByHltName, hltNames, lepton1LowerPtCutsByHltName, lepton2LowerPtCutsByHltName, lepton1UpperEtaCutsByHltName, lepton2UpperEtaCutsByHltName](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
			{
				bool diTauPairFiredTrigger = false;
				LOG(DEBUG) << "Beginning of lambda function for " << hltNames.first + "hehehyehe";
				bool checkLep1 = std::find(lepton1CheckTriggerMatchByHltName.begin(), lepton1CheckTriggerMatchByHltName.end(), hltNames.first) != lepton1CheckTriggerMatchByHltName.end();
				bool checkLep2 = std::find(lepton2CheckTriggerMatchByHltName.begin(), lepton2CheckTriggerMatchByHltName.end(), hltNames.first) != lepton2CheckTriggerMatchByHltName.end();
				for (auto hltName: hltNames.second)
				{
					bool hltFired1 = false;
					bool hltFired2 = false;
					if (checkLep1)
					{
						LOG(DEBUG) << "Checking trigger object matching for lepton 1";
						if (product.m_detailedTriggerMatchedLeptons.find(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).first)) != product.m_detailedTriggerMatchedLeptons.end())
						{
							auto trigger1 = product.m_detailedTriggerMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).first));
							for (auto hlts: (*trigger1))
							{
								if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
								{
									for (auto matchedObjects: hlts.second)
									{
										if (matchedObjects.second.size() > 0) hltFired1 = true;
									}
								}
							}
							LOG(DEBUG) << "Found trigger for the lepton 1? " << hltFired1;
							// passing kinematic cuts for trigger
							if (lepton1LowerPtCutsByHltName.find(hltName) != lepton1LowerPtCutsByHltName.end())
							{
								hltFired1 = hltFired1 && (product.m_validDiTauPairCandidates.at(0).first->p4.Pt() > *std::max_element(lepton1LowerPtCutsByHltName.at(hltName).begin(), lepton1LowerPtCutsByHltName.at(hltName).end()));
								LOG(DEBUG) << "lepton 1 Pt: " << product.m_validDiTauPairCandidates.at(0).first->p4.Pt() << " threshold: " << *std::max_element(lepton1LowerPtCutsByHltName.at(hltName).begin(), lepton1LowerPtCutsByHltName.at(hltName).end());
							}
							if (lepton1UpperEtaCutsByHltName.find(hltName) != lepton1UpperEtaCutsByHltName.end())
							{
								hltFired1 = hltFired1 && (std::abs(product.m_validDiTauPairCandidates.at(0).first->p4.Eta()) < *std::min_element(lepton1UpperEtaCutsByHltName.at(hltName).begin(), lepton1UpperEtaCutsByHltName.at(hltName).end()));
								LOG(DEBUG) << "lepton 1 |Eta|: " << std::abs(product.m_validDiTauPairCandidates.at(0).first->p4.Eta()) << " threshold: " << *std::min_element(lepton1UpperEtaCutsByHltName.at(hltName).begin(), lepton1UpperEtaCutsByHltName.at(hltName).end());
							}
							LOG(DEBUG) << "lepton 1 passes also kinematic cuts? " << hltFired1;
							if(lepton1CheckL1Match)
							{
								if(product.m_detailedL1MatchedLeptons.find(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).first)) !=  product.m_detailedL1MatchedLeptons.end())
								{
									auto l1_1 = product.m_detailedL1MatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).first));
									for (auto hlts: l1_1)
									{
										if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
										{
											hltFired1 = hltFired1 && hlts.second;
										}
									}
								}
								LOG(DEBUG) << "lepton 1 passes also l1 matching? " << hltFired1;
							}
						}
					}
					else hltFired1 = true;
					if (checkLep2)
					{
						LOG(DEBUG) << "Checking trigger object matching for lepton 2";
						if (product.m_detailedTriggerMatchedLeptons.find(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).second)) != product.m_detailedTriggerMatchedLeptons.end())
						{
							auto trigger2 = product.m_detailedTriggerMatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).second));
							for (auto hlts: (*trigger2))
							{
								if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
								{
									for (auto matchedObjects: hlts.second)
									{
										if (matchedObjects.second.size() > 0) hltFired2 = true;
									}
								}
							}
							LOG(DEBUG) << "Found trigger for the lepton 2? " << hltFired2;
							// passing kinematic cuts for trigger
							if (lepton2LowerPtCutsByHltName.find(hltName) != lepton2LowerPtCutsByHltName.end())
							{
								hltFired2 = hltFired2 && (product.m_validDiTauPairCandidates.at(0).second->p4.Pt() > *std::max_element(lepton2LowerPtCutsByHltName.at(hltName).begin(), lepton2LowerPtCutsByHltName.at(hltName).end()));
								LOG(DEBUG) << "lepton 2 Pt: " << product.m_validDiTauPairCandidates.at(0).second->p4.Pt() << " threshold: " << *std::max_element(lepton2LowerPtCutsByHltName.at(hltName).begin(), lepton2LowerPtCutsByHltName.at(hltName).end());
							}
							if (lepton2UpperEtaCutsByHltName.find(hltName) != lepton2UpperEtaCutsByHltName.end())
							{
								hltFired2 = hltFired2 && (std::abs(product.m_validDiTauPairCandidates.at(0).second->p4.Eta()) < *std::min_element(lepton2UpperEtaCutsByHltName.at(hltName).begin(), lepton2UpperEtaCutsByHltName.at(hltName).end()));
								LOG(DEBUG) << "lepton 2 |Eta|: " << std::abs(product.m_validDiTauPairCandidates.at(0).second->p4.Eta()) << " threshold: " << *std::min_element(lepton2UpperEtaCutsByHltName.at(hltName).begin(), lepton2UpperEtaCutsByHltName.at(hltName).end());
							}
							LOG(DEBUG) << "lepton 2 passes also kinematic cuts? " << hltFired2;
							if(lepton2CheckL1Match)
							{
								if(product.m_detailedL1MatchedLeptons.find(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).second)) !=  product.m_detailedL1MatchedLeptons.end())
								{
									auto l1_2 = product.m_detailedL1MatchedLeptons.at(static_cast<KLepton*>(product.m_validDiTauPairCandidates.at(0).second));
									for (auto hlts: l1_2)
									{
										if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
										{
											hltFired2 = hltFired2 && hlts.second;
										}
									}
								}
								LOG(DEBUG) << "lepton 2 passes also l1 matching? " << hltFired2;
							}
						}
					}
					else hltFired2 = true;
					bool hltFired = hltFired1 && hltFired2;
					diTauPairFiredTrigger = diTauPairFiredTrigger || hltFired;
				}
				LOG(DEBUG) << "Tau pair with valid trigger match? " << diTauPairFiredTrigger;
				return diTauPairFiredTrigger;
			});
		}
	}

	virtual void Produce(event_type const& event, product_type & product,
											 setting_type const& settings, metadata_type const& metadata) const override
	{
		product.m_validDiTauPairCandidates.clear();
		LOG(DEBUG) << this->GetProducerId() << " Produce: -----START-----";
		LOG(DEBUG) << "Processing run:lumi:event " << event.m_eventInfo->nRun << ":" << event.m_eventInfo->nLumi << ":" << event.m_eventInfo->nEvent;
		LOG(DEBUG) << "Size of valid candidates for lepton 1: " << (product.*m_validLeptonsMember1).size();
		LOG(DEBUG) << "Size of valid candidates for lepton 2: " << (product.*m_validLeptonsMember2).size();

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

				// delta R cut
				validDiTauPair = validDiTauPair && ((settings.GetDiTauPairMinDeltaRCut() < 0.0) || (diTauPair.GetDeltaR() > static_cast<double>(settings.GetDiTauPairMinDeltaRCut())));
				LOG(DEBUG) << "Pair passed the delta R cut of " << settings.GetDiTauPairMinDeltaRCut() << "? " << validDiTauPair <<  ", because computed value is " << diTauPair.GetDeltaR();

				// check possible additional criteria from subclasses
				validDiTauPair = validDiTauPair && AdditionalCriteria(diTauPair, event, product, settings, metadata);
				LOG(DEBUG) << "Pair passed additional Criteria? " << validDiTauPair;
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
		// another debug output at the end: which pair is selected?

		// Loop over valid diTauPairs with deltaR:
		for(unsigned int i=0;i<product.m_validDiTauPairCandidates.size();i++)
		{
				LOG(DEBUG) << "Delta R separation within valid Pair:" << product.m_validDiTauPairCandidates.at(i).GetDeltaR();
		}
		if(product.m_validDiTauPairCandidates.size()>0)
		{
			LOG(DEBUG) << "First Tau Candidate in first pair: " << product.m_validDiTauPairCandidates.at(0).first->p4;
			LOG(DEBUG) << "Second Tau Candidate in first pair: " << product.m_validDiTauPairCandidates.at(0).second->p4;
		}
		LOG(DEBUG) << this->GetProducerId() << " Produce: -----END-----";
	}


protected:
	// Can be overwritten for special use cases
	virtual bool AdditionalCriteria(DiTauPair const& diTauPair, event_type const& event,
																	product_type& product, setting_type const& settings, metadata_type const& metadata) const
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

	std::map<size_t, std::vector<float> > m_lepton1UpperEtaCutsByIndex;
	std::map<std::string, std::vector<float> > m_lepton1UpperEtaCutsByHltName;
	std::map<size_t, std::vector<float> > m_lepton2UpperEtaCutsByIndex;
	std::map<std::string, std::vector<float> > m_lepton2UpperEtaCutsByHltName;

	std::map<std::string, std::vector<std::string> > m_hltFiredBranchNames;

};


class NewValidTTPairCandidatesProducer: public NewValidDiTauPairCandidatesProducerBase<KTau, KTau>
{
public:
	NewValidTTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class NewValidMTPairCandidatesProducer: public NewValidDiTauPairCandidatesProducerBase<KMuon, KTau>
{
public:
	NewValidMTPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class NewValidETPairCandidatesProducer: public NewValidDiTauPairCandidatesProducerBase<KElectron, KTau>
{
public:
	NewValidETPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class NewValidEMPairCandidatesProducer: public NewValidDiTauPairCandidatesProducerBase<KMuon, KElectron>
{
public:
	NewValidEMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class NewValidMMPairCandidatesProducer: public NewValidDiTauPairCandidatesProducerBase<KMuon, KMuon>
{
public:
	NewValidMMPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};

class NewValidEEPairCandidatesProducer: public NewValidDiTauPairCandidatesProducerBase<KElectron, KElectron>
{
public:
	NewValidEEPairCandidatesProducer();
	virtual std::string GetProducerId() const override;
};
