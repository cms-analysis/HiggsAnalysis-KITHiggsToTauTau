
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"


/**
*/
class HttEnumTypes {

public:

	enum class DecayChannel : int
	{
		NONE = -1,
		TT   = 0,
		MT   = 1,
		ET   = 2,
		EM   = 3,
		MM   = 4,
		EE   = 5
	};
	static DecayChannel ToDecayChannel(std::string const& decayChannelString)
	{
		if (decayChannelString == "tt") return DecayChannel::TT;
		else if (decayChannelString == "mt") return DecayChannel::MT;
		else if (decayChannelString == "et") return DecayChannel::ET;
		else if (decayChannelString == "em") return DecayChannel::EM;
		else if (decayChannelString == "mm") return DecayChannel::MM;
		else if (decayChannelString == "ee") return DecayChannel::EE;
		return DecayChannel::NONE;
	}
	
	enum class EventCategory : int
	{
		NONE                  = -1,
		
		INCLUSIVE             = 0,
		ZERO_JET              = 1,
		ONE_JET               = 2,
		TWO_JET               = 3,
		
		ZERO_JET_LOW_PT       = 4,
		ZERO_JET_HIGH_PT      = 5,
		ONE_JET_LOW_PT        = 6,
		ONE_JET_HIGH_PT       = 7,
		ONE_JET_HIGH_PT_BOOST = 8,
		ONE_JET_BOOST         = 9,
		ONE_JET_LARGE_BOOST   = 10,
		TWO_JET_VBF           = 11,
		TWO_JET_VBF_LOOSE     = 12,
		TWO_JET_VBF_TIGHT     = 13,
	};
	static EventCategory ToEventCategory(std::string const& eventCategory)
	{
		if (eventCategory == "inclusive") return EventCategory::INCLUSIVE;
		else if (eventCategory == "zero_jet") return EventCategory::ZERO_JET;
		else if (eventCategory == "one_jet") return EventCategory::ONE_JET;
		else if (eventCategory == "two_jet") return EventCategory::TWO_JET;
		
		else if (eventCategory == "zero_jet_low_pt") return EventCategory::ZERO_JET_LOW_PT;
		else if (eventCategory == "zero_jet_high_pt") return EventCategory::ZERO_JET_HIGH_PT;
		else if (eventCategory == "one_jet_low_pt") return EventCategory::ONE_JET_LOW_PT;
		else if (eventCategory == "one_jet_high_pt") return EventCategory::ONE_JET_HIGH_PT;
		else if (eventCategory == "one_jet_high_pt_boost") return EventCategory::ONE_JET_HIGH_PT_BOOST;
		else if (eventCategory == "one_jet_boost") return EventCategory::ONE_JET_BOOST;
		else if (eventCategory == "one_jet_large_boost") return EventCategory::ONE_JET_LARGE_BOOST;
		else if (eventCategory == "two_jet_vbf") return EventCategory::TWO_JET_VBF;
		else if (eventCategory == "two_jet_vbf_loose") return EventCategory::TWO_JET_VBF_LOOSE;
		else if (eventCategory == "two_jet_vbf_tight") return EventCategory::TWO_JET_VBF_TIGHT;
		
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
	};
	static SystematicShift ToSystematicShift(std::string const& systematicShift)
	{
		if (systematicShift == "central") return SystematicShift::CENTRAL;
		else return SystematicShift::NONE;
	}
};

