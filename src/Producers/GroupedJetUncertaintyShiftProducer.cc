
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GroupedJetUncertaintyShiftProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"


GroupedJetUncertaintyShiftProducer::~GroupedJetUncertaintyShiftProducer()
{
}

std::string GroupedJetUncertaintyShiftProducer::GetProducerId() const
{
	return "GroupedJetUncertaintyShiftProducer";
}

void GroupedJetUncertaintyShiftProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	uncertaintyFile = settings.GetJetEnergyCorrectionUncertaintyParameters();
	individualUncertainties = settings.GetJetEnergyCorrectionSplitUncertaintyParameterNames();
	
	// make sure the necessary parameters are configured
	assert(uncertaintyFile != "");

	std::map<std::string, std::vector<float> > m_correlationMapFromSettings;

	m_correlationMapFromSettings = Utility::ParseMapTypes<std::string, float>(Utility::ParseVectorToMap(settings.GetJetEnergyCorrectionCorrelationMap()));

	float correlation = 0;
	if( individualUncertainties.size() > 0){
		for (std::string const& uncertainty : individualUncertainties)
		{
			// only do string comparison once per uncertainty
			HttEnumTypes::JetEnergyUncertaintyShiftName individualUncertainty = HttEnumTypes::ToJetEnergyUncertaintyShiftName(uncertainty);
			
			if (individualUncertainty == HttEnumTypes::JetEnergyUncertaintyShiftName::NONE)
			{
				std::cout << "JetEnergyUncertaintyShift enum not found" << std::endl;
				continue;
			}
			//std::cout << "uncertainty:\t" << uncertainty << std::endl;
			correlation = m_correlationMapFromSettings.at(uncertainty).at(0);

			individualUncertaintyEnumsMap.insert(std::pair<HttEnumTypes::JetEnergyUncertaintyShiftName,float>  (individualUncertainty, correlation));
			std::cout << uncertainty << "   :   " << correlation << std::endl;

			// get the individual uncertainties map from the JEC.txt file.
			if (settings.GetJetEnergyCorrectionSplitUncertainty()
				&& settings.GetAbsJetEnergyCorrectionSplitUncertaintyShift() != 0.0
				&& individualUncertainty != HttEnumTypes::JetEnergyUncertaintyShiftName::Closure)
			{
				JetCorrectorParameters jetCorPar(uncertaintyFile, uncertainty);
				jetUncMap[individualUncertainty] = new JetCorrectionUncertainty(jetCorPar);
			}
		}
	}
}

void GroupedJetUncertaintyShiftProducer::Produce(event_type const& event, product_type& product,
		setting_type const& settings, metadata_type const& metadata) const
{
	// shift copies of previously corrected jets
	// container for the uncertainty values of the groupings for each Jet
	/*	std::map<std::string, std::vector<double>> groupedUncertainties;			
	for (std::pair<std::string, std::vector<std::string>> group : uncertaintyGroupings) 
	{
		// groupedUncertainties.insert(std::pair<std::string, std::vector<double>>(group.first, std::vector<double>((product.m_correctedTaggedJets).size(), 0.))); 
		groupedUncertainties[group.first] = std::vector<double>((product.m_correctedTaggedJets).size(), 0.); 
	}*/
						
	std::vector<KJet*> copiedJets;
	if (settings.GetJetsCorrectedInKappa())
	{
		copiedJets.resize((event.m_tjets)->size());
		size_t jetIndex = 0;
		for (typename std::vector<KJet>::iterator jet = (event.m_tjets)->begin(); jet != (event.m_tjets)->end(); ++jet)
		{
			copiedJets[jetIndex]= &(*jet);
			++jetIndex;
		}
	}
	else
	{
		for (typename std::vector<std::shared_ptr<KJet> >::iterator jet = (product.m_correctedTaggedJets).begin(); jet != (product.m_correctedTaggedJets).end(); ++jet)
		{
			copiedJets.push_back((jet->get()));
		}
	}
	if (settings.GetJetEnergyCorrectionSplitUncertainty() && settings.GetAbsJetEnergyCorrectionSplitUncertaintyShift() != 0.0)
	{
		
		unsigned iJet = 0;
		for (std::vector<KJet*>::iterator jet = copiedJets.begin(); jet != copiedJets.end(); ++jet, ++iJet)
		{
			double unc = 0;
			double groupunc =0;
			double junc = 0;
			product.m_MET_shift.p4 += (*jet)->p4; //Add the original p4 of the jet

			// Get the uncertainty for the jets for each individual and the total uncertainty
			if (std::abs((*jet)->p4.Eta()) < 5.2 && (*jet)->p4.Pt() > 9.0)
			{	
				for ( std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, float>::const_iterator it= individualUncertaintyEnumsMap.begin(); it != individualUncertaintyEnumsMap.end(); ++it)
				{
					// Take the uncertainty from the previously stored jetUncMap and perform the shifts.
					JetCorrectionUncertainty* tmpUncertainty = jetUncMap.at(it->first);
					tmpUncertainty->setJetEta((*jet)->p4.Eta());
					tmpUncertainty->setJetPt((*jet)->p4.Pt());
					unc = tmpUncertainty->getUncertainty(settings.GetIsShiftUp()); //shiftUp==true: Up, ==false:Down
					if(settings.GetIsCorrelated())
					{
						groupunc += it->second *unc*unc;
					}
					else
					{
						groupunc += (1.-it->second) *unc*unc;	
					}
				}
			}

			junc = std::sqrt(groupunc); //uncertainty for a group is the square root

			// apply the shift to the jet four-vector
			(*jet)->p4 = (*jet)->p4 *  (1.0 + (settings.GetIsShiftUp() ? 1.0 : -1.0) * junc * settings.GetAbsJetEnergyCorrectionSplitUncertaintyShift());
			//The shift to be applied to the MET is defined by summing together the 4-vectors of all jets in the collection before and after the JES shifts are applied. The MET shift is then the difference between the 2 resultant 4-vectors
			product.m_MET_shift.p4 -= (*jet)->p4; //substract the p4 of the shifted jet, met 
		}
	}
	/*
	size_t taggedJetIndex = 0;
	for (KJets::iterator taggedJet = (product.m_correctedJetsBySplitUncertainty).begin(); taggedJet != (product.m_correctedJetsBySplitUncertainty).end(); ++taggedJet)
	{
		product.m_correctedTaggedJets[taggedJetIndex] = std::shared_ptr<KJet>(&(*taggedJet));
		++taggedJetIndex;
	}*/
}


