#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include <TMath.h>
#include <Math/VectorUtil.h>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TagAndProbePairProducer.h"
#include <assert.h>
#include <boost/regex.hpp>
#include "Kappa/DataFormats/interface/Kappa.h"


void TagAndProbeMuonPairProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	validMuonsInput = ToValidMuonsInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidMuonsInput())));
	//muonID = ToMuonID(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.*GetMuonID)())));
	std::string weightName = settings.GetEventWeight();
	MuonIDshortTerm = (settings.GetMuonID() == "medium2016");
	bool IsData = settings.GetInputIsData();
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "wt", [weightName](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> weight;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			weight.push_back(product.m_weights.at(weightName));
		}
		return weight;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "n_vtx", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> nvtx;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			nvtx.push_back(event.m_vertexSummary->nVertices);
		}
		return nvtx;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "run", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> Run;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			Run.push_back(event.m_eventInfo->nRun);
		}
		return Run;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "pt_t", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> pt_tag;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			pt_tag.push_back(TagAndProbePair->first->p4.Pt());
		}
		return pt_tag;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "eta_t", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> eta_tag;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			eta_tag.push_back(TagAndProbePair->first->p4.Eta());
		}
		return eta_tag;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "phi_t", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> phi_tag;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			phi_tag.push_back(TagAndProbePair->first->p4.Phi());
		}
		return phi_tag;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "id_t", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> id_tag;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			id_tag.push_back(TagAndProbePair->first->idMedium());
		}
		return id_tag;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "iso_t", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> iso_tag;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			iso_tag.push_back(TagAndProbePair->first->pfIso());
		}
		return iso_tag;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "muon_p", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> muon_probe;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			muon_probe.push_back(TagAndProbePair->second->isGlobalMuon());
		}
		return muon_probe;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trk_p", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trk_probe;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			trk_probe.push_back(TagAndProbePair->second->isTrackerMuon());
		}
		return trk_probe;
	});	
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "pt_p", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> pt_probe;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			pt_probe.push_back(TagAndProbePair->second->p4.Pt());
		}
		return pt_probe;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "eta_p", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> eta_probe;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			eta_probe.push_back(TagAndProbePair->second->p4.Eta());
		}
		return eta_probe;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "phi_p", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> phi_probe;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			phi_probe.push_back(TagAndProbePair->second->p4.Phi());
		}
		return phi_probe;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "id_p", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> id_probe;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			id_probe.push_back(TagAndProbePair->second->idMedium());
		}
		return id_probe;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "iso_p", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> iso_probe;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			iso_probe.push_back(TagAndProbePair->second->pfIso());
		}
		return iso_probe;
	});
	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "m_ll", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<float> mll;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
	       TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			mll.push_back((TagAndProbePair->first->p4 + TagAndProbePair->second->p4).M());
		}
		return mll;
	});
	//Trigger info
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trg_t_IsoMu22", [IsData](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trg;
		bool noHlt = false;
		if (product.m_selectedHltNames.empty()) noHlt = true;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
							TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			if (noHlt)
			{
				trg.push_back(false);
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
							trg.push_back(true);
						}
					}                                                                                                                                                                                                                                                
				}
				if (!Hltfired)
				{
					trg.push_back(false);
				}                                                                                                                                                                                                                                              
			}
		}
		return trg;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trg_t_IsoMu19Tau", [IsData](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trg;
		bool noHlt = false;
		if (product.m_selectedHltNames.empty()) noHlt = true;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
							TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			if (noHlt)
			{
				trg.push_back(false);
			}else{
				auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->first);
				bool Hltfired = false;
				for (auto hlts: (trigger))         
				{
					if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v", boost::regex::icase | boost::regex::extended)))
					{
						if (IsData && hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
						{
							Hltfired = true;
							trg.push_back(true);
						}
					}                                                                                                                                                                                                                                                
				}
				if (!Hltfired)
				{
					trg.push_back(false);
				}                                                                                                                                                                                                                                               
			}
		}
		return trg;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trg_p_IsoMu22", [IsData](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trg;
		bool noHlt = false;
		if (product.m_selectedHltNames.empty()) noHlt = true;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
							TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			if (noHlt)
			{
				trg.push_back(false);
			}else{
				auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
				bool Hltfired = false;
				for (auto hlts: (trigger))         
				{
					if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu22_v", boost::regex::icase | boost::regex::extended)))
					{
						if (IsData && hlts.second["hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09"].size() > 0)
						{
							Hltfired = true;
							trg.push_back(true);
						}
					}                                                                                                                                                                                                                                                
				}
				if (!Hltfired)
				{
					trg.push_back(false);
				}                                                                                                                                                                                                                                               
			}
		}
		return trg;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trg_p_IsoTkMu22", [IsData](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trg;
		bool noHlt = false;
		if (product.m_selectedHltNames.empty()) noHlt = true;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
							TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			if (noHlt)
			{
				trg.push_back(false);
			}else{
				auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
				bool Hltfired = false;
				for (auto hlts: (trigger))         
				{
					if (boost::regex_search(hlts.first, boost::regex("HLT_IsoTkMu22_v", boost::regex::icase | boost::regex::extended)))
					{
						if (IsData && hlts.second["hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09"].size() > 0)
						{
							Hltfired = true;
							trg.push_back(true);
						}
					}                                                                                                                                                                                                                                                
				}
				if (!Hltfired)
				{
					trg.push_back(false);
				}                                                                                                                                                                                                                                               
			}
		}
		return trg;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trg_p_PFTau120", [IsData](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trg;
		bool noHlt = false;
		if (product.m_selectedHltNames.empty()) noHlt = true;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
							TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			if (noHlt)
			{
				trg.push_back(false);
			}else{
				auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
				bool Hltfired = false;
				for (auto hlts: (trigger))         
				{
					if (boost::regex_search(hlts.first, boost::regex("HLT_VLooseIsoPFTau120_Trk50_eta2p1_v", boost::regex::icase | boost::regex::extended)))
					{
						if (IsData && hlts.second["hltPFTau120TrackPt50LooseAbsOrRelVLooseIso"].size() > 0)
						{
							Hltfired = true;
							trg.push_back(true);
						}
					}                                                                                                                                                                                                                                                
				}
				if (!Hltfired)
				{
					trg.push_back(false);
				}                                                                                                                                                                                                                                            
			}
		}
		return trg;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trg_p_IsoMu19TauL1", [IsData](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trg;
		bool noHlt = false;
		if (product.m_selectedHltNames.empty()) noHlt = true;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
							TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			if (noHlt)
			{
				trg.push_back(false);
			}else{
				auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
				bool Hltfired = false;
				for (auto hlts: (trigger))         
				{
					if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v", boost::regex::icase | boost::regex::extended)))
					{
						if (IsData && hlts.second["hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
						{
							Hltfired = true;
							trg.push_back(true);
						}
					}                                                                                                                                                                                                                                                
				}
				if (!Hltfired)
				{
					trg.push_back(false);
				}
			}
		}
		return trg;
	});
	LambdaNtupleConsumer<HttTypes>::AddVIntQuantity(metadata, "trg_p_IsoMu19Tau", [IsData](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata){
		std::vector<int> trg;
		bool noHlt = false;
		if (product.m_selectedHltNames.empty()) noHlt = true;
		for (std::vector<std::pair<KMuon*, KMuon*>>::const_iterator TagAndProbePair = product.m_TagAndProbeMuonPairs.begin();
							TagAndProbePair != product.m_TagAndProbeMuonPairs.end(); ++TagAndProbePair)
		{
			if (noHlt)
			{
				trg.push_back(false);
			}else{
				auto trigger = product.m_detailedTriggerMatchedMuons.at(TagAndProbePair->second);
				bool Hltfired = false;
				for (auto hlts: (trigger))         
				{
					if (boost::regex_search(hlts.first, boost::regex("HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v", boost::regex::icase | boost::regex::extended)))
					{
						if (IsData && hlts.second["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09"].size() > 0)
						{
							Hltfired = true;
							trg.push_back(true);
						}
					}                                                                                                                                                                                                                                                
				}
				if (!Hltfired)
				{
					trg.push_back(false);
				}
			}
		}
		return trg;
	});
}

