
#include "Artus/Utility/interface/RootFileHelper.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DataMcScaleFactorProducers.h"


DataMcScaleFactorProducerBase::DataMcScaleFactorProducerBase(
		std::vector<std::string>& (setting_type::*GetEfficiencyData)(void) const,
		std::vector<std::string>& (setting_type::*GetEfficiencyMc)(void) const,
		std::string (setting_type::*GetEfficiencyHistogram)(void) const,
		std::string const& weightName
) :
	GetEfficiencyData(GetEfficiencyData),
	GetEfficiencyMc(GetEfficiencyMc),
	GetEfficiencyHistogram(GetEfficiencyHistogram),
	m_weightName(weightName)
{
}

void DataMcScaleFactorProducerBase::Init(setting_type const& settings)
{
	// parse settings for efficiency files
	// and read the histograms from the files
	// Data
	std::map<std::string, std::vector<std::string> > efficiencyFilesDataByHltName;
	std::map<size_t, std::vector<std::string> > efficiencyFilesDataByIndex = Utility::ParseMapTypes<size_t, std::string>(
			Utility::ParseVectorToMap((settings.*GetEfficiencyData)()),
			efficiencyFilesDataByHltName
	);
	efficienciesDataByHltName = RootFileHelper::SafeGetMap<std::string, TH2F>(
			efficiencyFilesDataByHltName, (settings.*GetEfficiencyHistogram)()
	);
	efficienciesDataByIndex = RootFileHelper::SafeGetMap<size_t, TH2F>(
			efficiencyFilesDataByIndex, (settings.*GetEfficiencyHistogram)()
	);
	
	// MC
	std::map<std::string, std::vector<std::string> > efficiencyFilesMcByHltName;
	std::map<size_t, std::vector<std::string> > efficiencyFilesMcByIndex = Utility::ParseMapTypes<size_t, std::string>(
			Utility::ParseVectorToMap((settings.*GetEfficiencyMc)()),
			efficiencyFilesMcByHltName
	);
	efficienciesMcByHltName = RootFileHelper::SafeGetMap<std::string, TH2F>(
			efficiencyFilesMcByHltName, (settings.*GetEfficiencyHistogram)()
	);
	efficienciesMcByIndex = RootFileHelper::SafeGetMap<size_t, TH2F>(
			efficiencyFilesMcByIndex, (settings.*GetEfficiencyHistogram)()
	);
	
	// consistency checks for settings
	assert(efficienciesDataByHltName.size() == efficienciesMcByHltName.size());
	assert(efficienciesDataByIndex.size() == efficienciesMcByIndex.size());
	
	for (std::map<std::string, std::vector<TH2F*> >::const_iterator efficiencyDataByHltName = efficienciesDataByHltName.begin();
	     efficiencyDataByHltName != efficienciesDataByHltName.end();
	     ++efficiencyDataByHltName)
	{
		assert(efficienciesMcByHltName.count(efficiencyDataByHltName->first) > 0);
	}
	
	for (std::map<size_t, std::vector<TH2F*> >::const_iterator efficiencyDataByIndex = efficienciesDataByIndex.begin();
	     efficiencyDataByIndex != efficienciesDataByIndex.end();
	     ++efficiencyDataByIndex)
	{
		assert(efficienciesMcByIndex.count(efficiencyDataByIndex->first) > 0);
	}
	
}

void DataMcScaleFactorProducerBase::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{
	// read bin contents from ROOT histograms
	// Data
	std::vector<double> efficienciesData = GetEfficiencies(efficienciesDataByHltName,
	                                                       efficienciesDataByIndex,
	                                                       event, product, settings);
	
	// MC
	std::vector<double> efficienciesMc = GetEfficiencies(efficienciesMcByHltName,
	                                                     efficienciesMcByIndex,
	                                                     event, product, settings);
	
	// calculate the weight
	for (size_t efficiencyIndex = 0; efficiencyIndex < efficienciesData.size();
	     ++efficiencyIndex)
	{
		double weight = 1.0;
		if (efficienciesMc[efficiencyIndex] != 0.0)
		{
			weight = efficienciesData[efficiencyIndex] / efficienciesMc[efficiencyIndex];
		}
		product.m_weights[std::string(m_weightName + std::to_string(efficiencyIndex+1))] = weight;
	}
	
}


