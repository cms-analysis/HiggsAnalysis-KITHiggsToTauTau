
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"
#include "Artus/KappaAnalysis/interface/KappaEnumTypes.h"


/**
*/
class HttEnumTypes : public KappaEnumTypes {

public:

	enum class DecayChannel : int
	{
		NONE = -1,
		TT   = 0,
		MT   = 1,
		ET   = 2,
		EM   = 3,
		MM   = 4,
		EE   = 5,

		//Higgs produced in association with a top quark pair (TTH)
		TTH_TTE = 6,
		TTH_TTM = 7
	};
	static DecayChannel ToDecayChannel(std::string const& decayChannelString)
	{
		if (decayChannelString == "tt") return DecayChannel::TT;
		else if (decayChannelString == "mt") return DecayChannel::MT;
		else if (decayChannelString == "et") return DecayChannel::ET;
		else if (decayChannelString == "em") return DecayChannel::EM;
		else if (decayChannelString == "mm") return DecayChannel::MM;
		else if (decayChannelString == "ee") return DecayChannel::EE;
		else if (decayChannelString == "tte") return DecayChannel::TTH_TTE;
		else if (decayChannelString == "ttm") return DecayChannel::TTH_TTM;
		return DecayChannel::NONE;
	}
	
	enum class EventCategory : int
	{
		NONE                        = -1,
		
		INCLUSIVE                   = 0,
		ZERO_JET                    = 1,
		ONE_JET                     = 2,
		TWO_JET                     = 3,
		
		ZERO_JET_LOW_PT             = 11,
		ZERO_JET_MEDIUM_PT          = 12,
		ZERO_JET_HIGH_PT            = 13,
		
		ONE_JET_LOW_PT              = 21,
		ONE_JET_MEDIUM_PT           = 22,
		ONE_JET_HIGH_PT             = 23,
		ONE_JET_HIGH_PT_BOOST       = 24,
		ONE_JET_HIGH_PT_LARGE_BOOST = 25,
		
		TWO_JET_VBF                 = 31,
		TWO_JET_VBF_LOOSE           = 32,
		TWO_JET_VBF_TIGHT           = 33,

		TTH_1TAG_2JETS              = 41,
		TTH_1TAG_3JETS              = 42,
		TTH_1TAG_4JETS              = 43,
		TTH_2TAG_2JETS              = 44,
		TTH_2TAG_3JETS              = 45,
		TTH_2TAG_4JETS              = 46,
	};
	static EventCategory ToEventCategory(std::string const& eventCategory)
	{
		if (eventCategory == "inclusive") return EventCategory::INCLUSIVE;
		else if (eventCategory == "zero_jet") return EventCategory::ZERO_JET;
		else if (eventCategory == "one_jet") return EventCategory::ONE_JET;
		else if (eventCategory == "two_jet") return EventCategory::TWO_JET;
		
		else if (eventCategory == "zero_jet_low_pt") return EventCategory::ZERO_JET_LOW_PT;
		else if (eventCategory == "zero_jet_medium_pt") return EventCategory::ZERO_JET_MEDIUM_PT;
		else if (eventCategory == "zero_jet_high_pt") return EventCategory::ZERO_JET_HIGH_PT;
		
		else if (eventCategory == "one_jet_low_pt") return EventCategory::ONE_JET_LOW_PT;
		else if (eventCategory == "one_jet_medium_pt") return EventCategory::ONE_JET_MEDIUM_PT;
		else if (eventCategory == "one_jet_high_pt") return EventCategory::ONE_JET_HIGH_PT;
		else if (eventCategory == "one_jet_high_pt_boost") return EventCategory::ONE_JET_HIGH_PT_BOOST;
		else if (eventCategory == "one_jet_high_pt_large_boost") return EventCategory::ONE_JET_HIGH_PT_LARGE_BOOST;
		
		else if (eventCategory == "two_jet_vbf") return EventCategory::TWO_JET_VBF;
		else if (eventCategory == "two_jet_vbf_loose") return EventCategory::TWO_JET_VBF_LOOSE;
		else if (eventCategory == "two_jet_vbf_tight") return EventCategory::TWO_JET_VBF_TIGHT;
		
		else if (eventCategory == "tth_1tag_2jets") return EventCategory::TTH_1TAG_2JETS;
		else if (eventCategory == "tth_1tag_3jets") return EventCategory::TTH_1TAG_3JETS;
		else if (eventCategory == "tth_1tag_4jets") return EventCategory::TTH_1TAG_4JETS;
		else if (eventCategory == "tth_2tag_2jets") return EventCategory::TTH_2TAG_2JETS;
		else if (eventCategory == "tth_2tag_3jets") return EventCategory::TTH_2TAG_3JETS;
		else if (eventCategory == "tth_2tag_4jets") return EventCategory::TTH_2TAG_4JETS;
		return EventCategory::NONE;
	}
	
	enum class TauTauRestFrameReco : int
	{
		NONE  = -1,
		VISIBLE_LEPTONS = 0,
		VISIBLE_LEPTONS_MET = 1,
		COLLINEAR_APPROXIMATION  = 2,
		SVFIT  = 3,
	};
	static TauTauRestFrameReco ToTauTauRestFrameReco(std::string const& tauTauRestFrameReco)
	{
		if (tauTauRestFrameReco == "visible_leptons") return TauTauRestFrameReco::VISIBLE_LEPTONS;
		else if (tauTauRestFrameReco == "visible_leptons_met") return TauTauRestFrameReco::VISIBLE_LEPTONS_MET;
		else if (tauTauRestFrameReco == "collinear_approximation") return TauTauRestFrameReco::COLLINEAR_APPROXIMATION;
		else if (tauTauRestFrameReco == "svfit") return TauTauRestFrameReco::SVFIT;
		else return TauTauRestFrameReco::NONE;
	}
	
	enum class SystematicShift : int
	{
		NONE = -1,
		CENTRAL = 0,
		TAU_ES = 1,
	};
};

