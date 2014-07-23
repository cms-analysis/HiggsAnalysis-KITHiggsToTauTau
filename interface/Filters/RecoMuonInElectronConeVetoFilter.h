
#pragma once

#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


/** Filter for Veto on reco muon (without ID requirement) withing electron cone
 *  Required config tags:
 *  - RecoMuonInElectronConeLowerPtCut
 *  - RecoMuonInElectronConeUpperAbsEtaCut
 *  - RecoMuonInElectronConeSize
 */
class RecoMuonInElectronConeVetoFilter: public FilterBase<HttTypes> {
public:
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
			return "reco_muon_in_electron_cone_veto";
	}

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
							   setting_type const& settings) const ARTUS_CPP11_OVERRIDE;

};

