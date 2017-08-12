
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/MadGraphTools.h"
#include "TDatabasePDG.h"

class MadGraphReweightingProducer: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings) const override;

private:
	int GetMixingAngleKey(float mixingAngleOverPiHalf) const;
	std::string GetLabelForWeightsMap(float mixingAngleOverPiHalf) const;
	
	std::map<std::string, std::vector<std::string> > m_madGraphProcessDirectoriesByName;
	//std::map<HttEnumTypes::MadGraphProductionModeGGH, std::vector<std::string> > m_madGraphProcessDirectories;
	std::map<std::string, std::map<int, MadGraphTools*> > m_madGraphTools;

	TDatabasePDG* m_databasePDG = nullptr;
	
	static bool MadGraphParticleOrdering(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2);
};

