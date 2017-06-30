
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/RecoilCorrector.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/MEtSys.h"

#include <boost/regex.hpp>


/**
   \brief Corrects the MET created by the MET producer
   
   Run this producer after the Valid(Tagged)JetsProducer, since it relies on the number of
   jets in the event.
*/


template<class TMet>
class MetCorrectorBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	enum CorrectionMethod { NONE=0, QUANTILE_MAPPING=1, MEAN_RESOLUTION=2};
	
	MetCorrectorBase(TMet* product_type::*metMemberUncorrected,
			 TMet product_type::*metMemberCorrected,
			 std::vector<float> product_type::*metCorrections,
			 std::string (setting_type::*GetRecoilCorrectorFile)(void) const,
			 std::string (setting_type::*GetMetShiftCorrectorFile)(void) const,
			 bool (setting_type::*GetUpdateMetWithCorrectedLeptons)(void) const
	) :
		ProducerBase<HttTypes>(),
		m_metMemberUncorrected(metMemberUncorrected),
		m_metMemberCorrected(metMemberCorrected),
		m_metCorrections(metCorrections),
		GetRecoilCorrectorFile(GetRecoilCorrectorFile),
		GetMetShiftCorrectorFile(GetMetShiftCorrectorFile),
		GetUpdateMetWithCorrectedLeptons(GetUpdateMetWithCorrectedLeptons)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
		m_recoilCorrector = new RecoilCorrector((settings.*GetRecoilCorrectorFile)());
		
		if ((settings.GetMetSysType() != 0) || (settings.GetMetSysShift() != 0))
		{
			m_metShiftCorrector = new MEtSys((settings.*GetMetShiftCorrectorFile)());

			if (settings.GetMetSysType() == 1)
			{
				m_sysType = MEtSys::SysType::Response;
			}
			else if (settings.GetMetSysType() == 2)
			{
				m_sysType = MEtSys::SysType::Resolution;
			}
			else
			{
				m_sysType = MEtSys::SysType::NoType;
				LOG(FATAL) << "Invalid HttSettings::MetSysType option";
			}
			
			if (settings.GetMetSysShift() > 0)
			{
				m_sysShift = MEtSys::SysShift::Up;
			}
			else
			{
				m_sysShift = MEtSys::SysShift::Down;
			}
		}

		// determine process type, trigger several decisions later
		if (boost::regex_search(settings.GetNickname(), boost::regex("DY.?JetsToLL|W.?JetsToLNu|HToTauTau", boost::regex::extended)))
		{
			m_processType = MEtSys::ProcessType::BOSON;
		}
		else if (boost::regex_search(settings.GetNickname(), boost::regex("TT", boost::regex::extended)))
		{
			m_processType = MEtSys::ProcessType::TOP;
		}
		else
		{
			m_processType = MEtSys::ProcessType::EWK;
		}
		m_isWJets = boost::regex_search(settings.GetNickname(), boost::regex("W.?JetsToLNu", boost::regex::icase | boost::regex::extended));
		
		m_doMetSys = ((settings.GetMetSysType() != 0) || (settings.GetMetSysShift() != 0));

		if(settings.GetMetCorrectionMethod() == "quantileMapping")
			m_correctionMethod = MetCorrectorBase::CorrectionMethod::QUANTILE_MAPPING;
		else if(settings.GetMetCorrectionMethod() == "meanResolution")
			m_correctionMethod = MetCorrectorBase::CorrectionMethod::MEAN_RESOLUTION;
		else
		{
			m_correctionMethod = MetCorrectorBase::CorrectionMethod::NONE;
			LOG(FATAL) << "Invalid MetCorrectionMethod option. Available are 'quantileMapping' and 'meanResolution'";
		}

		if (settings.GetMetUncertaintyShift())
		{
			m_metUncertaintyType = HttEnumTypes::ToMETUncertaintyType(settings.GetMetUncertaintyType());
		}
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		assert(m_metMemberUncorrected != nullptr);
                //std::cout << "MET CORRECTOR RUNNING!!!" << std::endl;
		// Retrieve the needed informations from the event content
		// and replace nominal met four vector by one shifted by
		// specific uncertainty in order to propagate it through
		// entire analysis if required by configuration
		float metX = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Px() : (product.*m_metMemberUncorrected)->p4.Px();
		float metY = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Py() : (product.*m_metMemberUncorrected)->p4.Py();
		float metEnergy = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].energy() : (product.*m_metMemberUncorrected)->p4.energy();
		float metResolution = std::sqrt(metEnergy * metEnergy - metX * metX - metY * metY);
                //std::cout << "uncorrected met_x: " << metX << std::endl;
                //std::cout << "uncorrected met_y: " << metY << std::endl;
                // Corrections, if the WJetsErsatz method is applied
                if (product.m_cleanedMuonForWJetsErsatz)
                {
                    metX += product.m_cleanedMuonForWJetsErsatz->p4.Px();
                    metY += product.m_cleanedMuonForWJetsErsatz->p4.Py();
                    //std::cout << "cleaned muon p_x: " << product.m_cleanedMuonForWJetsErsatz->p4.Px() << std::endl;
                    //std::cout << "cleaned muon p_y: " << product.m_cleanedMuonForWJetsErsatz->p4.Py() << std::endl;
                    //std::cout << "corrected met_x for wjets ersatz: " << metX << std::endl;
                    //std::cout << "corrected met_y for wjets ersatz: " << metY << std::endl;
                }

		// Recalculate MET if lepton energies have been corrected:
		// MetX' = MetX + Px - Px'
		// MetY' = MetY + Py - Py'
		// MET' = sqrt(MetX' * MetX' + MetY' * MetY')
		//std::cout << "Pipeline: " << settings.GetRootFileFolder() << std::endl;
		if ((settings.*GetUpdateMetWithCorrectedLeptons)())
		{
			/*// Electrons
			for (std::vector<std::shared_ptr<KElectron> >::iterator electron = product.m_correctedElectrons.begin();
				 electron != product.m_correctedElectrons.end(); ++electron)
			{
				// Only update MET if there actually was a correction applied
				if (Utility::ApproxEqual(electron->get()->p4, const_cast<KLepton*>(product.m_originalLeptons[electron->get()])->p4))
					continue;

				float eX = electron->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[electron->get()])->p4.Px();
				float eY = electron->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[electron->get()])->p4.Py();

				metX -= eX;
				metY -= eY;
			}

			// Muons
			for (std::vector<std::shared_ptr<KMuon> >::iterator muon = product.m_correctedMuons.begin();
				 muon != product.m_correctedMuons.end(); ++muon)
			{
				// Only update MET if there actually was a correction applied
				if (Utility::ApproxEqual(muon->get()->p4, const_cast<KLepton*>(product.m_originalLeptons[muon->get()])->p4))
					continue;

				float eX = muon->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[muon->get()])->p4.Px();
				float eY = muon->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[muon->get()])->p4.Py();

				metX -= eX;
				metY -= eY;
			}

			// Taus
			for (std::vector<std::shared_ptr<KTau> >::iterator tau = product.m_correctedTaus.begin();
				 tau != product.m_correctedTaus.end(); ++tau)
			{
				// Only update MET if there actually was a correction applied
				if (Utility::ApproxEqual(tau->get()->p4, const_cast<KLepton*>(product.m_originalLeptons[tau->get()])->p4))
					continue;

				float eX = tau->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[tau->get()])->p4.Px();
				float eY = tau->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[tau->get()])->p4.Py();

				metX -= eX;
				metY -= eY;
			}*/
			float eX = 0.0;
			float eY = 0.0;

			KLV* lep1 = product.m_validDiTauPairCandidates[0].first;
			KLV* lep2 = product.m_validDiTauPairCandidates[0].second;

			if(product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
			{
				float eX1 = 0.0;
				float eX2 = 0.0;
				float eY1 = 0.0;
				float eY2 = 0.0;
				for (std::vector<std::shared_ptr<KElectron> >::iterator e = product.m_correctedElectrons.begin();
					 e != product.m_correctedElectrons.end(); ++e)
				{
					if(e->get()->p4 == lep1->p4)
					{
						eX1 = e->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Px();
						eY1 = e->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Py();
					}
				}
				for (std::vector<std::shared_ptr<KTau> >::iterator t = product.m_correctedTaus.begin();
					 t != product.m_correctedTaus.end(); ++t)
				{
					if(t->get()->p4 == lep2->p4)
					{
						eX2 = t->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Px();
						eY2 = t->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Py();
					}
				}
				eX = eX1 + eX2;
				eY = eY1 + eY2;
			}
			else if(product.m_decayChannel == HttEnumTypes::DecayChannel::MT)
			{
				//std::cout << "Compute lepton corrections for MT channel" << std::endl;
				float eX1 = 0.0;
				float eX2 = 0.0;
				float eY1 = 0.0;
				float eY2 = 0.0;
				for (std::vector<std::shared_ptr<KMuon> >::iterator m = product.m_correctedMuons.begin();
					 m != product.m_correctedMuons.end(); ++m)
				{
					if(m->get()->p4 == lep1->p4)
					{
						//std::cout << "Found a muon matching first pair member" << std::endl;
						eX1 = m->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Px();
						eY1 = m->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Py();
					}
				}
				for (std::vector<std::shared_ptr<KTau> >::iterator t = product.m_correctedTaus.begin();
					 t != product.m_correctedTaus.end(); ++t)
				{
					if(t->get()->p4 == lep2->p4)
					{
						//std::cout << "Found a tau matching second pair member" << std::endl;
						eX2 = t->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Px();
						eY2 = t->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Py();
					}
				}
				eX = eX1 + eX2;
				eY = eY1 + eY2;
				//std::cout << "Corrections X,Y:" << eX << "," << eY << std::endl;
			}
			else if(product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
			{
				float eX1 = 0.0;
				float eX2 = 0.0;
				float eY1 = 0.0;
				float eY2 = 0.0;
				for (std::vector<std::shared_ptr<KTau> >::iterator t = product.m_correctedTaus.begin();
					 t != product.m_correctedTaus.end(); ++t)
				{
					if(t->get()->p4 == lep1->p4)
					{
						eX1 = t->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Px();
						eY1 = t->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Py();
					}
				}
				for (std::vector<std::shared_ptr<KTau> >::iterator t = product.m_correctedTaus.begin();
					 t != product.m_correctedTaus.end(); ++t)
				{
					if(t->get()->p4 == lep2->p4)
					{
						eX2 = t->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Px();
						eY2 = t->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[t->get()])->p4.Py();
					}
				}
				eX = eX1 + eX2;
				eY = eY1 + eY2;
			}
			else if(product.m_decayChannel == HttEnumTypes::DecayChannel::EM)
			{
				float eX1 = 0.0;
				float eX2 = 0.0;
				float eY1 = 0.0;
				float eY2 = 0.0;
				for (std::vector<std::shared_ptr<KElectron> >::iterator e = product.m_correctedElectrons.begin();
					 e != product.m_correctedElectrons.end(); ++e)
				{
					if(e->get()->p4 == lep1->p4)
					{
						eX1 = e->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Px();
						eY1 = e->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Py();
					}
				}
				for (std::vector<std::shared_ptr<KMuon> >::iterator m = product.m_correctedMuons.begin();
					 m != product.m_correctedMuons.end(); ++m)
				{
					if(m->get()->p4 == lep2->p4)
					{
						eX2 = m->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Px();
						eY2 = m->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Py();
					}
				}
				eX = eX1 + eX2;
				eY = eY1 + eY2;
			}
			else if(product.m_decayChannel == HttEnumTypes::DecayChannel::MM)
			{
				float eX1 = 0.0;
				float eX2 = 0.0;
				float eY1 = 0.0;
				float eY2 = 0.0;
				for (std::vector<std::shared_ptr<KMuon> >::iterator m = product.m_correctedMuons.begin();
					 m != product.m_correctedMuons.end(); ++m)
				{
					if(m->get()->p4 == lep1->p4)
					{
						eX1 = m->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Px();
						eY1 = m->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Py();
					}
				}
				for (std::vector<std::shared_ptr<KMuon> >::iterator m = product.m_correctedMuons.begin();
					 m != product.m_correctedMuons.end(); ++m)
				{
					if(m->get()->p4 == lep2->p4)
					{
						eX2 = m->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Px();
						eY2 = m->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[m->get()])->p4.Py();
					}
				}
				eX = eX1 + eX2;
				eY = eY1 + eY2;
			}
			else if(product.m_decayChannel == HttEnumTypes::DecayChannel::EE)
			{
				float eX1 = 0.0;
				float eX2 = 0.0;
				float eY1 = 0.0;
				float eY2 = 0.0;
				for (std::vector<std::shared_ptr<KElectron> >::iterator e = product.m_correctedElectrons.begin();
					 e != product.m_correctedElectrons.end(); ++e)
				{
					if(e->get()->p4 == lep1->p4)
					{
						eX1 = e->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Px();
						eY1 = e->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Py();
					}
				}
				for (std::vector<std::shared_ptr<KElectron> >::iterator e = product.m_correctedElectrons.begin();
					 e != product.m_correctedElectrons.end(); ++e)
				{
					if(e->get()->p4 == lep2->p4)
					{
						eX2 = e->get()->p4.Px() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Px();
						eY2 = e->get()->p4.Py() - const_cast<KLepton*>(product.m_originalLeptons[e->get()])->p4.Py();
					}
				}
				eX = eX1 + eX2;
				eY = eY1 + eY2;
			}
			metX -= eX;
			metY -= eY;
		}
                //std::cout << "Met X,Y after WJetsErsatz & Lepton Corrections: " << metX << " " << metY << std::endl;
		
		// Recoil corrections follow
		int nJets30 = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);

		// In selected W+Jets events one of the leptons is faked by hadronic jet and this
		// jet should be counted as a part of hadronic recoil to the W boson
		if(m_isWJets || product.m_cleanedMuonForWJetsErsatz)
		{
                        //std::cout << "WJets recognized, so +1 to nJets30 " << std::endl;
			nJets30 += 1;
		}
		
		float genPx = 0.;  // generator Z(W) px
		float genPy = 0.;  // generator Z(W) py
		float visPx = 0.;  // visible (generator) Z(W) px
		float visPy = 0.;  // visible (generator) Z(W) py
		
		for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
		 genParticle != event.m_genParticles->end(); ++genParticle)
		{
			int pdgId = std::abs(genParticle->pdgId);
			
			if ( (pdgId >= DefaultValues::pdgIdElectron && pdgId <= DefaultValues::pdgIdNuTau && genParticle->fromHardProcessFinalState()) ||
			     (genParticle->isDirectHardProcessTauDecayProduct()) )
			{
                                //std::cout << "Adding Px, Py of particle with pdgId " << pdgId << " to genPx, genPy" << std::endl;
				genPx += genParticle->p4.Px();
				genPy += genParticle->p4.Py();
				
				if ( !(pdgId == DefaultValues::pdgIdNuE || pdgId == DefaultValues::pdgIdNuMu || pdgId == DefaultValues::pdgIdNuTau) )
				{
                                        if(product.m_cleanedMuonForWJetsErsatz)
                                        {
                                            //std::cout << "Pt,Eta,Phi of gen muon to be neglected: " << product.m_genParticleMatchedMuons[static_cast<KMuon*>(product.m_cleanedMuonForWJetsErsatz)]->p4.Pt() << std::endl;
                                            //std::cout << " " << product.m_genParticleMatchedMuons[static_cast<KMuon*>(product.m_cleanedMuonForWJetsErsatz)]->p4.Eta();
                                            //std::cout << " " << product.m_genParticleMatchedMuons[static_cast<KMuon*>(product.m_cleanedMuonForWJetsErsatz)]->p4.Phi() << std::endl;
                                            //std::cout << "Pt,Eta,Phi of current gen muon: " << genParticle->p4.Pt();
                                            //std::cout << " " << genParticle->p4.Eta();
                                            //std::cout << " " << genParticle->p4.Phi() << std::endl;
                                            bool etamatch = product.m_genParticleMatchedMuons[static_cast<KMuon*>(product.m_cleanedMuonForWJetsErsatz)]->p4.Eta() == genParticle->p4.Eta();
                                            bool phimatch = product.m_genParticleMatchedMuons[static_cast<KMuon*>(product.m_cleanedMuonForWJetsErsatz)]->p4.Phi() == genParticle->p4.Phi();
                                            if( !(etamatch && phimatch) )
                                            {
                                                visPx += genParticle->p4.Px();
                                                visPy += genParticle->p4.Py();
                                            }
                                            else
                                            {
                                                //std::cout << "Found WJets Ersatz neutrino match ----> neglecting muon!!!" << std::endl;
                                            }
                                        }
                                        else
                                        {
                                            visPx += genParticle->p4.Px();
                                            visPy += genParticle->p4.Py();
                                        }
				}
			}
		}
		
		// Save the ingredients for the correction
		(product.*m_metCorrections).push_back(genPx);
		(product.*m_metCorrections).push_back(genPy);
		(product.*m_metCorrections).push_back(visPx);
		(product.*m_metCorrections).push_back(visPy);
		
		float correctedMetX, correctedMetY;
		
		if(m_correctionMethod == MetCorrectorBase::CorrectionMethod::QUANTILE_MAPPING)
			m_recoilCorrector->Correct(
				metX,
				metY,
				genPx,
				genPy,
				visPx,
				visPy,
				nJets30,
				correctedMetX,
				correctedMetY);
		else if(m_correctionMethod == MetCorrectorBase::CorrectionMethod::MEAN_RESOLUTION)
			m_recoilCorrector->CorrectByMeanResolution(
				metX,
				metY,
				genPx,
				genPy,
				visPx,
				visPy,
				nJets30,
				correctedMetX,
				correctedMetY);
		
		(product.*m_metMemberCorrected) = *(product.*m_metMemberUncorrected);
		
		// Apply the recoil correction to the MET object (only for DY, W and Higgs samples)
		if (m_processType == MEtSys::ProcessType::BOSON)
		{
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				correctedMetX,
				correctedMetY,
				0.,
				std::sqrt(metResolution * metResolution + correctedMetX * correctedMetX + correctedMetY * correctedMetY));
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
		else if ((settings.*GetUpdateMetWithCorrectedLeptons)()) // Apply at least corrections from lepton adjustments
		{
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				metX,
				metY,
				0.,
				std::sqrt(metResolution * metResolution + metX * metX + metY * metY));
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
		else if (settings.GetMetUncertaintyShift()) // If no other corrections are applied, use MET shifted by uncertainty if required by configuration
		{
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Px(),
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Py(),
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Pz(),
				(product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].energy());
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
		
		// Apply the correction to the MET object, if required (done for all the samples)
		if (m_doMetSys)
		{
			float correctedMetShiftX, correctedMetShiftY;
			
			m_metShiftCorrector->ApplyMEtSys(
				(product.*m_metMemberCorrected).p4.Px(), (product.*m_metMemberCorrected).p4.Py(),
				genPx, genPy,
				visPx, visPy,
				nJets30,
				m_processType,
				m_sysType,
				m_sysShift,
				correctedMetShiftX,
				correctedMetShiftY
			);
			
			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				correctedMetShiftX,
				correctedMetShiftY,
				0.,
				std::sqrt(metResolution * metResolution + correctedMetShiftX * correctedMetShiftX + correctedMetShiftY * correctedMetShiftY));
			if (m_correctGlobalMet)
			{
				product.m_met = product.*m_metMemberCorrected;
			}
		}
	}

