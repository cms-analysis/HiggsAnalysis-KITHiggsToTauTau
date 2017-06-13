
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

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
		TAU_ES_1PRONG = 2,
		TAU_ES_1PRONGPI0S = 3,
		TAU_ES_3PRONG = 4,
		TAU_ELECTRON_FAKE_ES = 5,
		TAU_ELECTRON_FAKE_ES_1PRONG = 6,
		TAU_ELECTRON_FAKE_ES_1PRONGPI0S = 7,
		TAU_ELECTRON_FAKE_ES_3PRONG = 8,
		TAU_MUON_FAKE_ES = 9,
		TAU_MUON_FAKE_ES_1PRONG = 10,
		TAU_MUON_FAKE_ES_1PRONGPI0S = 11,
		TAU_MUON_FAKE_ES_3PRONG = 12,
		TAU_JET_FAKE_ES = 13
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
	
	enum class MadGraphProductionModeGGH : int
	{
		NONE  = -1,
		gg_x0 = 0,
		bbx_x0 = 1,
		gg_x0g = 2,
		gb_x0b = 3,
		gbx_x0bx = 4,
		gu_x0u = 5,
		gux_x0ux = 6,
		bbx_x0g = 7,
		uux_x0g = 8,
		bb_x0bb = 9,
		bbx_x0bbx = 10,
		bbx_x0gg = 11,
		bbx_x0uux = 12,
		bxbx_x0bxbx = 13,
		gb_x0gb = 14,
		gbx_x0gbx = 15,
		gg_x0bbx = 16,
		gg_x0gg = 17,
		gg_x0uux = 18,
		gu_x0gu = 19,
		gux_x0gux = 20,
		ub_x0ub = 21,
		ubx_x0ubx = 22,
		uc_x0uc = 23,
		ucx_x0ucx = 24,
		uu_x0uu = 25,
		uux_x0bbx = 26,
		uux_x0ccx = 27,
		uux_x0gg = 28,
		uux_x0uux = 29,
		uxb_x0uxb = 30,
		uxbx_x0uxbx = 31,
		uxcx_x0uxcx = 32,
		uxux_x0uxux = 33,
		bb_x0gbb = 34,
		bbx_x0gbbx = 35,
		bbx_x0ggg = 36,
		bbx_x0guux = 37,
		bxbx_x0gbxbx = 38,
		gb_x0bbbx = 39,
		gb_x0x0ggb = 40,
		gb_x0uuxb = 41,
		gbx_x0bbxbx = 42,
		gbx_x0ggbx = 43,
		gbx_x0uuxbx = 44,
		gg_x0gbbx = 45,
		gg_x0ggg = 46,
		gg_x0guux = 47,
		gu_x0ggu = 48,
		gu_x0ubbx = 49,
		gu_x0uccx = 50,
		gu_x0uuux = 51,
		gux_x0cuxcx = 52,
		gux_x0ggux = 53,
		gux_x0uuxux = 54,
		gux_x0uxbbx = 55,
		ub_x0gub = 56,
		uxb_x0gubx = 57,
		uc_x0guc = 58,
		ucx_x0gucx = 59,
		uu_x0guu = 60,
		uux_x0gbbx = 61,
		uux_x0gccx = 62,
		uux_x0ggg = 63,
		uux_x0guux = 64,
		uxb_x0guxb = 65,
		uxbx_x0guxbx = 66,
		uxcx_x0guxcx = 67,
		uxux_x0guxux = 68
		
	};
	static MadGraphProductionModeGGH ToMadGraphProductionModeGGH(std::string const& madGraphProductionModeGGH)
	{
		if (madGraphProductionModeGGH == "gg_x0") return MadGraphProductionModeGGH::gg_x0;
		else if (madGraphProductionModeGGH == "bbx_x0") return MadGraphProductionModeGGH::bbx_x0;
		else if (madGraphProductionModeGGH == "gg_x0g") return MadGraphProductionModeGGH::gg_x0g;
		else if (madGraphProductionModeGGH == "gb_x0b") return MadGraphProductionModeGGH::gb_x0b;
		else if (madGraphProductionModeGGH == "gbx_x0bx") return MadGraphProductionModeGGH::gbx_x0bx;
		else if (madGraphProductionModeGGH == "gu_x0u") return MadGraphProductionModeGGH::gu_x0u;
		else if (madGraphProductionModeGGH == "gux_x0ux") return MadGraphProductionModeGGH::gux_x0ux;
		else if (madGraphProductionModeGGH == "bbx_x0g") return MadGraphProductionModeGGH::bbx_x0g;
		else if (madGraphProductionModeGGH == "uux_x0g") return MadGraphProductionModeGGH::uux_x0g;
		else if (madGraphProductionModeGGH == "bb_x0bb") return MadGraphProductionModeGGH::bb_x0bb;
		else if (madGraphProductionModeGGH == "bbx_x0bbx") return MadGraphProductionModeGGH::bbx_x0bbx;
		else if (madGraphProductionModeGGH == "bbx_x0gg") return MadGraphProductionModeGGH::bbx_x0gg;
		else if (madGraphProductionModeGGH == "bbx_x0uux") return MadGraphProductionModeGGH::bbx_x0uux;
		else if (madGraphProductionModeGGH == "bxbx_x0bxbx") return MadGraphProductionModeGGH::bxbx_x0bxbx;
		else if (madGraphProductionModeGGH == "gb_x0gb") return MadGraphProductionModeGGH::gb_x0gb;
		else if (madGraphProductionModeGGH == "gbx_x0gbx") return MadGraphProductionModeGGH::gbx_x0gbx;
		else if (madGraphProductionModeGGH == "gg_x0bbx") return MadGraphProductionModeGGH::gg_x0bbx;
		else if (madGraphProductionModeGGH == "gg_x0gg") return MadGraphProductionModeGGH::gg_x0gg;
		else if (madGraphProductionModeGGH == "gg_x0uux") return MadGraphProductionModeGGH::gg_x0uux;
		else if (madGraphProductionModeGGH == "gu_x0gu") return MadGraphProductionModeGGH::gu_x0gu;
		else if (madGraphProductionModeGGH == "gux_x0gux") return MadGraphProductionModeGGH::gux_x0gux;	
		else if (madGraphProductionModeGGH == "ub_x0ub") return MadGraphProductionModeGGH::ub_x0ub;	
		else if (madGraphProductionModeGGH == "ubx_x0ubx") return MadGraphProductionModeGGH::ubx_x0ubx;
		else if (madGraphProductionModeGGH == "uc_x0uc") return MadGraphProductionModeGGH::uc_x0uc;
		else if (madGraphProductionModeGGH == "ucx_x0ucx") return MadGraphProductionModeGGH::ucx_x0ucx;
		else if (madGraphProductionModeGGH == "uu_x0uu") return MadGraphProductionModeGGH::uu_x0uu;
		else if (madGraphProductionModeGGH == "uux_x0bbx") return MadGraphProductionModeGGH::uux_x0bbx;
		else if (madGraphProductionModeGGH == "uux_x0ccx") return MadGraphProductionModeGGH::uux_x0ccx;
		else if (madGraphProductionModeGGH == "uux_x0gg") return MadGraphProductionModeGGH::uux_x0gg;
		else if (madGraphProductionModeGGH == "uux_x0uux") return MadGraphProductionModeGGH::uux_x0uux;
		else if (madGraphProductionModeGGH == "uxb_x0uxb") return MadGraphProductionModeGGH::uxb_x0uxb;
		else if (madGraphProductionModeGGH == "uxbx_x0uxbx") return MadGraphProductionModeGGH::uxbx_x0uxbx;
		else if (madGraphProductionModeGGH == "uxcx_x0uxcx") return MadGraphProductionModeGGH::uxcx_x0uxcx;
		else if (madGraphProductionModeGGH == "uxux_x0uxux") return MadGraphProductionModeGGH::uxux_x0uxux;
		else if (madGraphProductionModeGGH == "bb_x0gbb") return MadGraphProductionModeGGH::bb_x0gbb;
		else if (madGraphProductionModeGGH == "bbx_x0gbbx") return MadGraphProductionModeGGH::bbx_x0gbbx;
		else if (madGraphProductionModeGGH == "bbx_x0ggg") return MadGraphProductionModeGGH::bbx_x0ggg;
		else if (madGraphProductionModeGGH == "bbx_x0guux") return MadGraphProductionModeGGH::bbx_x0guux;
		else if (madGraphProductionModeGGH == "bxbx_x0gbxbx") return MadGraphProductionModeGGH::bxbx_x0gbxbx;
		else if (madGraphProductionModeGGH == "gb_x0bbbx") return MadGraphProductionModeGGH::gb_x0bbbx;
		else if (madGraphProductionModeGGH == "gb_x0x0ggb") return MadGraphProductionModeGGH::gb_x0x0ggb;
		else if (madGraphProductionModeGGH == "gb_x0uuxb") return MadGraphProductionModeGGH::gb_x0uuxb;
		else if (madGraphProductionModeGGH == "gbx_x0bbxbx") return MadGraphProductionModeGGH::gbx_x0bbxbx;
		else if (madGraphProductionModeGGH == "gbx_x0ggbx") return MadGraphProductionModeGGH::gbx_x0ggbx;
		else if (madGraphProductionModeGGH == "gbx_x0uuxbx") return MadGraphProductionModeGGH::gbx_x0uuxbx;
		else if (madGraphProductionModeGGH == "gg_x0gbbx") return MadGraphProductionModeGGH::gg_x0gbbx;
		else if (madGraphProductionModeGGH == "gg_x0ggg") return MadGraphProductionModeGGH::gg_x0ggg;
		else if (madGraphProductionModeGGH == "gg_x0guux") return MadGraphProductionModeGGH::gg_x0guux;
		else if (madGraphProductionModeGGH == "gu_x0ggu") return MadGraphProductionModeGGH::gu_x0ggu;
		else if (madGraphProductionModeGGH == "gu_x0ubbx") return MadGraphProductionModeGGH::gu_x0ubbx;
		else if (madGraphProductionModeGGH == "gu_x0uccx") return MadGraphProductionModeGGH::gu_x0uccx;
		else if (madGraphProductionModeGGH == "gu_x0uuux") return MadGraphProductionModeGGH::gu_x0uuux;
		else if (madGraphProductionModeGGH == "gux_x0cuxcx") return MadGraphProductionModeGGH::gux_x0cuxcx;
		else if (madGraphProductionModeGGH == "gux_x0ggux") return MadGraphProductionModeGGH::gux_x0ggux;
		else if (madGraphProductionModeGGH == "gux_x0uuxux") return MadGraphProductionModeGGH::gux_x0uuxux;
		else if (madGraphProductionModeGGH == "gux_x0uxbbx") return MadGraphProductionModeGGH::gux_x0uxbbx;
		else if (madGraphProductionModeGGH == "ub_x0gub") return MadGraphProductionModeGGH::ub_x0gub;
		else if (madGraphProductionModeGGH == "uxb_x0gubx") return MadGraphProductionModeGGH::uxb_x0gubx;
		else if (madGraphProductionModeGGH == "uc_x0guc") return MadGraphProductionModeGGH::uc_x0guc;
		else if (madGraphProductionModeGGH == "ucx_x0gucx") return MadGraphProductionModeGGH::ucx_x0gucx;
		else if (madGraphProductionModeGGH == "uu_x0guu") return MadGraphProductionModeGGH::uu_x0guu;
		else if (madGraphProductionModeGGH == "uux_x0gbbx") return MadGraphProductionModeGGH::uux_x0gbbx;
		else if (madGraphProductionModeGGH == "uux_x0gccx") return MadGraphProductionModeGGH::uux_x0gccx;
		else if (madGraphProductionModeGGH == "uux_x0ggg") return MadGraphProductionModeGGH::uux_x0ggg;
		else if (madGraphProductionModeGGH == "uux_x0guux") return MadGraphProductionModeGGH::uux_x0guux;
		else if (madGraphProductionModeGGH == "uxb_x0guxb") return MadGraphProductionModeGGH::uxb_x0guxb;
		else if (madGraphProductionModeGGH == "uxbx_x0guxbx") return MadGraphProductionModeGGH::uxbx_x0guxbx;
		else if (madGraphProductionModeGGH == "uxcx_x0guxcx") return MadGraphProductionModeGGH::uxcx_x0guxcx;
		else if (madGraphProductionModeGGH == "uxux_x0guxux") return MadGraphProductionModeGGH::uxux_x0guxux;
		else return MadGraphProductionModeGGH::NONE;
	};

	enum class JetEnergyUncertaintyShiftName : int
	{
		NONE,
		AbsoluteFlavMap,
		AbsoluteMPFBias,
		AbsoluteScale,
		AbsoluteStat,
		FlavorQCD,
		Fragmentation,
		PileUpDataMC,
		PileUpPtBB,
		PileUpPtEC1,
		PileUpPtEC2,
		PileUpPtHF,
		PileUpPtRef,
		RelativeBal,
		RelativeFSR,
		RelativeJEREC1,
		RelativeJEREC2,
		RelativeJERHF,
		RelativePtBB,
		RelativePtEC1,
		RelativePtEC2,
		RelativePtHF,
		RelativeStatEC,
		RelativeStatFSR,
		RelativeStatHF,
		SinglePionECAL,
		SinglePionHCAL,
		TimePtEta,
		Total,
		Closure // individual uncertainties added in quadrature. to be compared to 'Total' for closure test
	};

	static JetEnergyUncertaintyShiftName ToJetEnergyUncertaintyShiftName(std::string const& jetEnergyCorrectionUncertainty)
	{
		if (jetEnergyCorrectionUncertainty == "AbsoluteFlavMap") return JetEnergyUncertaintyShiftName::AbsoluteFlavMap;
		else if (jetEnergyCorrectionUncertainty == "AbsoluteMPFBias") return JetEnergyUncertaintyShiftName::AbsoluteMPFBias;
		else if (jetEnergyCorrectionUncertainty == "AbsoluteScale") return JetEnergyUncertaintyShiftName::AbsoluteScale;
		else if (jetEnergyCorrectionUncertainty == "AbsoluteStat") return JetEnergyUncertaintyShiftName::AbsoluteStat;
		else if (jetEnergyCorrectionUncertainty == "FlavorQCD") return JetEnergyUncertaintyShiftName::FlavorQCD;
		else if (jetEnergyCorrectionUncertainty == "Fragmentation") return JetEnergyUncertaintyShiftName::Fragmentation;
		else if (jetEnergyCorrectionUncertainty == "PileUpDataMC") return JetEnergyUncertaintyShiftName::PileUpDataMC;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtBB") return JetEnergyUncertaintyShiftName::PileUpPtBB;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtEC1") return JetEnergyUncertaintyShiftName::PileUpPtEC1;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtEC2") return JetEnergyUncertaintyShiftName::PileUpPtEC2;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtHF") return JetEnergyUncertaintyShiftName::PileUpPtHF;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtRef") return JetEnergyUncertaintyShiftName::PileUpPtRef;
		else if (jetEnergyCorrectionUncertainty == "RelativeBal") return JetEnergyUncertaintyShiftName::RelativeBal;
		else if (jetEnergyCorrectionUncertainty == "RelativeFSR") return JetEnergyUncertaintyShiftName::RelativeFSR;
		else if (jetEnergyCorrectionUncertainty == "RelativeJEREC1") return JetEnergyUncertaintyShiftName::RelativeJEREC1;
		else if (jetEnergyCorrectionUncertainty == "RelativeJEREC2") return JetEnergyUncertaintyShiftName::RelativeJEREC2;
		else if (jetEnergyCorrectionUncertainty == "RelativeJERHF") return JetEnergyUncertaintyShiftName::RelativeJERHF;
		else if (jetEnergyCorrectionUncertainty == "RelativePtBB") return JetEnergyUncertaintyShiftName::RelativePtBB;
		else if (jetEnergyCorrectionUncertainty == "RelativePtEC1") return JetEnergyUncertaintyShiftName::RelativePtEC1;
		else if (jetEnergyCorrectionUncertainty == "RelativePtEC2") return JetEnergyUncertaintyShiftName::RelativePtEC2;
		else if (jetEnergyCorrectionUncertainty == "RelativePtHF") return JetEnergyUncertaintyShiftName::RelativePtHF;
		else if (jetEnergyCorrectionUncertainty == "RelativeStatEC") return JetEnergyUncertaintyShiftName::RelativeStatEC;
		else if (jetEnergyCorrectionUncertainty == "RelativeStatFSR") return JetEnergyUncertaintyShiftName::RelativeStatFSR;
		else if (jetEnergyCorrectionUncertainty == "RelativeStatHF") return JetEnergyUncertaintyShiftName::RelativeStatHF;
		else if (jetEnergyCorrectionUncertainty == "SinglePionECAL") return JetEnergyUncertaintyShiftName::SinglePionECAL;
		else if (jetEnergyCorrectionUncertainty == "SinglePionHCAL") return JetEnergyUncertaintyShiftName::SinglePionHCAL;
		else if (jetEnergyCorrectionUncertainty == "TimePtEta") return JetEnergyUncertaintyShiftName::TimePtEta;
		else if (jetEnergyCorrectionUncertainty == "Total") return JetEnergyUncertaintyShiftName::Total;
		else if (jetEnergyCorrectionUncertainty == "Closure") return JetEnergyUncertaintyShiftName::Closure;
		else return JetEnergyUncertaintyShiftName::NONE;
	}

	static KMETUncertainty::Type ToMETUncertaintyType(std::string const& metUncertainty)
	{
		if (metUncertainty == "JetResUp") return KMETUncertainty::JetResUp;
		else if (metUncertainty == "JetResDown") return KMETUncertainty::JetResDown;
		else if (metUncertainty == "JetEnUp") return KMETUncertainty::JetEnUp;
		else if (metUncertainty == "JetEnDown") return KMETUncertainty::JetEnDown;
		else if (metUncertainty == "MuonEnUp") return KMETUncertainty::MuonEnUp;
		else if (metUncertainty == "MuonEnDown") return KMETUncertainty::MuonEnDown;
		else if (metUncertainty == "ElectronEnUp") return KMETUncertainty::ElectronEnUp;
		else if (metUncertainty == "ElectronEnDown") return KMETUncertainty::ElectronEnDown;
		else if (metUncertainty == "TauEnUp") return KMETUncertainty::TauEnUp;
		else if (metUncertainty == "TauEnDown") return KMETUncertainty::TauEnDown;
		else if (metUncertainty == "UnclusteredEnUp") return KMETUncertainty::UnclusteredEnUp;
		else if (metUncertainty == "UnclusteredEnDown") return KMETUncertainty::UnclusteredEnDown;
		else if (metUncertainty == "PhotonEnUp") return KMETUncertainty::PhotonEnUp;
		else if (metUncertainty == "PhotonEnDown") return KMETUncertainty::PhotonEnDown;
		else if (metUncertainty == "NoShift") return KMETUncertainty::NoShift;
		else if (metUncertainty == "METUncertaintySize") return KMETUncertainty::METUncertaintySize;
		else if (metUncertainty == "JetResUpSmear") return KMETUncertainty::JetResUpSmear;
		else if (metUncertainty == "JetResDownSmear") return KMETUncertainty::JetResDownSmear;
		else if (metUncertainty == "METFullUncertaintySize") return KMETUncertainty::METFullUncertaintySize;
		else return KMETUncertainty::NoShift;
		LOG(FATAL) << "You need to specify an implemented MET uncertainty in your config.";
	};
};

