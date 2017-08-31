
#include <Math/VectorUtil.h>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/RecoMuonInElectronConeVetoFilter.h"



bool RecoMuonInElectronConeVetoFilter::DoesEventPass(event_type const& event,
                                                     product_type const& product,
                                                     setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_muons);
	
	for (std::vector<KElectron*>::const_iterator electron = product.m_validElectrons.begin();
	     electron != product.m_validElectrons.end(); ++electron)
	{
		for (std::vector<KMuon>::const_iterator muon = event.m_muons->begin();
		     muon != event.m_muons->end(); ++muon)
		{
			if ((muon->p4.Pt() > settings.GetRecoMuonInElectronConeLowerPtCut()) &&
			    (std::abs(muon->p4.Eta()) < settings.GetRecoMuonInElectronConeUpperAbsEtaCut()) &&
			    (ROOT::Math::VectorUtil::DeltaR((*electron)->p4, muon->p4) < settings.GetRecoMuonInElectronConeSize()))
			{
				return false;
			}
		}
	}
	
	return true;
}
