
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
class TaggedJetUncertaintyShiftProducer: public ProducerBase<HttTypes>
{
public:

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	std::string GetProducerId() const override;
	virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::string uncertaintyFile;
	std::vector<std::string> individualUncertainties;
	std::map<std::string, std::vector<std::string>> uncertaintyGroupings;
	std::vector<HttEnumTypes::JetEnergyUncertaintyShiftName> uncertaintyGroupingNames;
	std::vector<HttEnumTypes::JetEnergyUncertaintyShiftName> individualUncertaintyEnums;

	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, JetCorrectionUncertainty*> jetUncMap;

	KappaEnumTypes::JetIDVersion jetIDVersion;
	KappaEnumTypes::JetID jetID;

	std::map<std::string, std::vector<float> > lowerPtCuts;
	std::map<std::string, std::vector<float> > upperAbsEtaCuts;

	std::map<size_t, std::vector<std::string> > puJetIdsByIndex;
	std::map<std::string, std::vector<std::string> > puJetIdsByHltName;
	std::map<std::string, std::vector<float> > jetTaggerLowerCutsByTaggerName;
	std::map<std::string, std::vector<float> > jetTaggerUpperCutsByTaggerName;
	KappaEnumTypes::JetIDVersion pujetIDVersion;
	KappaEnumTypes::JetID pujetID;
	std::string jetPuJetIDName;

	RecoJetGenParticleMatchingProducer::JetMatchingAlgorithm m_jetMatchingAlgorithm;

	KappaEnumTypes::BTagScaleFactorMethod m_bTagSFMethod;
	float m_bTagWorkingPoint;
	BTagSF m_bTagSf;

	void ProduceShift(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata, bool shiftUp,
	                  std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>>& correctedJetsBySplitUncertainty,
	                  std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>>& correctedBTaggedJetsBySplitUncertainty) const;
};