void TagAndProbeMuonPairProducer::Produce(event_type const& event, product_type& product,
					setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_muons);
	// select input source
	std::vector<KMuon*> muons;
	std::vector<KMuon*> ProbeMembers;
	std::vector<KMuon*> TagMembers;
	if ((validMuonsInput == ValidMuonsInput::AUTO && (product.m_correctedMuons.size() > 0)) || (validMuonsInput == ValidMuonsInput::CORRECTED))
	{
		muons.resize(product.m_correctedMuons.size());
		size_t muonIndex = 0;
		for (std::vector<std::shared_ptr<KMuon>>::iterator muon = product.m_correctedMuons.begin();
			muon != product.m_correctedMuons.end(); ++muon)
		{
			muons[muonIndex] = muon->get();
			++muonIndex;
		}
	}
	else
	{
		muons.resize(event.m_muons->size());
		size_t muonIndex = 0;
		for (KMuons::iterator muon = event.m_muons->begin(); muon != event.m_muons->end(); ++muon)
		{
			muons[muonIndex] = &(*muon);
			++muonIndex;
		}
	}
	//loop over muons
	for (std::vector<KMuon*>::iterator muon = muons.begin(); muon != muons.end(); ++muon)
	{
		product.m_validMuons.push_back(*muon);  //needed for ValidMuonsFilter
		
		//probe filter
		if (
			(*muon)->p4.Pt() > 10.0 &&
			std::abs((*muon)->p4.Eta()) < 2.4 &&
			(*muon)->isTrackerMuon()
		){
			ProbeMembers.push_back(*muon);
			//std::cout << std::endl <<"IsProbe! ";
		}
		//calculate muon isolation
		double chargedIsolationPtSum = (*muon)->sumChargedHadronPtR04;
		double neutralIsolationPtSum = (*muon)->sumNeutralHadronEtR04;
		double photonIsolationPtSum = (*muon)->sumPhotonEtR04;
		double deltaBetaIsolationPtSum = (*muon)->sumPUPtR04;
		double isolationPtSum = (chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - 0.5 * deltaBetaIsolationPtSum))/(*muon)->p4.Pt();
		//tag filter
		if (
			(*muon)->p4.Pt() > 23.0 &&
			std::abs((*muon)->p4.Eta()) < 2.4 &&
			std::abs((*muon)->dxy) < 0.045 &&
			std::abs((*muon)->dz) < 0.2 &&
			( MuonIDshortTerm ? IsMediumMuon2016ShortTerm(*muon, event, product) : IsMediumMuon2016(*muon, event, product) ) &&
			isolationPtSum < 0.15
		){
			TagMembers.push_back(*muon);
			//std::cout << "IsTag! ";
		}
		//std::cout << "Pt: " << (*muon)->p4.Pt() << " Eta: " << (*muon)->p4.Eta() << " dxy: " << (*muon)->dxy << " dz: " << (*muon)->dz << " ID: " << IsMediumMuon2016ShortTerm(*muon, event, product) << " Iso: " << isolationPtSum << std::endl;
		//std::cout << "chargedIsolationPtSum " << chargedIsolationPtSum << " neutralIsolationPtSum " << neutralIsolationPtSum << " photonIsolationPtSum " << photonIsolationPtSum << " deltaBetaIsolationPtSum " << deltaBetaIsolationPtSum << std::endl;
	}
	//erzeuge Paare
	for (std::vector<KMuon*>::iterator TagMember = TagMembers.begin(); TagMember != TagMembers.end(); ++TagMember)
	{
		for (std::vector<KMuon*>::iterator ProbeMember = ProbeMembers.begin(); ProbeMember != ProbeMembers.end(); ++ProbeMember)
		{
			if (
				((*TagMember)->charge()+(*ProbeMember)->charge() == 0) && (ROOT::Math::VectorUtil::DeltaR((*TagMember)->p4, (*ProbeMember)->p4) > 0.5)
			){
				product.m_TagAndProbeMuonPairs.push_back(std::make_pair(*TagMember, *ProbeMember));
			}
		}
	}
}

