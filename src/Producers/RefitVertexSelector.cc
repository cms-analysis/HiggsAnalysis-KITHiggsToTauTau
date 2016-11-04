
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RefitVertexSelector.h"

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "boost/functional/hash.hpp"


void RefitVertexSelectorBase::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	

}


void RefitVertexSelectorBase::Produce(event_type const& event, product_type& product,
										setting_type const& settings) const
{
	
	assert(product.m_ptOrderedLeptons.size() > 0);

	// create hashes from lepton selection
	std::vector<KLepton*> leptons = product.m_ptOrderedLeptons;
	std::vector<size_t> hashes;

	if (leptons.size() == 2){
		
		size_t hash = 0;

		for (auto lepton : leptons){
			boost::hash_combine(hash, lepton->internalId);
		} // for over leptons
		hashes.push_back(hash);

		std::swap(leptons[0], leptons[1]);
		hash = 0;
		for (auto lepton : leptons){
			boost::hash_combine(hash, lepton->internalId);
		}
		hashes.push_back(hash);

	} // if leptons.size==2


	// find the vertex among the refitted vertices
	//bool foundRefitPV = false;

	for (auto vertex : *(event.m_refitVertices)){
		if ( std::find(hashes.begin(), hashes.end(), vertex.leptonSelectionHash) != hashes.end() ){
			product.m_refitPV = &vertex;
			//foundRefitPV = true;
			break;
		}
	} // loop over refitted vertices collection

	
	// find the vertex among the refitted vertices calculated w/ beamspot constraint
	//bool foundRefitBSPV = false;

	for (auto vertex : *(event.m_refitBSVertices)){
		if ( std::find(hashes.begin(), hashes.end(), vertex.leptonSelectionHash) != hashes.end() ){
			product.m_refitBSPV = &vertex;
			//foundRefitBSPV = true;
			break;
		}
	} // loop over refitted vertices collection

}


std::string RefitVertexSelector::GetProducerId() const
{
	return "RefitVertexSelector";
}


void RefitVertexSelector::Init(setting_type const& settings)
{
	RefitVertexSelectorBase::Init(settings);
}


void RefitVertexSelector::Produce(event_type const& event, product_type& product,
									setting_type const& settings) const
{
	RefitVertexSelectorBase::Produce(event, product, settings);
}
