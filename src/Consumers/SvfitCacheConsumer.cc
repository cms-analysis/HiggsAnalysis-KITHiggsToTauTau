
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/SvfitCacheConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"


void SvfitCacheConsumer::Init(Pipeline<HttTypes>* pipeline) {
	ConsumerBase<HttTypes>::Init(pipeline);

	RootFileHelper::SafeCd(GetPipelineSettings().GetRootOutFile(),
	                       GetPipelineSettings().GetRootFileFolder());
	
	m_svfitCacheTree = new TTree(GetPipelineSettings().GetSvfitCacheTree().c_str(), GetPipelineSettings().GetSvfitCacheTree().c_str());
	m_svfitCacheTreeInitialised = false;
}

void SvfitCacheConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product) {
	ConsumerBase<HttTypes>::ProcessFilteredEvent(event, product);

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


void SvfitCacheConsumer::Finish()
{
	RootFileHelper::SafeCd(GetPipelineSettings().GetRootOutFile(),
	                       GetPipelineSettings().GetRootFileFolder());
	
	m_svfitCacheTree->Write(m_svfitCacheTree->GetName());
}

