
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"


bool HttValidTausProducer::AdditionalCriteria(KTau* tau,
                                              event_type const& event, product_type& product,
                                              setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_tauMetadata);
	assert(event.m_vertexSummary);
	
	HttProduct& specProduct = static_cast<HttProduct&>(product);
	HttSettings const& specSettings = static_cast<HttSettings const&>(settings);

	bool validTau = ValidTausProducer::AdditionalCriteria(tau, event, product, settings, metadata);
	
	double isolationPtSum = tau->getDiscriminator(specSettings.GetTauDiscriminatorIsolationName(), event.m_tauMetadata);
	double isolationPtSumOverPt = isolationPtSum / tau->p4.Pt();
	
	specProduct.m_leptonIsolation[tau] = isolationPtSum;
	specProduct.m_leptonIsolationOverPt[tau] = isolationPtSumOverPt;
	specProduct.m_tauIsolation[tau] = isolationPtSum;
	specProduct.m_tauIsolationOverPt[tau] = isolationPtSumOverPt;
	
	// custom isolation cut
	validTau = validTau && ((isolationPtSum < specSettings.GetTauDiscriminatorIsolationCut()) ? settings.GetDirectIso() : (!settings.GetDirectIso()));
	
	// custom tau isolation based on BDT
	if (validTau && (! specSettings.GetTauDiscriminatorMvaIsolation().empty())) {
		int currentTauIndex = product.m_validTaus.size();
		for (std::map<size_t, std::vector<float> >::const_iterator MvaIsolationCutByIndex = MvaIsolationCutsByIndex.begin(); MvaIsolationCutByIndex != MvaIsolationCutsByIndex.end(); ++MvaIsolationCutByIndex)
		{
			if (currentTauIndex == (int) MvaIsolationCutByIndex->first)
			{
				validTau = validTau && ApplyCustomMvaIsolationCut(tau, event, MvaIsolationCutByIndex->second);
			}
		}
	}
	
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
	for (std::vector<KElectron*>::const_iterator electron = product.m_validElectrons.begin(); validTau && electron != product.m_validElectrons.end(); ++electron)
		{
			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*electron)->p4) > specSettings.GetTauElectronLowerDeltaRCut();
		}
	for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); validTau && muon != product.m_validMuons.end(); ++muon)
		{
			validTau = validTau && ROOT::Math::VectorUtil::DeltaR(tau->p4, (*muon)->p4) > specSettings.GetTauMuonLowerDeltaRCut();
		}

	// cut on impact parameters of track
	validTau = validTau
	                && (specSettings.GetTauTrackDzCut() <= 0.0 || std::abs(tau->track.getDz(&event.m_vertexSummary->pv)) < specSettings.GetTauTrackDzCut());

	// cut on the pT of the leading tau track
	if (specSettings.GetTauLeadingTrackPtCut() >= 0.0)
		validTau = validTau && tau->chargedHadronCandidates.size() > 0 && tau->chargedHadronCandidates[0].p4.Pt() > specSettings.GetTauLeadingTrackPtCut();

	// cut on the tau track multiplicity
	validTau = validTau && (specSettings.GetTauTrackMultiplicityCut() <= 0.0 || tau->chargedHadronCandidates.size() <= specSettings.GetTauTrackMultiplicityCut());

	return validTau;
}


bool HttValidTausProducer::ApplyCustomMvaIsolationCut(KTau* tau, event_type const& event,
	                                              std::vector<float> MvaIsolationCuts) const
{
	bool validTau = true;

	float discriminator = tau->getDiscriminator("hpsPFTauDiscriminationByIsolationMVA2raw", event.m_tauMetadata);

	validTau = validTau && discriminator > *std::max_element(MvaIsolationCuts.begin(), MvaIsolationCuts.end());
	
	return validTau;
}


bool HttValidTausProducer::ApplyCustomElectronRejection(KTau* tau, event_type const& event,
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

	int category = (int)(tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejectioncategory", event.m_tauMetadata) + 0.5);
	float discriminator = tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejection", event.m_tauMetadata);

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

