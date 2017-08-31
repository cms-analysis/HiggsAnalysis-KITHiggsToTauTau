
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidGenTausProducer.h"


void HttValidGenTausProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	m_deltaR = 0.3; //todo: read in from settings
	m_validateMatching = true;
	m_swapIfNecessary = true;
	return;
}

void HttValidGenTausProducer::Produce(event_type const& event, product_type& product,
									  setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_genTaus);
	
	if (event.m_genTaus->empty()) return; // no genTaus, nothing to do

	CopyVectors(event, product, settings, metadata);
	SortVectors(event, product, settings, metadata);
	if (m_validateMatching)
		ValidateMatching(event, product, settings, metadata);

	return;
}

void HttValidGenTausProducer::CopyVectors(event_type const& event, product_type& product,
		setting_type const& settings, metadata_type const& metadata) const
{
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
}

void HttValidGenTausProducer::SortVectors(event_type const& event, product_type& product,
		setting_type const& settings, metadata_type const& metadata) const
{
	// count to determine the decay channel according to generator Taus
	int nElectrons = product.m_validGenTausToElectrons.size();
	int nMuons = product.m_validGenTausToMuons.size();
	int nHadrons = product.m_validGenTausToTaus.size();

	auto ptSorter = [](const KGenTau * a, const KGenTau * b) -> bool { return a->visible.p4.Pt() > b->visible.p4.Pt(); };
	std::sort(product.m_ptOrderedGenTaus.begin(), product.m_ptOrderedGenTaus.end(), ptSorter);
	std::sort(product.m_validGenTausToElectrons.begin(), product.m_validGenTausToElectrons.end(), ptSorter);
	std::sort(product.m_validGenTausToMuons.begin(), product.m_validGenTausToMuons.end(), ptSorter);
	std::sort(product.m_validGenTausToTaus.begin(), product.m_validGenTausToTaus.end(), ptSorter);
	std::sort(product.m_flavourOrderedGenTaus.begin(), product.m_flavourOrderedGenTaus.end(), ptSorter);
	auto chargeSorter = [](const KGenTau * a, const KGenTau * b) -> bool { return a->charge() > b->charge(); };
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
			std::cout << "Event Category does not match generated Taus"; //Todo: do something with this insight
	}
	return;
}

void HttValidGenTausProducer::ValidateMatching(event_type const& event, product_type& product,
		setting_type const& settings, metadata_type const& metadata) const
{
	if (DoesGenRecoMatch(product.m_ptOrderedLeptons, product.m_ptOrderedGenTaus)) {}  // do something
	if (DoesGenRecoMatch(product.m_flavourOrderedLeptons , product.m_flavourOrderedGenTaus)) {} // do something
	if (DoesGenRecoMatch(product.m_chargeOrderedLeptons, product.m_chargeOrderedGenTaus)) {}  // do something
	if (DoesGenRecoMatch(product.m_validElectrons, product.m_validGenTausToElectrons)) {}  // do something
	if (DoesGenRecoMatch(product.m_validMuons, product.m_validGenTausToMuons)) {}  // do something
	if (DoesGenRecoMatch(product.m_validTaus, product.m_validGenTausToTaus)) {}  // do something

	// todo: try to swap leptons in genTau vectors and see if this better to reco.
	// flag: m_swapIfNecessary

	return;
}

