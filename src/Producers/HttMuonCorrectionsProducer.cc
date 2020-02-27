
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <TRandom3.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttMuonCorrectionsProducer.h"

#include "TLorentzVector.h"

void HttMuonCorrectionsProducer::AdditionalCorrections(KMuon* muon, event_type const& event,
                                                       product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	MuonCorrectionsProducer::AdditionalCorrections(muon, event, product, settings, metadata);

	// Systematic Uncertainty for Muon Energy Scale
	float muonEnergyCorrectionShift = 1.0;
	if ( TMath::Abs(muon->p4.Eta()) > 0.4 &&  TMath::Abs(muon->p4.Eta()) < 1.2)
	{
		muonEnergyCorrectionShift += static_cast<HttSettings const&>(settings).GetMuonEnergyCorrectionShiftEta0p4to1p2();
	}
	else if ( TMath::Abs(muon->p4.Eta()) > 1.2 &&  TMath::Abs(muon->p4.Eta()) < 2.1)
	{
		muonEnergyCorrectionShift += static_cast<HttSettings const&>(settings).GetMuonEnergyCorrectionShiftEta1p2to2p1();
	}
	else if ( TMath::Abs(muon->p4.Eta()) > 2.1)
	{
		muonEnergyCorrectionShift += static_cast<HttSettings const&>(settings).GetMuonEnergyCorrectionShiftEtaGt2p1();
	}
	if (muonEnergyCorrectionShift != 1.0)
	{
		muon->p4 = muon->p4 * muonEnergyCorrectionShift;
	}

	float randomMuonEnergySmearing = static_cast<HttSettings const&>(settings).GetRandomMuonEnergySmearing();
	if (randomMuonEnergySmearing != 0.0)
	{
		double r;
		TRandom *r3 = new TRandom3();
		r3->SetSeed(event.m_eventInfo->nEvent);
		r = (1.0+r3->Gaus(0.0,randomMuonEnergySmearing));
		muon->p4 = muon->p4 * r;
	}
}
