#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/KaonsProducer.h"

// #include "Artus/Utility/interface/DefaultValues.h"
// #include "Artus/Utility/interface/SafeMap.h"

// #include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

inline std::string KaonsProducer::GetProducerId() const { return "KaonsProducer"; }

void KaonsProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

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

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "kaonNumber", [](event_type const& event, product_type const& product)
	{
		return product.kaonNumber;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "kaonMass", [](event_type const& event, product_type const& product)
	{
		return product.kaonMass;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "kaonMassLV", [](event_type const& event, product_type const& product)
	{
		return product.kaonMassLV;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "kaonPosDaugterMass", [](event_type const& event, product_type const& product)
	{
		return product.kaonPosDaugterMass;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity(metadata, "kaonNegDaugterMass", [](event_type const& event, product_type const& product)
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
                            setting_type const& settings, metadata_type const& metadata) const
{
	dout();
	using std::vector;
	product.kaonNumber = 0;

	assert(event.m_taus);
	assert(event.m_beamSpot);

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
			if (UseVertex)
			{
				if (pow(singleKaonCand->referencePosPV.x() - referencePos.x(), 2) + pow(singleKaonCand->referencePosPV.y() - referencePos.y(), 2) + pow(singleKaonCand->referencePosPV.z() - referencePos.z(), 2) > 0 )
				{
					dout("wrong PV is taken");
					exit(1);
				}
			}
			else
			{
				if (pow(singleKaonCand->referencePosBS.x() - referencePos.x(), 2) + pow(singleKaonCand->referencePosBS.y() - referencePos.y(), 2) + pow(singleKaonCand->referencePosBS.z() - referencePos.z(), 2) > 0 )
				{
					dout("wrong BS is taken:", singleKaonCand->referencePosBS.x() - referencePos.x(), singleKaonCand->referencePosBS.y() - referencePos.y(), singleKaonCand->referencePosBS.z() - referencePos.z());
					exit(1);
				}
			}

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

			// the POCA should at least be in the sensitive volume
				if (sqrt(pow(singleKaonCand->POCA.x(), 2) + pow(singleKaonCand->POCA.y(),2)) > 120 || std::abs(singleKaonCand->POCA.z()) > 300.) continue;  // 120 - outer radius of strip detector; 300cm -- with EndCup

			// calculate mPiPi
				if (singleKaonCand->initialFirstTSCP.mass() > MPiPiCut) continue;
			if ( singleKaonCand->secondaryVertex.nDOF == 0 || singleKaonCand->secondaryVertex.chi2 / singleKaonCand->secondaryVertex.nDOF > VtxChi2Cut) continue;

			float sigmaDistMagXY, sigmaDistMagXYZ, distMagXY, distMagXYZ, pointingAngle2D, pointingAngle3D;
			if (UseVertex)
			{
				sigmaDistMagXY = singleKaonCand->sigmaDistMagXYPV;
				sigmaDistMagXYZ = singleKaonCand->sigmaDistMagXYZPV;
				distMagXY = singleKaonCand->distMagXYPV;
				distMagXYZ = singleKaonCand->distMagXYZPV;
				pointingAngle2D = singleKaonCand->angleXYPV;
				pointingAngle3D = singleKaonCand->angleXYZPV;
			}
			else
			{
				sigmaDistMagXY = singleKaonCand->sigmaDistMagXYBS;
				sigmaDistMagXYZ = singleKaonCand->sigmaDistMagXYZBS;
				distMagXY = singleKaonCand->distMagXYBS;
				distMagXYZ = singleKaonCand->distMagXYZBS;
				pointingAngle2D = singleKaonCand->angleXYBS;
				pointingAngle3D = singleKaonCand->angleXYZPS;
			}

			//!
			if (distMagXY / sigmaDistMagXY < VtxDecaySigXYCut)
			{
				dout("didn't pass 2D significance");
				continue;
			}
			if (distMagXYZ / sigmaDistMagXYZ < VtxDecaySigXYZCut)
			{
				dout("didn't pass 3D significance:", singleKaonCand->distMagXYZPV, "/", singleKaonCand->sigmaDistMagXYZPV, "<", VtxDecaySigXYZCut);
				continue;
			}

			// make sure the vertex radius is within the inner track hit radius - NOT ON MINIAOD LEVEL?
			// check if either track has a hit radially inside the vertex position minus this number times the sigma of the vertex fit
			// note: Set this to -1 to disable this cut, which MUST be done if you want to run on the AOD track collection!
			if (InnerHitPosCut > 0)
			{
				RMPoint posTkHitPos = singleKaonCand->firstTransPFCand.bestTrack.ref;
				RMPoint negTkHitPos = singleKaonCand->secondTransPFCand.bestTrack.ref;
				double posTkHitPosDist =  sqrt(pow(posTkHitPos.x() - referencePos.x(), 2) + pow(posTkHitPos.y() - referencePos.y(), 2));
				double negTkHitPosDist = sqrt(pow(negTkHitPos.x() - referencePos.x(), 2) + pow(negTkHitPos.y() - referencePos.y(), 2));

				if (posTkHitPosDist < (distMagXY - sigmaDistMagXY * InnerHitPosCut))
				{
					dout("failed posTkHitPosDist cut:", posTkHitPosDist, "<", (distMagXY - sigmaDistMagXY * InnerHitPosCut));
					continue;
				}
				if (negTkHitPosDist < (distMagXY - sigmaDistMagXY * InnerHitPosCut))
				{
					dout("failed negTkHitPosDist cut:", negTkHitPosDist, "<", (distMagXY - sigmaDistMagXY * InnerHitPosCut));
					continue;
				}
			}

			// cos(angleXY) between x and p of K candidate
			// cos(angleXYZ) between x and p of K candidate
			if (pointingAngle2D < CosThetaXYCut) continue;// 2D pointing angle
			if (pointingAngle3D < CosThetaXYZCut) continue;// 3D pointing angle

			dout("PASSED");

			product.kaonMass.push_back(singleKaonCand->kMass);
			product.kaonPosDaugterMass.push_back(singleKaonCand->firstPiMomentumClosestToSV.mass());
			product.kaonNegDaugterMass.push_back(singleKaonCand->secondPiMomentumClosestToSV.mass());
			product.kaonNumber++;
		}

	}

	dout("End event\n\n\n");
}
