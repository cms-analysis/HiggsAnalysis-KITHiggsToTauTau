
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TaggedJetUncertaintyShiftProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"


std::string TaggedJetUncertaintyShiftProducer::GetProducerId() const
{
	return "TaggedJetUncertaintyShiftProducer";
}

void TaggedJetUncertaintyShiftProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	uncertaintyFile = settings.GetJetEnergyCorrectionUncertaintyParameters();
	individualUncertainties = settings.GetJetEnergyCorrectionSplitUncertaintyParameterNames();

	// make sure the necessary parameters are configured
	assert(uncertaintyFile != "");
	assert(individualUncertainties.size() > 0);

	jetIDVersion = KappaEnumTypes::ToJetIDVersion(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetJetIDVersion())));
	jetID = KappaEnumTypes::ToJetID(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetJetID())));

	// implementation not nice at the moment. feel free to improve it :)
	lowerPtCuts = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetJetLowerPtCuts()));
	upperAbsEtaCuts = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetJetUpperAbsEtaCuts()));

	if (lowerPtCuts.size() > 1)
		LOG(FATAL) << "TaggedJetUncertaintyShiftProducer: lowerPtCuts.size() = " << lowerPtCuts.size() << ". Current implementation requires it to be <= 1.";
	if (upperAbsEtaCuts.size() > 1)
		LOG(FATAL) << "TaggedJetUncertaintyShiftProducer: upperAbsEtaCuts.size() = " << upperAbsEtaCuts.size() << ". Current implementation requires it to be <= 1.";
	
	// some inputs needed for b-tagging
	std::map<std::string, std::vector<float> > bTagWorkingPointsTmp = Utility::ParseMapTypes<std::string, float>(
			Utility::ParseVectorToMap(settings.GetBTaggerWorkingPoints())
	);

	// initialize b-tag scale factor class only if shifts are to be applied
	if (settings.GetJetEnergyCorrectionSplitUncertainty()
		&& settings.GetAbsJetEnergyCorrectionSplitUncertaintyShift() != 0.0
		&& settings.GetUseJECShiftsForBJets())
	{
		m_bTagSf = BTagSF(settings.GetBTagScaleFactorFile(), settings.GetBTagEfficiencyFile());
		m_bTagWorkingPoint = bTagWorkingPointsTmp.begin()->second.at(0);
		if (settings.GetApplyBTagSF() && !settings.GetInputIsData())
		{
			m_bTagSFMethod = KappaEnumTypes::ToBTagScaleFactorMethod(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetBTagSFMethod())));
			m_bTagSf.initBtagwp(bTagWorkingPointsTmp.begin()->first);
		}
	}

	// settings used by the ValidJetsProducers
	puJetIdsByIndex = Utility::ParseMapTypes<size_t, std::string>(
			Utility::ParseVectorToMap(settings.GetPuJetIDs()),
			puJetIdsByHltName
	);
	jetTaggerLowerCutsByTaggerName = Utility::ParseMapTypes<std::string, float>(
			Utility::ParseVectorToMap(settings.GetJetTaggerLowerCuts()),
			jetTaggerLowerCutsByTaggerName
	);
	jetTaggerUpperCutsByTaggerName = Utility::ParseMapTypes<std::string, float>(
			Utility::ParseVectorToMap(settings.GetJetTaggerUpperCuts()),
			jetTaggerUpperCutsByTaggerName
	);
	
	// settings used by the RecoJetGenParticleMatchingProducer
	m_jetMatchingAlgorithm = RecoJetGenParticleMatchingProducer::ToJetMatchingAlgorithm(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetJetMatchingAlgorithm())));
	
	for (std::string const& uncertainty : individualUncertainties)
	{
		// only do string comparison once per uncertainty
		HttEnumTypes::JetEnergyUncertaintyShiftName individualUncertainty = HttEnumTypes::ToJetEnergyUncertaintyShiftName(uncertainty);
		if (individualUncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::NONE)
			continue;
		individualUncertaintyEnums.push_back(individualUncertainty);

		// create uncertainty map (only if shifts are to be applied)
		if (settings.GetJetEnergyCorrectionSplitUncertainty()
			&& settings.GetAbsJetEnergyCorrectionSplitUncertaintyShift() != 0.0
			&& individualUncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
		{
			JetCorrectorParameters jetCorPar(uncertaintyFile, uncertainty);
			jetUncMap[individualUncertainty] = new JetCorrectionUncertainty(jetCorPar);
		}

		// add quantities to event
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetspt30_"+uncertainty+"Up", [individualUncertainty](event_type const& event, product_type const& product) -> int
		{
			int nJetsPt30 = DefaultValues::UndefinedInt;
			if ((product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyUp).end())
			{
				nJetsPt30 = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty)->second, 30.0);
			}
			return nJetsPt30;
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetspt30_"+uncertainty+"Down", [individualUncertainty](event_type const& event, product_type const& product) -> int
		{
			int nJetsPt30 = DefaultValues::UndefinedInt;
			if ((product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyDown).end())
			{
				nJetsPt30 = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty)->second, 30.0);
			}
			return nJetsPt30;
		});

		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mjj_"+uncertainty+"Up", [individualUncertainty](event_type const& event, product_type const& product) -> float
		{
			if ((product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyUp).end())
			{
				std::vector<KJet> const& shiftedJets = (product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? (shiftedJets.at(0).p4 + shiftedJets.at(1).p4).mass() : DefaultValues::UndefinedFloat;
			}
			return DefaultValues::UndefinedFloat;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mjj_"+uncertainty+"Down", [individualUncertainty](event_type const& event, product_type const& product) -> float
		{
			if ((product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyDown).end())
			{
				std::vector<KJet> const& shiftedJets = (product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? (shiftedJets.at(0).p4 + shiftedJets.at(1).p4).mass() : DefaultValues::UndefinedFloat;
			}
			return DefaultValues::UndefinedFloat;
		});

		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdeta_"+uncertainty+"Up", [individualUncertainty](event_type const& event, product_type const& product)
		{
			if ((product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyUp).end())
			{
				std::vector<KJet> const& shiftedJets = (product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? std::abs(shiftedJets.at(0).p4.Eta() - shiftedJets.at(1).p4.Eta()) : DefaultValues::UndefinedFloat;
			}
			return DefaultValues::UndefinedFloat;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdeta_"+uncertainty+"Down", [individualUncertainty](event_type const& event, product_type const& product)
		{
			if ((product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyDown).end())
			{
				std::vector<KJet> const& shiftedJets = (product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? std::abs(shiftedJets.at(0).p4.Eta() - shiftedJets.at(1).p4.Eta()) : DefaultValues::UndefinedFloat;
			}
			return DefaultValues::UndefinedFloat;
		});

		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdphi_"+uncertainty+"Up", [individualUncertainty](event_type const& event, product_type const& product) -> float
		{
			if ((product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyUp).end())
			{
				std::vector<KJet> const& shiftedJets = (product.m_correctedJetsBySplitUncertaintyUp).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? ROOT::Math::VectorUtil::DeltaPhi(shiftedJets.at(0).p4, shiftedJets.at(1).p4) * (shiftedJets.at(0).p4.Eta() > 0.0 ? 1.0 : -1.0) : DefaultValues::UndefinedFloat;
			}
			return DefaultValues::UndefinedFloat;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdphi_"+uncertainty+"Down", [individualUncertainty](event_type const& event, product_type const& product) -> float
		{
			if ((product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertaintyDown).end())
			{
				std::vector<KJet> const& shiftedJets = (product.m_correctedJetsBySplitUncertaintyDown).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? ROOT::Math::VectorUtil::DeltaPhi(shiftedJets.at(0).p4, shiftedJets.at(1).p4) * (shiftedJets.at(0).p4.Eta() > 0.0 ? 1.0 : -1.0) : DefaultValues::UndefinedFloat;
			}
			return DefaultValues::UndefinedFloat;
		});

		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nbtag_"+uncertainty+"Up", [individualUncertainty](event_type const& event, product_type const& product) -> int
		{
			int nbtag = DefaultValues::UndefinedInt;
			if ((product.m_correctedBTaggedJetsBySplitUncertaintyUp).find(individualUncertainty) != (product.m_correctedBTaggedJetsBySplitUncertaintyUp).end())
			{
				nbtag = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedBTaggedJetsBySplitUncertaintyUp).find(individualUncertainty)->second, 20.0);
			}
			return nbtag;
		});
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nbtag_"+uncertainty+"Down", [individualUncertainty](event_type const& event, product_type const& product) -> int
		{
			int nbtag = DefaultValues::UndefinedInt;
			if ((product.m_correctedBTaggedJetsBySplitUncertaintyDown).find(individualUncertainty) != (product.m_correctedBTaggedJetsBySplitUncertaintyDown).end())
			{
				nbtag = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedBTaggedJetsBySplitUncertaintyDown).find(individualUncertainty)->second, 20.0);
			}
			return nbtag;
		});
	}
}

