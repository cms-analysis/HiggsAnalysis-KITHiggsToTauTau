
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttElectronCorrectionsProducer.h"


void HttElectronCorrectionsProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ElectronCorrectionsProducer::Init(settings, metadata);
	
	eleEnergyCorrection = ToElectronEnergyCorrection(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(static_cast<HttSettings const&>(settings).GetElectronEnergyCorrection())));
}

void HttElectronCorrectionsProducer::AdditionalCorrections(KElectron* electron, event_type const& event,
                                                      product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	ElectronCorrectionsProducer::AdditionalCorrections(electron, event, product, settings, metadata);
	
	if (eleEnergyCorrection == ElectronEnergyCorrection::FALL2015)
	{
	        electron->p4 = electron->p4 * (1.0);
	}
	else if (eleEnergyCorrection != ElectronEnergyCorrection::NONE)
	{
		LOG(FATAL) << "Electron energy correction of type " << Utility::ToUnderlyingValue(eleEnergyCorrection) << " not yet implemented!";
	}
	
	float eleEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetElectronEnergyCorrectionShift();
	float eleEnergyCorrectionShiftEB = static_cast<HttSettings const&>(settings).GetElectronEnergyCorrectionShiftEB();
	float eleEnergyCorrectionShiftEE = static_cast<HttSettings const&>(settings).GetElectronEnergyCorrectionShiftEE();

	if (eleEnergyCorrectionShift != 1.0 && (eleEnergyCorrectionShiftEB != 1.0 || eleEnergyCorrectionShiftEE != 1.0))
	{
		LOG(FATAL) << "Too many different electron energy corrections (all eta, barrel-only, endcap-only)";
	}
	
	if (eleEnergyCorrectionShift != 1.0)
	{
		electron->p4 = electron->p4 * eleEnergyCorrectionShift;
	}
	if (eleEnergyCorrectionShiftEB != 1.0 || eleEnergyCorrectionShiftEE != 1.0)
	{
		if (std::abs(electron->p4.Eta()) < DefaultValues::EtaBorderEB)
		{
			electron->p4 = electron->p4 * eleEnergyCorrectionShiftEB;
		}
		else
		{
			electron->p4 = electron->p4 * eleEnergyCorrectionShiftEE;
		}
	}
}