protected:
	TMet* product_type::*m_metMemberUncorrected;
	TMet product_type::*m_metMemberCorrected;
	std::vector<float> product_type::*m_metCorrections;
	std::string (setting_type::*GetRecoilCorrectorFile)(void) const;
	std::string (setting_type::*GetMetShiftCorrectorFile)(void) const;
	RecoilCorrector* m_recoilCorrector;
	MEtSys* m_metShiftCorrector;
	MEtSys::ProcessType m_processType;
	MEtSys::SysType m_sysType;
	MEtSys::SysShift m_sysShift;
	bool m_isWJets;
	bool m_doMetSys;
	CorrectionMethod m_correctionMethod;
	bool m_correctGlobalMet;
	bool (setting_type::*GetUpdateMetWithCorrectedLeptons)(void) const;
	KMETUncertainty::Type m_metUncertaintyType;
};



/**
   \brief Corrector for (PF) MET
*/
class MetCorrector: public MetCorrectorBase<KMET>
{
public:
	MetCorrector();
	virtual void Init(setting_type const& settings) override;
	virtual std::string GetProducerId() const override;
};

/**
   \brief Corrector for MVAMET
*/
class MvaMetCorrector: public MetCorrectorBase<KMET>
{
public:
	MvaMetCorrector();
	virtual void Init(setting_type const& settings) override;
	virtual std::string GetProducerId() const override;
};
