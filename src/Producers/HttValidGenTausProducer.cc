
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidGenTausProducer.h"


void HttValidGenTausProducer::Init(setting_type const& settings)
{
	return;
}

void HttValidGenTausProducer::Produce(event_type const& event, product_type& product,
									  setting_type const& settings) const
{
	if (event.m_genTaus->empty()) return; // nothing to do here

	// copy from event to vectors in product
	for (unsigned int i = 0; i < event.m_genTaus->size(); i++)
	{
		product.m_ptOrderedGenTaus.push_back(&event.m_genTaus->at(i));
		product.m_flavourOrderedGenTaus.push_back(&event.m_genTaus->at(i));
		product.m_chargeOrderedGenTaus.push_back(&event.m_genTaus->at(i));

		if (event.m_genTaus->at(i).isElectronicDecay())
			product.m_validGenTausToElectrons.push_back(&event.m_genTaus->at(i));
		if (event.m_genTaus->at(i).isMuonicDecay())
			product.m_validGenTausToMuons.push_back(&event.m_genTaus->at(i));
		if (event.m_genTaus->at(i).isHadronicDecay())
			product.m_validGenTausToTaus.push_back(&event.m_genTaus->at(i));
	}

	// count to determine the decay channel according to generator Taus
	int nElectrons = product.m_validGenTausToElectrons.size();
	int nMuons = product.m_validGenTausToMuons.size();
	int nHadrons = product.m_validGenTausToTaus.size();

	// sorting
	auto ptSorter = [](const KDataGenTau * a, const KDataGenTau * b) -> bool { return a->p4_vis.Pt() > b->p4_vis.Pt(); };
	std::sort(product.m_ptOrderedGenTaus.begin(), product.m_ptOrderedGenTaus.end(), ptSorter);
	std::sort(product.m_validGenTausToElectrons.begin(), product.m_validGenTausToElectrons.end(), ptSorter);
	std::sort(product.m_validGenTausToMuons.begin(), product.m_validGenTausToMuons.end(), ptSorter);
	std::sort(product.m_validGenTausToTaus.begin(), product.m_validGenTausToTaus.end(), ptSorter);
	std::sort(product.m_flavourOrderedGenTaus.begin(), product.m_flavourOrderedGenTaus.end(), ptSorter);
	auto chargeSorter = [](const KDataGenTau * a, const KDataGenTau * b) -> bool { return a->charge() > b->charge(); };
	std::sort(product.m_chargeOrderedGenTaus.begin(), product.m_chargeOrderedGenTaus.end(), chargeSorter);

	if (event.m_genTaus->size() == 2) // everything else would be ambigious
	{
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::TT) && (nHadrons == 2)) {}
		else if ((product.m_decayChannel == HttEnumTypes::DecayChannel::MM) && (nMuons == 2)) {}
		else if ((product.m_decayChannel == HttEnumTypes::DecayChannel::EE) && (nElectrons == 2)) {}
		else if ((product.m_decayChannel == HttEnumTypes::DecayChannel::MT) && (nMuons == 1) && (nHadrons == 1))
		{
			if (product.m_flavourOrderedGenTaus.at(0)->isMuonicDecay()) {}
			else
				std::reverse(product.m_flavourOrderedGenTaus.begin(), product.m_flavourOrderedGenTaus.end());
		}
		else if ((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) && (nElectrons == 1) && (nHadrons == 1))
		{
			if (product.m_flavourOrderedGenTaus.at(0)->isElectronicDecay()) {}
			else
				std::reverse(product.m_flavourOrderedGenTaus.begin(), product.m_flavourOrderedGenTaus.end());
		}
		else if ((product.m_decayChannel == HttEnumTypes::DecayChannel::EM) && (nElectrons == 1) && (nMuons == 1))
		{
			if (product.m_flavourOrderedGenTaus.at(0)->isElectronicDecay()) {}
			else
				std::reverse(product.m_flavourOrderedGenTaus.begin(), product.m_flavourOrderedGenTaus.end());
		}
		else
			std::cout << "Event Category does not match generated Taus"; //Todo: handle this case
	}

	return;
};