void TaggedJetUncertaintyShiftProducer::Produce(event_type const& event, product_type& product,
		setting_type const& settings, metadata_type const& metadata) const
{
	ProduceShift(event, product, settings, metadata, true,
	             product.m_correctedJetsBySplitUncertaintyUp,
	             product.m_correctedBTaggedJetsBySplitUncertaintyUp);
	
	ProduceShift(event, product, settings, metadata, false,
	             product.m_correctedJetsBySplitUncertaintyDown,
	             product.m_correctedBTaggedJetsBySplitUncertaintyDown);
}

void TaggedJetUncertaintyShiftProducer::ProduceShift(event_type const& event, product_type& product,
		setting_type const& settings, metadata_type const& metadata, bool shiftUp,
		std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>>& correctedJetsBySplitUncertainty,
		std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>>& correctedBTaggedJetsBySplitUncertainty) const
{
	// only do all of this if uncertainty shifts should be applied
	if (settings.GetJetEnergyCorrectionSplitUncertainty() && settings.GetAbsJetEnergyCorrectionSplitUncertaintyShift() != 0.0)
	{
		// shift copies of previously corrected jets
		std::vector<double> closureUncertainty((product.m_correctedTaggedJets).size(), 0.);
		for (HttEnumTypes::JetEnergyUncertaintyShiftName const& uncertainty : individualUncertaintyEnums)
		{

			// construct copies of jets in order not to modify actual (corrected) jets
			std::vector<KJet> copiedJets;
			for (typename std::vector<std::shared_ptr<KJet> >::iterator jet = (product.m_correctedTaggedJets).begin();
				 jet != (product.m_correctedTaggedJets).end(); ++jet)
			{
				copiedJets.push_back(KJet(*(jet->get())));
			}

			unsigned iJet = 0;
			for (std::vector<KJet>::iterator jet = copiedJets.begin(); jet != copiedJets.end(); ++jet, ++iJet)
			{
				double unc = 0;

				if (std::abs(jet->p4.Eta()) < 5.2 && jet->p4.Pt() > 9.0 && uncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
				{
					JetCorrectionUncertainty* tmpUncertainty = jetUncMap.at(uncertainty);
					tmpUncertainty->setJetEta(jet->p4.Eta());
					tmpUncertainty->setJetPt(jet->p4.Pt());
					unc = tmpUncertainty->getUncertainty(true);
				}
				closureUncertainty.at(iJet) = closureUncertainty.at(iJet) + unc*unc;

				if (uncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
				{
					unc = std::sqrt(closureUncertainty.at(iJet));
				}
				
				jet->p4 = jet->p4 * (1.0 + (shiftUp ? 1.0 : -1.0) * unc * settings.GetAbsJetEnergyCorrectionSplitUncertaintyShift());
			}
			
			// sort vectors of shifted jets by pt
			std::sort(copiedJets.begin(), copiedJets.end(),
					  [](KJet const& jet1, KJet const& jet2) -> bool
					  { return jet1.p4.Pt() > jet2.p4.Pt(); });

			// create new vector with shifted jets that pass ID as in ValidJetsProducer
			std::vector<KJet> shiftedJets;
			std::vector<KJet> shiftedBTaggedJets;
			for (std::vector<KJet>::iterator jet = copiedJets.begin(); jet != copiedJets.end(); ++jet)
			{
				bool validJet = true;

				// passed jet id?
				validJet = validJet && ValidJetsProducer::passesJetID(&*(jet), jetIDVersion, jetID);

				// kinematic cuts
				// implementation not nice at the moment. feel free to improve it :)
				for (std::map<std::string, std::vector<float> >::const_iterator lowerPtCut = lowerPtCuts.begin(); lowerPtCut != lowerPtCuts.end() && validJet; ++lowerPtCut)
					if (jet->p4.Pt() < *std::max_element(lowerPtCut->second.begin(), lowerPtCut->second.end()))
						validJet = false;
				for (std::map<std::string, std::vector<float> >::const_iterator upperAbsEtaCut = upperAbsEtaCuts.begin(); upperAbsEtaCut != upperAbsEtaCuts.end() && validJet; ++upperAbsEtaCut)
					if (std::abs(jet->p4.Eta()) > *std::min_element(upperAbsEtaCut->second.begin(), upperAbsEtaCut->second.end()))
						validJet = false;

				// remove leptons from list of jets via simple DeltaR isolation
				for (std::vector<KLepton*>::const_iterator lepton = product.m_validLeptons.begin(); validJet && lepton != product.m_validLeptons.end(); ++lepton)
					validJet = validJet && ROOT::Math::VectorUtil::DeltaR(jet->p4, (*lepton)->p4) > settings.GetJetLeptonLowerDeltaRCut();
				
				// check possible analysis-specific criteria
				validJet = validJet && HttValidTaggedJetsProducer::AdditionalCriteriaStatic(&(*jet),
				                                                                            puJetIdsByIndex, puJetIdsByHltName,
				                                                                            jetTaggerLowerCutsByTaggerName, jetTaggerUpperCutsByTaggerName,
				                                                                            event, product, settings, metadata);
				if (validJet)
				{
					KGenParticle* matchedParticle = RecoJetGenParticleMatchingProducer::Match(event, product, settings, static_cast<KLV*>(&(*jet)), m_jetMatchingAlgorithm);
					if (((matchedParticle == nullptr) && settings.GetInvalidateNonGenParticleMatchingRecoJets()) ||
						((matchedParticle != nullptr) && settings.GetInvalidateGenParticleMatchingRecoJets()))
						validJet = false;
				}
				
				if (validJet) shiftedJets.push_back(*jet);

				if (settings.GetUseJECShiftsForBJets())
				{
					// determine if jet is btagged
					bool validBJet = true;
					KJet tjet = *(static_cast<KJet*>(&(*jet)));

					float combinedSecondaryVertex = tjet.getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);

					if (combinedSecondaryVertex < m_bTagWorkingPoint ||
						std::abs(tjet.p4.eta()) > settings.GetBTaggedJetAbsEtaCut())
						validBJet = false;

					//entry point for Scale Factor (SF) of btagged jets
					if (settings.GetApplyBTagSF() && !settings.GetInputIsData())
					{
						//https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#2a_Jet_by_jet_updating_of_the_b
						if (m_bTagSFMethod == KappaEnumTypes::BTagScaleFactorMethod::PROMOTIONDEMOTION)
						{
						
							int jetHadronFlavor = tjet.hadronFlavour;
							int jetPartonFlavor = tjet.partonFlavour;
							int jetflavor = jetHadronFlavor + (jetHadronFlavor == 0) * (jetPartonFlavor);

							unsigned int btagSys = BTagSF::kNo;
							unsigned int bmistagSys = BTagSF::kNo;

							bool taggedBefore = validBJet;
							validBJet = m_bTagSf.isbtagged(
									tjet.p4.pt(),
									tjet.p4.eta(),
									combinedSecondaryVertex,
									jetflavor,
									btagSys,
									bmistagSys,
									settings.GetYear(),
									m_bTagWorkingPoint
							);
							
							if (taggedBefore != validBJet) LOG_N_TIMES(20, DEBUG) << "Promoted/demoted : " << validBJet;
						}
						//todo
						else if (m_bTagSFMethod == KappaEnumTypes::BTagScaleFactorMethod::OTHER) {}
					}

					if (validBJet) shiftedBTaggedJets.push_back(tjet);
				}
			}
			
			correctedJetsBySplitUncertainty[uncertainty] = shiftedJets;
			correctedBTaggedJetsBySplitUncertainty[uncertainty] = shiftedBTaggedJets;
		}
	}
}

