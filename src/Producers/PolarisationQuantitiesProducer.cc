
#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/PolarisationQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/A1Helper.h"

#include <Math/VectorUtil.h>


std::string PolarisationQuantitiesProducer::GetProducerId() const
{
	return "PolarisationQuantitiesProducer";
}

void PolarisationQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1OmegaHHKinFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaHHKinFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1OmegaHHKinFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaHHKinFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1OmegaSvfit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaSvfit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1OmegaSvfit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaSvfit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("rhoNeutralChargedAsymmetry_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_rhoNeutralChargedAsymmetry, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("rhoNeutralChargedAsymmetry_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_rhoNeutralChargedAsymmetry, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleOverFullEnergyHHKinFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleOverFullEnergyHHKinFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleOverFullEnergySvfit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleOverFullEnergySvfit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleToFullAngleHHKinFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleHHKinFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleToFullAngleHHKinFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleHHKinFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleToFullAngleSvfit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleSvfit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleToFullAngleSvfit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleSvfit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauPolarisationDiscriminatorHHKinFit", [](event_type const& event, product_type const& product) {
		return static_cast<float>(product.m_tauPolarisationDiscriminatorHHKinFit);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauPolarisationDiscriminatorSvfit", [](event_type const& event, product_type const& product) {
		return static_cast<float>(product.m_tauPolarisationDiscriminatorSvfit);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauPolarisationDiscriminatorSimpleFit", [](event_type const& event, product_type const& product) {
		return static_cast<float>(product.m_tauPolarisationDiscriminatorSimpleFit);
	});
}

