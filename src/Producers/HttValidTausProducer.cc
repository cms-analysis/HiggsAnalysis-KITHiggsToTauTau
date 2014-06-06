
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

			int category = (int)(tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejectioncategory", event.m_tauDiscriminatorMetadata) + 0.5);
			float discriminator = tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejection", event.m_tauDiscriminatorMetadata);

			//https://github.com/ajgilbert/ICHiggsTauTau/blob/cb76c9ec03ff3091e8ee3229ff76ec75f6ec34b8/Analysis/Utilities/src/FnPredicates.cc#L319-L329
			if (category < 0)
				validTau = validTau && false;
			else if (category > 15)
				validTau = validTau && true;
			else 
				validTau = validTau && discriminator > tauDiscriminatorAntiElectronMvaCuts[category];
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

