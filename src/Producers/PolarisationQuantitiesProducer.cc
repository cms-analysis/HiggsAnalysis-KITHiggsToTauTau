
#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/PolarisationQuantitiesProducer.h"

#include "TauPolSoftware/TauDecaysInterface/interface/TauPolInterface.h"

#include <Math/VectorUtil.h>


PolarisationQuantitiesProducerBase::PolarisationQuantitiesProducerBase(
		std::string name,
		std::map<KLepton*, RMFLV> product_type::*fittedTausMember,
		std::map<KLepton*, double> product_type::*polarisationOmegasMember,
		std::map<KLepton*, double> product_type::*polarisationOmegaBarsMember,
		double product_type::*polarisationCombinedOmegaMember,
		double product_type::*polarisationCombinedOmegaBarMember
) :
	m_name(name),
	m_fittedTausMember(fittedTausMember),
	m_polarisationOmegasMember(polarisationOmegasMember),
	m_polarisationOmegaBarsMember(polarisationOmegaBarsMember),
	m_polarisationCombinedOmegaMember(polarisationCombinedOmegaMember),
	m_polarisationCombinedOmegaBarMember(polarisationCombinedOmegaBarMember)
{
}

void PolarisationQuantitiesProducerBase::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	// add possible quantities for the lambda ntuples consumers
	for (size_t leptonIndex = 0; leptonIndex < 2; ++leptonIndex)
	{
		std::string namePostfix = m_name+"_" + std::to_string(leptonIndex+1);
		
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "polarisationOmega"+namePostfix, [leptonIndex, this](event_type const& event, product_type const& product) {
			return static_cast<float>(SafeMap::GetWithDefault((product.*m_polarisationOmegasMember), product.m_flavourOrderedLeptons.at(leptonIndex), DefaultValues::UndefinedDouble));
		});
		
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "polarisationOmegaBar"+namePostfix, [leptonIndex, this](event_type const& event, product_type const& product) {
			return static_cast<float>(SafeMap::GetWithDefault((product.*m_polarisationOmegaBarsMember), product.m_flavourOrderedLeptons.at(leptonIndex), DefaultValues::UndefinedDouble));
		});
	}
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "polarisationCombinedOmega"+m_name, [this](event_type const& event, product_type const& product) {
		return (product.*m_polarisationCombinedOmegaMember);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "polarisationCombinedOmegaBar"+m_name, [this](event_type const& event, product_type const& product) {
		return (product.*m_polarisationCombinedOmegaBarMember);
	});
	
	/* old version
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "a1OmegaHHKinFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaHHKinFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "a1OmegaHHKinFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaHHKinFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "a1OmegaSvfit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaSvfit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "a1OmegaSvfit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaSvfit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "a1OmegaSimpleFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaSimpleFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "a1OmegaSimpleFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1OmegaSimpleFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "rhoNeutralChargedAsymmetry_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_rhoNeutralChargedAsymmetry, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "rhoNeutralChargedAsymmetry_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_rhoNeutralChargedAsymmetry, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleOverFullEnergyHHKinFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleOverFullEnergyHHKinFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleOverFullEnergySvfit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleOverFullEnergySvfit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleOverFullEnergySimpleFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergySimpleFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleOverFullEnergySimpleFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergySimpleFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleToFullAngleHHKinFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleHHKinFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleToFullAngleHHKinFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleHHKinFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleToFullAngleSvfit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleSvfit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleToFullAngleSvfit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleSvfit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleToFullAngleSimpleFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleSimpleFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visibleToFullAngleSimpleFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleToFullAngleSimpleFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauPolarisationDiscriminatorHHKinFit", [](event_type const& event, product_type const& product) {
		return static_cast<float>(product.m_tauPolarisationDiscriminatorHHKinFit);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauPolarisationDiscriminatorSvfit", [](event_type const& event, product_type const& product) {
		return static_cast<float>(product.m_tauPolarisationDiscriminatorSvfit);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauPolarisationDiscriminatorSimpleFit", [](event_type const& event, product_type const& product) {
		return static_cast<float>(product.m_tauPolarisationDiscriminatorSimpleFit);
	});
	*/
}

