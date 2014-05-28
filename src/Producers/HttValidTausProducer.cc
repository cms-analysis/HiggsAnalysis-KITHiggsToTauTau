
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"


void HttValidTausProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidTausProducer::InitGlobal(globalSettings);
	
	tauDiscriminatorIsolationCut = globalSettings.GetTauDiscriminatorIsolationCut();
	tauDiscriminatorAntiElectronMvaCuts = globalSettings.GetTauDiscriminatorAntiElectronMvaCuts();
	tauDiscriminatorAntiElectronMvaCutsLeptonIndices = globalSettings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices();
}

void HttValidTausProducer::InitLocal(setting_type const& settings)
{
	ValidTausProducer::InitLocal(settings);
	
	tauDiscriminatorIsolationCut = settings.GetTauDiscriminatorIsolationCut();
	tauDiscriminatorAntiElectronMvaCuts = settings.GetTauDiscriminatorAntiElectronMvaCuts();
	tauDiscriminatorAntiElectronMvaCutsLeptonIndices = settings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices();
}

bool HttValidTausProducer::AdditionalCriteria(KDataPFTau* tau,
                                              event_type const& event,
                                              product_type& product) const
{
	bool validTau = ValidTausProducer::AdditionalCriteria(tau, event, product);
	
	double isolationPtSum = tau->getDiscriminator("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits", event.m_tauDiscriminatorMetadata);
	double isolationPtSumOverPt = isolationPtSum / tau->p4.Pt();
	
	product.m_leptonIsolation[tau] = isolationPtSum;
	product.m_leptonIsolationOverPt[tau] = isolationPtSumOverPt;
	
	// custom isolation cut
	validTau = validTau && isolationPtSum < tauDiscriminatorIsolationCut;
	
	// custom electron rejection
	if (validTau && (! tauDiscriminatorAntiElectronMvaCuts.empty())) {
		if(tauDiscriminatorAntiElectronMvaCutsLeptonIndices.empty()) {
			validTau = validTau && tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejection", event.m_tauDiscriminatorMetadata) > tauDiscriminatorAntiElectronMvaCuts[tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejectioncategory", event.m_tauDiscriminatorMetadata)];
		}
		else {
			int currentTauIndex = product.m_validTaus.size();
			for (std::vector<int>::const_iterator tauIndex = tauDiscriminatorAntiElectronMvaCutsLeptonIndices.begin();
			     tauIndex != tauDiscriminatorAntiElectronMvaCutsLeptonIndices.end(); ++tauIndex)
			{
				if (currentTauIndex == *tauIndex) {
					validTau = validTau && tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejection", event.m_tauDiscriminatorMetadata) > tauDiscriminatorAntiElectronMvaCuts[tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejectioncategory", event.m_tauDiscriminatorMetadata)];
				}
			}
		}
	}
	
	return validTau;
}

