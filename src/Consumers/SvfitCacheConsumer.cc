
#include "Artus/Utility/interface/RootFileHelper.h"
#include <boost/filesystem/convenience.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/SvfitCacheConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include <TDirectory.h>


void SvfitCacheConsumer::Init(setting_type const& settings)
{
	ConsumerBase<HttTypes>::Init(settings);

	TDirectory* tmpDirectory = gDirectory;
	RootFileHelper::SafeCd(settings.GetRootOutFile(),
	                       settings.GetRootFileFolder());
	
	m_svfitCacheTree = new TTree(settings.GetSvfitCacheTree().c_str(),
	                             settings.GetSvfitCacheTree().c_str());
	gDirectory = tmpDirectory;
	m_svfitCacheTreeInitialised = false;
}

void SvfitCacheConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product,
                                              setting_type const& settings)
{
	// make sure the SvfitOutputFile option is set reasonably
	assert((! settings.GetGenerateSvfitInput()) || (settings.GetSvfitOutFile().find(".root") != std::string::npos) || settings.GetUseFirstInputFileNameForSvfit());
	ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings);
	if (settings.GetGenerateSvfitInput())
	{
		if(!settings.GetUpdateSvfitCache() || (settings.GetUpdateSvfitCache() && product.m_svfitResults.recalculated))
		{
			if (! m_svfitCacheTreeInitialised)
			{
				std::string cacheFilename;
				if(settings.GetUseFirstInputFileNameForSvfit())
				{
					cacheFilename = boost::filesystem::basename(boost::filesystem::path(settings.GetInputFiles().at(0)))+std::string("-SvfitCacheInput-")+settings.GetRootFileFolder()+std::to_string(m_fileIndex)+std::string(".root");
				}
				else
				{
					cacheFilename = boost::filesystem::basename(boost::filesystem::path(settings.GetSvfitOutFile()))+settings.GetRootFileFolder()+std::to_string(m_fileIndex)+std::string(".root");
				}
				TFile* SvfitFile = new TFile(cacheFilename.c_str(),"RECREATE");
				RootFileHelper::SafeCd(SvfitFile, settings.GetRootFileFolder());
				m_svfitCacheTree->Write(m_svfitCacheTree->GetName());
				SvfitFile->Close();
				m_svfitCacheTree->Delete();
				m_svfitCacheTree = new TTree(settings.GetSvfitCacheTree().c_str(),
			                             	 settings.GetSvfitCacheTree().c_str());
				if (! m_firstSvfitCacheFile)
				{
			    	m_fileIndex++;
				}
				else
				{
			    	m_firstSvfitCacheFile = false;
				}
				product.m_svfitEventKey.CreateBranches(m_svfitCacheTree);
				product.m_svfitInputs.CreateBranches(m_svfitCacheTree);
				product.m_svfitResults.CreateBranches(m_svfitCacheTree);
				m_svfitCacheTreeInitialised = true;
			}
			if (product.m_svfitCalculated)
			{
				m_svfitCacheTree->Fill();
			}
			// at reaching a predefined threshold create the outputfile with index m_fileIndex and save the tree
			// afterwards crear the Cache tree
			if ( m_svfitCacheTree->GetEntries() == settings.GetSvfitInputCutOff())
			{
				m_svfitCacheTreeInitialised = false;
			}
		}
	}
	else
	{
		if (! m_svfitCacheTreeInitialised)
		{
			product.m_svfitEventKey.CreateBranches(m_svfitCacheTree);
			product.m_svfitInputs.CreateBranches(m_svfitCacheTree);
			product.m_svfitResults.CreateBranches(m_svfitCacheTree);
			m_svfitCacheTreeInitialised = true;
		}
		if (product.m_svfitCalculated)
		{
				m_svfitCacheTree->Fill();
		}
	}
}


void SvfitCacheConsumer::Finish(setting_type const& settings)
{
	if (settings.GetGenerateSvfitInput())
	{
		//write remaining Cache tree to the last file and write it
		std::string cacheFilename;
		if(m_svfitCacheTree->GetEntries() == 0) // do not save empty cache files
			return;
		if(settings.GetUseFirstInputFileNameForSvfit())
		{
			cacheFilename = boost::filesystem::basename(boost::filesystem::path(settings.GetInputFiles().at(0)))+std::string("-SvfitCacheInput-")+settings.GetRootFileFolder()+std::to_string(m_fileIndex)+std::string(".root");
		}
		else
		{
			cacheFilename = boost::filesystem::basename(boost::filesystem::path(settings.GetSvfitOutFile()))+settings.GetRootFileFolder()+std::to_string(m_fileIndex)+std::string(".root");
		}
		TFile* SvfitFile = new TFile(cacheFilename.c_str(),"RECREATE");
		RootFileHelper::SafeCd(SvfitFile, settings.GetRootFileFolder());
		m_svfitCacheTree->Write(m_svfitCacheTree->GetName());
		SvfitFile->Close();
	}
	else
	{
		RootFileHelper::SafeCd(settings.GetRootOutFile(),
		                       settings.GetRootFileFolder());
		m_svfitCacheTree->Write(m_svfitCacheTree->GetName());
	}
}

