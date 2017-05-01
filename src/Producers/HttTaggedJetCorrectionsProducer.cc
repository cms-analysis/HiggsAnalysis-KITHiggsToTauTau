
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTaggedJetCorrectionsProducer.h"

std::string HttTaggedJetCorrectionsProducer::GetProducerId() const
{
	return "HttTaggedJetCorrectionsProducer";
}

void HttTaggedJetCorrectionsProducer::Init(setting_type const& settings)
{
	TaggedJetCorrectionsProducer::Init(settings);

	// only do all of this if uncertainty shifts should be applied
	if (settings.GetJetEnergyCorrectionSplitUncertainty() && settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0)
	{
		uncertaintyFile = settings.GetJetEnergyCorrectionSplitUncertaintyParameters();
		individualUncertainties = settings.GetJetEnergyCorrectionSplitUncertaintyParameterNames();

		// make sure the necessary parameters are configured
		assert(uncertaintyFile != "");
		assert(individualUncertainties.size() > 0);

		for (auto const& uncertainty : individualUncertainties)
		{
			// only do string comparison once per uncertainty
			HttEnumTypes::JetEnergyUncertaintyShiftName individualUncertainty = ToJetEnergyUncertaintyShiftName(uncertainty);
			if (individualUncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::NONE)
				continue;
			individualUncertaintyEnums.push_back(individualUncertainty);

			// create uncertainty map
			if (individualUncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
			{
				JetCorrectorParameters const * jetCorPar = new JetCorrectorParameters(uncertaintyFile, uncertainty);
				JetCorParMap[individualUncertainty] = jetCorPar;

				JetCorrectionUncertainty * jecUnc(new JetCorrectionUncertainty(*JetCorParMap[individualUncertainty]));
				JetUncMap[individualUncertainty] = jecUnc;
			}

			// add quantities to event
			// TODO: implement nbtag?
			// TODO: store undefined variables in any case?
			std::string shift = settings.GetJetEnergyCorrectionUncertaintyShift() > 0.0 ? "up" : "down";

			std::string njetsQuantity = "njetspt30_" + uncertainty + "_" + shift;
			LambdaNtupleConsumer<HttTypes>::AddIntQuantity(njetsQuantity, [individualUncertainty](spec_event_type const& event, spec_product_type const& product)
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).at(individualUncertainty);
				return KappaProduct::GetNJetsAbovePtThreshold(shiftedJets, 30.0);
			});

			std::string mjjQuantity = "mjj_" + uncertainty + "_" + shift;
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(mjjQuantity, [individualUncertainty](spec_event_type const& event, spec_product_type const& product)
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).at(individualUncertainty);
				return shiftedJets.size() > 1 ? (shiftedJets.at(0)->p4 + shiftedJets.at(1)->p4).mass() : DefaultValues::UndefinedFloat;
			});

			std::string jdetaQuantity = "jdeta_" + uncertainty + "_" + shift;
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(jdetaQuantity, [individualUncertainty](spec_event_type const& event, spec_product_type const& product)
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).at(individualUncertainty);
				return shiftedJets.size() > 1 ? std::abs(shiftedJets.at(0)->p4.Eta() - shiftedJets.at(1)->p4.Eta()) : -1;
			});

			std::string njetingapQuantity = "njetingap_" + uncertainty + "_" + shift;
			LambdaNtupleConsumer<HttTypes>::AddIntQuantity(njetingapQuantity, [individualUncertainty](spec_event_type const& event, spec_product_type const& product)
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).at(individualUncertainty);
				int nJetInGap = 0;
				float minEta = std::min(shiftedJets.at(0)->p4.Eta(), shiftedJets.at(1)->p4.Eta());
				float maxEta = std::max(shiftedJets.at(0)->p4.Eta(), shiftedJets.at(1)->p4.Eta());
				for (std::vector<KJet*>::const_iterator jet = shiftedJets.begin(); jet != shiftedJets.end(); ++jet)
				{
					if ((*jet) == shiftedJets.at(0) || (*jet) == shiftedJets.at(1))
						continue;
					if (minEta < (*jet)->p4.Eta() && (*jet)->p4.Eta() < maxEta && (*jet)->p4.Pt() > 30.0)
						nJetInGap++;
				}
				return nJetInGap;
			});
		}
	}
}

void HttTaggedJetCorrectionsProducer::Produce(event_type const& event, product_type& product,
		setting_type const& settings, spec_product_type& spec_product) const
{
	TaggedJetCorrectionsProducer::Produce(event, product, settings);
	// only do all of this if uncertainty shifts should be applied
	if (settings.GetJetEnergyCorrectionSplitUncertainty() && settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0)
	{
		// first copy corrected jets
		std::vector<KJet*> shiftedJets;
		for (typename std::vector<std::shared_ptr<KJet> >::iterator jet = (product.m_correctedTaggedJets).begin();
			 jet != (product.m_correctedTaggedJets).end(); ++jet)
		{
			shiftedJets.push_back(jet->get());
		}

		// now shift previously copied corrected jets
		std::vector<double> closureUncertainty(shiftedJets.size(), 0.);
		for (auto const& uncertainty : individualUncertaintyEnums)
		{
			unsigned iJet = 0;
			for (std::vector<KJet*>::iterator jet = shiftedJets.begin(); jet != shiftedJets.end(); ++jet, ++iJet)
			{
				double unc = 0;

				if (std::abs((*jet)->p4.Eta()) < 5.2 && (*jet)->p4.Pt() > 9. && uncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
				{
					JetUncMap.at(uncertainty)->setJetEta((*jet)->p4.Eta());
					JetUncMap.at(uncertainty)->setJetPt((*jet)->p4.Pt());
					unc = JetUncMap.at(uncertainty)->getUncertainty(true);
				}
				closureUncertainty.at(iJet) = closureUncertainty.at(iJet) + unc*unc;

				if (uncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
				{
					unc = std::sqrt(closureUncertainty.at(iJet));
				}

				(*jet)->p4 = (*jet)->p4 * (1 + unc * settings.GetJetEnergyCorrectionUncertaintyShift());
			}
			// sort vectors of shifted jets by pt
			std::sort(shiftedJets.begin(), shiftedJets.end(),
					  [](KJet* jet1, KJet* jet2) -> bool
					  { return jet1->p4.Pt() > jet2->p4.Pt(); });

			// TODO: create new vector with shifted jets that pass ID as in ValidJetsProducer
			//       move criteria to separate function in ValidJetsProducer and call function here?

			(spec_product.m_correctedJetsBySplitUncertainty)[uncertainty] = shiftedJets;
		}
	}
}

