
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

#include "HTT-utilities/RecoilCorrections/interface/RecoilCorrector.h"
#include "HTT-utilities/RecoilCorrections/interface/MEtSys.h"

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

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);

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
				// m_sysType = MEtSys::SysType::NoType;
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
	                     setting_type const& settings, metadata_type const& metadata) const override
	{
		assert(m_metMemberUncorrected != nullptr);

		// Retrieve the needed informations from the event content
		// and replace nominal met four vector by one shifted by
		// specific uncertainty in order to propagate it through
		// entire analysis if required by configuration
		float metX = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Px() : (product.*m_metMemberUncorrected)->p4.Px();
		float metY = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].Py() : (product.*m_metMemberUncorrected)->p4.Py();
		float metEnergy = settings.GetMetUncertaintyShift() ? (product.*m_metMemberUncorrected)->p4_shiftedByUncertainties[m_metUncertaintyType].energy() : (product.*m_metMemberUncorrected)->p4.energy();
		float metResolutionSquared = metEnergy * metEnergy - metX * metX - metY * metY;
		// float metResolution = metResolutionSquared > 0 ? std::sqrt(metResolutionSquared) : 0;

		// Recalculate MET if lepton energies have been corrected:
		// MetX' = MetX + Px - Px'
		// MetY' = MetY + Py - Py'
		// MET' = sqrt(MetX' * MetX' + MetY' * MetY')
		if ((settings.*GetUpdateMetWithCorrectedLeptons)())
		{
			// Electrons
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
			}
		}

		// Recoil corrections follow
		int nJets30 = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);

		// In selected W+Jets events one of the leptons is faked by hadronic jet and this
		// jet should be counted as a part of hadronic recoil to the W boson
		if(m_isWJets)
		{
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
				genPx += genParticle->p4.Px();
				genPy += genParticle->p4.Py();

				if ( !(pdgId == DefaultValues::pdgIdNuE || pdgId == DefaultValues::pdgIdNuMu || pdgId == DefaultValues::pdgIdNuTau) )
				{
					visPx += genParticle->p4.Px();
					visPy += genParticle->p4.Py();
				}
			}
		}

		// Save the ingredients for the correction
		(product.*m_metCorrections).push_back(genPx);
		(product.*m_metCorrections).push_back(genPy);
		(product.*m_metCorrections).push_back(visPx);
		(product.*m_metCorrections).push_back(visPy);

		float correctedMetX(metX), correctedMetY(metY);

		if(m_correctionMethod == MetCorrectorBase::CorrectionMethod::QUANTILE_MAPPING)
			m_recoilCorrector->CorrectWithHist(
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
				std::sqrt(metResolutionSquared + correctedMetX * correctedMetX + correctedMetY * correctedMetY));
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
				std::sqrt(metResolutionSquared + metX * metX + metY * metY));
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
		if (m_processType != MEtSys::ProcessType::BOSON && m_processType != MEtSys::ProcessType::TOP)   //only for MC with no recoilcorrections, calculated in TaggedJetUncertaintyShiftProducer
		{
			product.m_met.p4 += product.m_MET_shift.p4;
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
				// m_processType,
				m_sysType,
				m_sysShift,
				correctedMetShiftX,
				correctedMetShiftY
			);

			(product.*m_metMemberCorrected).p4.SetPxPyPzE(
				correctedMetShiftX,
				correctedMetShiftY,
				0.,
				std::sqrt(metResolutionSquared + correctedMetShiftX * correctedMetShiftX + correctedMetShiftY * correctedMetShiftY));
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
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual std::string GetProducerId() const override;
};

/**
   \brief Corrector for MVAMET
*/
class MvaMetCorrector: public MetCorrectorBase<KMET>
{
public:
	MvaMetCorrector();
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual std::string GetProducerId() const override;
};

/**
   \brief Corrector for PUPPIMET
*/
class PuppiMetCorrector: public MetCorrectorBase<KMET>
{
public:
	PuppiMetCorrector();
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual std::string GetProducerId() const override;
};
