
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/PreselectionFilter.h"


bool PreselectionFilter::DoesEventPassLocal(HttEvent const& event,
                                            HttProduct const& product,
                                            HttPipelineSettings const& settings) const
{
	return (product.m_decayChannel == HttProduct::ToDecayChannel(settings.GetChannel()));
}

