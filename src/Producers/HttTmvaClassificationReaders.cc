
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTmvaClassificationReaders.h"

	
AntiTtbarDiscriminatorTmvaReader::AntiTtbarDiscriminatorTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&setting_type::GetAntiTtbarTmvaInputQuantities,
	                                       &setting_type::GetAntiTtbarTmvaMethods,
	                                       &setting_type::GetAntiTtbarTmvaWeights,
	                                       &product_type::m_antiTtbarDiscriminators)
{
}

