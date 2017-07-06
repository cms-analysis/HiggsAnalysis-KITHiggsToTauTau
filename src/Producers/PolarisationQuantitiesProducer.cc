
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosBeta_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosBeta, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosBeta_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosBeta, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinBeta_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinBeta, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinBeta_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinBeta, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosTheta_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosTheta, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosTheta_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosTheta, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinTheta_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinTheta, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinTheta_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinTheta, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosPsi_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosPsi, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1CosPsi_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1CosPsi, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinPsi_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinPsi, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1SinPsi_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1SinPsi, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
	});
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1optimumVariableSimpleFit_1", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1optimumVariableSimpleFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("a1optimumVariableSimpleFit_2", [](event_type const& event, product_type const& product) {
		return static_cast<float>(SafeMap::GetWithDefault(product.m_a1optimumVariableSimpleFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble));
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

			// SimpleFit version --- only for A1 decay channel
			if (Utility::Contains(product.m_SimpleFitTaus, *lepton))
			{
				RMFLV* fittedTauSimpleFit = &(SafeMap::Get(product.m_SimpleFitTaus, *lepton));
				product.m_a1optimumVariableSimpleFit[*lepton] = (fittedTauSimpleFit->E() != 0.0 ? (*lepton)->p4.E() / fittedTauSimpleFit->E() :  DefaultValues::UndefinedDouble);  // TODO: change the definition of variables
			}
			++indexLepton;
		}
	} // limit scope of indexLepton
	
	double valueV = 0.0;
	
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
			
			// calculate auxiliary variables for angles
			std::vector<double> valuesA;
			std::vector<double> valuesB;

			for (std::vector<RMFLV*>::iterator pion = pions.begin(); pion != pions.end(); ++pion)
			{
				valuesA.push_back((((*tau)->p4.E()*((*tau)->p4.Vect().Dot((*pion)->Vect()))) - ((*pion)->E()*std::pow((*tau)->p4.Vect().R(), 2))) / std::pow((*tau)->p4.mass(), 2));
				valuesB.push_back((std::pow(((*pion)->E()*(*tau)->p4.E()) - ((*pion)->Vect().Dot((*tau)->p4.Vect())), 2) - (std::pow((*pion)->mass(), 2)*std::pow((*tau)->p4.mass(), 2))) / std::pow((*tau)->p4.mass(), 2));
			}
			double valueLambda = std::pow(valuesB[0], 2) + std::pow(valuesB[1], 2) + std::pow(valuesB[2], 2) - 2.0 * ((valuesB[0]*valuesB[1]) + (valuesB[0]*valuesB[2]) + (valuesB[1]*valuesB[2]));
			double valueT = std::sqrt(-valueLambda) / 2.0;
			
			std::vector<double> valuesS;
			valuesS.push_back(((*pions[1])+(*pions[2])).M2());
			valuesS.push_back(((*pions[2])+(*pions[0])).M2());
			valuesS.push_back(((*pions[0])+(*pions[1])).M2());
			double valueQ = (*tau)->p4.M2();
			valueQ *= 1.0;
			
			// calculate angles
			product.m_a1CosTheta[*tau] = (2*((pions[0]->E() + pions[1]->E() + pions[2]->E())/(*tau)->p4.E())*std::pow((*tau)->p4.mass(), 2) - std::pow((*tau)->p4.mass(), 2) - std::pow(valueQ, 2)) / ((std::pow((*tau)->p4.mass(), 2) - std::pow(valueQ, 2))*std::sqrt(1 - std::pow((*tau)->p4.mass(), 2) / std::pow((*tau)->p4.E(), 2)));	
			product.m_a1SinTheta[*tau] = std::sqrt(1 - std::pow(product.m_a1CosTheta[*tau], 2));
			product.m_a1CosBeta[*tau] = pions[2]->Vect().Dot(pions[0]->Vect().Cross(pions[1]->Vect())) / ((pions[0]->Vect() + pions[1]->Vect() + pions[2]->Vect()).R() * valueT);
			product.m_a1SinBeta[*tau] = std::sqrt(1 - std::pow(product.m_a1CosBeta[*tau], 2));
			product.m_a1CosGamma[*tau] = valuesA[2] / ((pions[0]->Vect() + pions[1]->Vect() + pions[2]->Vect()).R()*std::sqrt(valuesB[2])*std::sin(std::acos(product.m_a1CosBeta[*tau])));
			product.m_a1SinGamma[*tau] = (-product.m_a1CosGamma[*tau] / valueT) * ((valuesB[2]*valuesA[0]/valuesA[1]) - ((valuesB[1]-valuesB[0]-valuesB[2])/2.0));
			
			product.m_a1CosPsi[*tau] = (product.m_a1CosBeta[*tau]*(std::pow((*tau)->p4.mass(), 2) + std::pow(valueQ, 2)) + (std::pow((*tau)->p4.mass(), 2) - std::pow(valueQ, 2))) / (product.m_a1CosBeta[*tau]*(std::pow((*tau)->p4.mass(), 2) - std::pow(valueQ, 2)) + (std::pow((*tau)->p4.mass(), 2) + std::pow(valueQ, 2)));
			product.m_a1SinPsi[*tau] = std::sqrt(1 - std::pow(product.m_a1CosPsi[*tau], 2));
	
			// calculate auxiliary variables for optimum variable
			double valueU = 0.5*(3*std::pow(product.m_a1CosPsi[*tau], 2) - 1)*(1 - std::pow((*tau)->p4.mass(),2)/std::pow(valueQ, 2));
			valueV = 0.5*(3*std::pow(product.m_a1CosPsi[*tau], 2) - 1)*product.m_a1CosTheta[*tau]*(1 + std::pow((*tau)->p4.mass(),2)/std::pow(valueQ, 2)) + 3.0/2*2*product.m_a1SinPsi[*tau]*product.m_a1CosPsi[*tau]*std::sqrt(std::pow((*tau)->p4.mass(),2)/std::pow(valueQ, 2))*product.m_a1SinTheta[*tau];
			double valueV1V1 = (4*std::pow(pions[0]->mass(), 2) - valuesS[1]) - std::pow(valuesS[2] - valuesS[0], 2) / (4*std::pow(valueQ, 2));
			double valueV2V2 = (4*std::pow(pions[0]->mass(), 2) - valuesS[0]) - std::pow(valuesS[2] - valuesS[1], 2) / (4*std::pow(valueQ, 2));
			double valueV1V2 = (0.5*std::pow(pions[0]->mass(), 2) + valuesS[2] - std::pow(valueQ, 2)) - (valuesS[2] - valuesS[0])*(valuesS[2] - valuesS[1]) / (4*std::pow(valueQ, 2));
			double valueH0 = 2.0/3*(std::pow(2*std::pow(pions[0]->mass(), 2) - valuesS[0] - valuesS[1], 2)/std::pow(valueQ, 2)) - 8.0/3*std::pow(pions[0]->mass(), 2);

			double valueH = std::pow((valuesS[0]*valuesS[1]*valuesS[2] - std::pow(pions[0]->mass(), 2)*(std::pow(std::pow(valueQ, 2) - std::pow(pions[0]->mass(), 2), 2))) / valueH0*std::pow(valueQ, 2),2);
			// mass and width values from PDG 2014
			double gammaA10 = 0.250;
			double gammaRho10 = 0.149;
			double gammaRho20 = 0.400;
			double massA1 = 1.230;
			double massRho1 = 0.775;
			double massRho2 = 1.465;
	
			// g values necessary for Gamma functions in Eq. 65 in ref. Z. Phys. C Particles and Fields 56, 661-671, 1992)
			double gvalueQ = (std::pow(valueQ, 2) > std::pow(massRho1 + pions[0]->mass(), 2) ? std::pow(valueQ, 2)*(1.623 + 10.38/std::pow(valueQ, 2) + 0.65/std::pow(valueQ, 2)) : 4.1*std::pow(std::pow(valueQ, 2) - 9*std::pow(pions[0]->mass(), 2), 3)*(1 - 3.3*(std::pow(valueQ, 2) - 9*std::pow(pions[0]->mass(), 2)) + 5.8*std::pow(std::pow(valueQ, 2) - 9*std::pow(pions[0]->mass(),2), 2)));
			double gvalueA1 = (std::pow(massA1, 2) > std::pow(massRho1 + pions[0]->mass(), 2) ? std::pow(massA1, 2)*(1.623 + 10.38/std::pow(massA1, 2) + 0.65/std::pow(massA1, 2)) : 4.1*std::pow(std::pow(massA1, 2) - 9*std::pow(pions[0]->mass(), 2), 3)*(1 - 3.3*(std::pow(massA1, 2) - 9*std::pow(pions[0]->mass(), 2)) + 5.8*std::pow(std::pow(massA1, 2) - 9*std::pow(pions[0]->mass(),2), 2)));

			// Gamma funtions necessary for Breit Wigner resonances
			double gammaA1 = gammaA10*gvalueQ/gvalueA1;
			double gammaRho1 = gammaRho10*massRho1/std::sqrt(std::pow(valueQ, 2))*std::pow(0.5*std::sqrt(std::pow(valueQ, 2) - 4*std::pow(pions[0]->mass(), 2)) / (0.5*std::sqrt(std::pow(massRho1, 2) - 4*std::pow(pions[0]->mass(), 2))), 3);			
			double gammaRho2 = gammaRho20*massRho2/std::sqrt(std::pow(valueQ, 2))*std::pow(0.5*std::sqrt(std::pow(valueQ, 2) - 4*std::pow(pions[0]->mass(), 2)) / (0.5*std::sqrt(std::pow(massRho2, 2) - 4*std::pow(pions[0]->mass(), 2))), 3);			

			// Breit Wigner fuctions for A1
			std::vector<double> RealBWa1;
			RealBWa1.push_back(std::pow(massA1, 2)*(std::pow(massA1, 2) - valuesS[0])/(std::pow(std::pow(massA1, 2) - valuesS[0], 2) + std::pow(massA1, 2)*std::pow(gammaA1, 2)));
			RealBWa1.push_back(std::pow(massA1, 2)*(std::pow(massA1, 2) - valuesS[1])/(std::pow(std::pow(massA1, 2) - valuesS[1], 2) + std::pow(massA1, 2)*std::pow(gammaA1, 2)));
			RealBWa1.push_back(std::pow(massA1, 2)*(std::pow(massA1, 2) - std::pow(valueQ, 2))/(std::pow(std::pow(massA1, 2) -  std::pow(valueQ, 2), 2) + std::pow(massA1, 2)*std::pow(gammaA1, 2)));	
			std::vector<double> ImBWa1;
			ImBWa1.push_back(std::pow(massA1, 3)*gammaA1/(std::pow(std::pow(massA1, 2) - valuesS[0], 2) + std::pow(massA1, 2)*std::pow(gammaA1, 2)));
			ImBWa1.push_back(std::pow(massA1, 3)*gammaA1/(std::pow(std::pow(massA1, 2) - valuesS[1], 2) + std::pow(massA1, 2)*std::pow(gammaA1, 2)));			
			ImBWa1.push_back(std::pow(massA1, 3)*gammaA1/(std::pow(std::pow(massA1, 2) - std::pow(valueQ, 2), 2) + std::pow(massA1, 2)*std::pow(gammaA1, 2)));

			// Breit Wigner fuctions for rho1
			std::vector<double> RealBWrho1;
			RealBWrho1.push_back(std::pow(massRho1, 2)*(std::pow(massRho1, 2) - valuesS[0])/(std::pow(std::pow(massRho1, 2) - valuesS[0], 2) + std::pow(massRho1, 2)*std::pow(gammaRho1, 2)));
			RealBWrho1.push_back(std::pow(massRho1, 2)*(std::pow(massRho1, 2) - valuesS[1])/(std::pow(std::pow(massRho1, 2) - valuesS[1], 2) + std::pow(massRho1, 2)*std::pow(gammaRho1, 2)));
			RealBWrho1.push_back(std::pow(massRho1, 2)*(std::pow(massRho1, 2) - std::pow(valueQ, 2))/(std::pow(std::pow(massRho1, 2) - std::pow(valueQ, 2), 2) + std::pow(massRho1, 2)*std::pow(gammaRho1, 2)));
			std::vector<double> ImBWrho1;
			ImBWrho1.push_back(std::pow(massRho1, 3)*gammaRho1/(std::pow(std::pow(massRho1, 2) - valuesS[0], 2) + std::pow(massRho1, 2)*std::pow(gammaRho1, 2)));
			ImBWrho1.push_back(std::pow(massRho1, 3)*gammaRho1/(std::pow(std::pow(massRho1, 2) - valuesS[1], 2) + std::pow(massRho1, 2)*std::pow(gammaRho1, 2)));
			ImBWrho1.push_back(std::pow(massRho1, 3)*gammaRho1/(std::pow(std::pow(massRho1, 2) - std::pow(valueQ, 2), 2) + std::pow(massRho1, 2)*std::pow(gammaRho1, 2)));

			// Breit Wigner fuctions for rho2
			std::vector<double> RealBWrho2;
			RealBWrho2.push_back(std::pow(massRho2, 2)*(std::pow(massRho2, 2) - valuesS[0])/(std::pow(std::pow(massRho2, 2) - valuesS[0], 2) + std::pow(massRho2, 2)*std::pow(gammaRho2, 2)));
			RealBWrho2.push_back(std::pow(massRho2, 2)*(std::pow(massRho2, 2) - valuesS[1])/(std::pow(std::pow(massRho2, 2) - valuesS[1], 2) + std::pow(massRho2, 2)*std::pow(gammaRho2, 2)));
			RealBWrho2.push_back(std::pow(massRho2, 2)*(std::pow(massRho2, 2) - std::pow(valueQ, 2))/(std::pow(std::pow(massRho2, 2) - std::pow(valueQ, 2), 2) + std::pow(massRho2, 2)*std::pow(gammaRho2, 2)));
			std::vector<double> ImBWrho2;
			ImBWrho2.push_back(std::pow(massRho2, 3)*gammaRho2/(std::pow(std::pow(massRho2, 2) - valuesS[0], 2) + std::pow(massRho2, 2)*std::pow(gammaRho2, 2)));
			ImBWrho2.push_back(std::pow(massRho2, 3)*gammaRho2/(std::pow(std::pow(massRho2, 2) - valuesS[1], 2) + std::pow(massRho2, 2)*std::pow(gammaRho2, 2)));
			ImBWrho2.push_back(std::pow(massRho2, 3)*gammaRho2/(std::pow(std::pow(massRho2, 2) - std::pow(valueQ, 2), 2) + std::pow(massRho2, 2)*std::pow(gammaRho2, 2)));	

			// Breit Wigner fuctions for taking into account the contribution from two rho mesons, rho1 and rho2
			std::vector<double> RealBrho1;
			std::vector<double> ImBrho1;
			if(RealBWrho1.size() != 0){
				for(unsigned int iMinv=0; iMinv < RealBWrho1.size(); iMinv++){
					double beta = -0.145;
					RealBrho1.push_back((RealBWrho1[iMinv] + beta*RealBWrho2[iMinv])/(1.0 + beta));
					ImBrho1.push_back((ImBWrho1[iMinv] + beta*ImBWrho2[iMinv])/(1.0 + beta));
				}
			}
			// Form factors
			double fpi = 0.093;
			double RealformFactor1 =- 2*std::sqrt(2)/(3.0*fpi)*ImBWa1[2]*ImBrho1[1];
			double ImformFactor1 =- 2*std::sqrt(2)/(3.0*fpi)*RealBWa1[2]*RealBrho1[1];
			double RealformFactor2 =- 2*std::sqrt(2)/(3.0*fpi)*ImBWa1[2]*ImBrho1[0];
			double ImformFactor2 =- 2*std::sqrt(2)/(3.0*fpi)*RealBWa1[2]*RealBrho1[0];

			// Structure functions
			double structureFWA = -valueV1V1*(std::pow(RealformFactor1, 2) + std::pow(ImformFactor1, 2)) - valueV2V2*(std::pow(RealformFactor2, 2) + std::pow(ImformFactor2, 2)) - 2*valueV1V2*(RealformFactor1*RealformFactor2 + ImformFactor1*ImformFactor2);			

			double structureFWC = -(valueV1V1 + 2*valueH)*(std::pow(RealformFactor1, 2) + std::pow(ImformFactor1, 2)) - (valueV2V2 + 2*valueH)*(std::pow(RealformFactor2, 2) + std::pow(ImformFactor2, 2)) - (2*valueV1V2 - 4*valueH)*(RealformFactor1*RealformFactor2 + ImformFactor1*ImformFactor2);		

			double structureFWD = - std::sqrt(valueH)*(2*std::sqrt(-valueV1V1 - valueH)*(std::pow(RealformFactor1, 2) + std::pow(ImformFactor1, 2)) - 2*std::sqrt(-valueV2V2) - valueH*(std::pow(RealformFactor2, 2) + std::pow(ImformFactor2, 2)) + 1.0/(std::pow(valueQ, 2)*std::sqrt(valueH0))*(std::pow(valueQ, 2) - std::pow(pions[0]->mass(),2) + valuesS[2])*(valuesS[0] - valuesS[1])*(RealformFactor1*RealformFactor2 + ImformFactor1*ImformFactor2));			

			double structureFWE = 3*std::sqrt(valueH*valueH0)*(RealformFactor1*ImformFactor2 + ImformFactor1*RealformFactor2);

			// f and g functions for the omega calculation w=f/g
			double functionF = 1.0/3*((2 + std::pow((*tau)->p4.mass(),2)/std::pow(valueQ, 2)) + 0.5*(3*std::pow(product.m_a1CosBeta[*tau], 2) - 1)*valueU)*structureFWA - 0.5*std::pow(product.m_a1SinBeta[*tau], 2)*(std::pow(product.m_a1CosGamma[*tau], 2) - std::pow(product.m_a1SinGamma[*tau], 2))*valueU*structureFWC + 0.5*std::pow(product.m_a1SinBeta[*tau], 2)*2*product.m_a1CosGamma[*tau]*product.m_a1SinGamma[*tau]*valueU*structureFWD + product.m_a1CosPsi[*tau]*product.m_a1CosBeta[*tau]*structureFWE;

			double functionG = 1.0/3*(product.m_a1CosTheta[*tau]*(std::pow((*tau)->p4.mass(), 2)/std::pow(valueQ, 2) - 2) - 1.0/3*(3*product.m_a1CosBeta[*tau] - 1)*valueV)*structureFWA + 0.5*std::pow(product.m_a1SinBeta[*tau], 2)*(std::pow(product.m_a1CosGamma[*tau], 2) - std::pow(product.m_a1SinGamma[*tau], 2))*valueV*structureFWC + 0.5*std::pow(product.m_a1SinBeta[*tau], 2)*(std::pow(product.m_a1CosGamma[*tau], 2) - std::pow(product.m_a1SinGamma[*tau], 2))*valueV*structureFWD - product.m_a1CosBeta[*tau]*(product.m_a1CosTheta[*tau]* product.m_a1CosPsi[*tau] +  product.m_a1CosTheta[*tau]*product.m_a1SinPsi[*tau]*std::sqrt(std::pow((*tau)->p4.mass(), 2)/std::pow(valueQ, 2)))*structureFWE;

			product.m_a1optimumVariableSimpleFit[*tau] = (functionG != 0.0 ? functionF / functionG :  0.0);

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
				product.m_tauPolarisationDiscriminatorSimpleFit = SafeMap::GetWithDefault(product.m_a1optimumVariableSimpleFit, static_cast<KLepton*>(*tau), DefaultValues::UndefinedDouble);
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
