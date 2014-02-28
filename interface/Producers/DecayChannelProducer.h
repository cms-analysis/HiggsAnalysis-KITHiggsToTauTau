
#pragma once

#include "Artus/Utility/interface/EnumHelper.h"

#include "../HttTypes.h"


class DecayChannelProducer: public HttGlobalProducerBase {
public:

	virtual std::string GetProducerId() ARTUS_CPP11_OVERRIDE {
		return "decay_channels";
	}
	
	DecayChannelProducer() : HttGlobalProducerBase() {};

	virtual bool ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE
	{
		
		product.m_decayChannel = DecayChannel::NONE;
		
		RMDataLV* lepton1 = 0;
		RMDataLV* lepton2 = 0;
		
		// just for testing
		// TODO: need to make use of trigger decisions
		size_t nElectrons = product.m_validElectrons.size();
		size_t nMuons = product.m_validMuons.size();
		size_t nTaus = product.m_validTaus.size();
		
		if(nTaus >= 2) {
			lepton1 = &(product.m_validTaus[0]->p4);
			lepton2 = &(product.m_validTaus[1]->p4);
			product.m_decayChannel = DecayChannel::TT;
		}
		else if(nTaus == 1) {
			lepton2 = &(product.m_validTaus[0]->p4);
			if(nMuons >= 1) {
				lepton1 = &(product.m_validMuons[0]->p4);
				product.m_decayChannel = DecayChannel::MT;
			}
			else if(nElectrons >= 1) {
				lepton1 = &(product.m_validElectrons[0]->p4);
				product.m_decayChannel = DecayChannel::ET;
			}
		}
		else {
			if(nMuons >= 2) {
				lepton1 = &(product.m_validMuons[0]->p4);
				lepton2 = &(product.m_validMuons[1]->p4);
				product.m_decayChannel = DecayChannel::MM;
			}
			else if(nMuons >= 1 && nElectrons >= 1) {
				lepton1 = &(product.m_validElectrons[0]->p4);
				lepton2 = &(product.m_validMuons[0]->p4);
				product.m_decayChannel = DecayChannel::EM;
			}
			else if(nElectrons >= 2) {
				lepton1 = &(product.m_validElectrons[0]->p4);
				lepton2 = &(product.m_validElectrons[1]->p4);
				product.m_decayChannel = DecayChannel::EE;
			}
		}
		
		if(product.m_decayChannel != DecayChannel::NONE) {
			// fill p4 pointers ordered by pt
			if(lepton1->Pt() >= lepton2->Pt()) {
				product.m_ptOrderedLeptons.push_back(lepton1);
				product.m_ptOrderedLeptons.push_back(lepton2);
			}
			else {
				product.m_ptOrderedLeptons.push_back(lepton2);
				product.m_ptOrderedLeptons.push_back(lepton1);
			}
			
			// fill p4 pointers ordered by flavour (according to channel name)
			product.m_flavourOrderedLeptons.push_back(lepton1);
			product.m_flavourOrderedLeptons.push_back(lepton2);
		}
		
		std::cout << EnumHelper::toUnderlyingValue(product.m_decayChannel) << std::endl;
		
		return true;
	}
};


