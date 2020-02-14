
#include <vector>
#include <numeric>
#include <functional>

#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/regex.hpp>

#include "Artus/Utility/interface/RootFileHelper.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DataMcScaleFactorProducers.h"


DataMcScaleFactorProducerBase::DataMcScaleFactorProducerBase(
		std::vector<std::string>& (setting_type::*GetEfficiencyData)(void) const,
		std::vector<std::string>& (setting_type::*GetEfficiencyMc)(void) const,
		std::string (setting_type::*GetEfficiencyHistogram)(void) const,
		std::string (setting_type::*GetEfficiencyMode)(void) const,
		std::string const& weightName
) :
	GetEfficiencyData(GetEfficiencyData),
	GetEfficiencyMc(GetEfficiencyMc),
	GetEfficiencyHistogram(GetEfficiencyHistogram),
	GetEfficiencyMode(GetEfficiencyMode),
	m_weightName(weightName)
{
}

void DataMcScaleFactorProducerBase::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
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
	
	m_scaleFactorMode =  HttEnumTypes::ToDataMcScaleFactorProducerMode(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.*GetEfficiencyMode)())));
	
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
                                    setting_type const& settings, metadata_type const& metadata) const
{
	// read bin contents from ROOT histograms
	// Data
	std::vector<std::vector<double> > efficienciesData = GetEfficiencies(
			efficienciesDataByHltName,
			efficienciesDataByIndex,
			event, product, settings, metadata
	);
	
	// MC
	std::vector<std::vector<double> > efficienciesMc = GetEfficiencies(
			efficienciesMcByHltName,
			efficienciesMcByIndex,
			event, product, settings, metadata
	);

	// calculate the weight
	if (m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::MULTIPLY_WEIGHTS)
	{
		for (size_t efficiencyIndex = 0; efficiencyIndex < efficienciesData.size();
			 ++efficiencyIndex)
		{
			double efficiencyData = std::accumulate(
					efficienciesData[efficiencyIndex].begin(), efficienciesData[efficiencyIndex].end(),
					1.0, std::multiplies<double>()
			);
			double efficiencyMc = std::accumulate(
					efficienciesMc[efficiencyIndex].begin(), efficienciesMc[efficiencyIndex].end(),
					1.0, std::multiplies<double>()
			);
			double weight = ((efficiencyMc == 0.0) ? 1.0 : (efficiencyData / efficiencyMc));
			product.m_weights[std::string(m_weightName + "_" + std::to_string(efficiencyIndex+1))] = weight;
		}
	}
	else if (m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::CORRELATE_TRIGGERS)
	{
		assert((efficienciesData.size() == 2) &&
		       (efficienciesData[0].size() == 2) &&
		       (efficienciesData[1].size() == 2) &&
		       (efficienciesMc.size() == 2) &&
		       (efficienciesMc[0].size() == 2) &&
		       (efficienciesMc[1].size() == 2));

		double efficiencyData = efficienciesData[0][0]*efficienciesData[1][1] + efficienciesData[0][1]*efficienciesData[1][0] - efficienciesData[0][1]*efficienciesData[1][1];
		double efficiencyMc = efficienciesMc[0][0]*efficienciesMc[1][1] + efficienciesMc[0][1]*efficienciesMc[1][0] - efficienciesMc[0][1]*efficienciesMc[1][1];
		double weight = ((efficiencyMc == 0.0) ? 1.0 : (efficiencyData / efficiencyMc));
		product.m_weights[std::string(m_weightName + "_1")] = weight;
	}

	else if (m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::CROSS_TRIGGERS)
	{
		assert((efficienciesData.size() == 1) &&
		       (efficienciesData[0].size() == 2) &&
		       (efficienciesMc.size() == 1) &&
		       (efficienciesMc[0].size() == 2) &&
		       (product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2) &&
		       (product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2));

		//TODO here the thing is changed
		LOG(DEBUG) << " DATA: eff single lepton trigg:" << efficienciesData[0][0] << " eff cross trigger lepton:  " <<  efficienciesData[0][1] << std::endl;
		LOG(DEBUG) << " MC: eff single lepton trigg:" << efficienciesMc[0][0] << " eff cross trigger lepton:  " <<  efficienciesMc[0][1] << std::endl;
		LOG(DEBUG) << "--------------------------------------------------------------------------------------------------------------------------" << std::endl;
		double efficiencyData = efficienciesData[0][0]*(1.0-product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[1]) + efficienciesData[0][1]*product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[1];
		double efficiencyMc = efficienciesMc[0][0]*(1.0-product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1])  + efficienciesMc[0][1]*product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1];
		double weight = ((efficiencyMc == 0.0) ? 1.0 : (efficiencyData / efficiencyMc));
		LOG(DEBUG) << "weight: " << weight << std::endl;
		LOG(DEBUG) << "-------------------------------------------------------------------------------------------------------------------------" << std::endl;
		product.m_weights[std::string(m_weightName + "_1")] = weight;
	}
	else if (m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::MULTIPLY_TAU2017_WEIGTHS)
	{
		assert((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2) &&
		       (product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2));
		double efficiencyData =product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[0] * product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[1];
		double efficiencyMc = product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[0] * product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1];
		double weight = ((efficiencyMc == 0.0) ? 1.0 : (efficiencyData / efficiencyMc));
		product.m_weights[std::string(m_weightName + "_1")] = weight;
	}
}


