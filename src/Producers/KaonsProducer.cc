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

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nK", [](event_type const& event, product_type const& product)
	{
		return product.m_nK;
	});

	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("m_K", [](event_type const& event, product_type const& product)
	{
		return product.m_K;
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
	product.m_nK = 1;

	assert(event.m_taus);
	assert(event.m_beamSpot);

	// select input source
	vector<KTau*> taus;
	vector<KTrack> theTrackCollection;
	
	// Create list of pions tracks
	/*
		edm::Handle<reco::TrackCollection> theTrackHandle;
		iEvent.getByToken(token_tracks, theTrackHandle);
		if (!theTrackHandle->size()) return;
		const reco::TrackCollection* theTrackCollection = theTrackHandle.product();
	*/
	taus.resize(event.m_taus->size());
	for (KTaus::iterator tau = event.m_taus->begin(); tau != event.m_taus->end(); ++tau)
	{
		KPFCandidates jet_charged = tau->chargedHadronCandidates;

		for (KPFCandidates::iterator chargedPrt = jet_charged.begin(); chargedPrt != jet_charged.end(); ++chargedPrt)
		{
			
			theTrackCollection.push_back(chargedPrt->bestTrack);
		}

		for (KPFCandidates::iterator chargedPrt = tau->isolationChargedHadronCandidates.begin(); chargedPrt != tau->isolationChargedHadronCandidates.end(); ++chargedPrt)
			theTrackCollection.push_back(chargedPrt->bestTrack);
	}
	dout("Total theTrackCollection size:", theTrackCollection.size());

	// Get the BS
	/*
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
	RMPoint referenceVtx;
	//!!!!!if (UseVertex) referenceVtx = (event.m_vertexSummary->pv[0].position);
	
	// STORE ALSO THE TRANSIENT TRACK
	/*
		edm::ESHandle<MagneticField> theMagneticFieldHandle;
		iSetup.get<IdealMagneticFieldRecord>().get(theMagneticFieldHandle);
		const MagneticField* theMagneticField = theMagneticFieldHandle.product();
	*/

	// Preselection for the tracks
	/*
		std::vector<reco::TrackRef> theTrackRefs;
		std::vector<reco::TransientTrack> theTransTracks;

		// fill vectors of TransientTracks and TrackRefs after applying preselection cuts
		for (reco::TrackCollection::const_iterator iTk = theTrackCollection->begin(); iTk != theTrackCollection->end(); ++iTk) 
		{
			const reco::Track* tmpTrack = &(*iTk);
			double ipsigXY = std::abs(tmpTrack->dxy(*theBeamSpot)/tmpTrack->dxyError());
			if (useVertex_) ipsigXY = std::abs(tmpTrack->dxy(referencePos)/tmpTrack->dxyError());
			double ipsigZ = std::abs(tmpTrack->dz(referencePos)/tmpTrack->dzError());

			if (tmpTrack->normalizedChi2() < tkChi2Cut_ && tmpTrack->numberOfValidHits() >= tkNHitsCut_ &&
			tmpTrack->pt() > tkPtCut_ && ipsigXY > tkIPSigXYCut_ && ipsigZ > tkIPSigZCut_) 
			{
				reco::TrackRef tmpRef(theTrackHandle, std::distance(theTrackCollection->begin(), iTk));
				theTrackRefs.push_back(std::move(tmpRef));
				reco::TransientTrack tmpTransient(*tmpRef, theMagneticField);
				theTransTracks.push_back(std::move(tmpTransient));
			}
		}
		// good tracks have now been selected for vertexing
	*/
	vector<KTrack*> theTrackRefs;
	//vector<KTrack> theTransTracks;

	//TODO: write iterator for KTracks //for (KTrack::iterator iTk = theTrackCollection.begin(); iTk != theTrackCollection.end(); ++iTk) 
	for(unsigned int i = 0; i < theTrackCollection.size(); i++)
	{
		KTrack* tmpTrack = &theTrackCollection[i];
		double ipsigXY = std::abs(tmpTrack->getDxy(&theBeamSpot) / tmpTrack->errDxy);//std::abs(tmpTrack->getDxy(*theBeamSpot) / tmpTrack->errDxy);
		double ipsigZ  = std::abs(tmpTrack->getDz(&theBeamSpot) / tmpTrack->errDz);//std::abs(tmpTrack->getDz(*referencePos)  / tmpTrack->errDz);
		
		dout("ipsigXY =", ipsigXY, "= tmpTrack->getDxy(&theBeamSpot) / tmpTrack->errDxy =", tmpTrack->getDxy(&theBeamSpot), "/", tmpTrack->errDxy);

		dout("i:", i , "\n\t",
			"nValidHits:", (int)tmpTrack->nValidHits(), ">=", (int)TkNHitsCut , "\n\t",
			"tmpTrack->p4.Pt()", tmpTrack->p4.Pt(), ">", TkPtCut , "\n\t",
			"ipsigXY", ipsigXY, ">", TkIPSigXYCut , "\n\t",
			"ipsigZ", ipsigZ, ">", TkIPSigZCut);

		if (//tmpTrack->chi2 / tmpTrack->nDOF < TkChi2Cut &&
			(int)tmpTrack->nValidHits() >= (int)TkNHitsCut &&
			tmpTrack->p4.Pt() > TkPtCut &&
			ipsigXY > TkIPSigXYCut &&
			ipsigZ > TkIPSigZCut
			) 
		{
		    theTrackRefs.push_back(tmpTrack);
			// 	reco::TransientTrack tmpTransient(*tmpRef, theMagneticField);
			// 	theTransTracks.push_back(std::move(tmpTransient));
		}
	}
	dout("len theTrackRefs", theTrackRefs.size());

	// loop over tracks and vertex good charged track pairs
	for (unsigned int trdx1 = 0; trdx1 < theTrackRefs.size(); ++trdx1) 
	{
		for (unsigned int trdx2 = trdx1 + 1; trdx2 < theTrackRefs.size(); ++trdx2) 
		{
			dout("i,j:", trdx1, trdx2);
			KTrack* positiveTrackRef;
			KTrack* negativeTrackRef;
			// reco::TransientTrack* posTransTkPtr = nullptr;
			// reco::TransientTrack* negTransTkPtr = nullptr;

			if (theTrackRefs[trdx1]->charge < 0. && theTrackRefs[trdx2]->charge > 0.) 
			{
				negativeTrackRef = theTrackRefs[trdx1];
				positiveTrackRef = theTrackRefs[trdx2];
				// negTransTkPtr = &theTransTracks[trdx1];
				// posTransTkPtr = &theTransTracks[trdx2];
			} 
			else if (theTrackRefs[trdx1]->charge > 0. && theTrackRefs[trdx2]->charge < 0.) 
			{
				negativeTrackRef = theTrackRefs[trdx2];
				positiveTrackRef = theTrackRefs[trdx1];
				// negTransTkPtr = &theTransTracks[trdx2];
				// posTransTkPtr = &theTransTracks[trdx1];
			} 
			else
			{
				dout("Unvalid pair of tracks");
				continue;
			}

			// intersection of two lines instead of Kalman fit SV
			double A = positiveTrackRef->p4.x() != 0 ? positiveTrackRef->p4.y() / positiveTrackRef->p4.x() : 0;
			double B = negativeTrackRef->p4.x() != 0 ? negativeTrackRef->p4.y() / negativeTrackRef->p4.x() : 0;
			double C = positiveTrackRef->ref.y();
			double D = negativeTrackRef->ref.y();
			RMPoint vtxPos((D - C) / (A - B), (A * D - B * C) / (A - B), 0);

			SVector3 distVecXY(vtxPos.x() - referencePos.x(), vtxPos.y() - referencePos.y(), 0.);
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
				if (positiveTrackRef->p4.X() * negativeTrackRef->p4.X() 
					+ positiveTrackRef->p4.Y() * negativeTrackRef->p4.Y() 
					+ positiveTrackRef->p4.Z() * negativeTrackRef->p4.Z() < 0) 
			{
				dout("Tracks have negative scalar product");
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
				if (InnerHitPosCut > 0.) //  && positiveTrackRef->innerOk() // Reference to additional information stored only on RECO.
				{
					RMPoint posTkHitPos = positiveTrackRef->innerPosition; // innerPosition - might be not stored in miniaod ? maybe try to use refpoint instead
					double posTkHitPosD2 =  pow(posTkHitPos.x() - referencePos.x(), 2) + pow(posTkHitPos.y() - referencePos.y(), 2);
					if (sqrt(posTkHitPosD2) < (distMagXY - sigmaDistMagXY * InnerHitPosCut)) continue; // no sigmaDistMagXY
				}
				if (InnerHitPosCut > 0.) //  && negativeTrackRef->innerOk() // Reference to additional information stored only on RECO.
				{
					RMPoint negTkHitPos = negativeTrackRef->innerPosition;
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
			RMFLV positiveP(positiveTrackRef->p4);
			RMFLV negativeP(negativeTrackRef->p4);
			RMFLV totalP(positiveP + negativeP);

			// calculate total energy of V0 3 ways: assume it's a kShort, a Lambda, or a LambdaBar.
			double piPlusE = sqrt(positiveP.mag2() + piMassSquared);
			double piMinusE = sqrt(negativeP.mag2() + piMassSquared);
			double protonE = sqrt(positiveP.mag2() + protonMassSquared);
			double antiProtonE = sqrt(negativeP.mag2() + protonMassSquared);
			double kShortETot = piPlusE + piMinusE;
			double lambdaEtot = protonE + piMinusE;
			double lambdaBarEtot = antiProtonE + piPlusE;

			dout("pion assumption:", piPlusE, piMinusE, 
				"proton assumption:", protonE, antiProtonE, 
				"kShortETo:t", kShortETot, "lambdaEtot:", lambdaEtot, "lambdaBarEtot:", lambdaBarEtot);

			// Create momentum 4-vectors for the 3 candidate types
			RMFLV kShortP4(totalP.x(), totalP.y(), totalP.z(), kShortETot);
			RMFLV lambdaP4(totalP.x(), totalP.y(), totalP.z(), lambdaEtot);
			RMFLV lambdaBarP4(totalP.x(), totalP.y(), totalP.z(), lambdaBarEtot);

			dout("mass:", kShortP4.mass(), lambdaP4.mass(), lambdaBarP4.mass());
			product.m_K.push_back( kShortP4.mass());
			/*//For the rest the SV is missing
				reco::Particle::Point vtx(theVtx.x(), theVtx.y(), theVtx.z());
				const reco::Vertex::CovarianceMatrix vtxCov(theVtx.covariance());
				double vtxChi2(theVtx.chi2());
				double vtxNdof(theVtx.ndof());

				// Create the VertexCompositeCandidate object that will be stored in the Event
				reco::VertexCompositeCandidate* theKshort = nullptr;
				reco::VertexCompositeCandidate* theLambda = nullptr;
				reco::VertexCompositeCandidate* theLambdaBar = nullptr;

				if (doKShorts_) theKshort = new reco::VertexCompositeCandidate(0, kShortP4, vtx, vtxCov, vtxChi2, vtxNdof);

				if (doLambdas_) 
				{
					if (positiveP.mag2() > negativeP.mag2()) theLambda = new reco::VertexCompositeCandidate(0, lambdaP4, vtx, vtxCov, vtxChi2, vtxNdof);
					else theLambdaBar = new reco::VertexCompositeCandidate(0, lambdaBarP4, vtx, vtxCov, vtxChi2, vtxNdof);
				}

				// Create daughter candidates for the VertexCompositeCandidates
				reco::RecoChargedCandidate thePiPlusCand(
				1, reco::Particle::LorentzVector(positiveP.x(), positiveP.y(), positiveP.z(), piPlusE), vtx);
				thePiPlusCand.setTrack(positiveTrackRef);

				reco::RecoChargedCandidate thePiMinusCand(
				-1, reco::Particle::LorentzVector(negativeP.x(), negativeP.y(), negativeP.z(), piMinusE), vtx);
				thePiMinusCand.setTrack(negativeTrackRef);

				reco::RecoChargedCandidate theProtonCand(
				1, reco::Particle::LorentzVector(positiveP.x(), positiveP.y(), positiveP.z(), protonE), vtx);
				theProtonCand.setTrack(positiveTrackRef);

				reco::RecoChargedCandidate theAntiProtonCand(
				-1, reco::Particle::LorentzVector(negativeP.x(), negativeP.y(), negativeP.z(), antiProtonE), vtx);
				theAntiProtonCand.setTrack(negativeTrackRef);

				AddFourMomenta addp4;
				// Store the daughter Candidates in the VertexCompositeCandidates if they pass mass cuts
				if (doKShorts_) 
				{
					theKshort->addDaughter(thePiPlusCand);
					theKshort->addDaughter(thePiMinusCand);
					theKshort->setPdgId(310);
					addp4.set(*theKshort);
					if (theKshort->mass() < kShortMass + kShortMassCut_ && theKshort->mass() > kShortMass - kShortMassCut_) theKshorts.push_back(std::move(*theKshort));
				}
				if (doLambdas_ && theLambda) 
				{
					theLambda->addDaughter(theProtonCand);
					theLambda->addDaughter(thePiMinusCand);
					theLambda->setPdgId(3122);
					addp4.set( *theLambda );
					if (theLambda->mass() < lambdaMass + lambdaMassCut_ && theLambda->mass() > lambdaMass - lambdaMassCut_) theLambdas.push_back(std::move(*theLambda));
				}
				else if (doLambdas_ && theLambdaBar)
				{
					theLambdaBar->addDaughter(theAntiProtonCand);
					theLambdaBar->addDaughter(thePiPlusCand);
					theLambdaBar->setPdgId(-3122);
					addp4.set(*theLambdaBar);
					if (theLambdaBar->mass() < lambdaMass + lambdaMassCut_ && theLambdaBar->mass() > lambdaMass - lambdaMassCut_) theLambdas.push_back(std::move(*theLambdaBar));
				}

				delete theKshort;
				delete theLambda;
				delete theLambdaBar;
				theKshort = theLambda = theLambdaBar = nullptr;
			*/
		}
	}
}