void PolarisationQuantitiesProducerBase::Produce(
		event_type const& event,
		product_type& product,
		setting_type const& settings, metadata_type const& metadata
) const
{
	assert(product.m_flavourOrderedLeptons.size() > 1);
	
	std::vector<std::vector<TLorentzVector> > inputs;
	std::vector<std::string> types;
	std::vector<int> charges;

	
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
		 lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{

		if (((*lepton)->flavour() == KLeptonFlavour::ELECTRON) || ((*lepton)->flavour() == KLeptonFlavour::MUON))
		{
			inputs.push_back(GetInputLepton(product, *lepton));
			types.push_back("lepton");
			charges.push_back((*lepton)->charge());

		}
		else if ((*lepton)->flavour() == KLeptonFlavour::TAU)
		{
			KTau* tau = static_cast<KTau*>(*lepton);
			if ((tau->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) && (tau->chargedHadronCandidates.size() > 2))
			{
				inputs.push_back(GetInputA1(product, *lepton));
				types.push_back("a1");
				charges.push_back((*lepton)->charge());
			}
			else if ((tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero) &&
			         (tau->chargedHadronCandidates.size() > 0) &&
			         ((tau->piZeroCandidates.size() > 0) || (tau->gammaCandidates.size() > 0)))
			{
				inputs.push_back(GetInputRho(product, *lepton));
				types.push_back("rho");
				charges.push_back((*lepton)->charge());
			}
			else
			{
				inputs.push_back(GetInputPion(product, *lepton));
				types.push_back("pion");
				charges.push_back((*lepton)->charge());
			}
		}
		

		if (inputs.back().size() > 0)
		{
			TauPolInterface singleTauPolInterface(inputs.back(), types.back(), charges.back());
			if (singleTauPolInterface.isConfigured())
			{
				(product.*m_polarisationOmegasMember)[*lepton] = singleTauPolInterface.getOmega();
				(product.*m_polarisationOmegaBarsMember)[*lepton] = singleTauPolInterface.getOmegabar();
			}
		}
	}
	
	if ((inputs.at(0).size() > 0) && (inputs.at(1).size() > 0))
	{
		TauPolInterface diTauPolInterface(inputs.at(0), types.at(0), inputs.at(1), types.at(1), charges.at(0), charges.at(1));
		if (diTauPolInterface.isPairConfigured())
		{
			(product.*m_polarisationCombinedOmegaMember) = diTauPolInterface.getCombOmega();
			(product.*m_polarisationCombinedOmegaBarMember) = diTauPolInterface.getCombOmegaBar();
		}
	}
	
	/* old version
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
		
			// SimpleFit version
			if (Utility::Contains(product.m_simpleFitTaus, *lepton))
			{
				RMFLV fittedTauSimpleFit = SafeMap::Get(product.m_simpleFitTaus, *lepton);
				product.m_visibleOverFullEnergySimpleFit[*lepton] = (*lepton)->p4.E() / fittedTauSimpleFit.E();
				product.m_visibleToFullAngleSimpleFit[*lepton] = ROOT::Math::VectorUtil::Angle((*lepton)->p4, fittedTauSimpleFit);
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
		
			// SimpleFit version
			if (Utility::Contains(product.m_simpleFitTaus, static_cast<KLepton*>(*tau)))
			{
				std::vector<TLorentzVector> a1HelperInputsSvfit;
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get(product.m_simpleFitTaus, static_cast<KLepton*>(*tau))));
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piSingleChargeSign));
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign1));
				a1HelperInputsSvfit.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign2));
				a1Helper a1QuantitiesSvfit(a1HelperInputsSvfit, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>((*tau)->p4));
				product.m_a1OmegaSimpleFit[*tau] = a1QuantitiesSvfit.getA1omega();
			}
		
			if (! tauPolarisationDiscriminatorChosen)
			{
				product.m_tauPolarisationDiscriminatorHHKinFit = SafeMap::GetWithDefault(product.m_a1OmegaHHKinFit, static_cast<KLepton*>(*tau), DefaultValues::UndefinedDouble);
				product.m_tauPolarisationDiscriminatorSvfit = SafeMap::GetWithDefault(product.m_a1OmegaSvfit, static_cast<KLepton*>(*tau), DefaultValues::UndefinedDouble);
				product.m_tauPolarisationDiscriminatorSimpleFit = SafeMap::GetWithDefault(product.m_a1OmegaSimpleFit, static_cast<KLepton*>(*tau), DefaultValues::UndefinedDouble);
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
				product.m_tauPolarisationDiscriminatorSimpleFit = product.m_tauPolarisationDiscriminatorHHKinFit;
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
					product.m_tauPolarisationDiscriminatorSimpleFit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergySimpleFit, *lepton, DefaultValues::UndefinedDouble);
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
							product.m_tauPolarisationDiscriminatorSimpleFit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergySimpleFit, *lepton, DefaultValues::UndefinedDouble);
							muonFound = true;
						}
						else if (! electronFound)
						{
							product.m_tauPolarisationDiscriminatorHHKinFit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergyHHKinFit, *lepton, DefaultValues::UndefinedDouble);
							product.m_tauPolarisationDiscriminatorSvfit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergySvfit, *lepton, DefaultValues::UndefinedDouble);
							product.m_tauPolarisationDiscriminatorSimpleFit = SafeMap::GetWithDefault(product.m_visibleOverFullEnergySimpleFit, *lepton, DefaultValues::UndefinedDouble);
							electronFound = true;
						}
					}
				}
			}
		}
	}
	tauPolarisationDiscriminatorChosen = (tauPolarisationDiscriminatorChosen || (product.m_flavourOrderedLeptons.size() > 0));
	*/
}

std::vector<TLorentzVector> PolarisationQuantitiesProducerBase::GetInputLepton(product_type& product, KLepton* lepton) const
{
	std::vector<TLorentzVector> input;
	
	if (Utility::Contains((product.*m_fittedTausMember), lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get((product.*m_fittedTausMember), lepton)));
		
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(lepton->p4));
	}
	
	return input;
}

