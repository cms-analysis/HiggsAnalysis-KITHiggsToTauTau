
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RefitVertexSelector.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "boost/functional/hash.hpp"


std::string RefitVertexSelector::GetProducerId() const
{
	return "RefitVertexSelector";
}


void RefitVertexSelector::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	// add possible quantities for the lambda ntuples consumers

	// refitted PV coordinates and parameters
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVx", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->position.x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->position.y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->position.z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVchi2", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->chi2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVnDOF", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->nDOF : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVnTracks", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->nTracks : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVsigmaxx", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->covariance.At(0,0) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVsigmayy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->covariance.At(1,1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVsigmazz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->covariance.At(2,2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVsigmaxy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->covariance.At(0,1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVsigmaxz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->covariance.At(0,2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVsigmayz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != nullptr) ? (product.m_refitPV)->covariance.At(1,2) : DefaultValues::UndefinedFloat);
	});
	
	// refitted (w/ BS constraint) PV coordinates and parameters
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSx", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->position.x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->position.y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->position.z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSchi2", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->chi2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSnDOF", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->nDOF : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSnTracks", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->nTracks : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSsigmaxx", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->covariance.At(0,0) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSsigmayy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->covariance.At(1,1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSsigmazz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->covariance.At(2,2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSsigmaxy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->covariance.At(0,1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSsigmaxz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->covariance.At(0,2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refitPVBSsigmayz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPVBS != nullptr) ? (product.m_refitPVBS)->covariance.At(1,2) : DefaultValues::UndefinedFloat);
	});

	// track ref point coordinates
	// lepton1
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refP1x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refP1 != nullptr) ? (product.m_refP1)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refP1y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refP1 != nullptr) ? (product.m_refP1)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refP1z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refP1 != nullptr) ? (product.m_refP1)->z() : DefaultValues::UndefinedFloat);
	});
	// lepton2
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refP2x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refP2 != nullptr) ? (product.m_refP2)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refP2y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refP2 != nullptr) ? (product.m_refP2)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "refP2z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refP2 != nullptr) ? (product.m_refP2)->z() : DefaultValues::UndefinedFloat);
	});

	// track momentum coordinates
	// lepton1
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "track1p4x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_track1p4 != nullptr) ? (product.m_track1p4)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "track1p4y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_track1p4 != nullptr) ? (product.m_track1p4)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "track1p4z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_track1p4 != nullptr) ? (product.m_track1p4)->z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d3D_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_d3DnewPV1 ? product.m_d3DnewPV1 : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "err3D_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_err3DnewPV1 ? product.m_err3DnewPV1 : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d2D_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_d2DnewPV1 ? product.m_d2DnewPV1 : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "err2D_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_err2DnewPV1 ? product.m_err2DnewPV1 : DefaultValues::UndefinedFloat;
	});
	// lepton2
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "track2p4x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_track2p4 != nullptr) ? (product.m_track2p4)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "track2p4y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_track2p4 != nullptr) ? (product.m_track2p4)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "track2p4z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_track2p4 != nullptr) ? (product.m_track2p4)->z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d3D_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_d3DnewPV2 ? product.m_d3DnewPV2 : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "err3D_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_err3DnewPV2 ? product.m_err3DnewPV2 : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d2D_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_d2DnewPV2 ? product.m_d2DnewPV2 : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "err2D_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_err2DnewPV2 ? product.m_err2DnewPV2 : DefaultValues::UndefinedFloat;
	});
	
}


void RefitVertexSelector::Produce(event_type const& event, product_type& product,
                                  setting_type const& settings, metadata_type const& metadata) const
{
	
	assert(product.m_flavourOrderedLeptons.size() > 0);

	// create hashes from lepton selection
	std::vector<KLepton*> leptons = product.m_flavourOrderedLeptons;
	std::vector<size_t> hashes;

	if (leptons.size() == 2 && event.m_refitVertices && event.m_refitBSVertices){
		
		size_t hash = 0;

		// get reference point of the track
		product.m_refP1 = &((leptons.at(0))->track.ref);
		product.m_refP2 = &((leptons.at(1))->track.ref);

		// get momentum of the track
		product.m_track1p4 = &((leptons.at(0))->track.p4);
		product.m_track2p4 = &((leptons.at(1))->track.p4);

		for (auto lepton : leptons){
			boost::hash_combine(hash, lepton->internalId);
		} // for over leptons
		hashes.push_back(hash);

		std::swap(leptons.at(0), leptons.at(1));
		hash = 0;
		for (auto lepton : leptons){
			boost::hash_combine(hash, lepton->internalId);
		}
		hashes.push_back(hash);

		// find the vertex among the refitted vertices
		unsigned int index = 0;
		for (std::vector<KRefitVertex>::iterator vertex = event.m_refitVertices->begin(); vertex != event.m_refitVertices->end(); ++vertex){
			if ( std::find(hashes.begin(), hashes.end(), vertex->leptonSelectionHash) != hashes.end() ){
				product.m_refitPV = &(*vertex);
				break;
			}
			++index;
		} // loop over refitted vertices collection
	
		// find the vertex among the refitted vertices calculated w/ beamspot constraint
		for (std::vector<KRefitVertex>::iterator vertex = event.m_refitBSVertices->begin(); vertex != event.m_refitBSVertices->end(); ++vertex){
			if ( std::find(hashes.begin(), hashes.end(), vertex->leptonSelectionHash) != hashes.end() ){
				product.m_refitPVBS = &(*vertex);
				break;
			}
		} // loop over refitted vertices collection
	
	
		// get IP and corresponding error calculated with the IPTools methods
		if (product.m_refitPV && (index < event.m_refitVertices->size())){
			// lepton1
			if (index < leptons.at(0)->track.d3DnewPV.size())
			{
				product.m_d3DnewPV1 = leptons.at(0)->track.d3DnewPV.at(index);
				product.m_err3DnewPV1 = leptons.at(0)->track.err3DnewPV.at(index);
				product.m_d2DnewPV1 = leptons.at(0)->track.d2DnewPV.at(index);
				product.m_err2DnewPV1 = leptons.at(0)->track.err2DnewPV.at(index);
			}

			// lepton2
			if (index < leptons.at(1)->track.d3DnewPV.size())
			{
				product.m_d3DnewPV2 = leptons.at(1)->track.d3DnewPV.at(index);
				product.m_err3DnewPV2 = leptons.at(1)->track.err3DnewPV.at(index);
				product.m_d2DnewPV2 = leptons.at(1)->track.d2DnewPV.at(index);
				product.m_err2DnewPV2 = leptons.at(1)->track.err2DnewPV.at(index);
			}
		}

	} // if leptons.size==2

}

