
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTriggerSettingsProducer.h"

HttTriggerSettingsProducer::HttTriggerSettingsProducer() :
	ProducerBase<HttTypes>()
{
	
}
	
std::string HttTriggerSettingsProducer::GetProducerId() const
{
	return "HttTriggerSettingsProducer";
}

void HttTriggerSettingsProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	m_decayChannel = HttEnumTypes::ToDecayChannel(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetChannel())));
	
	m_electronTriggerFiltersByIndex = Utility::ParseMapTypes<size_t, std::string>(Utility::ParseVectorToMap(settings.GetElectronTriggerFilterNames()), m_electronTriggerFiltersByHltName);
	m_muonTriggerFiltersByIndex = Utility::ParseMapTypes<size_t, std::string>(Utility::ParseVectorToMap(settings.GetMuonTriggerFilterNames()), m_muonTriggerFiltersByHltName);
	m_tauTriggerFiltersByIndex = Utility::ParseMapTypes<size_t, std::string>(Utility::ParseVectorToMap(settings.GetTauTriggerFilterNames()), m_tauTriggerFiltersByHltName);
	m_jetTriggerFiltersByIndex = Utility::ParseMapTypes<size_t, std::string>(Utility::ParseVectorToMap(settings.GetJetTriggerFilterNames()), m_jetTriggerFiltersByHltName);
}

void HttTriggerSettingsProducer::Produce(event_type const& event, product_type& product,
                                         setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_eventInfo);

	product.m_settingsHltPaths.clear();
	
	product.m_settingsElectronTriggerFiltersByIndex.clear();
	product.m_settingsMuonTriggerFiltersByIndex.clear();
	product.m_settingsTauTriggerFiltersByIndex.clear();
	product.m_settingsJetTriggerFiltersByIndex.clear();
	
	product.m_settingsElectronTriggerFiltersByHltName.clear();
	product.m_settingsMuonTriggerFiltersByHltName.clear();
	product.m_settingsTauTriggerFiltersByHltName.clear();
	product.m_settingsJetTriggerFiltersByHltName.clear();

	uint64_t run = event.m_eventInfo->nRun;

	// https://github.com/ajgilbert/ICHiggsTauTau/blob/master/Analysis/HiggsTauTau/src/HTTTriggerFilter.cc
	if (m_decayChannel == HttEnumTypes::DecayChannel::MT)
	{
		if (run >= 190456 && run <= 193751)
		{
			std::string hltPath("HLT_IsoMu18_eta2p1_LooseIsoPFTau20");
		
			if (Utility::Contains(settings.GetHltPaths(), hltPath))
			{
				product.m_settingsHltPaths.push_back(hltPath);
			}
			
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_muonTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f18QL3crIsoFiltered10")))
			{
				product.m_settingsMuonTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f18QL3crIsoFiltered10");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltPFTau20IsoMuVertex")))
			{
				product.m_settingsTauTriggerFiltersByHltName[""] = std::vector<std::string>(1, "hltPFTau20IsoMuVertex");
			}
		}
		else if (run >= 193752)
		{
			std::string hltPath("HLT_IsoMu17_eta2p1_LooseIsoPFTau20");
			if (Utility::Contains(settings.GetHltPaths(), hltPath))
			{
				product.m_settingsHltPaths.push_back("HLT_IsoMu17_eta2p1_LooseIsoPFTau20");
			}
			
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_muonTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltL3crIsoL1sMu14erORMu16erL1f0L2f14QL3f17QL3crIsoRhoFiltered0p15")))
			{
				product.m_settingsMuonTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltL3crIsoL1sMu14erORMu16erL1f0L2f14QL3f17QL3crIsoRhoFiltered0p15");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltIsoMuPFTau20TrackLooseIso")))
			{
				product.m_settingsTauTriggerFiltersByHltName[hltPath] = std::vector<std::string>(1, "hltIsoMuPFTau20TrackLooseIso");
			}
		}
	}
	
	else if (m_decayChannel == HttEnumTypes::DecayChannel::ET)
	{
		if (run >= 190456 && run <= 193751)
		{
			std::string hltPath("HLT_Ele20_CaloIdVT_CaloIsoRhoT_TrkIdT_TrkIsoT_LooseIsoPFTau20");
			if (Utility::Contains(settings.GetHltPaths(), hltPath))
			{
				product.m_settingsHltPaths.push_back("HLT_Ele20_CaloIdVT_CaloIsoRhoT_TrkIdT_TrkIsoT_LooseIsoPFTau20");
			}
			
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_electronTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltEle20CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilterL1IsoEG18OrEG20")))
			{
				product.m_settingsElectronTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltEle20CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilterL1IsoEG18OrEG20");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltPFTauIsoEleVertex20")))
			{
				product.m_settingsTauTriggerFiltersByHltName[hltPath] = std::vector<std::string>(1, "hltPFTauIsoEleVertex20");
			}
		}
		else if (run >= 193752)
		{
			std::string hltPath("HLT_Ele22_eta2p1_WP90Rho_LooseIsoPFTau20");
			if (Utility::Contains(settings.GetHltPaths(), hltPath))
			{
				product.m_settingsHltPaths.push_back("HLT_Ele22_eta2p1_WP90Rho_LooseIsoPFTau20");
			}
			
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_electronTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltEle22WP90RhoTrackIsoFilter")))
			{
				product.m_settingsElectronTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltEle22WP90RhoTrackIsoFilter");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltIsoElePFTau20TrackLooseIso")))
			{
				product.m_settingsTauTriggerFiltersByHltName[hltPath] = std::vector<std::string>(1, "hltIsoElePFTau20TrackLooseIso");
			}
		}
	}
	
	else if (m_decayChannel == HttEnumTypes::DecayChannel::EM)
	{
		std::string hltPath;
		
		hltPath = "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL";
		if (run >= 190456 && run <= 191690)
		{
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_electronTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltMu8Ele17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter")))
			{
				product.m_settingsElectronTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltMu8Ele17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltL1MuOpenEG12L3Filtered8")))
			{
				product.m_settingsTauTriggerFiltersByHltName[hltPath] = std::vector<std::string>(1, "hltL1MuOpenEG12L3Filtered8");
			}
		}
		else if (run >= 191691)
		{
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_electronTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltMu8Ele17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter")))
			{
				product.m_settingsElectronTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltMu8Ele17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8")))
			{
				product.m_settingsTauTriggerFiltersByHltName[hltPath] = std::vector<std::string>(1, "hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8");
			}
		}
		
		hltPath = "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL";
		if (run >= 190456 && run <= 193751)
		{
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_electronTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter")))
			{
				product.m_settingsElectronTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltL1Mu12EG7L3MuFiltered17")))
			{
				product.m_settingsTauTriggerFiltersByHltName[hltPath] = std::vector<std::string>(1, "hltL1Mu12EG7L3MuFiltered17");
			}
		}
		else if (run >= 193752)
		{
			std::vector<std::string> filters;
			filters = SafeMap::GetWithDefault(m_electronTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter")))
			{
				product.m_settingsElectronTriggerFiltersByHltName[hltPath] =
						std::vector<std::string>(1, "hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter");
			}
			
			filters = SafeMap::GetWithDefault(m_tauTriggerFiltersByHltName, hltPath, std::vector<std::string>());
			if (Utility::Contains(filters, std::string("hltL1Mu12EG7L3MuFiltered17")))
			{
				product.m_settingsTauTriggerFiltersByHltName[hltPath] = std::vector<std::string>(1, "hltL1Mu12EG7L3MuFiltered17");
			}
		}
	}
}
