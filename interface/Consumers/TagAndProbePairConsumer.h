
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

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

#include "Kappa/DataFormats/interface/Kappa.h"
#include <boost/regex.hpp>


class TagAndProbeMuonPairConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override
	{
		return "TagAndProbeMuonPairConsumer";
	}
	
	void Init(setting_type const& settings, metadata_type& metadata) override {
		ConsumerBase<HttTypes>::Init(settings, metadata);
		
		usedMuonIDshortTerm = (settings.GetMuonID() == "medium2016");
		
		//fill quantity maps
		FloatQuantities["wt"]=0.0;
		IntQuantities["n_vtx"]=0;
		IntQuantities["run"]=0;
		IntQuantities["lumi"]=0;
		IntQuantities["evt"]=0;
		BoolQuantities["usedMuonIDshortTerm"]=usedMuonIDshortTerm;
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
		FloatQuantities["dxy_p"]=0.0;
		FloatQuantities["dz_p"]=0.0;
		BoolQuantities["gen_p"]=true;
		BoolQuantities["genZ_p"]=true;
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

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override
	{
		ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings, metadata);

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
				}else if(*quantity=="usedMuonIDshortTerm"){
					BoolQuantities["usedMuonIDshortTerm"]=usedMuonIDshortTerm;
				}else if(*quantity=="pt_t"){
					FloatQuantities["pt_t"]=TagAndProbePair->first->p4.Pt();
				}else if(*quantity=="eta_t"){
					FloatQuantities["eta_t"]=TagAndProbePair->first->p4.Eta();
				}else if(*quantity=="phi_t"){
					FloatQuantities["phi_t"]=TagAndProbePair->first->p4.Phi();
				}else if(*quantity=="id_t"){
					BoolQuantities["id_t"]=( usedMuonIDshortTerm ? IsMediumMuon2016ShortTerm(TagAndProbePair->first) : IsMediumMuon2016(TagAndProbePair->first) ) && std::abs(TagAndProbePair->first->dxy) < 0.045 && std::abs(TagAndProbePair->first->dz) < 0.2;
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
					BoolQuantities["id_p"]=( usedMuonIDshortTerm ? IsMediumMuon2016ShortTerm(TagAndProbePair->second) : IsMediumMuon2016(TagAndProbePair->second) ) && std::abs(TagAndProbePair->second->dxy) < 0.045 && std::abs(TagAndProbePair->second->dz) < 0.2;
				}else if(*quantity=="iso_p"){
					double chargedIsolationPtSum = TagAndProbePair->second->sumChargedHadronPtR04;
					double neutralIsolationPtSum = TagAndProbePair->second->sumNeutralHadronEtR04;
					double photonIsolationPtSum = TagAndProbePair->second->sumPhotonEtR04;
					double deltaBetaIsolationPtSum = TagAndProbePair->second->sumPUPtR04;
					FloatQuantities["iso_p"]=(chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/TagAndProbePair->second->p4.Pt();
				}else if(*quantity=="dxy_p"){
					FloatQuantities["dxy_p"]=std::abs(TagAndProbePair->second->dxy);
				}else if(*quantity=="dz_p"){
					FloatQuantities["dz_p"]=std::abs(TagAndProbePair->second->dz);
				}else if(*quantity=="gen_p"){
					if(IsData) BoolQuantities["gen_p"]=false;
					else BoolQuantities["gen_p"]=(product.m_genParticleMatchedMuons.find(TagAndProbePair->second) != product.m_genParticleMatchedMuons.end());
				}else if(*quantity=="genZ_p"){
					if(IsData) BoolQuantities["genZ_p"]=false;
					else if(product.m_genParticleMatchedMuons.find(TagAndProbePair->second) != product.m_genParticleMatchedMuons.end()){
						BoolQuantities["genZ_p"]=(std::find(product.m_genLeptonsFromBosonDecay.begin(), product.m_genLeptonsFromBosonDecay.end(), product.m_genParticleMatchedMuons.at(TagAndProbePair->second)) != product.m_genLeptonsFromBosonDecay.end());
					}else{
						BoolQuantities["genZ_p"]=false;
					}
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
								if (hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
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
								if (hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
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
				}
			}
			
			// fill tree
			this->m_tree->Fill();
		}
				
	}

	void Finish(setting_type const& settings, metadata_type const& metadata) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	bool usedMuonIDshortTerm = false;
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
	bool IsMediumMuon2016(KMuon* muon) const
	{
	        bool goodGlob = muon->isGlobalMuon()
	                                        && muon->normalizedChiSquare < 3
	                                        && muon->chiSquareLocalPos < 12
        	                                && muon->trkKink < 20;
        	bool isMedium = muon->idLoose()
        	                               	&& muon->validFractionOfTrkHits > 0.8
        	                                && muon->segmentCompatibility > (goodGlob ? 0.303 : 0.451);
        	return isMedium;
	}
};


class TagAndProbeElectronPairConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override
	{
		return "TagAndProbeElectronPairConsumer";
	}
	
	void Init(setting_type const& settings, metadata_type& metadata) override {
		ConsumerBase<HttTypes>::Init(settings, metadata);
		electronIDName = settings.GetElectronIDName();
		electronMvaIDCutEB1 = settings.GetElectronMvaIDCutEB1();
		electronMvaIDCutEB2 = settings.GetElectronMvaIDCutEB2();
		electronMvaIDCutEE = settings.GetElectronMvaIDCutEE();
		
		//fill quantity maps
		FloatQuantities["wt"]=0.0;
		IntQuantities["n_vtx"]=0;
		IntQuantities["run"]=0;
		IntQuantities["lumi"]=0;
		IntQuantities["evt"]=0;
		FloatQuantities["pt_t"]=0.0;
		FloatQuantities["pt_t_25eta2p1TightL1"]=0.0;
		FloatQuantities["eta_t"]=0.0;
		FloatQuantities["phi_t"]=0.0;
		BoolQuantities["id_t"]=false;
		FloatQuantities["iso_t"]=0.0;
		FloatQuantities["pt_p"]=0.0;
		FloatQuantities["eta_p"]=0.0;
		FloatQuantities["sc_eta_p"]=0.0;
		FloatQuantities["phi_p"]=0.0;
		BoolQuantities["id_p"]=false;
		FloatQuantities["iso_p"]=0.0;
		BoolQuantities["gen_p"]=true;
		BoolQuantities["genZ_p"]=true;
		FloatQuantities["m_ll"]=0.0;
		BoolQuantities["trg_t_Ele25eta2p1WPTight"]=false;
		BoolQuantities["trg_t_Ele27eta2p1WPTight"]=false;
		BoolQuantities["trg_t_Ele27eta2p1WPLoose"]=false;
		BoolQuantities["trg_p_Ele25eta2p1WPTight"]=false;
		BoolQuantities["trg_p_Ele27eta2p1WPTight"]=false;
		BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=false;
		BoolQuantities["trg_p_PFTau120"]=false;

		// create tree
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree = new TTree("ZeeTP", ("Tree for Pipeline \"" + settings.GetName() + "\"").c_str());

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

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override
	{
		ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings, metadata);

		// calculate values
		bool IsData = settings.GetInputIsData();
		for (std::vector<std::pair<KElectron*, KElectron*>>::const_iterator TagAndProbePair = product.m_TagAndProbeElectronPairs.begin();
				TagAndProbePair != product.m_TagAndProbeElectronPairs.end(); ++TagAndProbePair)
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
				}else if(*quantity=="pt_t_25eta2p1TightL1"){
					double pt_L1object = 0.0;
					if (!product.m_selectedHltNames.empty())
					{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->first);
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele25_eta2p1_WPTight_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								for (auto L1object: hlts.second["hltEle25erWPTightGsfTrackIsoFilter"])
								{
									if (L1object->p4.Pt() > pt_L1object) pt_L1object = L1object->p4.Pt();
								}
							}
						}
					}
					FloatQuantities["pt_t_25eta2p1TightL1"]=pt_L1object;
				}else if(*quantity=="eta_t"){
					FloatQuantities["eta_t"]=TagAndProbePair->first->p4.Eta();
				}else if(*quantity=="phi_t"){
					FloatQuantities["phi_t"]=TagAndProbePair->first->p4.Phi();
				}else if(*quantity=="id_t"){
					BoolQuantities["id_t"]=IsMVABased(TagAndProbePair->first, event, electronIDName) && std::abs(TagAndProbePair->first->track.getDxy(&event.m_vertexSummary->pv)) < 0.045 && std::abs(TagAndProbePair->first->track.getDz(&event.m_vertexSummary->pv)) < 0.2;
				}else if(*quantity=="iso_t"){
					FloatQuantities["iso_t"]=TagAndProbePair->first->pfIso(settings.GetElectronDeltaBetaCorrectionFactor())/TagAndProbePair->first->p4.Pt();
				}else if(*quantity=="pt_p"){
					FloatQuantities["pt_p"]=TagAndProbePair->second->p4.Pt();
				}else if(*quantity=="eta_p"){
					FloatQuantities["eta_p"]=TagAndProbePair->second->p4.Eta();
				}else if(*quantity=="sc_eta_p"){
					FloatQuantities["sc_eta_p"]=TagAndProbePair->second->superclusterPosition.Eta();
				}else if(*quantity=="phi_p"){
					FloatQuantities["phi_p"]=TagAndProbePair->second->p4.Phi();
				}else if(*quantity=="id_p"){
					BoolQuantities["id_p"]=IsMVABased(TagAndProbePair->second, event, electronIDName) && std::abs(TagAndProbePair->second->track.getDxy(&event.m_vertexSummary->pv)) < 0.045 && std::abs(TagAndProbePair->second->track.getDz(&event.m_vertexSummary->pv)) < 0.2;
				}else if(*quantity=="iso_p"){
					FloatQuantities["iso_p"]=TagAndProbePair->second->pfIso(settings.GetElectronDeltaBetaCorrectionFactor())/TagAndProbePair->second->p4.Pt();
				}else if(*quantity=="gen_p"){
					if(IsData) BoolQuantities["gen_p"]=false;
					else BoolQuantities["gen_p"]=(product.m_genParticleMatchedElectrons.find(TagAndProbePair->second) != product.m_genParticleMatchedElectrons.end());
				}else if(*quantity=="genZ_p"){
					if(IsData) BoolQuantities["genZ_p"]=false;
					else if(product.m_genParticleMatchedElectrons.find(TagAndProbePair->second) != product.m_genParticleMatchedElectrons.end()){
						BoolQuantities["genZ_p"]=(std::find(product.m_genLeptonsFromBosonDecay.begin(), product.m_genLeptonsFromBosonDecay.end(), product.m_genParticleMatchedElectrons.at(TagAndProbePair->second)) != product.m_genLeptonsFromBosonDecay.end());
					}else{
						BoolQuantities["genZ_p"]=false;
					}
				}else if(*quantity=="m_ll"){
					FloatQuantities["m_ll"]=(TagAndProbePair->first->p4 + TagAndProbePair->second->p4).M();
				}else if(*quantity=="trg_t_Ele25eta2p1WPTight"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_Ele25eta2p1WPTight"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele25_eta2p1_WPTight_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle25erWPTightGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_Ele25eta2p1WPTight"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_Ele25eta2p1WPTight"]=false;
						}
					}
				}else if(*quantity=="trg_t_Ele27eta2p1WPTight"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_Ele27eta2p1WPTight"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele27_eta2p1_WPTight_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle27erWPTightGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_Ele27eta2p1WPTight"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_Ele27eta2p1WPTight"]=false;
						}
					}
				}else if(*quantity=="trg_t_Ele27eta2p1WPLoose"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_t_Ele27eta2p1WPLoose"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->first);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele27_eta2p1_WPLoose_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle27erWPLooseGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_t_Ele27eta2p1WPLoose"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_t_Ele27eta2p1WPLoose"]=false;
						}
					}
				}else if(*quantity=="trg_p_Ele25eta2p1WPTight"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_Ele25eta2p1WPTight"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele25_eta2p1_WPTight_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle25erWPTightGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_Ele25eta2p1WPTight"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_Ele25eta2p1WPTight"]=false;
						}
					}
				}else if(*quantity=="trg_p_Ele27eta2p1WPTight"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_Ele27eta2p1WPTight"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele27_eta2p1_WPTight_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle27erWPTightGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_Ele27eta2p1WPTight"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_Ele27eta2p1WPTight"]=false;
						}
					}
				}else if(*quantity=="trg_p_Ele27eta2p1WPLoose"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele27_eta2p1_WPLoose_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle27erWPLooseGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=false;
						}
					}
				}else if(*quantity=="trg_p_PFTau120"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_PFTau120"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(TagAndProbePair->second);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau120_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
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
				}
			}
			// fill tree
			this->m_tree->Fill();
		}
				
	}

	void Finish(setting_type const& settings, metadata_type const& metadata) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	std::string electronIDName;
	double electronMvaIDCutEB1;
	double electronMvaIDCutEB2;
	double electronMvaIDCutEE;
	bool IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const
	{
		bool validElectron = true;
		validElectron = validElectron && (electron->track.nInnerHits <= 1);
		validElectron = validElectron && (! (electron->electronType & (1 << KElectronType::hasConversionMatch)));
	
		// https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2#General_Purpose_MVA_training_det
		// pT always greater than 10 GeV
		validElectron = validElectron &&
			(
				(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEB1)
				||
				(std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEB2)
				||
				(std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEE)
			);
	
		return validElectron;
	}
};


class TagAndProbeGenTauConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override
	{
		return "TagAndProbeGenTauConsumer";
	}
	
	void Init(setting_type const& settings, metadata_type& metadata) override {
		ConsumerBase<HttTypes>::Init(settings, metadata);
		//electronIDName = settings.GetElectronIDName();
		//electronMvaIDCutEB1 = settings.GetElectronMvaIDCutEB1();
		//electronMvaIDCutEB2 = settings.GetElectronMvaIDCutEB2();
		//electronMvaIDCutEE = settings.GetElectronMvaIDCutEE();
		
		//fill quantity maps
		FloatQuantities["wt"]=0.0;
		IntQuantities["n_vtx"]=0;
		IntQuantities["run"]=0;
		IntQuantities["lumi"]=0;
		IntQuantities["evt"]=0;
		//FloatQuantities["pt_t"]=0.0;
		//FloatQuantities["eta_t"]=0.0;
		//FloatQuantities["phi_t"]=0.0;
		//BoolQuantities["id_t"]=false;
		//FloatQuantities["iso_t"]=0.0;
		FloatQuantities["pt_p"]=0.0;
		FloatQuantities["eta_p"]=0.0;
		FloatQuantities["phi_p"]=0.0;
		BoolQuantities["id_p"]=false;
		FloatQuantities["isoMedium_p"]=0.0;
		FloatQuantities["isoTight_p"]=0.0;
		BoolQuantities["gen_p"]=false;
		//BoolQuantities["genZ_p"]=true;
		//FloatQuantities["m_ll"]=0.0;
		BoolQuantities["trg_p_PFTau120"]=false;
		BoolQuantities["trg_p_PFTau140"]=false;

		// create tree
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree = new TTree("GenTau", ("Tree for Pipeline \"" + settings.GetName() + "\"").c_str());

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

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override
	{
		ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings, metadata);

		// calculate values
		bool IsData = settings.GetInputIsData();
		for (std::vector<KTau*>::const_iterator tau = product.m_TagAndProbeGenTaus.begin();
				tau != product.m_TagAndProbeGenTaus.end(); ++tau)
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
				}else if(*quantity=="pt_p"){
					FloatQuantities["pt_p"]=(*tau)->p4.Pt();
				}else if(*quantity=="eta_p"){
					FloatQuantities["eta_p"]=(*tau)->p4.Eta();
				}else if(*quantity=="phi_p"){
					FloatQuantities["phi_p"]=(*tau)->p4.Phi();
				}else if(*quantity=="id_p"){
					oldTauDMs = settings.GetTauUseOldDMs();
					BoolQuantities["id_p"]=IsTauIDRecommendation13TeV(*tau, event, oldTauDMs);
				}else if(*quantity=="isoMedium_p"){
					FloatQuantities["isoMedium_p"]=(*tau)->getDiscriminator("byMediumIsolationMVArun2v1DBoldDMwLT", event.m_tauMetadata);
				}else if(*quantity=="isoTight_p"){
					FloatQuantities["isoTight_p"]=(*tau)->getDiscriminator("byTightIsolationMVArun2v1DBoldDMwLT", event.m_tauMetadata);
				}else if(*quantity=="gen_p"){
					if(IsData) BoolQuantities["gen_p"]=false;
					else if(product.m_genTauMatchedTaus.find(*tau) != product.m_genTauMatchedTaus.end() && product.m_genTauMatchedTaus.at(*tau)->isHadronicDecay() && std::abs((*tau)->p4.Pt()-product.m_genTauMatchedTaus.at(*tau)->p4.Pt()) < 5.0) BoolQuantities["gen_p"]=true;
					else BoolQuantities["gen_p"]=false;
				}else if(*quantity=="trg_p_PFTau120"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_PFTau120"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedTaus.at(*tau);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau120_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
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
				}else if(*quantity=="trg_p_PFTau140"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_PFTau140"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedTaus.at(*tau);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau140_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltPFTau140TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_PFTau140"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_PFTau140"]=false;
						}
					}
				}
			}
			// fill tree
			this->m_tree->Fill();
		}
				
	}

	void Finish(setting_type const& settings, metadata_type const& metadata) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	bool oldTauDMs;
	bool IsTauIDRecommendation13TeV(KTau* tau, event_type const& event, bool const& oldTauDMs, bool const& isAOD=false) const
	{
		const KVertex* vertex = new KVertex(event.m_vertexSummary->pv);
		float decayModeDiscriminator = (oldTauDMs ? tau->getDiscriminator("decayModeFinding", event.m_tauMetadata)
							  : tau->getDiscriminator("decayModeFindingNewDMs", event.m_tauMetadata));
		if(isAOD)
		{
			return ( decayModeDiscriminator > 0.5
				 && (std::abs(tau->track.ref.z() - vertex->position.z()) < 0.2)
				// tau dZ requirement for Phys14 sync
				//&& (Utility::ApproxEqual(tau->track.ref.z(), vertex->position.z()))
			);
		}
		else
		{
			return ( decayModeDiscriminator > 0.5
				 && std::abs(tau->dz) < 0.2
				// tau dZ requirement for Phys14 sync
				//&& (Utility::ApproxEqual(tau->track.ref.z(), vertex->position.z()))
			);
		}
	}
};


class TagAndProbeGenMuonConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override
	{
		return "TagAndProbeGenMuonConsumer";
	}
	
	void Init(setting_type const& settings, metadata_type& metadata) override {
		ConsumerBase<HttTypes>::Init(settings, metadata);
		
		usedMuonIDshortTerm = (settings.GetMuonID() == "medium2016");
		
		//fill quantity maps
		FloatQuantities["wt"]=0.0;
		IntQuantities["n_vtx"]=0;
		IntQuantities["run"]=0;
		IntQuantities["lumi"]=0;
		IntQuantities["evt"]=0;
		BoolQuantities["usedMuonIDshortTerm"]=usedMuonIDshortTerm;
		BoolQuantities["muon_p"]=false;
		BoolQuantities["trk_p"]=false;
		FloatQuantities["pt_p"]=0.0;
		FloatQuantities["eta_p"]=0.0;
		FloatQuantities["phi_p"]=0.0;
		BoolQuantities["id_p"]=false;
		FloatQuantities["iso_p"]=0.0;
		FloatQuantities["dxy_p"]=0.0;
		FloatQuantities["dz_p"]=0.0;
		BoolQuantities["gen_p"]=false;
		FloatQuantities["pt_gen"]=0.0;
		BoolQuantities["genZ_p"]=false;
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
		m_tree = new TTree("GenMuon", ("Tree for Pipeline \"" + settings.GetName() + "\"").c_str());

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

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override
	{
		ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings, metadata);

		// calculate values
		bool IsData = settings.GetInputIsData();
		for (std::vector<KMuon*>::const_iterator muon = product.m_TagAndProbeGenMuons.begin();
				muon != product.m_TagAndProbeGenMuons.end(); ++muon)
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
				}else if(*quantity=="usedMuonIDshortTerm"){
					BoolQuantities["usedMuonIDshortTerm"]=usedMuonIDshortTerm;
				}else if(*quantity=="muon_p"){
					BoolQuantities["muon_p"]=true;
				}else if(*quantity=="trk_p"){
					BoolQuantities["trk_p"]=false;
				}else if(*quantity=="pt_p"){
					FloatQuantities["pt_p"]=(*muon)->p4.Pt();
				}else if(*quantity=="eta_p"){
					FloatQuantities["eta_p"]=(*muon)->p4.Eta();
				}else if(*quantity=="phi_p"){
					FloatQuantities["phi_p"]=(*muon)->p4.Phi();
				}else if(*quantity=="id_p"){
					BoolQuantities["id_p"]=( usedMuonIDshortTerm ? IsMediumMuon2016ShortTerm(*muon) : IsMediumMuon2016(*muon) ) && std::abs((*muon)->dxy) < 0.045 && std::abs((*muon)->dz) < 0.2;
				}else if(*quantity=="iso_p"){
					double chargedIsolationPtSum = (*muon)->sumChargedHadronPtR04;
					double neutralIsolationPtSum = (*muon)->sumNeutralHadronEtR04;
					double photonIsolationPtSum = (*muon)->sumPhotonEtR04;
					double deltaBetaIsolationPtSum = (*muon)->sumPUPtR04;
					FloatQuantities["iso_p"]=(chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/(*muon)->p4.Pt();
				}else if(*quantity=="dxy_p"){
					FloatQuantities["dxy_p"]=std::abs((*muon)->dxy);
				}else if(*quantity=="dz_p"){
					FloatQuantities["dz_p"]=std::abs((*muon)->dz);
				}else if(*quantity=="gen_p"){
					if(IsData) BoolQuantities["gen_p"]=false;
					else BoolQuantities["gen_p"]=(product.m_genParticleMatchedMuons.find(*muon) != product.m_genParticleMatchedMuons.end());
					if(BoolQuantities["gen_p"] && std::abs((*muon)->p4.Pt()-product.m_genParticleMatchedMuons.at(*muon)->p4.Pt()) > 5.0) BoolQuantities["gen_p"] = false;
				}else if(*quantity=="pt_gen"){
					if(!IsData && (product.m_genParticleMatchedMuons.find(*muon) != product.m_genParticleMatchedMuons.end())) FloatQuantities["pt_gen"]=product.m_genParticleMatchedMuons.at(*muon)->p4.Pt();
					else FloatQuantities["pt_gen"]=0.0;
				}else if(*quantity=="genZ_p"){
					if(IsData) BoolQuantities["genZ_p"]=false;
					else if(product.m_genParticleMatchedMuons.find(*muon) != product.m_genParticleMatchedMuons.end()){
						BoolQuantities["genZ_p"]=(std::find(product.m_genLeptonsFromBosonDecay.begin(), product.m_genLeptonsFromBosonDecay.end(), product.m_genParticleMatchedMuons.at(*muon)) != product.m_genLeptonsFromBosonDecay.end());
					}else{
						BoolQuantities["genZ_p"]=false;
					}
				}else if(*quantity=="trg_p_IsoMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
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
				}else if(*quantity=="trg_p_IsoTkMu22"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu22"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu22_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
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
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
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
				}else if(*quantity=="trg_p_IsoTkMu22_eta2p1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu22_eta2p1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu22_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
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
				}else if(*quantity=="trg_p_IsoMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09"].size() > 0)
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
				}else if(*quantity=="trg_p_IsoTkMu24"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoTkMu24"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu24_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09"].size() > 0)
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
				}else if(*quantity=="trg_p_PFTau120"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_PFTau120"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau120_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
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
				}else if(*quantity=="trg_p_IsoMu19TauL1"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu19TauL1"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
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
				}else if(*quantity=="trg_p_IsoMu19Tau"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_IsoMu19Tau"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedMuons.at(*muon);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
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
				}
			}
			
			// fill tree
			if(BoolQuantities["gen_p"]) this->m_tree->Fill();
		}
				
	}

	void Finish(setting_type const& settings, metadata_type const& metadata) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	bool usedMuonIDshortTerm = false;
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
	bool IsMediumMuon2016(KMuon* muon) const
	{
	        bool goodGlob = muon->isGlobalMuon()
	                                        && muon->normalizedChiSquare < 3
	                                        && muon->chiSquareLocalPos < 12
        	                                && muon->trkKink < 20;
        	bool isMedium = muon->idLoose()
        	                               	&& muon->validFractionOfTrkHits > 0.8
        	                                && muon->segmentCompatibility > (goodGlob ? 0.303 : 0.451);
        	return isMedium;
	}
};


class TagAndProbeGenElectronConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override
	{
		return "TagAndProbeGenElectronConsumer";
	}
	
	void Init(setting_type const& settings, metadata_type& metadata) override {
		ConsumerBase<HttTypes>::Init(settings, metadata);
		electronIDName = settings.GetElectronIDName();
		electronMvaIDCutEB1 = settings.GetElectronMvaIDCutEB1();
		electronMvaIDCutEB2 = settings.GetElectronMvaIDCutEB2();
		electronMvaIDCutEE = settings.GetElectronMvaIDCutEE();
		
		//fill quantity maps
		FloatQuantities["wt"]=0.0;
		IntQuantities["n_vtx"]=0;
		IntQuantities["run"]=0;
		IntQuantities["lumi"]=0;
		IntQuantities["evt"]=0;
		FloatQuantities["pt_p"]=0.0;
		FloatQuantities["eta_p"]=0.0;
		FloatQuantities["sc_eta_p"]=0.0;
		FloatQuantities["phi_p"]=0.0;
		BoolQuantities["id_p"]=false;
		FloatQuantities["iso_p"]=0.0;
		BoolQuantities["gen_p"]=false;
		FloatQuantities["pt_gen"]=0.0;
		BoolQuantities["genZ_p"]=false;
		BoolQuantities["trg_p_Ele25eta2p1WPTight"]=false;
		BoolQuantities["trg_p_Ele27eta2p1WPTight"]=false;
		BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=false;
		BoolQuantities["trg_p_PFTau120"]=false;

		// create tree
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree = new TTree("GenElectron", ("Tree for Pipeline \"" + settings.GetName() + "\"").c_str());

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

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override
	{
		ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings, metadata);

		// calculate values
		bool IsData = settings.GetInputIsData();
		for (std::vector<KElectron*>::const_iterator electron = product.m_TagAndProbeGenElectrons.begin();
				electron != product.m_TagAndProbeGenElectrons.end(); ++electron)
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
				}else if(*quantity=="pt_p"){
					FloatQuantities["pt_p"]=(*electron)->p4.Pt();
				}else if(*quantity=="eta_p"){
					FloatQuantities["eta_p"]=(*electron)->p4.Eta();
				}else if(*quantity=="sc_eta_p"){
					FloatQuantities["sc_eta_p"]=(*electron)->superclusterPosition.Eta();
				}else if(*quantity=="phi_p"){
					FloatQuantities["phi_p"]=(*electron)->p4.Phi();
				}else if(*quantity=="id_p"){
					BoolQuantities["id_p"]=IsMVABased(*electron, event, electronIDName) && std::abs((*electron)->track.getDxy(&event.m_vertexSummary->pv)) < 0.045 && std::abs((*electron)->track.getDz(&event.m_vertexSummary->pv)) < 0.2;
				}else if(*quantity=="iso_p"){
					FloatQuantities["iso_p"]=(*electron)->pfIso(settings.GetElectronDeltaBetaCorrectionFactor())/(*electron)->p4.Pt();
				}else if(*quantity=="gen_p"){
					if(IsData) BoolQuantities["gen_p"]=false;
					else BoolQuantities["gen_p"]=(product.m_genParticleMatchedElectrons.find(*electron) != product.m_genParticleMatchedElectrons.end());
					if(BoolQuantities["gen_p"] && std::abs((*electron)->p4.Pt()-product.m_genParticleMatchedElectrons.at(*electron)->p4.Pt()) > 5.0) BoolQuantities["gen_p"] = false;
				}else if(*quantity=="pt_gen"){
					if(!IsData && (product.m_genParticleMatchedElectrons.find(*electron) != product.m_genParticleMatchedElectrons.end())) FloatQuantities["pt_gen"]=product.m_genParticleMatchedElectrons.at(*electron)->p4.Pt();
					else FloatQuantities["pt_gen"]=0.0;
				}else if(*quantity=="genZ_p"){
					if(IsData) BoolQuantities["genZ_p"]=false;
					else if(product.m_genParticleMatchedElectrons.find(*electron) != product.m_genParticleMatchedElectrons.end()){
						BoolQuantities["genZ_p"]=(std::find(product.m_genLeptonsFromBosonDecay.begin(), product.m_genLeptonsFromBosonDecay.end(), product.m_genParticleMatchedElectrons.at(*electron)) != product.m_genLeptonsFromBosonDecay.end());
					}else{
						BoolQuantities["genZ_p"]=false;
					}
				}else if(*quantity=="trg_p_Ele25eta2p1WPTight"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_Ele25eta2p1WPTight"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(*electron);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele25_eta2p1_WPTight_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle25erWPTightGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_Ele25eta2p1WPTight"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_Ele25eta2p1WPTight"]=false;
						}
					}
				}else if(*quantity=="trg_p_Ele27eta2p1WPTight"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_Ele27eta2p1WPTight"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(*electron);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele27_eta2p1_WPTight_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle27erWPTightGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_Ele27eta2p1WPTight"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_Ele27eta2p1WPTight"]=false;
						}
					}
				}else if(*quantity=="trg_p_Ele27eta2p1WPLoose"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(*electron);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_Ele27_eta2p1_WPLoose_Gsf_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltEle27erWPLooseGsfTrackIsoFilter"].size() > 0)
								{
									Hltfired = true;
									BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=true;
								}
							}
						}
						if (!Hltfired)
						{
							BoolQuantities["trg_p_Ele27eta2p1WPLoose"]=false;
						}
					}
				}else if(*quantity=="trg_p_PFTau120"){
					if (product.m_selectedHltNames.empty())
					{
						BoolQuantities["trg_p_PFTau120"]=false;
					}else{
						auto trigger = product.m_detailedTriggerMatchedElectrons.at(*electron);
						bool Hltfired = false;
						for (auto hlts: trigger)         
						{
							if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau120_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
							{
								if (hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
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
				}
			}
			// fill tree
			if(BoolQuantities["gen_p"]) this->m_tree->Fill();
		}
				
	}

	void Finish(setting_type const& settings, metadata_type const& metadata) override
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
		m_tree->Write(m_tree->GetName());
	}


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	std::string electronIDName;
	double electronMvaIDCutEB1;
	double electronMvaIDCutEB2;
	double electronMvaIDCutEE;
	bool IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const
	{
		bool validElectron = true;
		validElectron = validElectron && (electron->track.nInnerHits <= 1);
		validElectron = validElectron && (! (electron->electronType & (1 << KElectronType::hasConversionMatch)));
	
		// https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2#General_Purpose_MVA_training_det
		// pT always greater than 10 GeV
		validElectron = validElectron &&
			(
				(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEB1)
				||
				(std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEB2)
				||
				(std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId(idName, event.m_electronMetadata) > electronMvaIDCutEE)
			);
	
		return validElectron;
	}
};
