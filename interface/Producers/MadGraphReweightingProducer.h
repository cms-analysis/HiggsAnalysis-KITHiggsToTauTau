
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/MadGraphTools.h"
#include "TDatabasePDG.h"

class MadGraphReweightingProducer: public ProducerBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::map<std::string, std::vector<std::string> > m_madGraphProcessDirectoriesByName;
	std::map<std::string, std::map<int, MadGraphTools*> > m_madGraphTools;
	TDatabasePDG* m_databasePDG = nullptr;
	
	int GetMixingAngleKey(float mixingAngleOverPiHalf) const;
	std::string GetLabelForWeightsMap(float mixingAngleOverPiHalf) const;
	static bool MadGraphParticleOrderingLightBQuark(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2);
	static bool MadGraphParticleOrderingHeavyBQuark(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2);
};
