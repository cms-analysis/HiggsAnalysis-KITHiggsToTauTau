
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttMetadata.h"

HttMetadata::HttMetadata() : KappaMetadata()
{
}

HttMetadata::~HttMetadata()
{
	if (m_mela)
	{
		delete m_mela;
	}
}

