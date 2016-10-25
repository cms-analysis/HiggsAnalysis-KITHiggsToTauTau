
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttMuonCorrectionsProducer.h"

#include "TLorentzVector.h"

void HttMuonCorrectionsProducer::AdditionalCorrections(KMuon* muon, event_type const& event,
                                                       product_type& product, setting_type const& settings) const
{
	MuonCorrectionsProducer::AdditionalCorrections(muon, event, product, settings);
	
	float muonEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetMuonEnergyCorrectionShift();
	if (muonEnergyCorrectionShift != 1.0)
	{
		muon->p4 = muon->p4 * muonEnergyCorrectionShift;
	}
}

