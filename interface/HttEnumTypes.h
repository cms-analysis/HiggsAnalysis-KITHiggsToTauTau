
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
		// Jet Energy Scale uncertainties grouped by eta
		Eta0To5,
		Eta0To3,
		Eta3To5,
		ClosureEta, // uncertainities grouped in eta added in quadrature to be compared to 'Total' for closure test 
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
		else if (jetEnergyCorrectionUncertainty == "Eta0To5") return JetEnergyUncertaintyShiftName::Eta0To5;
		else if (jetEnergyCorrectionUncertainty == "Eta0To3") return JetEnergyUncertaintyShiftName::Eta0To3;
		else if (jetEnergyCorrectionUncertainty == "Eta3To5") return JetEnergyUncertaintyShiftName::Eta3To5;
		else if (jetEnergyCorrectionUncertainty == "ClosureEta") return JetEnergyUncertaintyShiftName::ClosureEta;
		else if (jetEnergyCorrectionUncertainty == "Closure") return JetEnergyUncertaintyShiftName::Closure;
		else return JetEnergyUncertaintyShiftName::NONE;
	}
	
	static std::string FromJetEnergyUncertaintyShiftName(JetEnergyUncertaintyShiftName const& jetEnergyCorrectionUncertainty)
	{
		if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::AbsoluteFlavMap) return "AbsoluteFlavMap";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::AbsoluteMPFBias) return "AbsoluteMPFBias";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::AbsoluteScale) return "AbsoluteScale";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::AbsoluteStat) return "AbsoluteStat";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::FlavorQCD) return "FlavorQCD";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::Fragmentation) return "Fragmentation";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::PileUpDataMC) return "PileUpDataMC";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::PileUpPtBB) return "PileUpPtBB";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::PileUpPtEC1) return "PileUpPtEC1";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::PileUpPtEC2) return "PileUpPtEC2";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::PileUpPtHF) return "PileUpPtHF";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::PileUpPtRef) return "PileUpPtRef";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeBal) return "RelativeBal";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeFSR) return "RelativeFSR";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeJEREC1) return "RelativeJEREC1";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeJEREC2) return "RelativeJEREC2";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeJERHF) return "RelativeJERHF";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativePtBB) return "RelativePtBB"; 
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativePtEC1) return "RelativePtEC1";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativePtEC2) return "RelativePtEC2";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativePtHF) return "RelativePtHF";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeStatEC) return "RelativeStatEC";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeStatFSR) return "RelativeStatFSR";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::RelativeStatHF) return "RelativeStatHF";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::SinglePionECAL) return "SinglePionECAL";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::SinglePionHCAL) return "SinglePionHCAL";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::TimePtEta) return "TimePtEta";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::Total) return "Total";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::Eta0To5) return "Eta0To5";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::Eta0To3) return "Eta0To3";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::Eta3To5) return "Eta3To5";
		else if (jetEnergyCorrectionUncertainty == JetEnergyUncertaintyShiftName::ClosureEta) return "ClosureEta";
		else if (jetEnergyCorrectionUncertainty ==  JetEnergyUncertaintyShiftName::Closure) return "Closure";
		else return "";
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
