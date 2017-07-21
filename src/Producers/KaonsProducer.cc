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

void KaonsProducer::Produce(event_type const& event, product_type& product,
                                     setting_type const& settings) const
{
	dout();
	using std::vector;
	product.kaonNumber = 0;

	assert(event.m_taus);
	assert(event.m_beamSpot);

	// select input source from used ktuple
	vector<KTau*> taus;
	vector<KTrack> theTrackCollection;
	//map<KTrack, KPFCandidates> theKPFCandidatesMap;
	KPFCandidates theKPFCandidatesPionsCollection;
	// Create list of pions tracks
	/* V0Fitter
		edm::Handle<reco::TrackCollection> theTrackHandle;
		iEvent.getByToken(token_tracks, theTrackHandle);
		if (!theTrackHandle->size()) return;
		const reco::TrackCollection* theTrackCollection = theTrackHandle.product();
	*/
	taus.resize(event.m_taus->size());
	unsigned int isolStart = 0;
	for (KTaus::iterator tau = event.m_taus->begin(); tau != event.m_taus->end(); ++tau)
	{
		KPFCandidates hadronCandidates = tau->chargedHadronCandidates;
		for (auto chargedPrt = hadronCandidates.begin(); chargedPrt != hadronCandidates.end(); ++chargedPrt)
		{
			if (abs(chargedPrt->pdgId) == 211)
			{
				theTrackCollection.push_back(chargedPrt->bestTrack);
				//theKPFCandidatesMap[chargedPrt->bestTrack] = *chargedPrt;
				auto i = std::distance(hadronCandidates.begin(), chargedPrt);
				theKPFCandidatesPionsCollection.push_back(hadronCandidates[i]);
			}
			isolStart++;
		}

		hadronCandidates = tau->isolationChargedHadronCandidates;
		for (KPFCandidates::iterator chargedPrt = hadronCandidates.begin(); chargedPrt != hadronCandidates.end(); ++chargedPrt)
		{
			if (abs(chargedPrt->pdgId) == 211)
			{
				auto i = std::distance(hadronCandidates.begin(), chargedPrt);
				theTrackCollection.push_back(chargedPrt->bestTrack);
				theKPFCandidatesPionsCollection.push_back(hadronCandidates[i]);
			}
		}
	}
	dout("Total theTrackCollection size:", theTrackCollection.size(), "==", theKPFCandidatesPionsCollection.size());

	// Get the BS
	/* V0Fitter
		edm::Handle<reco::BeamSpot> theBeamSpotHandle;
		iEvent.getByToken(token_beamSpot, theBeamSpotHandle);
		const reco::BeamSpot* theBeamSpot = theBeamSpotHandle.product();
		math::XYZPoint referencePos(theBeamSpot->position());

		reco::Vertex referenceVtx;
		if (useVertex_)
		{
			edm::Handle<std::vector<reco::Vertex>> vertices;
			iEvent.getByToken(token_vertices, vertices);
			referenceVtx = vertices->at(0);
			referencePos = referenceVtx.position();
		}
	*/
	KBeamSpot theBeamSpot = (*event.m_beamSpot);
	RMPoint referencePos(theBeamSpot.position);
	KVertex referenceVtx;
	if (UseVertex)
	{
		referenceVtx = event.m_vertexSummary->pv;
		referencePos = referenceVtx.position;
	}

	// STORE ALSO THE TRANSIENT TRACK
	/* V0Fitter
		edm::ESHandle<MagneticField> theMagneticFieldHandle;
		iSetup.get<IdealMagneticFieldRecord>().get(theMagneticFieldHandle);
		const MagneticField* theMagneticField = theMagneticFieldHandle.product();

		std::vector<reco::TrackRef> theTrackRefs;
		std::vector<reco::TransientTrack> theTransTracks;
	*/

	// Preselection for the tracks -- cut on impact parameter of the track
		for (KPFCandidates::iterator it = theKPFCandidatesPionsCollection.begin();
                              it != theKPFCandidatesPionsCollection.end();
                              /*it++*/)
		{
				KTrack* tmpTrack = &(it->bestTrack);
				double ipsigXY = std::abs(tmpTrack->getDxy(&theBeamSpot) / tmpTrack->errDxy);
				if (UseVertex) ipsigXY = std::abs(tmpTrack->getDxy(&referenceVtx)/tmpTrack->errDxy);
				double ipsigZ  = std::abs(tmpTrack->getDz(&theBeamSpot) / tmpTrack->errDz);
				dout("\t\tipsigXY =", ipsigXY, "= tmpTrack->getDxy(&theBeamSpot) / tmpTrack->errDxy =", tmpTrack->getDxy(&theBeamSpot), "/", tmpTrack->errDxy);

				dout("\n\t",
					"nValidHits:", (int)tmpTrack->nValidHits(), ">=", (int)TkNHitsCut , "\n\t",
					"tmpTrack->p4.Pt()", tmpTrack->p4.Pt(), ">", TkPtCut , "\n\t",
					"ipsigXY", ipsigXY, ">", TkIPSigXYCut , "\n\t",
					"ipsigZ", ipsigZ, ">", TkIPSigZCut);
				dout("tmpTrack->d3D:", tmpTrack->d3D);

				if (//tmpTrack->chi2 / tmpTrack->nDOF < TkChi2Cut &&
					(int)tmpTrack->nValidHits() >= (int)TkNHitsCut &&
					tmpTrack->p4.Pt() > TkPtCut &&
					ipsigXY > TkIPSigXYCut &&
					ipsigZ > TkIPSigZCut
					)
				{
				    // Missing TransientTrack construction
					// 	reco::TransientTrack tmpTransient(*tmpRef, theMagneticField);
					// 	theTransTracks.push_back(std::move(tmpTransient));
					++it;
				}
				else it = theKPFCandidatesPionsCollection.erase(it);
		}

	// loop over tracks and vertex good charged track pairs
	for (unsigned int trdx1 = 0; trdx1 < theKPFCandidatesPionsCollection.size(); ++trdx1)
	{
		for (unsigned int trdx2 = trdx1 + 1; trdx2 < theKPFCandidatesPionsCollection.size(); ++trdx2)
		{
			KPFCandidate positivePionCand, negativePionCand;
			KTrack firsTrackRef_cand = theKPFCandidatesPionsCollection[trdx1].bestTrack;
			KTrack secondTrackRef_cand = theKPFCandidatesPionsCollection[trdx2].bestTrack;
			// reco::TransientTrack* posTransTkPtr = nullptr, negTransTkPtr = nullptr;

			if (firsTrackRef_cand.charge < 0. && secondTrackRef_cand.charge > 0.)
			{
				negativePionCand = theKPFCandidatesPionsCollection[trdx1];
				positivePionCand = theKPFCandidatesPionsCollection[trdx2];
			}
			else if (firsTrackRef_cand.charge > 0. && secondTrackRef_cand.charge < 0.)
			{
				negativePionCand = theKPFCandidatesPionsCollection[trdx2];
				positivePionCand = theKPFCandidatesPionsCollection[trdx1];
			}
			else
			{
				dout("Unvalid pair of tracks");
				continue;
			}

			// intersection of two lines instead of Kalman fit SV
				dout("\t\tintersection of two lines instead of Kalman fit SV:");
				dout("\t\t\tpos:(", positivePionCand.bestTrack.ref.x(), ",", positivePionCand.bestTrack.ref.y(), ")", "mom: [", positivePionCand.bestTrack.p4.x(), ",", positivePionCand.bestTrack.p4.y(), "]");
				dout("\t\t\tpos:(", negativePionCand.bestTrack.ref.x(), ",", negativePionCand.bestTrack.ref.y(), ")", "mom: [", negativePionCand.bestTrack.p4.x(), ",", negativePionCand.bestTrack.p4.y(), "]");
				double A = positivePionCand.bestTrack.p4.x() != 0 ? positivePionCand.bestTrack.p4.y() / positivePionCand.bestTrack.p4.x() : 0;
				double B = negativePionCand.bestTrack.p4.x() != 0 ? negativePionCand.bestTrack.p4.y() / negativePionCand.bestTrack.p4.x() : 0;
				double C = positivePionCand.bestTrack.ref.y() - A * positivePionCand.bestTrack.ref.x();
				double D = negativePionCand.bestTrack.ref.y() - B * negativePionCand.bestTrack.ref.x();
				RMPoint vtxPos((D - C) / (A - B), (A * D - B * C) / (A - B), 0);

				SVector3 distVecXY(vtxPos.x() - referencePos.x(), vtxPos.y() - referencePos.y(), 0.);
				SVector3 distposRefPoint(positivePionCand.bestTrack.p4.x() - referencePos.x(), positivePionCand.bestTrack.p4.y() - referencePos.y(), 0.);
				SVector3 distnegRefPoint(negativePionCand.bestTrack.p4.x() - referencePos.x(), negativePionCand.bestTrack.p4.y() - referencePos.y(), 0.);
				dout("\t\t\tvtxPos: (", vtxPos.x(), ",", vtxPos.y(), ")\tdistVecXY:", ROOT::Math::Mag(distVecXY), "ROOT::Math::Mag(distposRefPoint):", ROOT::Math::Mag(distposRefPoint), "ROOT::Math::Mag(distnegRefPoint)", ROOT::Math::Mag(distnegRefPoint));
				//double distMagXY = ROOT::Math::Mag(distVecXY);

				//NEED TRANSIENT TRACK
				/*
					// measure distance between tracks at their closest approach
					if (!posTransTkPtr->impactPointTSCP().isValid() || !negTransTkPtr->impactPointTSCP().isValid()) continue;
					FreeTrajectoryState const & posState = posTransTkPtr->impactPointTSCP().theState();
					FreeTrajectoryState const & negState = negTransTkPtr->impactPointTSCP().theState();
					ClosestApproachInRPhi cApp;
					cApp.calculate(posState, negState);
					if (!cApp.status()) continue;
					float dca = std::abs(cApp.distance());
					if (dca > TkDCACut) continue;

					// the POCA should at least be in the sensitive volume
					GlobalPoint cxPt = cApp.crossingPoint();
					if (sqrt(cxPt.x()*cxPt.x() + cxPt.y()*cxPt.y()) > 120. || std::abs(cxPt.z()) > 300.) continue;
				
					// the tracks should at least point in the same quadrant
					TrajectoryStateClosestToPoint const & posTSCP = posTransTkPtr->trajectoryStateClosestToPoint(cxPt);
					TrajectoryStateClosestToPoint const & negTSCP = negTransTkPtr->trajectoryStateClosestToPoint(cxPt);
					if (!posTSCP.isValid() || !negTSCP.isValid()) continue;
					if (posTSCP.momentum().dot(negTSCP.momentum())  < 0) continue;

					// calculate mPiPi
					double totalE = sqrt(posTSCP.momentum().mag2() + piMassSquared) + sqrt(negTSCP.momentum().mag2() + piMassSquared);
					double totalESq = totalE*totalE;
					double totalPSq = (posTSCP.momentum() + negTSCP.momentum()).mag2();
					double mass = sqrt(totalESq - totalPSq);
					if (mass > mPiPiCut_) continue;

					// Fill the vector of TransientTracks to send to KVF
					std::vector<reco::TransientTrack> transTracks;
					transTracks.reserve(2);
					transTracks.push_back(*posTransTkPtr);
					transTracks.push_back(*negTransTkPtr);

					// create the vertex fitter object and vertex the tracks
					TransientVertex theRecoVertex;
					if (vertexFitter_)
					{
						KalmanVertexFitter theKalmanFitter(useRefTracks_ == 0 ? false : true);
						theRecoVertex = theKalmanFitter.vertex(transTracks);
					}
					else if (!vertexFitter_)
					{
						useRefTracks_ = false;
						AdaptiveVertexFitter theAdaptiveFitter;
						theRecoVertex = theAdaptiveFitter.vertex(transTracks);
					}
					if (!theRecoVertex.isValid()) continue;

					reco::Vertex theVtx = theRecoVertex;
					if (theVtx.normalizedChi2() > vtxChi2Cut_) continue;
					GlobalPoint vtxPos(theVtx.x(), theVtx.y(), theVtx.z());

					// 2D decay significance
					SMatrixSym3D totalCov = theBeamSpot->rotatedCovariance3D() + theVtx.covariance();
					if (useVertex_) totalCov = referenceVtx.covariance() + theVtx.covariance();
					SVector3 distVecXY(vtxPos.x()-referencePos.x(), vtxPos.y()-referencePos.y(), 0.);
					double distMagXY = ROOT::Math::Mag(distVecXY);
					double sigmaDistMagXY = sqrt(ROOT::Math::Similarity(totalCov, distVecXY)) / distMagXY;
					if (distMagXY/sigmaDistMagXY < vtxDecaySigXYCut_) continue;

					// 3D decay significance
					SVector3 distVecXYZ(vtxPos.x()-referencePos.x(), vtxPos.y()-referencePos.y(), vtxPos.z()-referencePos.z());
					double distMagXYZ = ROOT::Math::Mag(distVecXYZ);
					double sigmaDistMagXYZ = sqrt(ROOT::Math::Similarity(totalCov, distVecXYZ)) / distMagXYZ;
					if (distMagXYZ/sigmaDistMagXYZ < vtxDecaySigXYZCut_) continue;
				*/
					// the tracks should at least point in the same quadrant
					// TrajectoryStateClosestToPoint const & posTSCP = posTransTkPtr->trajectoryStateClosestToPoint(cxPt);
					// TrajectoryStateClosestToPoint const & negTSCP = negTransTkPtr->trajectoryStateClosestToPoint(cxPt);
					// if (!posTSCP.isValid() || !negTSCP.isValid()) continue;
					if (positivePionCand.bestTrack.p4.X() * negativePionCand.bestTrack.p4.X()
						+ positivePionCand.bestTrack.p4.Y() * negativePionCand.bestTrack.p4.Y()
						+ positivePionCand.bestTrack.p4.Z() * negativePionCand.bestTrack.p4.Z() < 0)
					{
						dout("Tracks have negative scalar product\n");
						continue;
					}

					if (ROOT::Math::Mag(distVecXY) > ROOT::Math::Mag(distposRefPoint) || ROOT::Math::Mag(distVecXY) > ROOT::Math::Mag(distnegRefPoint) )
					{
						dout("SV is further then one of the tracks ref points\n");
						continue;
					}

			// significance analogue
			/*
				// 2D pointing angle
				double dx = theVtx.x()-referencePos.x();
				double dy = theVtx.y()-referencePos.y();
				double px = totalP.x();
				double py = totalP.y();
				double angleXY = (dx*px+dy*py)/(sqrt(dx*dx+dy*dy)*sqrt(px*px+py*py));
				if (angleXY < cosThetaXYCut_) continue;

				// 3D pointing angle
				double dz = theVtx.z()-referencePos.z();
				double pz = totalP.z();
				double angleXYZ = (dx*px + dy*py + dz*pz) / (sqrt(dx*dx+dy*dy+dz*dz)*sqrt(px*px+py*py+pz*pz));
				if (angleXYZ < cosThetaXYZCut_) continue;
			*/
			/*
				//ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> >
				SMatrixSym3D totalCov = theBeamSpot->rotatedCovariance3D() + theVtx.covariance();
				if (UseVertex) totalCov = referenceVtx.covariance() + theVtx.covariance(); // NO z-component fot the cov matrix
				SVector3 distVecXY(vtxPos.x() - referencePos.x(), vtxPos.y()-referencePos.y(), 0.);
				double distMagXY = ROOT::Math::Mag(distVecXY);
				double sigmaDistMagXY = sqrt(ROOT::Math::Similarity(totalCov, distVecXY)) / distMagXY;
				if (distMagXY/sigmaDistMagXY < vtxDecaySigXYCut_) continue;
				
				// 3D decay significance analogue
				SVector3 distVecXYZ(vtxPos.x()-referencePos.x(), vtxPos.y()-referencePos.y(), vtxPos.z()-referencePos.z());
				double distMagXYZ = ROOT::Math::Mag(distVecXYZ);
				double sigmaDistMagXYZ = sqrt(ROOT::Math::Similarity(totalCov, distVecXYZ)) / distMagXYZ;
				if (distMagXYZ/sigmaDistMagXYZ < vtxDecaySigXYZCut_) continue;
			*/

			// make sure the vertex radius is within the inner track hit radius
				/*
				if (InnerHitPosCut > 0.) //  && positivePionCand->innerOk() // Reference to additional information stored only on RECO.
				{
					RMPoint posTkHitPos = positivePionCand->innerPosition; // innerPosition - might be not stored in miniaod ? maybe try to use refpoint instead
					double posTkHitPosD2 =  pow(posTkHitPos.x() - referencePos.x(), 2) + pow(posTkHitPos.y() - referencePos.y(), 2);
					if (sqrt(posTkHitPosD2) < (distMagXY - sigmaDistMagXY * InnerHitPosCut)) continue; // no sigmaDistMagXY
				}
				if (InnerHitPosCut > 0.) //  && negativePionCand.bestTrack.innerOk() // Reference to additional information stored only on RECO.
				{
					RMPoint negTkHitPos = negativePionCand.bestTrack.innerPosition;
					double negTkHitPosD2 =  pow(negTkHitPos.x() - referencePos.x(), 2) + pow(negTkHitPos.y() - referencePos.y(), 2);
					if (sqrt(negTkHitPosD2) < (distMagXY - sigmaDistMagXY * InnerHitPosCut)) continue; // no sigmaDistMagXY
				}
				*/
			
			/* // Recalculating the momentum of Kaon daughters from the fit
				std::auto_ptr<TrajectoryStateClosestToPoint> trajPlus;
				std::auto_ptr<TrajectoryStateClosestToPoint> trajMins;
				std::vector<reco::TransientTrack> theRefTracks;
				if (theRecoVertex.hasRefittedTracks()) theRefTracks = theRecoVertex.refittedTracks();

				if (useRefTracks_ && theRefTracks.size() > 1)
				{
					reco::TransientTrack* thePositiveRefTrack = 0;
					reco::TransientTrack* theNegativeRefTrack = 0;

					for (std::vector<reco::TransientTrack>::iterator iTrack = theRefTracks.begin(); iTrack != theRefTracks.end(); ++iTrack)
					{
						if (iTrack->track().charge() > 0.) thePositiveRefTrack = &*iTrack;
						else if (iTrack->track().charge() < 0.) theNegativeRefTrack = &*iTrack;
					}
					if (thePositiveRefTrack == 0 || theNegativeRefTrack == 0) continue;

					trajPlus.reset(new TrajectoryStateClosestToPoint(thePositiveRefTrack->trajectoryStateClosestToPoint(vtxPos)));
					trajMins.reset(new TrajectoryStateClosestToPoint(theNegativeRefTrack->trajectoryStateClosestToPoint(vtxPos)));
				}
				else
				{
					trajPlus.reset(new TrajectoryStateClosestToPoint(posTransTkPtr->trajectoryStateClosestToPoint(vtxPos)));
					trajMins.reset(new TrajectoryStateClosestToPoint(negTransTkPtr->trajectoryStateClosestToPoint(vtxPos)));
				}

				if (trajPlus.get() == 0 || trajMins.get() == 0 || !trajPlus->isValid() || !trajMins->isValid()) continue;

				GlobalVector positiveP(trajPlus->momentum());
				GlobalVector negativeP(trajMins->momentum());
				GlobalVector totalP(positiveP + negativeP);
			*/
			RMFLV pfCandPositiveP(positivePionCand.p4), pfCandNegativeP(negativePionCand.p4);
			RMFLV pfCandtotalP(pfCandPositiveP + pfCandNegativeP);
			dout("RMFLV for pfCand:", positivePionCand.p4.X(), positivePionCand.p4.Y(), positivePionCand.p4.Z(), positivePionCand.p4.mass(), positivePionCand.bestTrack.p4.E());

			// calculate total energy of V0 3 ways: assume it's a kShort, a Lambda, or a LambdaBar.

			dout("mass:", pfCandtotalP.mass());
			dout("pion mass:", pfCandPositiveP.mass(), pfCandNegativeP.mass());

			product.kaonMass.push_back(pfCandtotalP.mass());
			product.kaonPosDaugterMass.push_back(pfCandPositiveP.mass());
			product.kaonNegDaugterMass.push_back(pfCandNegativeP.mass());

			product.kaonNumber++;
		}
	}
	dout("End event\n\n\n");
}
