
#pragma once

#include <cstdint>
#include <cassert>

#include <boost/algorithm/string/predicate.hpp>

#include <TTree.h>
#include <Math/Vector4D.h>
#include <Math/Vector4Dfwd.h>

#include "Artus/Core/interface/EventBase.h"
#include "Artus/Core/interface/ProductBase.h"
#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Configuration/interface/SettingsBase.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "Kappa/DataFormats/interface/Kappa.h"
#include <boost/regex.hpp>

template<class TTypes>
class TagAndProbeMuonPairConsumer: public ConsumerBase<TTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	typedef typename TTypes::event_type event_type;
	typedef typename TTypes::product_type product_type;
	typedef typename TTypes::setting_type setting_type;
	
	std::string GetConsumerId() const override
	{
		return "TagAndProbeMuonPairConsumer";
	}
	
	void Init(setting_type const& settings) override {
		ConsumerBase<TTypes>::Init(settings);
		
		//fill quantity maps
		FloatQuantities["wt"]=0.0;
		IntQuantities["n_vtx"]=0;
		IntQuantities["run"]=0;
		IntQuantities["lumi"]=0;
		IntQuantities["evt"]=0;
		FloatQuantities["pt_t"]=0.0;
		FloatQuantities["eta_t"]=0.0;
		FloatQuantities["phi_t"]=0.0;
		BoolQuantities["id_t"]=false;
		FloatQuantities["iso_t"]=0.0;
		BoolQuantities["muon_p"]=false;
		BoolQuantities["trk_p"]=false;
		FloatQuantities["pt_p"]=0.0;
		FloatQuantities["eta_p"]=0.0;
		FloatQuantities["phi_p"]=0.0;
		BoolQuantities["id_p"]=false;
		FloatQuantities["iso_p"]=0.0;
		FloatQuantities["m_ll"]=0.0;
		BoolQuantities["trg_t_IsoMu22"]=false;
		BoolQuantities["trg_t_IsoMu22_eta2p1"]=false;
		BoolQuantities["trg_t_IsoMu24"]=false;
		BoolQuantities["trg_t_IsoMu19Tau"]=false;
		BoolQuantities["trg_p_IsoMu22"]=false;
		BoolQuantities["trg_p_IsoTkMu22"]=false;
		BoolQuantities["trg_p_IsoMu22_eta2p1"]=false;
		BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=false;
		BoolQuantities["trg_p_IsoMu24"]=false;
		BoolQuantities["trg_p_IsoTkMu24"]=false;
		BoolQuantities["trg_p_PFTau120"]=false;
		BoolQuantities["trg_p_IsoMu19TauL1"]=false;
		BoolQuantities["trg_p_IsoMu19Tau"]=false;

		// create tree
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree = new TTree("ZmmTP", ("Tree for Pipeline \"" + settings.GetName() + "\"").c_str());

		// create branches
		for (std::vector<std::string>::iterator quantity = settings.GetQuantities().begin();
		     quantity != settings.GetQuantities().end(); ++quantity)
		{
			if(BoolQuantities.find(*quantity) != BoolQuantities.end()){
				m_tree->Branch(quantity->c_str(), &(BoolQuantities[*quantity]), (*quantity + "/O").c_str());
			}else if(IntQuantities.find(*quantity) != IntQuantities.end()){
				m_tree->Branch(quantity->c_str(), &(IntQuantities[*quantity]), (*quantity + "/I").c_str());
			}else if(FloatQuantities.find(*quantity) != FloatQuantities.end()){
				m_tree->Branch(quantity->c_str(), &(FloatQuantities[*quantity]), (*quantity + "/F").c_str());
			}
		}
	}

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings ) override
	{
		ConsumerBase<TTypes>::ProcessFilteredEvent(event, product, settings);

		// calculate values
		bool IsData = settings.GetInputIsData();
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
				TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			for (std::vector<std::string>::iterator quantity = settings.GetQuantities().begin();
					quantity != settings.GetQuantities().end(); ++quantity)
			{
				if(*quantity=="wt"){
					FloatQuantities["wt"]=product.m_weights.at(settings.GetEventWeight());
				}else if(*quantity=="n_vtx"){
					IntQuantities["n_vtx"]=event.m_vertexSummary->nVertices;
				}else if(*quantity=="run"){
					IntQuantities["run"]=event.m_eventInfo->nRun;
				}else if(*quantity=="lumi"){
					IntQuantities["lumi"]=event.m_eventInfo->nLumi;
				}else if(*quantity=="evt"){
					IntQuantities["evt"]=event.m_eventInfo->nEvent;
				}else if(*quantity=="pt_t"){
					FloatQuantities["pt_t"]=TagAndProbePair->first->p4.Pt();
				}else if(*quantity=="eta_t"){
					FloatQuantities["eta_t"]=TagAndProbePair->first->p4.Eta();
				}else if(*quantity=="phi_t"){
					FloatQuantities["phi_t"]=TagAndProbePair->first->p4.Phi();
				}else if(*quantity=="id_t"){
					BoolQuantities["id_t"]=IsMediumMuon2016ShortTerm(TagAndProbePair->first) && std::abs(TagAndProbePair->first->dxy) < 0.045 && std::abs(TagAndProbePair->first->dz) < 0.2;
				}else if(*quantity=="iso_t"){
					double chargedIsolationPtSum = TagAndProbePair->first->sumChargedHadronPtR04;
					double neutralIsolationPtSum = TagAndProbePair->first->sumNeutralHadronEtR04;
					double photonIsolationPtSum = TagAndProbePair->first->sumPhotonEtR04;
					double deltaBetaIsolationPtSum = TagAndProbePair->first->sumPUPtR04;
					FloatQuantities["iso_t"]=(chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/TagAndProbePair->first->p4.Pt();
				}else if(*quantity=="muon_p"){
					BoolQuantities["muon_p"]=true;
				}else if(*quantity=="trk_p"){
					BoolQuantities["trk_p"]=false;
				}else if(*quantity=="pt_p"){
					FloatQuantities["pt_p"]=TagAndProbePair->second->p4.Pt();
				}else if(*quantity=="eta_p"){
					FloatQuantities["eta_p"]=TagAndProbePair->second->p4.Eta();
				}else if(*quantity=="phi_p"){
					FloatQuantities["phi_p"]=TagAndProbePair->second->p4.Phi();
				}else if(*quantity=="id_p"){
					BoolQuantities["id_p"]=IsMediumMuon2016ShortTerm(TagAndProbePair->second) && std::abs(TagAndProbePair->second->dxy) < 0.045 && std::abs(TagAndProbePair->second->dz) < 0.2;
				}else if(*quantity=="iso_p"){
					double chargedIsolationPtSum = TagAndProbePair->second->sumChargedHadronPtR04;
					double neutralIsolationPtSum = TagAndProbePair->second->sumNeutralHadronEtR04;
					double photonIsolationPtSum = TagAndProbePair->second->sumPhotonEtR04;
					double deltaBetaIsolationPtSum = TagAndProbePair->second->sumPUPtR04;
					FloatQuantities["iso_p"]=(chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/TagAndProbePair->second->p4.Pt();
				}else if(*quantity=="m_ll"){
					FloatQuantities["m_ll"]=(TagAndProbePair->first->p4 + TagAndProbePair->second->p4).M();
				}else if(*quantity=="trg_t_IsoMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu22"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu22"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_t_IsoMu22"]=true;
				}else if(*quantity=="trg_t_IsoMu22_eta2p1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu22_eta2p1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu22_eta2p1"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_t_IsoMu22_eta2p1"]=true;
				}else if(*quantity=="trg_t_IsoMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu24"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu24"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_t_IsoMu24"]=true;
				}else if(*quantity=="trg_t_IsoMu19Tau"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_IsoMu19Tau"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_IsoMu19Tau"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_IsoMu19Tau"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_t_IsoMu19Tau"]=true;
				}else if(*quantity=="trg_p_IsoMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu22"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu22"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoMu22"]=true;
				}else if(*quantity=="trg_p_IsoTkMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoTkMu22"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoTkMu22"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoTkMu22"]=true;
				}else if(*quantity=="trg_p_IsoMu22_eta2p1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu22_eta2p1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu22_eta2p1"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoMu22_eta2p1"]=true;
				}else if(*quantity=="trg_p_IsoTkMu22_eta2p1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=true;
				}else if(*quantity=="trg_p_IsoMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu24"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu24"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoMu24"]=true;
				}else if(*quantity=="trg_p_IsoTkMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoTkMu24"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoTkMu24"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoTkMu24"]=true;
				}else if(*quantity=="trg_p_PFTau120"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_PFTau120"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau120_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_PFTau120"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_PFTau120"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_PFTau120"]=true;
				}else if(*quantity=="trg_p_IsoMu19TauL1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu19TauL1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu19TauL1"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu19TauL1"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoMu19TauL1"]=true;
				}else if(*quantity=="trg_p_IsoMu19Tau"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu19Tau"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v", boost::regex::icase | boost::regex::extended)))
							{
								if (IsData && hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_IsoMu19Tau"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_IsoMu19Tau"]=false;
						}
					}
					if (!IsData) BoolQuantities["trg_p_IsoMu19Tau"]=true;
				}
			}
			
			// fill tree
			this->m_tree->Fill();
		}
				
	}

	void Finish(setting_type const& settings) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Short_Term_Medium_Muon_Definitio
	bool IsMediumMuon2016ShortTerm(KMuon* muon) const
	{
	        bool goodGlob = muon->isGlobalMuon()
	                                        && muon->normalizedChiSquare < 3
	                                        && muon->chiSquareLocalPos < 12
        	                                && muon->trkKink < 20;
        	bool isMedium = muon->idLoose()
        	                               	&& muon->validFractionOfTrkHits > 0.49
        	                                && muon->segmentCompatibility > (goodGlob ? 0.303 : 0.451);
        	return isMedium;
	}
};

