
#include <boost/algorithm/string/predicate.hpp>

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"


void HttLambdaNtupleConsumer::Init(Pipeline<HttTypes> * pset)
{
	// loop over all quantities containing "weight" (case-insensitive)
	// and try to find them in the weights map to write them out
	for(auto const & quantity : pset->GetSettings().GetQuantities()) {
		if(boost::algorithm::icontains(quantity, "weight")) {
			m_valueExtractorMap[quantity] = [&quantity](HttEvent const& event, HttProduct const& product) {
				return Utility::GetWithDefault(product.m_weights, quantity, 1.0);
			};
		}
	}
		m_valueExtractorMap["TauSpinnerWeight"] = [](HttEvent const & event, HttProduct const & product){
if(product.m_tauSpinnerWeight == product.m_tauSpinnerWeight) // Avoiding 'nan' 
	return product.m_tauSpinnerWeight;
else
	{
	// 'Nan' Debug output
	/*std::cout << "\nHiggsPx=" << product.m_genHiggs[0]->p4.Px() << "|";
	std::cout << "HiggsPy=" << product.m_genHiggs[0]->p4.Py() << "|";
	std::cout << "HiggsPz=" << product.m_genHiggs[0]->p4.Pz() << "|";
	std::cout << "HiggsE=" << product.m_genHiggs[0]->p4.e() << "|";
	std::cout << "HiggsPdgId=" << product.m_genHiggs[0]->pdgId() << "|";

	std::cout << "1TauPx=" << product.m_genHiggsDaughters[0][0]->p4.Px() << "|";
	std::cout << "1TauPy=" << product.m_genHiggsDaughters[0][0]->p4.Py() << "|";
	std::cout << "1TauPz=" << product.m_genHiggsDaughters[0][0]->p4.Pz() << "|";
	std::cout << "1TauE=" << product.m_genHiggsDaughters[0][0]->p4.e() << "|";
	std::cout << "1TauPdgId=" << product.m_genHiggsDaughters[0][0]->pdgId() << "|";

	std::cout << "2TauPx=" << product.m_genHiggsDaughters[0][1]->p4.Px() << "|";
	std::cout << "2TauPy=" << product.m_genHiggsDaughters[0][1]->p4.Py() << "|";
	std::cout << "2TauPz=" << product.m_genHiggsDaughters[0][1]->p4.Pz() << "|";
	std::cout << "2TauE=" << product.m_genHiggsDaughters[0][1]->p4.e() << "|";
	std::cout << "2TauPdgId=" << product.m_genHiggsDaughters[0][1]->pdgId() << "|";

		for(unsigned int i=0; i<product.m_genHiggsGranddaughters[0][0].size(); i++)
		{
			std::ostringstream index;
			index << i+1;
			//std::string Index(index.str());
			std::string name = "1Tau" + index.str() + "Daughter";
			std::cout << name << "Px=" << product.m_genHiggsGranddaughters[0][0][i]->p4.Px() << "|";
			std::cout << name << "Py=" << product.m_genHiggsGranddaughters[0][0][i]->p4.Py() << "|";
			std::cout << name << "Pz=" << product.m_genHiggsGranddaughters[0][0][i]->p4.Pz() << "|";
			std::cout << name << "E="  << product.m_genHiggsGranddaughters[0][0][i]->p4.e() << "|";
			std::cout << name << "PdgId=" << product.m_genHiggsGranddaughters[0][0][i]->pdgId() << "|";				
		}  

		for(unsigned int i=0; i<product.m_genHiggsGranddaughters[0][1].size(); i++)
		{
			std::ostringstream index;
			index << i+1;
			//std::string Index(index.str());
			std::string name = "2Tau" + index.str() + "Daughter";
			std::cout << name << "Px=" << product.m_genHiggsGranddaughters[0][1][i]->p4.Px() << "|";
			std::cout << name << "Py=" << product.m_genHiggsGranddaughters[0][1][i]->p4.Py() << "|";
			std::cout << name << "Pz=" << product.m_genHiggsGranddaughters[0][1][i]->p4.Pz() << "|";
			std::cout << name << "E="  << product.m_genHiggsGranddaughters[0][1][i]->p4.e() << "|";
			std::cout << name << "PdgId=" << product.m_genHiggsGranddaughters[0][1][i]->pdgId() << "|";		
		}
	
	std::cout << std::endl;
	*/
	return -777.0;
	}
 };
	m_valueExtractorMap["PhiStar"] = [](HttEvent const & event, HttProduct const & product) {return product.m_PhiStar; };
	m_valueExtractorMap["PsiStarCP"] = [](HttEvent const & event, HttProduct const & product) {return product.m_PsiStarCP; };	
	m_valueExtractorMap["MassRoundOff1"] = [](HttEvent const & event, HttProduct const & product) {return product.m_MassRoundOff1; };
	m_valueExtractorMap["MassRoundOff2"] = [](HttEvent const & event, HttProduct const & product) {return product.m_MassRoundOff2; };
	//Higgs
	m_valueExtractorMap["1genHiggsPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 1 ? product.m_genHiggs.at(0)->p4.Pt(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggsPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 1 ? product.m_genHiggs.at(0)->p4.Pz(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggsPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 1 ? product.m_genHiggs.at(0)->p4.Phi(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggsEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 1 ? product.m_genHiggs.at(0)->p4.Eta(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggsMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 1 ? product.m_genHiggs.at(0)->p4.mass(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggsPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 1 ? product.m_genHiggs.at(0)->pdgId(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggsStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 1 ? product.m_genHiggs.at(0)->status(): UNDEFINED_VALUE;
	}; 
	m_valueExtractorMap["genHiggsSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size();
	};


	m_valueExtractorMap["2genHiggsPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 2 ? product.m_genHiggs.at(1)->p4.Pt(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["2genHiggsPz"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 2 ? product.m_genHiggs.at(1)->p4.Pz(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["2genHiggsPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 2 ? product.m_genHiggs.at(1)->p4.Phi(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["2genHiggsEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 2 ? product.m_genHiggs.at(1)->p4.Eta(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["2genHiggsMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 2 ? product.m_genHiggs.at(1)->p4.mass(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["2genHiggsPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 2 ? product.m_genHiggs.at(1)->pdgId(): UNDEFINED_VALUE;
	};
	m_valueExtractorMap["2genHiggsStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggs.size() >= 2 ? product.m_genHiggs.at(1)->status(): UNDEFINED_VALUE;
	};
	
	// Higgs daughters
	m_valueExtractorMap["1genHiggsDaughterSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.size() >= 1 ? product.m_genHiggsDaughters.at(0).size() : 0;
	};
		m_valueExtractorMap["2genHiggsDaughterSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.size() >= 2 ? product.m_genHiggsDaughters.at(1).size() : 0;
	};
	
	m_valueExtractorMap["1genHiggs1DaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 1 ? product.m_genHiggsDaughters.at(0).at(0)->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs1DaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 1 ? product.m_genHiggsDaughters.at(0).at(0)->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs1DaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 1 ? product.m_genHiggsDaughters.at(0).at(0)->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs1DaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 1 ? product.m_genHiggsDaughters.at(0).at(0)->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs1DaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 1 ? product.m_genHiggsDaughters.at(0).at(0)->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs1DaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 1 ? product.m_genHiggsDaughters.at(0).at(0)->status() : UNDEFINED_VALUE;
	};

        
	m_valueExtractorMap["1genHiggs2DaughterPt"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 2 ? product.m_genHiggsDaughters.at(0).at(1)->p4.Pt() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs2DaughterPhi"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 2 ? product.m_genHiggsDaughters.at(0).at(1)->p4.Phi() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs2DaughterEta"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 2 ? product.m_genHiggsDaughters.at(0).at(1)->p4.Eta() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs2DaughterMass"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 2 ? product.m_genHiggsDaughters.at(0).at(1)->p4.mass() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs2DaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 2 ? product.m_genHiggsDaughters.at(0).at(1)->pdgId() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs2DaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsDaughters.at(0).size() >= 2 ? product.m_genHiggsDaughters.at(0).at(1)->status() : UNDEFINED_VALUE;
	};

	
	m_valueExtractorMap["2genHiggs1DaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (( product.m_genHiggs.size() >= 2) && (product.m_genHiggsDaughters.at(1).size() >= 1)) ? product.m_genHiggsDaughters.at(1).at(0)->pdgId() : 0;
	};
	m_valueExtractorMap["2genHiggs1DaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (( product.m_genHiggs.size() >= 2) && (product.m_genHiggsDaughters.at(1).size() >= 1 )) ? product.m_genHiggsDaughters.at(1).at(0)->status() : 0;
	};
		
	m_valueExtractorMap["2genHiggs2DaughterPdgId"] = [](HttEvent const & event, HttProduct const & product)
	{
		return  (( product.m_genHiggs.size() >= 2) && (product.m_genHiggsDaughters.at(1).size() >= 2 )) ? product.m_genHiggsDaughters.at(1).at(1)->pdgId() : 0;
	};
	m_valueExtractorMap["2genHiggs2DaughterStatus"] = [](HttEvent const & event, HttProduct const & product)
	{
		return (( product.m_genHiggs.size() >= 2) && (product.m_genHiggsDaughters.at(1).size() >= 2 )) ? product.m_genHiggsDaughters.at(1).at(1)->status() : 0;
	};
	//Higgs granddaughters
	
	m_valueExtractorMap["1genHiggs1DaughterGranddaughterSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsGranddaughters.at(0).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(0).size() : UNDEFINED_VALUE;
	};
	m_valueExtractorMap["1genHiggs2DaughterGranddaughterSize"] = [](HttEvent const & event, HttProduct const & product)
	{
		return product.m_genHiggsGranddaughters.at(0).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(1).size() : UNDEFINED_VALUE;
	};
	
	//1DaughterGranddaughters
	m_valueExtractorMap["1genHiggs1Daughter1GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(0).at(0)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter1GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(0).at(0)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter1GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(0).at(0)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter1GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(0).at(0)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter1GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(0).at(0)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs1Daughter1GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(0).at(0)->status(): 0;};

	m_valueExtractorMap["1genHiggs1Daughter2GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(0).at(1)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter2GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(0).at(1)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter2GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(0).at(1)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter2GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(0).at(1)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter2GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(0).at(1)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs1Daughter2GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(0).at(1)->status(): 0;};


	m_valueExtractorMap["1genHiggs1Daughter3GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(0).at(2)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter3GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(0).at(2)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter3GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(0).at(2)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter3GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(0).at(2)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter3GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(0).at(2)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs1Daughter3GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(0).at(2)->status(): 0;};

	m_valueExtractorMap["1genHiggs1Daughter4GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(0).at(3)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter4GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(0).at(3)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter4GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(0).at(3)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter4GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(0).at(3)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs1Daughter4GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(0).at(3)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs1Daughter4GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(0).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(0).at(3)->status(): 0;};



	//2DaughterGranddaughters
	m_valueExtractorMap["1genHiggs2Daughter1GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(1).at(0)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter1GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(1).at(0)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter1GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(1).at(0)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter1GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(1).at(0)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter1GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(1).at(0)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs2Daughter1GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 1 ? product.m_genHiggsGranddaughters.at(0).at(1).at(0)->status(): 0;};

	m_valueExtractorMap["1genHiggs2Daughter2GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(1).at(1)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter2GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(1).at(1)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter2GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(1).at(1)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter2GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(1).at(1)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter2GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(1).at(1)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs2Daughter2GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 2 ? product.m_genHiggsGranddaughters.at(0).at(1).at(1)->status(): 0;};


	m_valueExtractorMap["1genHiggs2Daughter3GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(1).at(2)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter3GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(1).at(2)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter3GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(1).at(2)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter3GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(1).at(2)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter3GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(1).at(2)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs2Daughter3GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 3 ? product.m_genHiggsGranddaughters.at(0).at(1).at(2)->status(): 0;};

	m_valueExtractorMap["1genHiggs2Daughter4GranddaughterPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(1).at(3)->p4.Pt(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter4GranddaughterPhi"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(1).at(3)->p4.Phi(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter4GranddaughterEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(1).at(3)->p4.Eta(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter4GranddaughterMass"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(1).at(3)->p4.mass(): UNDEFINED_VALUE; };
	m_valueExtractorMap["1genHiggs2Daughter4GranddaughterPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(1).at(3)->pdgId(): 0; };
	m_valueExtractorMap["1genHiggs2Daughter4GranddaughterStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genHiggsGranddaughters.at(0).at(1).size() >= 4 ? product.m_genHiggsGranddaughters.at(0).at(1).at(3)->status(): 0;};

	// tests for lepton producers
	m_valueExtractorMap["hardLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[0]->Pt(); };
	m_valueExtractorMap["hardLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[0]->Eta(); };
	m_valueExtractorMap["softLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[1]->Pt(); };
	m_valueExtractorMap["softLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[1]->Eta(); };
	m_valueExtractorMap["diLepMass"] = [](HttEvent const& event, HttProduct const& product) { return (*(product.m_ptOrderedLeptons[0]) + *(product.m_ptOrderedLeptons[1])).mass(); };
	m_valueExtractorMap["decayChannelIndex"] = [](HttEvent const& event, HttProduct const& product) { return Utility::ToUnderlyingValue(product.m_decayChannel); };


	LambdaNtupleConsumerBase<HttTypes>::Init(pset);
}

