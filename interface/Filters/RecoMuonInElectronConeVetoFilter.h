
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
	
	virtual std::string GetFilterId() const override {
		return "RecoMuonInElectronConeVetoFilter";
	}

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
							   setting_type const& settings, metadata_type const& metadata) const override;

};

