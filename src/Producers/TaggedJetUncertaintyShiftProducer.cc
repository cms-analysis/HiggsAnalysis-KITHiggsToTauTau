
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TaggedJetUncertaintyShiftProducer.h"

std::string TaggedJetUncertaintyShiftProducer::GetProducerId() const
{
	return "TaggedJetUncertaintyShiftProducer";
}

void TaggedJetUncertaintyShiftProducer::Init(setting_type const& settings)
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

		// create uncertainty map (only if shifts are to be applied)
		if (settings.GetJetEnergyCorrectionSplitUncertainty()
			&& settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0
			&& individualUncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
		{
			JetCorrectorParameters const * jetCorPar = new JetCorrectorParameters(uncertaintyFile, uncertainty);
			JetCorParMap[individualUncertainty] = jetCorPar;

			JetCorrectionUncertainty * jecUnc(new JetCorrectionUncertainty(*JetCorParMap[individualUncertainty]));
			JetUncMap[individualUncertainty] = jecUnc;
		}

		// add quantities to event
		std::string njetsQuantity = "njetspt30_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(njetsQuantity, [individualUncertainty](event_type const& event, product_type const& product)
		{
			int nJetsPt30 = 0;
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				nJetsPt30 = KappaProduct::GetNJetsAbovePtThreshold((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second, 30.0);
			}
			return nJetsPt30;
		});

		std::string mjjQuantity = "mjj_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(mjjQuantity, [individualUncertainty](event_type const& event, product_type const& product)
		{
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? (shiftedJets.at(0)->p4 + shiftedJets.at(1)->p4).mass() : -11.f;
			}
			return -11.f;
		});

		std::string jdetaQuantity = "jdeta_" + uncertainty;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(jdetaQuantity, [individualUncertainty](event_type const& event, product_type const& product)
		{
			float jdeta = -1;
			if ((product.m_correctedJetsBySplitUncertainty).find(individualUncertainty) != (product.m_correctedJetsBySplitUncertainty).end())
			{
				std::vector<KJet*> shiftedJets = (product.m_correctedJetsBySplitUncertainty).find(individualUncertainty)->second;
				return shiftedJets.size() > 1 ? std::abs(shiftedJets.at(0)->p4.Eta() - shiftedJets.at(1)->p4.Eta()) : -1;
			}
			return jdeta;
		});
	}
}

void TaggedJetUncertaintyShiftProducer::Produce(event_type const& event, product_type& product,
		setting_type const& settings) const
{
	// only do all of this if uncertainty shifts should be applied
	if (settings.GetJetEnergyCorrectionSplitUncertainty() && settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0)
	{
		// shift copies of previously corrected jets
		std::vector<double> closureUncertainty((product.m_correctedTaggedJets).size(), 0.);
		for (auto const& uncertainty : individualUncertaintyEnums)
		{

			// construct copies of jets in order not to modify actual (corrected) jets
			std::vector<KJet*> copiedJets;
			for (typename std::vector<std::shared_ptr<KJet> >::iterator jet = (product.m_correctedTaggedJets).begin();
				 jet != (product.m_correctedTaggedJets).end(); ++jet)
			{
				copiedJets.push_back(new KJet(*(jet->get())));
			}

			unsigned iJet = 0;
			for (std::vector<KJet*>::iterator jet = copiedJets.begin(); jet != copiedJets.end(); ++jet, ++iJet)
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
			std::sort(copiedJets.begin(), copiedJets.end(),
					  [](KJet* jet1, KJet* jet2) -> bool
					  { return jet1->p4.Pt() > jet2->p4.Pt(); });

			// TODO: create new vector with shifted jets that pass ID as in ValidJetsProducer
			//       move criteria to separate function in ValidJetsProducer and call function here?
			std::vector<KJet*> shiftedJets = copiedJets;

			(product.m_correctedJetsBySplitUncertainty)[uncertainty] = shiftedJets;
		}
	}
}

