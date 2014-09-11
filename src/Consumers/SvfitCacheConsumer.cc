
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
	ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product, settings);

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


void SvfitCacheConsumer::Finish(setting_type const& settings)
{
	RootFileHelper::SafeCd(settings.GetRootOutFile(),
	                       settings.GetRootFileFolder());
	
	m_svfitCacheTree->Write(m_svfitCacheTree->GetName());
}