// return linear interpolation between bin contents of neighboring bins
double DataMcScaleFactorProducerBase::GetEfficienciesFromHistograms(std::vector<TH2F*> const& histograms,
                                                                    KLepton* lepton) const
{
	double efficiency = 1.0;
	for (std::vector<TH2F*>::const_iterator histogram = histograms.begin();
	     histogram != histograms.end(); ++histogram)
	{
		int globalBin = (*histogram)->FindBin(lepton->p4.Pt(), lepton->p4.Eta());
		int xBin, yBin, zBin;
		(*histogram)->GetBinXYZ(globalBin, xBin, yBin, zBin);
		int globalBinUp = (*histogram)->GetBin((xBin <= (*histogram)->GetNbinsX() ? xBin+1 : xBin), yBin, zBin);
		
		float binContent = (*histogram)->GetBinContent(globalBin);
		float binContentUp = (*histogram)->GetBinContent(globalBinUp);
		
		float interpolationFactor = (lepton->p4.Pt() - (*histogram)->GetXaxis()->GetBinLowEdge(xBin)) /
		                            ((*histogram)->GetXaxis()->GetBinUpEdge(xBin) - (*histogram)->GetXaxis()->GetBinLowEdge(xBin));
		float linearInterpolation = (binContent * interpolationFactor) + (binContentUp * (1.0 - interpolationFactor));
		
		efficiency *= linearInterpolation;
		//efficiency *= (*histogram)->GetBinContent((*histogram)->FindBin(lepton->p4.Pt(), lepton->p4.Eta()));
	}
	return efficiency;
}


std::vector<double> DataMcScaleFactorProducerBase::GetEfficiencies(
		std::map<std::string, std::vector<TH2F*> > const& efficienciesByHltName,
		std::map<size_t, std::vector<TH2F*> > const& efficienciesByIndex,
		event_type const& event, product_type const& product, setting_type const& settings) const
{
	std::vector<double> efficiencies(efficienciesByHltName.size() + efficienciesByIndex.size(), 1.0);
	size_t index = 0;
	
	for (std::map<std::string, std::vector<TH2F*> >::const_iterator efficiencyByHltName = efficienciesByHltName.begin();
	     efficiencyByHltName != efficienciesByHltName.end();
	     ++efficiencyByHltName)
	{
		if (efficiencyByHltName->first == "default")
		{
			for (std::vector<KLepton*>::const_iterator lepton = product.m_flavourOrderedLeptons.begin();
			     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
			{
				efficiencies[index++] = GetEfficienciesFromHistograms(
						efficiencyByHltName->second,
						*lepton
				);
			}
		}
		else
		{
			// TODO
			LOG(FATAL) << "Efficiencies per HLT name are not yet implemented!";
		}
	}
	
	for (std::map<size_t, std::vector<TH2F*> >::const_iterator efficiencyByIndex = efficienciesByIndex.begin();
	     efficiencyByIndex != efficienciesByIndex.end();
	     ++efficiencyByIndex)
	{
		if (efficiencyByIndex->first < product.m_flavourOrderedLeptons.size())
		{
			efficiencies[index++] = GetEfficienciesFromHistograms(
					efficiencyByIndex->second,
					product.m_flavourOrderedLeptons.at(efficiencyByIndex->first)
			);
		}
	}
	
	return efficiencies;
}


TriggerWeightProducer::TriggerWeightProducer() :
	DataMcScaleFactorProducerBase(&setting_type::GetTriggerEfficiencyData,
	                              &setting_type::GetTriggerEfficiencyMc,
	                              &setting_type::GetTriggerEfficiencyHistogram,
	                              "triggerWeight")
{
}


IdentificationWeightProducer::IdentificationWeightProducer() :
	DataMcScaleFactorProducerBase(&setting_type::GetIdentificationEfficiencyData,
	                              &setting_type::GetIdentificationEfficiencyMc,
	                              &setting_type::GetIdentificationEfficiencyHistogram,
	                              "identificationWeight")
{
}

