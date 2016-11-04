
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RefitVertexSelector.h"



void RefitVertexSelectorBase::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	
	// thePV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVx", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.x();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVy", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVz", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.z();
	});

	// refitted PV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitPVx", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitPV ? (product.m_refitPV)->position.x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitPVy", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitPV ? (product.m_refitPV)->position.y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitPVz", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitPV ? (product.m_refitPV)->position.z() : DefaultValues::UndefinedFloat);
	});
	
	// refitted (w/ BS constraint) PV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitBSPVx", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitBSPV ? (product.m_refitBSPV)->position.x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitBSPVy", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitBSPV ? (product.m_refitBSPV)->position.y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitBSPVz", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitBSPV ? (product.m_refitBSPV)->position.z(): DefaultValues::UndefinedFloat);
	});

}


void RefitVertexSelectorBase::Produce(event_type const& event, product_type& product,
										setting_type const& settings) const
{
	
	assert(product.m_ptOrderedLeptons.size() > 0);

	// save thePV
	product.m_thePV = &event.m_vertexSummary->pv;

	// create hashes from lepton selection
	std::vector<KLepton*> leptons = product.m_ptOrderedLeptons;
	std::vector<size_t> hashes;

	if (leptons.size() == 2 && event.m_refitVertices && event.m_refitBSVertices){
		
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