// https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Short_Term_Medium_Muon_Definitio
bool TagAndProbeMuonPairProducer::IsMediumMuon2016ShortTerm(KMuon* muon, event_type const& event, product_type& product) const
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
bool TagAndProbeMuonPairProducer::IsMediumMuon2016(KMuon* muon, event_type const& event, product_type& product) const
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

void TagAndProbeElectronPairProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	validElectronsInput = ToValidElectronsInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidElectronsInput())));
	electronIDName = settings.GetElectronIDName();
	electronMvaIDCutEB1 = settings.GetElectronMvaIDCutEB1();
	electronMvaIDCutEB2 = settings.GetElectronMvaIDCutEB2();
	electronMvaIDCutEE = settings.GetElectronMvaIDCutEE();
}

void TagAndProbeElectronPairProducer::Produce(event_type const& event, product_type& product,
					setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_electrons);
	// select input source
	std::vector<KElectron*> electrons;
	std::vector<KElectron*> ProbeMembers;
	std::vector<KElectron*> TagMembers;
	if ((validElectronsInput == ValidElectronsInput::AUTO && (product.m_correctedElectrons.size() > 0)) || (validElectronsInput == ValidElectronsInput::CORRECTED))
	{
		electrons.resize(product.m_correctedElectrons.size());
		size_t electronIndex = 0;
		for (std::vector<std::shared_ptr<KElectron> >::iterator electron = product.m_correctedElectrons.begin();
		     electron != product.m_correctedElectrons.end(); ++electron)
		{
			electrons[electronIndex] = electron->get();
			++electronIndex;
		}
	}
	else
	{
		electrons.resize(event.m_electrons->size());
		size_t electronIndex = 0;
		for (KElectrons::iterator electron = event.m_electrons->begin(); electron != event.m_electrons->end(); ++electron)
		{
			electrons[electronIndex] = &(*electron);
			++electronIndex;
		}
	}
	//loop over electrons
	for (std::vector<KElectron*>::iterator electron = electrons.begin(); electron != electrons.end(); ++electron)
	{
		product.m_validElectrons.push_back(*electron); //needed for ValidElectronsFilter
		
		//probe filter
		if (
			(*electron)->p4.Pt() > 10.0 &&
			std::abs((*electron)->p4.Eta()) < 2.5
		){
			ProbeMembers.push_back(*electron);
		}
		//tag filter
		if (
			(*electron)->p4.Pt() > 26.0 &&
			std::abs((*electron)->p4.Eta()) < 2.1 &&
			std::abs((*electron)->track.getDxy(&event.m_vertexSummary->pv)) < 0.045 &&
			std::abs((*electron)->track.getDz(&event.m_vertexSummary->pv)) < 0.2 &&
			IsMVABased(*electron, event, electronIDName) &&
			(*electron)->pfIso(settings.GetElectronDeltaBetaCorrectionFactor())/(*electron)->p4.Pt() < 0.1
		){
			TagMembers.push_back(*electron);
		}
	}
	//erzeuge Paare
	for (std::vector<KElectron*>::iterator TagMember = TagMembers.begin(); TagMember != TagMembers.end(); ++TagMember)
	{
		for (std::vector<KElectron*>::iterator ProbeMember = ProbeMembers.begin(); ProbeMember != ProbeMembers.end(); ++ProbeMember)
		{
			if (
				((*TagMember)->charge()+(*ProbeMember)->charge() == 0) && (ROOT::Math::VectorUtil::DeltaR((*TagMember)->p4, (*ProbeMember)->p4) > 0.5)
			){
				product.m_TagAndProbeElectronPairs.push_back(std::make_pair(*TagMember, *ProbeMember));
			}
		}
	}
}

