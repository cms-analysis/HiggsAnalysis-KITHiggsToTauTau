
#pragma once

#include "Artus/Filter/interface/CutFilterBase.h"

#include "../HttTypes.h"


/** Cut Filter: product.m_ptOrderedLeptons[0]->Pt() > settings.GetLowerCutHardLepPt()
 *  Required config tag: LowerCutHardLepPt
 */
class LeptonsPtCutFilter: public CutRangeFilterBase<HttTypes> {
public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE;
	virtual void InitGlobal(global_setting_type const& globalSettings) ARTUS_CPP11_OVERRIDE;
	virtual void InitLocal(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

private:
	void Init(float const& lowerCutHardLepPt);
};


