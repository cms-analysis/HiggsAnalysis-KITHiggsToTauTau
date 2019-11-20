
#pragma once


#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/regex.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Filter the events where the dilepton pair is likely to come from a Z boson decay
 */
class ZBosonVetoFilter: public FilterBase<HttTypes> {
public:

	virtual std::string GetFilterId() const override {
			return "ZBosonVetoFilter";
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
				   setting_type const& settings, metadata_type const& metadata) const override;

private:

	enum class ZBosonVetoType : int
	{
		NONE  = -1,
		HF = 0,
		LF = 1
	};

	static ZBosonVetoType ToZBosonVetoType(std::string const& vetoType)
	{
		if (vetoType == "heavyflavor") return ZBosonVetoType::HF;
		else if (vetoType == "lightflavor") return ZBosonVetoType::LF;
		else return ZBosonVetoType::NONE;
	}

	ZBosonVetoType vetoType;
};