bool TagAndProbeElectronPairProducer::IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const
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


/*
TagAndProbeGenElectronProducer::TagAndProbeGenElectronProducer() :
	TagAndProbeGenLeptonProducer<KElectron>(&event_type::m_electrons,
						  &product_type::m_correctedElectrons,
						  &product_type::m_validElectrons,
						  &product_type::m_TagAndProbeGenElectrons)
{
}
void TagAndProbeGenElectronProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	TagAndProbeGenLeptonProducer<KElectron>::Init(settings, metadata);
	
	validLeptonsInput = ToValidLeptonsInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidElectronsInput())));
}
std::string TagAndProbeGenElectronProducer::GetProducerId() const
{
	return "TagAndProbeGenElectronProducer";
}

TagAndProbeGenMuonProducer::TagAndProbeGenMuonProducer() :
	TagAndProbeGenLeptonProducer<KMuon>(&event_type::m_muons,
						  &product_type::m_correctedMuons,
						  &product_type::m_validMuons,
						  &product_type::m_TagAndProbeGenMuons)
{
}
void TagAndProbeGenMuonProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	TagAndProbeGenLeptonProducer<KMuon>::Init(settings, metadata);
	
	validLeptonsInput = ToValidLeptonsInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidMuonsInput())));
}
std::string TagAndProbeGenMuonProducer::GetProducerId() const
{
	return "TagAndProbeGenMuonProducer";
}

TagAndProbeGenTauProducer::TagAndProbeGenTauProducer() :
	TagAndProbeGenLeptonProducer<KTau>(&event_type::m_taus,
						  &product_type::m_correctedTaus,
						  &product_type::m_validTaus,
						  &product_type::m_TagAndProbeGenTaus)
{
}
void TagAndProbeGenTauProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	TagAndProbeGenLeptonProducer<KTau>::Init(settings, metadata);
	
	validLeptonsInput = ToValidLeptonsInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidTausInput())));
}
std::string TagAndProbeGenTauProducer::GetProducerId() const
{
	return "TagAndProbeGenTauProducer";
}
*/