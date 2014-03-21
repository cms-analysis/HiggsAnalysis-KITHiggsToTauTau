
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEventProvider.h"

/**
   \brief class to connect the analysis specific event content to the pipelines.
*/


HttEventProvider::HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType) :
		KappaEventProvider<HttTypes>(fileInterface, inpType)
{

}

void HttEventProvider::WireEvent(global_setting_type const& globalSettings)
{
	KappaEventProvider::WireEvent(globalSettings);
}

