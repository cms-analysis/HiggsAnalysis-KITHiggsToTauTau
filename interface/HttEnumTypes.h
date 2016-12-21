
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
	
	enum class DataMcScaleFactorProducerMode : int
	{
		NONE  = -1,
		MULTIPLY_WEIGHTS = 0,
		CORRELATE_TRIGGERS = 1,
	};
	static DataMcScaleFactorProducerMode ToDataMcScaleFactorProducerMode(std::string const& dataMcScaleFactorProducerMode)
	{
		if (dataMcScaleFactorProducerMode == "multiply_weights") return DataMcScaleFactorProducerMode::MULTIPLY_WEIGHTS;
		else if (dataMcScaleFactorProducerMode == "correlate_triggers") return DataMcScaleFactorProducerMode::CORRELATE_TRIGGERS;
		else return DataMcScaleFactorProducerMode::NONE;
	}
	
	enum class SystematicShift : int
	{
		NONE = -1,
		CENTRAL = 0,
		TAU_ES = 1,
	};

	enum class SvfitCacheMissBehaviour : int
	{
		assert = 0,
		undefined  = 1,
		recalculate = 2
	};

	static SvfitCacheMissBehaviour ToSvfitCacheMissBehaviour(std::string const& configstring)
	{
		if (configstring == "undefined") return SvfitCacheMissBehaviour::undefined;
		else if (configstring == "recalculate") return SvfitCacheMissBehaviour::recalculate;

		return SvfitCacheMissBehaviour::assert;
	};
	
	enum class GenMatchingCode : int
	{
		NONE             = -1,
		IS_ELE_PROMPT    = 1,
		IS_MUON_PROMPT   = 2,
		IS_ELE_FROM_TAU  = 3,
		IS_MUON_FROM_TAU = 4,
		IS_TAU_HAD_DECAY = 5,
		IS_FAKE          = 6
	};
};