// return linear interpolation between bin contents of neighboring bins
std::vector<double> DataMcScaleFactorProducerBase::GetEfficienciesFromHistograms(
		std::vector<TH2F*> const& histograms,
		KLepton* lepton) const
{
	std::vector<double> efficiencies;
	for (std::vector<TH2F*>::const_iterator histogram = histograms.begin();
	     histogram != histograms.end(); ++histogram)
	{
		int globalBin = (*histogram)->FindBin(lepton->p4.Pt(), lepton->p4.Eta());
// 		int xBin, yBin, zBin;
// 		(*histogram)->GetBinXYZ(globalBin, xBin, yBin, zBin);
// 		int globalBinUp = (*histogram)->GetBin((xBin <= (*histogram)->GetNbinsX() ? xBin+1 : xBin), yBin, zBin);
		
// 		float binContent = (*histogram)->GetBinContent(globalBin);
// 		float binContentUp = (*histogram)->GetBinContent(globalBinUp);
		
// 		float interpolationFactor = (lepton->p4.Pt() - (*histogram)->GetXaxis()->GetBinLowEdge(xBin)) /
// 		                            ((*histogram)->GetXaxis()->GetBinUpEdge(xBin) - (*histogram)->GetXaxis()->GetBinLowEdge(xBin));
// 		float linearInterpolation = (binContent * interpolationFactor) + (binContentUp * (1.0 - interpolationFactor));
		
// 		efficiencies.push_back((linearInterpolation);
		efficiencies.push_back((*histogram)->GetBinContent(globalBin));
		
	}
	return efficiencies;
}


std::vector<std::vector<double> > DataMcScaleFactorProducerBase::GetEfficiencies(
		std::map<std::string, std::vector<TH2F*> > const& efficienciesByHltName,
		std::map<size_t, std::vector<TH2F*> > const& efficienciesByIndex,
		event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) const
{
	std::vector<std::vector<double> > efficiencies(efficienciesByHltName.size() + efficienciesByIndex.size(), std::vector<double>());
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
			for (std::vector<KLepton*>::const_iterator lepton = product.m_flavourOrderedLeptons.begin();
			     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
			{
				std::map<std::string, std::map<std::string, std::vector<KLV*> > >* matchedHlts = SafeMap::Get(
						product.m_detailedTriggerMatchedLeptons,
						*lepton
				);
				for (std::map<std::string, std::map<std::string, std::vector<KLV*> > >::iterator matchedHlt = matchedHlts->begin();
				     matchedHlt != matchedHlts->end(); ++matchedHlt)
				{
					std::map<std::string, std::vector<KLV*> > matchedFilters = SafeMap::Get(*matchedHlts, matchedHlt->first);
					for (std::map<std::string, std::vector<KLV*> >::iterator matchedFilter = matchedFilters.begin();
					     matchedFilter != matchedFilters.end(); ++matchedFilter)
					{
						if (boost::regex_search(matchedFilter->first, boost::regex(efficiencyByHltName->first, boost::regex::icase | boost::regex::extended)))
						{
							efficiencies[index++] = GetEfficienciesFromHistograms(
									efficiencyByHltName->second,
									*lepton
							);
						}
					}
				}
			}
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
	                              &setting_type::GetTriggerEfficiencyMode,
	                              "triggerWeight")
{
}


IdentificationWeightProducer::IdentificationWeightProducer() :
	DataMcScaleFactorProducerBase(&setting_type::GetIdentificationEfficiencyData,
	                              &setting_type::GetIdentificationEfficiencyMc,
	                              &setting_type::GetIdentificationEfficiencyHistogram,
	                              &setting_type::GetIdentificationEfficiencyMode,
	                              "identificationWeight")
{
}

// ==========================================================================================

LepTauScaleFactorWeightProducer::LepTauScaleFactorWeightProducer(
		std::vector<std::string>& (setting_type::*GetWeightFiles)(void) const,
		std::vector<std::string>& (setting_type::*GetWeightHistograms)(void) const
) :
	GetWeightFiles(GetWeightFiles),
	GetWeightHistograms(GetWeightHistograms)
{
}


void LepTauScaleFactorWeightProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	// read the histograms from the weight file
	std::map<std::string, std::vector<std::string> > weightFilesByName;
	std::map<size_t, std::vector<std::string> > weightFilesByIndex = Utility::ParseMapTypes<size_t, std::string>(
			Utility::ParseVectorToMap((settings.*GetWeightFiles)()),
			weightFilesByName
	);
	
	for (std::map<size_t, std::vector<std::string> >::const_iterator weightFileByIndex = weightFilesByIndex.begin();
	     weightFileByIndex != weightFilesByIndex.end(); ++weightFileByIndex)
	{
		assert(weightFileByIndex->second.size() == 1);
		
		std::string weightFileName = weightFileByIndex->second.at(0);
		std::vector<TH1F*> weightHistos = RootFileHelper::SafeGetVector<TH1F>(weightFileName, (settings.*GetWeightHistograms)());
		
		weightsByIndex.insert(std::make_pair(weightFileByIndex->first, weightHistos));
	}
}

void LepTauScaleFactorWeightProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings, metadata_type const& metadata) const
{
	for (std::map<size_t, std::vector<TH1F*> >::const_iterator weightByIndex = weightsByIndex.begin();
	     weightByIndex != weightsByIndex.end(); ++weightByIndex)
	{
		size_t leptonIndex = weightByIndex->first;
		
		if (leptonIndex < product.m_flavourOrderedLeptons.size())
		{
			for (std::vector<TH1F*>::const_iterator weightHisto = weightByIndex->second.begin();
			     weightHisto != weightByIndex->second.end(); ++weightHisto)
			{
				int bin = (*weightHisto)->FindBin(std::abs(product.m_flavourOrderedLeptons[leptonIndex]->p4.Eta()));
				double weight = (*weightHisto)->GetBinContent(bin);
				
				std::string weightName = std::string((*weightHisto)->GetTitle()) + "SFWeight_" + std::to_string(leptonIndex+1);
				
				product.m_optionalWeights[weightName] = weight;
			}
		}
	}
}


EleTauFakeRateWeightProducer::EleTauFakeRateWeightProducer() :
	LepTauScaleFactorWeightProducer(&setting_type::GetEleTauFakeRateWeightFile,
	                                &setting_type::GetEleTauFakeRateHistograms)
{
}

MuonTauFakeRateWeightProducer::MuonTauFakeRateWeightProducer() :
	LepTauScaleFactorWeightProducer(&setting_type::GetMuonTauFakeRateWeightFile,
	                                &setting_type::GetMuonTauFakeRateHistograms)
{
}

// ==========================================================================================

void PileUpJetIDScaleFactorWeightProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	std::string year = std::to_string(settings.GetYear());
	std::string pileUpJetIDWorkingPoint = settings.GetPuJetID();
	std::string histoname;

	if(pileUpJetIDWorkingPoint == "loose")
	{
		histoname = year + "_" + "L";
	}
	else if(pileUpJetIDWorkingPoint == "medium")
	{
		histoname = year + "_" + "M";
	}
	else if(pileUpJetIDWorkingPoint == "tight")
	{
		histoname = year + "_" + "T";
	}

	std::string effFileName = settings.GetPuJetIDScaleFactorFilesPath() + "h2_eff_sf_" + histoname + ".root";
	std::string mistagFileName = settings.GetPuJetIDScaleFactorFilesPath() + "h2_mistag_sf_" + histoname + ".root";
	// read the histograms from the weight file
	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);

	TFile effFile(effFileName.c_str(), "READ");

	if (effFile.IsZombie()) {
		std::cout << "PileUpJetIDScaleFactorWeightProducer: file " << effFileName << " is not found...   quitting " << std::endl;
		exit(-1);
	}
	std::string effhistoname = "h2_eff_sf" + histoname;
	m_efficiencyScaleFactorHistogram = static_cast<TH2F*>(effFile.Get(effhistoname.c_str()));
	m_efficiencyScaleFactorHistogram->SetDirectory(nullptr);
	effFile.Close();

	TFile mistagFile(mistagFileName.c_str(), "READ");

	if (mistagFile.IsZombie()) {
		std::cout << "PileUpJetIDScaleFactorWeightProducer: file " << mistagFileName << " is not found...   quitting " << std::endl;
		exit(-1);
	}

	std::string mistaghistoname = "h2_mistag_sf" + histoname;
	m_mistagScaleFactorHistogram = static_cast<TH2F*>(mistagFile.Get(mistaghistoname.c_str()));
	m_mistagScaleFactorHistogram->SetDirectory(nullptr);
	mistagFile.Close();

	gDirectory = savedir;
	gFile = savefile;
}

void PileUpJetIDScaleFactorWeightProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings, metadata_type const& metadata) const
{
	double weight(1.0);
	for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin(); jet != product.m_validJets.end(); ++jet)
	{
		TH2F* weightHisto = nullptr;
		if (true) // TODO: add jen gen matching logic
		{
			// Apply efficiency SFs to real jets (matched to gen jet)
			weightHisto = m_efficiencyScaleFactorHistogram;
		}
		else
		{
			// Apply mistag SFs to PU jets (NOT matched to gen jet)
			weightHisto = m_mistagScaleFactorHistogram;
		}

		if(weightHisto != nullptr)
		{
			int bin = weightHisto->FindBin((*jet)->p4.Pt(), std::abs((*jet)->p4.Eta()));
			weight *= weightHisto->GetBinContent(bin);
		}
	}
	product.m_optionalWeights["pileupJetIDScaleFactorWeight"] = weight;
}
