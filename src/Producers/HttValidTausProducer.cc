
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"


bool HttValidTausProducer::AdditionalCriteria(KDataPFTau* tau,
                                              event_type const& event, product_type& product,
                                              setting_type const& settings) const
{
	bool validTau = ValidTausProducer<HttTypes>::AdditionalCriteria(tau, event, product, settings);
	
	double isolationPtSum = tau->getDiscriminator("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits", event.m_tauDiscriminatorMetadata);
	double isolationPtSumOverPt = isolationPtSum / tau->p4.Pt();
	
	product.m_leptonIsolation[tau] = isolationPtSum;
	product.m_leptonIsolationOverPt[tau] = isolationPtSumOverPt;
	
	// custom isolation cut
	validTau = validTau && isolationPtSum < settings.GetTauDiscriminatorIsolationCut();
	
	// custom electron rejection
	if (validTau && (! settings.GetTauDiscriminatorAntiElectronMvaCuts().empty())) {
		if(settings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().empty())
		{
			validTau = validTau && ApplyCustomElectronRejection(tau, event, settings);
		}
		else {
			int currentTauIndex = product.m_validTaus.size();
			for (std::vector<int>::const_iterator tauIndex = settings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().begin();
			     tauIndex != settings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().end(); ++tauIndex)
			{
				if (currentTauIndex == *tauIndex)
				{
					validTau = validTau && ApplyCustomElectronRejection(tau, event, settings);
				}
			}
		}
	}
	
	// remove taus which overlap with electrons and muons in a DeltaR cone
	for (std::vector<KDataElectron*>::const_iterator electron = product.m_validElectrons.begin(); validTau && electron != product.m_validElectrons.end(); ++electron)
		{
			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*electron)->p4) > settings.GetTauElectronLowerDeltaRCut();
		}
	for (std::vector<KDataMuon*>::const_iterator muon = product.m_validMuons.begin(); validTau && muon != product.m_validMuons.end(); ++muon)
		{
			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*muon)->p4) > settings.GetTauMuonLowerDeltaRCut();
		}

	// cut on impact parameters of track
	validTau = validTau
	                && (settings.GetTauTrackDzCut() <= 0.0 || std::abs(tau->track.getDz(&event.m_vertexSummary->pv)) < settings.GetTauTrackDzCut());

	return validTau;
}


bool HttValidTausProducer::ApplyCustomElectronRejection(KDataPFTau* tau, event_type const& event,
	                                                    setting_type const& settings) const
{
	bool validTau = true;

	// cut designed to suppress a spike in the tau eta distribution when using the MVA3 discriminator
	float zImpact = tau->track.ref.z() + (130. / tan(tau->p4.Theta()));

	if (zImpact > settings.GetTauLowerZImpactCut() && zImpact < settings.GetTauUpperZImpactCut())
	{
		validTau = validTau && false;
		return validTau;
	}

	int category = (int)(tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejectioncategory", event.m_tauDiscriminatorMetadata) + 0.5);
	float discriminator = tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejection", event.m_tauDiscriminatorMetadata);

	if (category < 0)
	{
		validTau = validTau && false;
	}
	else if (category > 15)
	{
		validTau = validTau && true;
	}
	else {
		validTau = validTau && discriminator > settings.GetTauDiscriminatorAntiElectronMvaCuts()[category];
	}
	
	return validTau;
}

