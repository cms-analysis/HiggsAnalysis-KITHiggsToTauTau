
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidMuonsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief GlobalProducer, for valid muons.
   
   Required config tags in addtion to the ones of the base class:
   - MuonChargedIsoVetoConeSizeEB (default given)
   - MuonChargedIsoVetoConeSizeEE (default given)
   - MuonNeutralIsoVetoConeSize (default given)
   - MuonPhotonIsoVetoConeSizeEB (default given)
   - MuonPhotonIsoVetoConeSizeEE (default given)
   - MuonDeltaBetaIsoVetoConeSize (default given)
   - MuonChargedIsoPtThreshold (default given)
   - MuonNeutralIsoPtThreshold (default given)
   - MuonPhotonIsoPtThreshold (default given)
   - MuonDeltaBetaIsoPtThreshold (default given)
   - MuonIsoSignalConeSize
   - MuonDeltaBetaCorrectionFactor
   - MuonIsoPtSumOverPtThresholdEB
   - MuonIsoPtSumOverPtThresholdEE
*/

class HttValidMuonsProducer: public ValidMuonsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	HttValidMuonsProducer(std::vector<KDataMuon*> product_type::*validMuons=&product_type::m_validMuons,
	                      std::vector<KDataMuon*> product_type::*invalidMuons=&product_type::m_invalidMuons,
	                      std::string (setting_type::*GetMuonID)(void) const=&setting_type::GetMuonID,
	                      std::string (setting_type::*GetMuonIsoType)(void) const=&setting_type::GetMuonIsoType,
	                      std::string (setting_type::*GetMuonIso)(void) const=&setting_type::GetMuonIso,
	                      std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetMuonLowerPtCuts,
	                      std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetMuonUpperAbsEtaCuts);


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataMuon* muon, event_type const& event,
	                                product_type& product, setting_type const& settings) const  ARTUS_CPP11_OVERRIDE;

};

