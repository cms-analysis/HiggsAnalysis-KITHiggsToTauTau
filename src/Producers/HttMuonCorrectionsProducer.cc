
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttMuonCorrectionsProducer.h"


void HttMuonCorrectionsProducer::Init(setting_type const& settings)
{
	MuonCorrectionsProducer::Init(settings);
	
	muonEnergyCorrection = ToMuonEnergyCorrection(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(static_cast<HttSettings const&>(settings).GetMuonEnergyCorrection())));
}

void HttMuonCorrectionsProducer::AdditionalCorrections(KMuon* muon, event_type const& event,
                                                       product_type& product, setting_type const& settings) const
{
	MuonCorrectionsProducer::AdditionalCorrections(muon, event, product, settings);
	
	if (muonEnergyCorrection == MuonEnergyCorrection::FALL2015)
	{
	        muon->p4 = muon->p4 * (1.0);
	}
	else if (muonEnergyCorrection != MuonEnergyCorrection::NONE)
	{
		LOG(FATAL) << "Muon energy correction of type " << Utility::ToUnderlyingValue(muonEnergyCorrection) << " not yet implemented!";
	}
	
	float muonEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetMuonEnergyCorrectionShift();
	if (muonEnergyCorrectionShift != 1.0)
	{
		muon->p4 = muon->p4 * muonEnergyCorrectionShift;
	}
}

