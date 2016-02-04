
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/SvfitCacheConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"


void SvfitCacheConsumer::Init(setting_type const& settings)
{
	ConsumerBase<HttTypes>::Init(settings);

	RootFileHelper::SafeCd(settings.GetRootOutFile(),
	                       settings.GetRootFileFolder());
	
	m_svfitCacheTree = new TTree(settings.GetSvfitCacheTree().c_str(),
	                             settings.GetSvfitCacheTree().c_str());
	m_svfitCacheTreeInitialised = false;
}

void SvfitCacheConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product,
                                              setting_type const& settings)
{
	// make sure the SvfitOutputFile option is set reasonably
	assert((! settings.GetGenerateSvFitInput()) || (settings.GetSvfitOutFile().find(".root") != std::string::npos));
	ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings);
	if (settings.GetGenerateSvFitInput())
	{
		if (! m_svfitCacheTreeInitialised)
		{
			TFile* SvfitFile = new TFile(settings.GetSvfitOutFile().replace(settings.GetSvfitOutFile().find(".root"), 5, std::to_string(fileindex)+std::string(".root")).c_str(), "RECREATE");
			RootFileHelper::SafeCd(SvfitFile, settings.GetRootFileFolder());
			m_svfitCacheTree->Write(m_svfitCacheTree->GetName());
			SvfitFile->Close();
			m_svfitCacheTree->Delete();
			m_svfitCacheTree = new TTree(settings.GetSvfitCacheTree().c_str(),
			                             settings.GetSvfitCacheTree().c_str());
			if (! m_firstSvfitCacheFile)
			{
			    fileindex++;
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
		// at reaching a predefined threshold create the outputfile with index fileindex and save the tree
		// afterwards crear the Cache tree
		if ( m_svfitCacheTree->GetEntries() == settings.GetSvFitInputCutOff())
		{
			m_svfitCacheTreeInitialised = false;
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
	if (settings.GetGenerateSvFitInput())
	{
		//write remaining Cache tree to the last file and write it
		TFile* SvfitFile = new TFile(settings.GetSvfitOutFile().replace(settings.GetSvfitOutFile().find(".root"),5,std::to_string(fileindex)+std::string(".root")).c_str(),"RECREATE");
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

