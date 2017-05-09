
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "Artus/KappaAnalysis/interface/Utility/BTagSF.h"

/**
   \brief Producer for jet energy scale corrections (Htt version).
   
   Mostly copied from https://github.com/truggles/FinalStateAnalysis/blob/miniAOD_8_0_25/PatTools/plugins/MiniAODJetFullSystematicsEmbedder.cc

   Required config tags
   - JetEnergyCorrectionSplitUncertaintyParameters (file location)
   - JetEnergyCorrectionSplitUncertaintyParameterNames (list of names)
*/
class TaggedJetUncertaintyShiftProducer: public ProducerBase<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	static HttEnumTypes::JetEnergyUncertaintyShiftName ToJetEnergyUncertaintyShiftName(std::string const& jetEnergyCorrectionUncertainty)
	{
		if (jetEnergyCorrectionUncertainty == "AbsoluteFlavMap") return HttEnumTypes::JetEnergyUncertaintyShiftName::AbsoluteFlavMap;
		else if (jetEnergyCorrectionUncertainty == "AbsoluteMPFBias") return HttEnumTypes::JetEnergyUncertaintyShiftName::AbsoluteMPFBias;
		else if (jetEnergyCorrectionUncertainty == "AbsoluteScale") return HttEnumTypes::JetEnergyUncertaintyShiftName::AbsoluteScale;
		else if (jetEnergyCorrectionUncertainty == "AbsoluteStat") return HttEnumTypes::JetEnergyUncertaintyShiftName::AbsoluteStat;
		else if (jetEnergyCorrectionUncertainty == "FlavorQCD") return HttEnumTypes::JetEnergyUncertaintyShiftName::FlavorQCD;
		else if (jetEnergyCorrectionUncertainty == "Fragmentation") return HttEnumTypes::JetEnergyUncertaintyShiftName::Fragmentation;
		else if (jetEnergyCorrectionUncertainty == "PileUpDataMC") return HttEnumTypes::JetEnergyUncertaintyShiftName::PileUpDataMC;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtBB") return HttEnumTypes::JetEnergyUncertaintyShiftName::PileUpPtBB;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtEC1") return HttEnumTypes::JetEnergyUncertaintyShiftName::PileUpPtEC1;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtEC2") return HttEnumTypes::JetEnergyUncertaintyShiftName::PileUpPtEC2;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtHF") return HttEnumTypes::JetEnergyUncertaintyShiftName::PileUpPtHF;
		else if (jetEnergyCorrectionUncertainty == "PileUpPtRef") return HttEnumTypes::JetEnergyUncertaintyShiftName::PileUpPtRef;
		else if (jetEnergyCorrectionUncertainty == "RelativeBal") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeBal;
		else if (jetEnergyCorrectionUncertainty == "RelativeFSR") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeFSR;
		else if (jetEnergyCorrectionUncertainty == "RelativeJEREC1") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeJEREC1;
		else if (jetEnergyCorrectionUncertainty == "RelativeJEREC2") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeJEREC2;
		else if (jetEnergyCorrectionUncertainty == "RelativeJERHF") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeJERHF;
		else if (jetEnergyCorrectionUncertainty == "RelativePtBB") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativePtBB;
		else if (jetEnergyCorrectionUncertainty == "RelativePtEC1") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativePtEC1;
		else if (jetEnergyCorrectionUncertainty == "RelativePtEC2") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativePtEC2;
		else if (jetEnergyCorrectionUncertainty == "RelativePtHF") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativePtHF;
		else if (jetEnergyCorrectionUncertainty == "RelativeStatEC") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeStatEC;
		else if (jetEnergyCorrectionUncertainty == "RelativeStatFSR") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeStatFSR;
		else if (jetEnergyCorrectionUncertainty == "RelativeStatHF") return HttEnumTypes::JetEnergyUncertaintyShiftName::RelativeStatHF;
		else if (jetEnergyCorrectionUncertainty == "SinglePionECAL") return HttEnumTypes::JetEnergyUncertaintyShiftName::SinglePionECAL;
		else if (jetEnergyCorrectionUncertainty == "SinglePionHCAL") return HttEnumTypes::JetEnergyUncertaintyShiftName::SinglePionHCAL;
		else if (jetEnergyCorrectionUncertainty == "TimePtEta") return HttEnumTypes::JetEnergyUncertaintyShiftName::TimePtEta;
		else if (jetEnergyCorrectionUncertainty == "Total") return HttEnumTypes::JetEnergyUncertaintyShiftName::Total;
		else if (jetEnergyCorrectionUncertainty == "Closure") return HttEnumTypes::JetEnergyUncertaintyShiftName::Closure;
		else return HttEnumTypes::JetEnergyUncertaintyShiftName::NONE;
	}

	virtual void Init(setting_type const& settings) override;
	std::string GetProducerId() const override;
	virtual void Produce(event_type const& event, product_type& product, setting_type const& settings) const override;

private:
	std::string uncertaintyFile;
	std::vector<std::string> individualUncertainties;
	std::vector<HttEnumTypes::JetEnergyUncertaintyShiftName> individualUncertaintyEnums;

	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, JetCorrectorParameters const*> JetCorParMap;
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, JetCorrectionUncertainty *> JetUncMap;

	KappaEnumTypes::JetIDVersion jetIDVersion;
	KappaEnumTypes::JetID jetID;

	std::map<std::string, std::vector<float> > lowerPtCuts;
	std::map<std::string, std::vector<float> > upperAbsEtaCuts;

	KappaEnumTypes::BTagScaleFactorMethod m_bTagSFMethod;
	float m_bTagWorkingPoint;
	BTagSF m_bTagSf;
};

