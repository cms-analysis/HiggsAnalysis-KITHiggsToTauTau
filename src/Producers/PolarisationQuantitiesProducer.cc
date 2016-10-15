
#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/PolarisationQuantitiesProducer.h"



std::string PolarisationQuantitiesProducer::GetProducerId() const
{
	return "PolarisationQuantitiesProducer";
}

void PolarisationQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosBeta_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosBeta, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosBeta_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosBeta, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosGamma_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosGamma, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosGamma_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosGamma, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinGamma_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinGamma, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinGamma_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinGamma, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("rhoNeutralChargedAsymmetry_1", [](event_type const& event, product_type const& product) {
                return static_cast<float>(SafeMap::GetWithDefault(product.m_rhoNeutralChargedAsymmetry, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
        });
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("rhoNeutralChargedAsymmetry_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_rhoNeutralChargedAsymmetry, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleOverFullEnergy_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergy, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visibleOverFullEnergy_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_visibleOverFullEnergy, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
}

void PolarisationQuantitiesProducer::Produce(
		event_type const& event,
		product_type& product,
		setting_type const& settings
) const
{
	// 3-prong method
	for (std::vector<KTau*>::iterator tau = product.m_validTaus.begin(); tau != product.m_validTaus.end(); ++tau)
	{
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
			
			// calculate auxiliary variables
			std::vector<double> valuesA;
			std::vector<double> valuesB;
			for (std::vector<RMFLV*>::iterator pion = pions.begin(); pion != pions.end(); ++pion)
			{
				valuesA.push_back((((*tau)->p4.E()*((*tau)->p4.Vect().Dot((*pion)->Vect()))) - ((*pion)->E()*std::pow((*tau)->p4.Vect().R(), 2))) / std::pow((*tau)->p4.mass(), 2));
				valuesB.push_back((std::pow(((*pion)->E()*(*tau)->p4.E()) - ((*pion)->Vect().Dot((*tau)->p4.Vect())), 2) - (std::pow((*pion)->mass(), 2)*std::pow((*tau)->p4.mass(), 2))) / std::pow((*tau)->p4.mass(), 2));
			}
			double valueLambda = std::pow(valuesB[0], 2) + std::pow(valuesB[1], 2) + std::pow(valuesB[2], 2) - 2.0 * ((valuesB[0]*valuesB[1]) + (valuesB[0]*valuesB[2]) + (valuesB[1]*valuesB[2]));
			double valueT = std::sqrt(-valueLambda) / 2.0;
			
			// calculate angles
			product.m_a1CosBeta[*tau] = pions[2]->Vect().Dot(pions[0]->Vect().Cross(pions[1]->Vect())) / ((*tau)->p4.Vect().R() * valueT);
			product.m_a1CosGamma[*tau] = valuesA[2] / ((*tau)->p4.Vect().R()*std::sqrt(valuesB[2])*std::sin(std::acos(product.m_a1CosBeta[*tau])));
			product.m_a1SinGamma[*tau] = (-product.m_a1CosGamma[*tau] / valueT) * ((valuesB[2]*valuesA[0]/valuesA[1]) - ((valuesB[1]-valuesB[0]-valuesB[2])/2.0));
		}
	}
	
	// 1-prong method
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		if (Utility::Contains(product.m_hhKinFitTaus, *lepton))
		{
			product.m_visibleOverFullEnergy[*lepton] = (*lepton)->p4.E() / SafeMap::Get(product.m_hhKinFitTaus, *lepton).E();
		}
	}
	
	// 1-prong + pi0 method
	for (std::vector<KTau*>::iterator tau = product.m_validTaus.begin(); tau != product.m_validTaus.end(); ++tau)
	{
		if (((*tau)->decayMode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero) &&
		    ((*tau)->chargedHadronCandidates.size() > 0) &&
		    (((*tau)->piZeroCandidates.size() > 0) || ((*tau)->gammaCandidates.size() > 0)))
		{
			double energyChargedPi = (*tau)->sumChargedHadronCandidates().E();
			double energyNeutralPi = (*tau)->piZeroMomentum().E();
			product.m_rhoNeutralChargedAsymmetry[*tau] = (((energyNeutralPi + energyChargedPi) != 0.0) ? (energyChargedPi - energyNeutralPi) / (energyChargedPi + energyNeutralPi) : 0.0);
		}
	}
}
