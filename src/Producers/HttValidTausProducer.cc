
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"


void HttValidTausProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidTausProducer::InitGlobal(globalSettings);
	
	// parse additional config tags
	discriminators = HttValidTausProducer::ParseTauDiscriminators(globalSettings.GetTauDiscriminators());
}

void HttValidTausProducer::InitLocal(setting_type const& settings)
{
	ValidTausProducer::InitLocal(settings);
	
	// parse additional config tags
	discriminators = HttValidTausProducer::ParseTauDiscriminators(settings.GetTauDiscriminators());
}

bool HttValidTausProducer::AdditionalCriteria(KDataPFTau* tau,
                                              event_type const& event,
                                              product_type& product) const
{
	bool validTau = ValidTausProducer::AdditionalCriteria(tau, event, product);
	
	
	// get pt-dependent discriminators
	int index = product.m_validTaus.size();
	std::vector<std::string> discriminatorNames = SafeMap::GetWithDefault(discriminators, index,
	                                              SafeMap::GetWithDefault(discriminators, -1, std::vector<std::string>()));
	
	// check discriminators
	for (stringvector::iterator discriminatorName = discriminatorNames.begin();
	     validTau && discriminatorName != discriminatorNames.end(); ++discriminatorName)
	{
		validTau = validTau && tau->hasID(*discriminatorName, event.m_tauDiscriminatorMetadata);
	}
	
	return validTau;
}

std::map<int, std::vector<std::string> > HttValidTausProducer::ParseTauDiscriminators(std::vector<std::string> discriminators)
{
	std::vector<std::string> defaultDiscriminators;
	std::map<int, std::vector<std::string> > parsedDiscriminators;
	
	for (std::vector<std::string>::iterator discriminator = discriminators.begin();
	     discriminator != discriminators.end(); ++discriminator)
	{
		std::vector<std::string> splitted;
		boost::algorithm::split(splitted, *discriminator, boost::algorithm::is_any_of(":"));
		transform(splitted.begin(), splitted.end(), splitted.begin(),
				  [](std::string s) { return boost::algorithm::trim_copy(s); });
		
		int index = -1;
		if (splitted.size() > 1) {
			index = std::stoi(splitted[0]);
		}
		
		if (parsedDiscriminators.count(index) == 0) {
			parsedDiscriminators[index] = std::vector<std::string>();
		}
		parsedDiscriminators[index].push_back(splitted[1]);
	}
	
	return parsedDiscriminators;
}

