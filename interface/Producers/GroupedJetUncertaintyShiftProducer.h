
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

#include "Artus/KappaAnalysis/interface/Utility/BTagSF.h"
#include "Artus/KappaAnalysis/interface/Producers/GenParticleMatchingProducers.h"

/**
   \brief Producer for jet energy scale corrections (Htt version).
   
   Mostly copied from https://github.com/truggles/FinalStateAnalysis/blob/miniAOD_8_0_25/PatTools/plugins/MiniAODJetFullSystematicsEmbedder.cc

   Required config tags
   - JetEnergyCorrectionSplitUncertaintyParameters (file location)
   - JetEnergyCorrectionSplitUncertaintyParameterNames (list of names)
*/
class GroupedJetUncertaintyShiftProducer: public ProducerBase<HttTypes>
{
public:
	virtual ~GroupedJetUncertaintyShiftProducer();
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual std::string GetProducerId() const override;

	void Produce(event_type const& event, product_type& product,
                 setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::string uncertaintyFile;
	std::vector<std::string> individualUncertainties;
	//std::map<std::string, std::vector<std::string>> uncertaintyGroupings;
	//std::vector<HttEnumTypes::JetEnergyUncertaintyShiftName> uncertaintyGroupingNames;
	std::vector<HttEnumTypes::JetEnergyUncertaintyShiftName> individualUncertaintyEnums;
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, float> individualUncertaintyEnumsMap;

	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, JetCorrectionUncertainty*> jetUncMap;
};


