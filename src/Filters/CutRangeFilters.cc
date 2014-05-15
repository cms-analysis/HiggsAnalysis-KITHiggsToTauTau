
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/CutRangeFilters.h"


std::string LeptonsPtCutFilter::GetFilterId() const
{
	return "leptons_pt_cut";
}

void LeptonsPtCutFilter::InitGlobal(global_setting_type const& globalSettings)
{
	CutRangeFilterBase<HttTypes>::InitGlobal(globalSettings);
	Init(globalSettings.GetLowerCutHardLepPt());
}

void LeptonsPtCutFilter::InitLocal(setting_type const& settings)
{
	CutRangeFilterBase<HttTypes>::InitLocal(settings);
	Init(settings.GetLowerCutHardLepPt());
}

void LeptonsPtCutFilter::Init(float const& lowerCutHardLepPt)
{
	m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[0]->Pt(); },
			CutRange::LowerThresholdCut(lowerCutHardLepPt)
	));
}