std::vector<TLorentzVector> PolarisationQuantitiesProducerBase::GetInputPion(product_type& product, KLepton* lepton) const
{
	std::vector<TLorentzVector> input;
	
	if (Utility::Contains((product.*m_fittedTausMember), lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get((product.*m_fittedTausMember), lepton)));
		
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(lepton->p4));
	}
	
	return input;
}

std::vector<TLorentzVector> PolarisationQuantitiesProducerBase::GetInputRho(product_type& product, KLepton* lepton) const
{
	std::vector<TLorentzVector> input;
	
	if (Utility::Contains((product.*m_fittedTausMember), lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get((product.*m_fittedTausMember), lepton)));
		
		KTau* tau = static_cast<KTau*>(lepton);
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(tau->sumChargedHadronCandidates()));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(tau->piZeroMomentum()));
	}
	
	return input;
}

std::vector<TLorentzVector> PolarisationQuantitiesProducerBase::GetInputA1(product_type& product, KLepton* lepton) const
{
	std::vector<TLorentzVector> input;
	
	if (Utility::Contains((product.*m_fittedTausMember), lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get((product.*m_fittedTausMember), lepton)));
		
		KTau* tau = static_cast<KTau*>(lepton);
		assert(tau->chargedHadronCandidates.size() > 2);
		
		// sort pions from a1 decay according to their charge
		RMFLV* piSingleChargeSign = nullptr;
		RMFLV* piDoubleChargeSign1 = nullptr;
		RMFLV* piDoubleChargeSign2 = nullptr;
		if ((tau->chargedHadronCandidates.at(0).charge() * tau->chargedHadronCandidates.at(1).charge()) > 0.0)
		{
			piSingleChargeSign = &(tau->chargedHadronCandidates.at(2).p4);
			piDoubleChargeSign1 = &(tau->chargedHadronCandidates.at(0).p4);
			piDoubleChargeSign2 = &(tau->chargedHadronCandidates.at(1).p4);
		}
		else if ((tau->chargedHadronCandidates.at(0).charge() * tau->chargedHadronCandidates.at(2).charge()) > 0.0)
		{
			piSingleChargeSign = &(tau->chargedHadronCandidates.at(1).p4);
			piDoubleChargeSign1 = &(tau->chargedHadronCandidates.at(0).p4);
			piDoubleChargeSign2 = &(tau->chargedHadronCandidates.at(2).p4);
		}
		else // if ((tau->chargedHadronCandidates.at(1).charge() * tau->chargedHadronCandidates.at(2).charge()) > 0.0)
		{
			piSingleChargeSign = &(tau->chargedHadronCandidates.at(0).p4);
			piDoubleChargeSign1 = &(tau->chargedHadronCandidates.at(1).p4);
			piDoubleChargeSign2 = &(tau->chargedHadronCandidates.at(2).p4);
		}
		
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piSingleChargeSign));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign1));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign2));
	}
	
	return input;
}


PolarisationQuantitiesSvfitProducer::PolarisationQuantitiesSvfitProducer() :
	PolarisationQuantitiesProducerBase(
			"Svfit",
			&product_type::m_svfitTaus,
			&product_type::m_polarisationOmegasSvfit,
			&product_type::m_polarisationOmegaBarsSvfit,
			&product_type::m_polarisationCombinedOmegaSvfit,
			&product_type::m_polarisationCombinedOmegaBarSvfit
	)
{
}

std::string PolarisationQuantitiesSvfitProducer::GetProducerId() const
{
	return "PolarisationQuantitiesSvfitProducer";
}


PolarisationQuantitiesSimpleFitProducer::PolarisationQuantitiesSimpleFitProducer() :
	PolarisationQuantitiesProducerBase(
			"SimpleFit",
			&product_type::m_simpleFitTaus,
			&product_type::m_polarisationOmegasSimpleFit,
			&product_type::m_polarisationOmegaBarsSimpleFit,
			&product_type::m_polarisationCombinedOmegaSimpleFit,
			&product_type::m_polarisationCombinedOmegaBarSimpleFit
	)
{
}

std::string PolarisationQuantitiesSimpleFitProducer::GetProducerId() const
{
	return "PolarisationQuantitiesSimpleFitProducer";
}


/*
PolarisationQuantitiesHHKinFitProducer::PolarisationQuantitiesHHKinFitProducer() :
	PolarisationQuantitiesProducerBase(
			"HHKinFit",
			&product_type::m_hhKinFitTaus,
			&product_type::m_polarisationOmegasHHKinFit,
			&product_type::m_polarisationOmegaBarsHHKinFit,
			&product_type::m_polarisationCombinedOmegaHHKinFit,
			&product_type::m_polarisationCombinedOmegaBarHHKinFit
	)
{
}

std::string PolarisationQuantitiesHHKinFitProducer::GetProducerId() const
{
	return "PolarisationQuantitiesHHKinFitProducer";
}
*/
