
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTmvaClassificationReaders.h"

	
AntiTtbarDiscriminatorTmvaReader::AntiTtbarDiscriminatorTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&spec_setting_type::GetAntiTtbarTmvaInputQuantities,
	                                       &spec_setting_type::GetAntiTtbarTmvaMethods,
	                                       &spec_setting_type::GetAntiTtbarTmvaWeights,
	                                       &spec_product_type::m_antiTtbarDiscriminators)
{
}

