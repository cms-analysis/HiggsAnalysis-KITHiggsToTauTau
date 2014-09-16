
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"
#include <iostream>

bool HttValidTausProducer::AdditionalCriteria(KDataPFTau* tau,
                                              event_type const& event, product_type& product,
                                              setting_type const& settings) const
{
	bool validTau = ValidTausProducer<HttTypes>::AdditionalCriteria(tau, event, product, settings);

// are applied anyway	
// 	// isolation cut
// 	double isolationPtSumOverPt = tau->getDiscriminator("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits", event.m_tauDiscriminatorMetadata) / tau->p4.Pt();
// 	std::cout << "old isolation raw " << isolationPtSumOverPt << std::endl;
// 	int iso = (int)(tau->hasID("hpsPFTauDiscriminationByTightIsolationMVA3oldDMwLT", event.m_tauDiscriminatorMetadata));
// 	std::cout << "isolation discrimator " << iso << " " << tau->hasID("hpsPFTauDiscriminationByTightIsolationMVA3oldDMwLT", event.m_tauDiscriminatorMetadata) << std::endl;

// 	validTau = validTau && iso>0.5;

// 	// against muon
// 	int againstMuons = (int)(tau->hasID("hpsPFTauDiscriminationByMVAMediumMuonRejection", event.m_tauDiscriminatorMetadata));
// 	std::cout << "against muons discrimator " << againstMuons << " " << tau->hasID("hpsPFTauDiscriminationByMVAMediumMuonRejection", event.m_tauDiscriminatorMetadata) << std::endl;

// 	// against electrons
// 	int againstElectrons = (int)(tau->hasID("hpsPFTauDiscriminationByLooseElectronRejection", event.m_tauDiscriminatorMetadata));
// 	std::cout << "against electrons discrimator " << againstElectrons << " " << tau->hasID("hpsPFTauDiscriminationByLooseElectronRejection", event.m_tauDiscriminatorMetadata) << std::endl;
	

// 	// remove taus which overlap with electrons and muons in a DeltaR cone
// 	for (std::vector<KDataElectron*>::const_iterator electron = product.m_validElectrons.begin(); validTau && electron != product.m_validElectrons.end(); ++electron)
// 		{
// 			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*electron)->p4) > settings.GetTauElectronLowerDeltaRCut();
// 		}
// 	for (std::vector<KDataMuon*>::const_iterator muon = product.m_validMuons.begin(); validTau && muon != product.m_validMuons.end(); ++muon)
// 		{
// 			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*muon)->p4) > settings.GetTauMuonLowerDeltaRCut();
// 		}

	// cut on impact parameters of track
	validTau = validTau
	                && (settings.GetTauTrackDzCut() <= 0.0 || std::abs(tau->track.getDz(&event.m_vertexSummary->pv)) < settings.GetTauTrackDzCut());

	return validTau;
}