void PolarisationQuantitiesProducer::Produce(
		event_type const& event,
		product_type& product,
		setting_type const& settings
) const
{
	bool tauPolarisationDiscriminatorChosen = false;
	// all numbers of prongs
	{
		size_t indexLepton = 0;
		for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
			 lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
		{
			// HHKinFit version
			if (Utility::Contains(product.m_hhKinFitTaus, *lepton))
			{
				RMFLV* fittedTauHHKinFit = &(SafeMap::Get(product.m_hhKinFitTaus, *lepton));
				product.m_visibleOverFullEnergyHHKinFit[*lepton] = (fittedTauHHKinFit->E() != 0.0 ? (*lepton)->p4.E() / fittedTauHHKinFit->E() : DefaultValues::UndefinedDouble);
				product.m_visibleToFullAngleHHKinFit[*lepton] = ROOT::Math::VectorUtil::Angle((*lepton)->p4, *fittedTauHHKinFit);
			}
		
			// SVfit version
			RMFLV* fittedTauSvfit = (indexLepton == 0 ? product.m_svfitResults.fittedTau1LV : product.m_svfitResults.fittedTau2LV);
			if (fittedTauSvfit != nullptr)
			{
				product.m_visibleOverFullEnergySvfit[*lepton] = (indexLepton == 0 ? (*lepton)->p4.E() / fittedTauSvfit->E() : product.m_svfitResults.fittedTau2ERatio);
				product.m_visibleToFullAngleSvfit[*lepton] = ROOT::Math::VectorUtil::Angle((*lepton)->p4, *fittedTauSvfit);
			}
			
			++indexLepton;
		}
	} // limit scope of indexLepton
	
	size_t indexLepton = 0;
	for (std::vector<KTau*>::iterator tau = product.m_validTaus.begin(); tau != product.m_validTaus.end(); ++tau)
	{
		// 3-prong method
		if (((*tau)->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
		    ((*tau)->chargedHadronCandidates.size() > 2))
		{
			// sort pions from a1 decay according to their charge
			RMFLV* piSingleChargeSign = nullptr;
			RMFLV* piDoubleChargeSign1 = nullptr;
			RMFLV* piDoubleChargeSign2 = nullptr;
			if (((*tau)->chargedHadronCandidates.at(0).charge() * (*tau)->chargedHadronCandidates.at(1).charge()) > 0.0)
			{
				piSingleChargeSign = &((*tau)->chargedHadronCandidates.at(2).p4);
				piDoubleChargeSign1 = &((*tau)->chargedHadronCandidates.at(0).p4);
				piDoubleChargeSign2 = &((*tau)->chargedHadronCandidates.at(1).p4);
			}
			else if (((*tau)->chargedHadronCandidates.at(0).charge() * (*tau)->chargedHadronCandidates.at(2).charge()) > 0.0)
			{
				piSingleChargeSign = &((*tau)->chargedHadronCandidates.at(1).p4);
				piDoubleChargeSign1 = &((*tau)->chargedHadronCandidates.at(0).p4);
				piDoubleChargeSign2 = &((*tau)->chargedHadronCandidates.at(2).p4);
			}
			else // if (((*tau)->chargedHadronCandidates.at(1).charge() * (*tau)->chargedHadronCandidates.at(2).charge()) > 0.0)
			{
				piSingleChargeSign = &((*tau)->chargedHadronCandidates.at(0).p4);
				piDoubleChargeSign1 = &((*tau)->chargedHadronCandidates.at(1).p4);
				piDoubleChargeSign2 = &((*tau)->chargedHadronCandidates.at(2).p4);
			}
			std::vector<RMFLV*> pions = { piDoubleChargeSign1, piDoubleChargeSign2, piSingleChargeSign };
			
			// HHKinFit version
			if (Utility::Contains(product.m_hhKinFitTaus, static_cast<KLepton*>(*tau)))
			{
				std::vector<TLorentzVector> a1HelperInputsHHKinFit;
				a1HelperInputsHHKinFit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get(product.m_hhKinFitTaus, static_cast<KLepton*>(*tau))));
				a1HelperInputsHHKinFit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piSingleChargeSign));
				a1HelperInputsHHKinFit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign1));
				a1HelperInputsHHKinFit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign2));
				a1Helper a1QuantitiesHHKinFit(a1HelperInputsHHKinFit, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>((*tau)->p4));
				product.m_a1OmegaHHKinFit[*tau] = a1QuantitiesHHKinFit.getA1omega();
			}
		
			// SVfit version
			RMFLV* fittedTauSvfit = (indexLepton == 0 ? product.m_svfitResults.fittedTau1LV : product.m_svfitResults.fittedTau2LV);
			if (fittedTauSvfit != nullptr)
			{
				std::vector<TLorentzVector> a1HelperInputsSvfit;
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*fittedTauSvfit));
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piSingleChargeSign));
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign1));
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign2));
				a1Helper a1QuantitiesSvfit(a1HelperInputsSvfit, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>((*tau)->p4));
				product.m_a1OmegaSvfit[*tau] = a1QuantitiesSvfit.getA1omega();
			}
		
			if (! tauPolarisationDiscriminatorChosen)
			{
				product.m_tauPolarisationDiscriminatorHHKinFit = SafeMap::GetWithDefault(product.m_a1OmegaHHKinFit, static_cast<KLepton*>(*tau), DefaultValues::UndefinedDouble);
				product.m_tauPolarisationDiscriminatorSvfit = SafeMap::GetWithDefault(product.m_a1OmegaSvfit, static_cast<KLepton*>(*tau), DefaultValues::UndefinedDouble);
				tauPolarisationDiscriminatorChosen = true;
			}
		}
		
		// 1-prong + pi0 method
		if (((*tau)->decayMode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero) &&
		    ((*tau)->chargedHadronCandidates.size() > 0) &&
		    (((*tau)->piZeroCandidates.size() > 0) || ((*tau)->gammaCandidates.size() > 0)))
		{
			double energyChargedPi = (*tau)->sumChargedHadronCandidates().E();
			double energyNeutralPi = (*tau)->piZeroMomentum().E();
			product.m_rhoNeutralChargedAsymmetry[*tau] = (((energyNeutralPi + energyChargedPi) != 0.0) ? (energyChargedPi - energyNeutralPi) / (energyChargedPi + energyNeutralPi) : 0.0);
			
			if (! tauPolarisationDiscriminatorChosen)
			{
				product.m_tauPolarisationDiscriminatorHHKinFit = SafeMap::Get(product.m_rhoNeutralChargedAsymmetry, static_cast<KLepton*>(*tau));
				product.m_tauPolarisationDiscriminatorSvfit = product.m_tauPolarisationDiscriminatorHHKinFit;
				tauPolarisationDiscriminatorChosen = true;
			}
		}
		
		++indexLepton;
	}
	
	// combination
	bool tauFound = false;
	bool muonFound = false;
	bool electronFound = false;
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		// prefer hadronic taus first, then muons and then electrons for the event-based discriminator
		if (! tauPolarisationDiscriminatorChosen)
		{
			if (! tauFound)
			{
				if ((*lepton)->flavour() == KLeptonFlavour::TAU)
				{
					product.m_tauPolarisationDiscriminatorHHKinFit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, *lepton, DefaultValues::UndefinedDouble);
					product.m_tauPolarisationDiscriminatorSvfit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, *lepton, DefaultValues::UndefinedDouble);
					tauFound = true;
				}
				else
				{
					if (! muonFound)
					{
						if ((*lepton)->flavour() == KLeptonFlavour::MUON)
						{
							product.m_tauPolarisationDiscriminatorHHKinFit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, *lepton, DefaultValues::UndefinedDouble);
							product.m_tauPolarisationDiscriminatorSvfit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, *lepton, DefaultValues::UndefinedDouble);
							muonFound = true;
						}
						else if (! electronFound)
						{
							product.m_tauPolarisationDiscriminatorHHKinFit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, *lepton, DefaultValues::UndefinedDouble);
							product.m_tauPolarisationDiscriminatorSvfit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, *lepton, DefaultValues::UndefinedDouble);
							electronFound = true;
						}
					}
				}
			}
		}
	}
	tauPolarisationDiscriminatorChosen = (tauPolarisationDiscriminatorChosen || (product.m_flavourOrderedLeptons.size() > 0));
	
}
