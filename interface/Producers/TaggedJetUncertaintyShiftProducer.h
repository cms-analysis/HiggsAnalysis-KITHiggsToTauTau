
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

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	std::string GetProducerId() const override;
	virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;

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

