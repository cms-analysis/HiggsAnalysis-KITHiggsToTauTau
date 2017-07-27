#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/KaonsProducer.h"

// #include "Artus/Utility/interface/DefaultValues.h"
// #include "Artus/Utility/interface/SafeMap.h"

// #include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

inline std::string KaonsProducer::GetProducerId() const { return "KaonsProducer"; }

void KaonsProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	UseVertex = settings.GetUseVertex();
	VertexFitter = settings.GetVertexFitter();
	UseRefTracks = settings.GetUseRefTracks();
	DoKShorts = settings.GetDoKShorts();
	DoLambdas = settings.GetDoLambdas();
	TkChi2Cut = settings.GetTkChi2Cut();
	TkNHitsCut = settings.GetTkNHitsCut();
	TkPtCut = settings.GetTkPtCut();
	TkIPSigXYCut = settings.GetTkIPSigXYCut();
	TkIPSigZCut = settings.GetTkIPSigZCut();
	VtxChi2Cut = settings.GetVtxChi2Cut();
	VtxDecaySigXYZCut = settings.GetVtxDecaySigXYZCut();
	VtxDecaySigXYCut = settings.GetVtxDecaySigXYCut();
	TkDCACut = settings.GetTkDCACut();
	MPiPiCut = settings.GetMPiPiCut();
	InnerHitPosCut = settings.GetInnerHitPosCut();
	CosThetaXYCut = settings.GetCosThetaXYCut();
	CosThetaXYZCut = settings.GetCosThetaXYZCut();
	KShortMassCut = settings.GetKShortMassCut();
	LambdaMassCut = settings.GetLambdaMassCut();
	KaonDebugOutput = settings.GetKaonDebugOutput();

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("kaonNumber", [](event_type const& event, product_type const& product)
	{
		return product.kaonNumber;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("kaonMass", [](event_type const& event, product_type const& product)
	{
		return product.kaonMass;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("kaonMassLV", [](event_type const& event, product_type const& product)
	{
		return product.kaonMassLV;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("kaonPosDaugterMass", [](event_type const& event, product_type const& product)
	{
		return product.kaonPosDaugterMass;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("kaonNegDaugterMass", [](event_type const& event, product_type const& product)
	{
		return product.kaonNegDaugterMass;
	});
	//TODO
	// register collection for Ks
	// first add it to the interface/HttProduct.h
}

bool KaonsProducer::TrackIsGood(KTrack tmpTrack, KBeamSpot theBeamSpot, RMPoint referencePos, KVertex referenceVtx, bool verbose) const
{
	double ipsigXY = std::abs(tmpTrack.getDxy(&theBeamSpot) / tmpTrack.errDxy());
	if (UseVertex) ipsigXY = std::abs(tmpTrack.getDxy(&referenceVtx)/tmpTrack.errDxy());
	double ipsigZ  = std::abs(tmpTrack.getDz(&theBeamSpot) / tmpTrack.errDz());
	if (verbose) 
	{
		dout("\t\tipsigXY =", ipsigXY, "= tmpTrack.getDxy(&theBeamSpot) / tmpTrack.errDxy() =", tmpTrack.getDxy(&theBeamSpot), "/", tmpTrack.errDxy());
		dout("\n\t",
		"nValidHits:", (int)tmpTrack.nValidHits(), ">=", (int)TkNHitsCut , "\n\t",
		"tmpTrack.p4.Pt()", tmpTrack.p4.Pt(), ">", TkPtCut , "\n\t",
		"ipsigXY", ipsigXY, ">", TkIPSigXYCut , "\n\t",
		"ipsigZ", ipsigZ, ">", TkIPSigZCut);
		dout("tmpTrack.d3D:", tmpTrack.d3D);
	}

	if ( !(tmpTrack.nDOF != 0 && tmpTrack.chi2 / tmpTrack.nDOF < TkChi2Cut))
	{
		if (verbose) dout("TrackIsGood::Didn't pass TkChi2Cut");
		return false;
	} 
	else if (!((int)tmpTrack.nValidHits() >= (int)TkNHitsCut))
	{
		if (verbose) dout("TrackIsGood::Didn't pass TkNHitsCut");
		return false;
	} 
	else if(!(tmpTrack.p4.Pt() > TkPtCut))
	{
		if (verbose) dout("TrackIsGood::Didn't pass TkPtCut");
		return false;
	} 
	else if(!(ipsigXY > TkIPSigXYCut))
	{
		if (verbose) dout("TrackIsGood::Didn't pass TkIPSigXYCut");
		return false;
	}
	else if(!(ipsigZ > TkIPSigZCut))
	{
		if (verbose) dout("TrackIsGood::Didn't pass TkIPSigZCut");
		return false;
	}
	else return true;

}

void KaonsProducer::Produce(event_type const& event, product_type& product,
                                     setting_type const& settings) const
{
	dout();
	using std::vector;
	product.kaonNumber = 0;

	assert(event.m_taus);
	assert(event.m_beamSpot);
	//
	KBeamSpot theBeamSpot = (*event.m_beamSpot);
	RMPoint referencePos(theBeamSpot.position);
	KVertex referenceVtx;
	if (UseVertex)
	{
		referenceVtx = event.m_vertexSummary->pv;
		referencePos = referenceVtx.position;
	}

	for (KTaus::iterator tau = event.m_taus->begin(); tau != event.m_taus->end(); ++tau)
	{
		KPFCandidates theKPFCandidatesPionsCollection;
		// Build the colection of tracks with indexes set up as for Kaons
		{
			// In signal cone
			KPFCandidates hadronCandidates = tau->chargedHadronCandidates;
			for (size_t i = 0; i < hadronCandidates.size(); ++i)
			{
				//TODO: move the check for pdgId on the Kappa level?
				//if (abs(chargedPrt->pdgId) == 211)
				if (hadronCandidates[i].bestTrack.magneticField != 0) // so the bestTrack was
				theKPFCandidatesPionsCollection.push_back(hadronCandidates[i]);
			}

			// In isolation code
			hadronCandidates = tau->isolationChargedHadronCandidates;
			for (size_t i = 0; i < hadronCandidates.size(); ++i)
			{
				if (hadronCandidates[i].bestTrack.magneticField != 0)
				theKPFCandidatesPionsCollection.push_back(hadronCandidates[i]);
			}
		}

		KKaonCandidates kshortCandidatesOfSingleJet = tau->kshortCandidates; // vector of all the Kaons 
		for (auto singleKaonCand = kshortCandidatesOfSingleJet.begin(); singleKaonCand != kshortCandidatesOfSingleJet.end(); ++singleKaonCand)
		{

			// Track validity check  // TODO: check that the tracks correspond accross collections
			{
				// short int trackIndex_1 = singleKaonCand->firstTransTrack.indexOfTrackInColl;
				// short int trackIndex_2 = singleKaonCand->secondTransTrack.indexOfTrackInColl;

				KTrack tmpTrack_1 = singleKaonCand->firstTransPFCand.bestTrack;//= theKPFCandidatesPionsCollection[trackIndex_1].bestTrack;
				KTrack tmpTrack_2 = singleKaonCand->secondTransPFCand.bestTrack;//= theKPFCandidatesPionsCollection[trackIndex_2].bestTrack;
		
				if (!TrackIsGood(tmpTrack_1, theBeamSpot, referencePos, referenceVtx, false) || 
					!TrackIsGood(tmpTrack_2, theBeamSpot, referencePos, referenceVtx, false)) continue;
			}

			// measure distance between tracks at their closest approach
			if (singleKaonCand->distanceOfClosestApproach > TkDCACut) continue;

			// the POCA should at least be in the sensitive volume TODO::KAPPA
				// GlobalPoint cxPt = cApp.crossingPoint(); // TODO::KAPPA
				if (sqrt(singleKaonCand->POCA.x() * singleKaonCand->POCA.x() + singleKaonCand->POCA.y() * singleKaonCand->POCA.y()) > 120. || std::abs(singleKaonCand->POCA.z()) > 300.) continue; 

			// calculate mPiPi
				if (singleKaonCand->initialFirstTSCP.mass() > MPiPiCut) continue;
			if ( singleKaonCand->secondaryVertex.nDOF == 0 || singleKaonCand->secondaryVertex.chi2 / singleKaonCand->secondaryVertex.nDOF > VtxChi2Cut) continue; 
			

			if (UseVertex)
			{
				if (singleKaonCand->distMagXYPV / singleKaonCand->sigmaDistMagXYPV < VtxDecaySigXYCut)
				{
					dout("didn't pass 2D signif PV");
					continue;
				}
				if (singleKaonCand->distMagXYZPV / singleKaonCand->sigmaDistMagXYZPV < VtxDecaySigXYZCut)
				{
					dout("didn't pass 3D signif BS:", singleKaonCand->distMagXYZPV, "/", singleKaonCand->sigmaDistMagXYZPV, "<", VtxDecaySigXYZCut);
					//continue;
				}
			}
			else
			{
				if (singleKaonCand->distMagXYBS / singleKaonCand->sigmaDistMagXYBS < VtxDecaySigXYCut)
				{
					dout("didn't pass 2D signif PV");
					continue;
				}
				if (singleKaonCand->distMagXYZBS / singleKaonCand->sigmaDistMagXYZBS < VtxDecaySigXYZCut)
				{
					dout("didn't pass 3D signif BS:", singleKaonCand->distMagXYZBS, "/", singleKaonCand->sigmaDistMagXYZBS, "<", VtxDecaySigXYZCut);
					//continue;
				}
			}

			// make sure the vertex radius is within the inner track hit radius - NOT ON MINIAOD LEVEL?
			/* TODO : use ref point
				if (InnerHitPosCut > 0. && positiveTrackRef->innerOk())  // TODO::KAPPA
				{
					reco::Vertex::Point posTkHitPos = positiveTrackRef->innerPosition(); // TODO::KAPPA
					double posTkHitPosD2 =  pow(posTkHitPos.x() - referencePos.x(), 2) + pow(posTkHitPos.y() - referencePos.y(), 2);

					if (sqrt(posTkHitPosD2) < (distMagXY - sigmaDistMagXY * innerHitPosCut_)) continue;
				}
				if (InnerHitPosCut > 0. && negativeTrackRef->innerOk()) 
				{
					reco::Vertex::Point negTkHitPos = negativeTrackRef->innerPosition();
					double negTkHitPosD2 = pow(negTkHitPos.x() - referencePos.x(), 2) + pow(negTkHitPos.y()-referencePos.y(), 2);

					if (sqrt(negTkHitPosD2) < (distMagXY - sigmaDistMagXY * innerHitPosCut_)) continue;
				}
			*/

			if (UseVertex)
			{
				// 2D pointing angle
				if (singleKaonCand->angleXYPV < CosThetaXYCut) continue;
				// 3D pointing angle
				if (singleKaonCand->angleXYZPV < CosThetaXYZCut) continue;
			}
			else
			{
				// 2D pointing angle
				if (singleKaonCand->angleXYBS < CosThetaXYCut) continue;
				// 3D pointing angle
				if (singleKaonCand->angleXYZPS < CosThetaXYZCut) continue;
			}			
			dout("PASSED");

			product.kaonMass.push_back(singleKaonCand->kMass);
			product.kaonPosDaugterMass.push_back(singleKaonCand->firstPiMomentumClosestToSV.mass());
			product.kaonNegDaugterMass.push_back(singleKaonCand->secondPiMomentumClosestToSV.mass());
			product.kaonNumber++;
		}

	}

	dout("End event\n\n\n");
}