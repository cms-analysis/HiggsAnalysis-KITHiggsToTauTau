
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
			JetCorrectorParameters const * jetCorPar = new JetCorrectorParameters(uncertaintyFile, uncertainty);
			JetCorParMap[individualUncertainty] = jetCorPar;

			JetCorrectionUncertainty * jecUnc(new JetCorrectionUncertainty(*JetCorParMap[individualUncertainty]));
			JetUncMap[individualUncertainty] = jecUnc;

			// add quantities to event
			// TODO: implement njetspt30, mjj, jdeta and njetingap (and nbtag?)
			std::string shift = settings.GetJetEnergyCorrectionUncertaintyShift() > 0.0 ? "up" : "down";
			std::string mjjQuantity = "mjj_" + uncertainty + "_" + shift;
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(mjjQuantity, [individualUncertainty](spec_event_type const& event, spec_product_type const& product)
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).at(individualUncertainty);
				if (shiftedJets.size() > 1)
				{
					return (shiftedJets.at(0)->p4 + shiftedJets.at(1)->p4).mass();
				}
				else
				{
					return DefaultValues::UndefinedFloat;
				}
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
		for (auto const& uncertainty : individualUncertaintyEnums)
		{
			for (std::vector<KJet*>::iterator jet = shiftedJets.begin(); jet != shiftedJets.end(); ++jet)
			{
				double unc = 0;

				if (std::abs((*jet)->p4.Eta()) < 5.2 && (*jet)->p4.Pt() > 9.){
					JetUncMap.at(uncertainty)->setJetEta((*jet)->p4.Eta());
					JetUncMap.at(uncertainty)->setJetPt((*jet)->p4.Pt());
					unc = JetUncMap.at(uncertainty)->getUncertainty(true);
				}

				(*jet)->p4 = (*jet)->p4 * (1 + unc * settings.GetJetEnergyCorrectionUncertaintyShift());
			}
			// sort vectors of corrected jets by pt
			std::sort(shiftedJets.begin(), shiftedJets.end(),
					  [](KJet* jet1, KJet* jet2) -> bool
					  { return jet1->p4.Pt() > jet2->p4.Pt(); });

			(spec_product.m_correctedJetsBySplitUncertainty)[uncertainty] = shiftedJets;
		}
	}
}

