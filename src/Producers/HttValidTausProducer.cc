
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
		if(settings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().empty()) {

			int category = (int)(tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejectioncategory", event.m_tauDiscriminatorMetadata) + 0.5);
			float discriminator = tau->getDiscriminator("hpsPFTauDiscriminationByMVA3rawElectronRejection", event.m_tauDiscriminatorMetadata);

			//https://github.com/ajgilbert/ICHiggsTauTau/blob/cb76c9ec03ff3091e8ee3229ff76ec75f6ec34b8/Analysis/Utilities/src/FnPredicates.cc#L319-L329
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
		}
		else {
			int currentTauIndex = product.m_validTaus.size();
			for (std::vector<int>::const_iterator tauIndex = settings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().begin();
			     tauIndex != settings.GetTauDiscriminatorAntiElectronMvaCutsLeptonIndices().end(); ++tauIndex)
			{
				if (currentTauIndex == *tauIndex) {

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
				}
			}
		}
	}
	
	return validTau;
}

