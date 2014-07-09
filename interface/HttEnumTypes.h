
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
		if (decayChannelString == "TT") return DecayChannel::TT;
		else if (decayChannelString == "MT") return DecayChannel::MT;
		else if (decayChannelString == "ET") return DecayChannel::ET;
		else if (decayChannelString == "EM") return DecayChannel::EM;
		else if (decayChannelString == "MM") return DecayChannel::MM;
		else if (decayChannelString == "EE") return DecayChannel::EE;
		return DecayChannel::NONE;
	}
	
	enum class EventCategory : int
	{
		NONE      = -1,
		INCLUSIVE = 0,
		ZERO_JET  = 1,
		BOOST     = 2,
		VBF       = 3
	};
	static EventCategory ToEventCategory(std::string const& eventCategoryString)
	{
		if (eventCategoryString == "INCLUSIVE") return EventCategory::INCLUSIVE;
		else if (eventCategoryString == "ZERO_JET") return EventCategory::ZERO_JET;
		else if (eventCategoryString == "BOOST") return EventCategory::BOOST;
		else if (eventCategoryString == "VBF") return EventCategory::VBF;
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

