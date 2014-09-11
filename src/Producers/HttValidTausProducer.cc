
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"


bool HttValidTausProducer::AdditionalCriteria(KDataPFTau* tau,
                                              KappaEvent const& event, KappaProduct& product,
                                              KappaSettings const& settings) const
{
	HttProduct& specProduct = static_cast<HttProduct&>(product);
	HttSettings const& specSettings = static_cast<HttSettings const&>(settings);

	bool validTau = ValidTausProducer::AdditionalCriteria(tau, event, product, settings);
	
	double isolationPtSum = tau->getDiscriminator("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits", event.m_tauDiscriminatorMetadata);
	double isolationPtSumOverPt = isolationPtSum / tau->p4.Pt();
	
	specProduct.m_leptonIsolation[tau] = isolationPtSum;
	specProduct.m_leptonIsolationOverPt[tau] = isolationPtSumOverPt;
	
	// custom isolation cut
	validTau = validTau && isolationPtSum < specSettings.GetTauDiscriminatorIsolationCut();
	
	// custom electron rejection
	if (validTau && (! specSettings.GetTauDiscriminatorAntiElectronMvaCuts().empty())) {
		if(specSettings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().empty())
		{
			validTau = validTau && ApplyCustomElectronRejection(tau, event, specSettings);
		}
		else {
			int currentTauIndex = product.m_validTaus.size();
			for (std::vector<int>::const_iterator tauIndex = specSettings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().begin();
			     tauIndex != specSettings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().end(); ++tauIndex)
			{
				if (currentTauIndex == *tauIndex)
				{
					validTau = validTau && ApplyCustomElectronRejection(tau, event, specSettings);
				}
			}
		}
	}
	
	// remove taus which overlap with electrons and muons in a DeltaR cone
	for (std::vector<KDataElectron*>::const_iterator electron = product.m_validElectrons.begin(); validTau && electron != product.m_validElectrons.end(); ++electron)
		{
			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*electron)->p4) > specSettings.GetTauElectronLowerDeltaRCut();
		}
	for (std::vector<KDataMuon*>::const_iterator muon = product.m_validMuons.begin(); validTau && muon != product.m_validMuons.end(); ++muon)
		{
			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*muon)->p4) > specSettings.GetTauMuonLowerDeltaRCut();
		}

	// cut on impact parameters of track
	validTau = validTau
	                && (specSettings.GetTauTrackDzCut() <= 0.0 || std::abs(tau->track.getDz(&event.m_vertexSummary->pv)) < specSettings.GetTauTrackDzCut());

	return validTau;
}


bool HttValidTausProducer::ApplyCustomElectronRejection(KDataPFTau* tau, KappaEvent const& event,
	                                                    HttSettings const& settings) const
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

