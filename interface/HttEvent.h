
#pragma once

#include <Kappa/DataFormats/interface/Kappa.h>

class HttEvent {
public:
	KGenEventMetadata* m_geneventmetadata;
	KEventMetadata* m_eventmetadata;
	KLumiMetadata* m_lumimetadata;
	KGenLumiMetadata* m_genlumimetadata;
	KFilterMetadata* m_filtermetadata;
	
	KFilterSummary* m_filter;
	KDataMuons* m_muons;
	
	float m_floatTheSim;
	float m_floatPtSim;
	float m_floatPSim;
	float m_floatPzSim;
};


