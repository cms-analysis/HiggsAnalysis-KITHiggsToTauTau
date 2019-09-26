#pragma once

#include <string>
#include <TFile.h>
#include <TH1.h>
#include <RooWorkspace.h>
#include <RooFunctor.h>
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

// #include "Artus/Utility/interface/ArtusLogging.h"

class FakeFactorProxy
{
public:
	FakeFactorProxy(std::string rooworkspace_file, std::string ff_function_variables, std::string decaychannel)
	{
		// std::cout << "FakeFactorProxy\n";
		m_decayChannel = decaychannel;
		m_ff_function_variables = ff_function_variables;

		std::string ffFractions_filename;

		if(m_decayChannel == "et")
		{
			ffFractions_filename = "$CMSSW_BASE/src/FakeFactorFiles/2017/et/fakeFactors.root";
		}
		else if(m_decayChannel == "mt")
		{
			ffFractions_filename = "$CMSSW_BASE/src/FakeFactorFiles/2017/mt/fakeFactors.root";
		}
		else if(m_decayChannel == "tt")
		{
			ffFractions_filename = "$CMSSW_BASE/src/FakeFactorFiles/2017/tt/fakeFactors.root";
		}

		std::map<std::string,std::string> ff_functions;

		if(m_decayChannel == "et")
		{
			ff_functions["w_fracs"] = "w_fracs_et";
			ff_functions["qcd_fracs"] = "qcd_fracs_et";
			ff_functions["ttbar_fracs"] = "ttbar_fracs_et";
			ff_functions["dy_fracs"] = "real_taus_fracs_et";
		}
		else if(m_decayChannel == "mt")
		{
			ff_functions["w_fracs"] = "w_fracs_mt";
			ff_functions["qcd_fracs"] = "qcd_fracs_mt";
			ff_functions["ttbar_fracs"] = "ttbar_fracs_mt";
			ff_functions["dy_fracs"] = "real_taus_fracs_mt";
		}
		else if(m_decayChannel == "tt")
		{
			ff_functions["w_fracs_1"] = "w_fracs_tt1";
			ff_functions["qcd_fracs_1"] = "qcd_fracs_tt1";
			ff_functions["ttbar_fracs_1"] = "ttbar_fracs_tt1";
			ff_functions["dy_fracs_1"] = "real_taus_fracs_tt1";

			ff_functions["w_fracs_2"] = "w_fracs_tt2",
			ff_functions["qcd_fracs_2"] = "qcd_fracs_tt2";
			ff_functions["ttbar_fracs_2"] = "ttbar_fracs_tt2";
			ff_functions["dy_fracs_2"] = "real_taus_fracs_tt2";
		}

		// std::cout << "Opening RooWorkSpace\n";
		TFile f(rooworkspace_file.c_str());
		m_workspace = (RooWorkspace*)f.Get("w");
		f.Close();

		for(auto ff_function: ff_functions)
		{
			fns_fractions[ff_function.first] = std::shared_ptr<RooFunctor>(
				m_workspace->function(ff_function.second.c_str())->functor(m_workspace->argSet(m_ff_function_variables.c_str())));
		}

		// std::cout << "Opening FakeFactor File: " << ffFractions_filename << "\n";
		TFile* ffTFile = TFile::Open(ffFractions_filename.c_str(), "READ");
		// std::cout << "Retrieving FakeFactor\n";
		FakeFactor* ff = (FakeFactor*)ffTFile->Get("ff_comb");
		// std::cout << "Setting m_ffComb\n";
		m_ffComb["inclusive"] = std::shared_ptr<FakeFactor>(ff);
		// std::cout << "Closing FakeFactor File\n";
		ffTFile->Close();
		// std::cout << "Deleting FakeFactor File\n";
		delete ffTFile;
		// std::cout << "FakeFactorProxy\n";
	}

	~FakeFactorProxy()
	{
		// delete m_workspace;
	};

	double GetScaleFactor(int index, float pt_1, float pt_2, float iso_1, int decayMode_1, int decayMode_2, float m_vis, float mt_1, int njetspt30)
	{
		std::vector<double> scaleFactor;

		if((m_decayChannel == "et") || (m_decayChannel == "mt"))
		{
			//Getting the fractions for the fakefactor
			std::vector<double> inputs(9);
			auto args = std::vector<double>{};
			double real_frac=0.; //fraction real taus
			double qcd_frac=0.5, w_frac=0.5, tt_frac=0., dy_frac=0.;

			// Tau pT
			inputs[0] = pt_2; // product.m_flavourOrderedLeptons[1]->p4.Pt();

			// For this quantity one has to be sure that the second lepton really is a tau
			inputs[1] = decayMode_2; // static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;

			// Number of Jets
			inputs[2] = njetspt30; // product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);

			// Visible mass
			inputs[3] = m_vis; // product.m_diLeptonSystem.mass();

			// Transverse Mass calculated from lepton and MET - needs Quantities to compute
			inputs[4] = mt_1; // Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);

			// Using lepton isolation over pT
			inputs[5] = iso_1; // SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());

			if (m_ff_function_variables == "decayMode,njets,pt")
			{
				args.push_back(decayMode_2); //decayMode
				args.push_back(njetspt30); //njets
				args.push_back(pt_2); //pt tau
			}
			else if (m_ff_function_variables == "njets,pt")
			{
				args.push_back(njetspt30); //njets
				args.push_back(pt_2); //pt tau
			}

			for(auto fns_fraction : fns_fractions)
			{
				// LOG(INFO) << "fns_fraction.first = " << fns_fraction.first;
				//qcd_frac
				if(fns_fraction.first == "qcd_fracs")
				{
					qcd_frac = fns_fraction.second->eval(args.data());
				}
				//wj_frac
				else if(fns_fraction.first == "w_fracs")
				{
					w_frac = fns_fraction.second->eval(args.data());
				}
				//tt_frac
				else if(fns_fraction.first == "ttbar_fracs")
				{
					tt_frac = fns_fraction.second->eval(args.data());
				}
				else if(fns_fraction.first == "dy_fracs") // only used for cptautau2017
				{
					dy_frac = fns_fraction.second->eval(args.data());
				}
				else
				{
					// LOG(WARNING) << "DID not find: \t \"" << fns_fraction.first << "\" LOOK INSIDE SETTINGS FAKEFACTOR OR JETTOTAUFAKESPRODUCER";
				}
			}
			// std::cout << "qcd_frac: " << qcd_frac << '\n';
			// std::cout << "w_frac: " << w_frac << '\n';
			// std::cout << "tt_frac: " << tt_frac << '\n';
			real_frac = dy_frac;

			double sum_of_bkg_fracs = (qcd_frac + w_frac + tt_frac > 0) ? qcd_frac + w_frac + tt_frac : 1.0;
			if (sum_of_bkg_fracs == 0) std::cout << "sum_of_bkg_fracs: " << sum_of_bkg_fracs << '\n';

			qcd_frac = qcd_frac/(sum_of_bkg_fracs);
			w_frac = w_frac/(sum_of_bkg_fracs);
			tt_frac = tt_frac/(sum_of_bkg_fracs);

			inputs[6] = qcd_frac;
			inputs[7] = w_frac;
			inputs[8] = tt_frac;

			for(auto ff_comb: m_ffComb)
			{
				// Retrieve nominal fake factors
				// To see the way to call each factor/systematic visit:
				// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766
				double fakefactor = ff_comb.second->value(inputs);
				// std::cout << "ff_comb.second->value(inputs): " << fakefactor << '\n';
				scaleFactor.push_back(fakefactor);
			}
		}
		else if(m_decayChannel == "tt")
		{
			std::vector<double> inputs1(8);
			std::vector<double> inputs2(8);

			// Tau pT
			inputs1[0] = pt_1; // product.m_flavourOrderedLeptons[0]->p4.Pt();
			inputs2[0] = pt_2; // product.m_flavourOrderedLeptons[1]->p4.Pt();

			inputs1[1] = pt_2; // product.m_flavourOrderedLeptons[1]->p4.Pt();
			inputs2[1] = pt_1; // product.m_flavourOrderedLeptons[0]->p4.Pt();

			// For this quantity one has to be sure that the second lepton really is a tau
			inputs1[2] = decayMode_1; // static_cast<KTau*>(product.m_flavourOrderedLeptons[0])->decayMode;
			inputs2[2] = decayMode_2; // static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;

			// Number of Jets
			inputs1[3] = njetspt30; // product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);
			inputs2[3] = inputs1[3];

			// Visible mass
			inputs1[4] = m_vis; // product.m_diLeptonSystem.mass();
			inputs2[4] = inputs1[4];

			auto args1 = std::vector<double>{};
			auto args2 = std::vector<double>{};

			double real_frac_1=0.; //fraction real taus
			double real_frac_2=0.; //fraction real taus
			double qcd_frac_1 = 1.0, w_frac_1 = 0.0, tt_frac_1 = 0.0, dy_frac_1 = 0.0, qcd_frac_2 = 1.0, w_frac_2 = 0.0, tt_frac_2 = 0.0, dy_frac_2 = 0.0;

			if (m_ff_function_variables == "decayMode,njets,pt")
			{
				args1.push_back(inputs1[2]); //decayMode
				args1.push_back(inputs1[3]); //njets
				args1.push_back(inputs1[0]); //pt tau

				args2.push_back(inputs2[2]); //decayMode
				args2.push_back(inputs2[3]); //njets
				args2.push_back(inputs2[0]); //pt tau
			}
			else if (m_ff_function_variables == "njets,pt")
			{
				args1.push_back(inputs1[3]); //njets
				args1.push_back(inputs1[0]); //pt tau

				args2.push_back(inputs2[3]); //njets
				args2.push_back(inputs2[0]); //pt tau
			}

			for(auto fns_fraction : fns_fractions)
			{
				//qcd_frac
				if(fns_fraction.first == "qcd_fracs_1")
				{
					qcd_frac_1 = fns_fraction.second->eval(args1.data());
				}
				else if(fns_fraction.first == "qcd_fracs_2")
				{
					qcd_frac_2 = fns_fraction.second->eval(args2.data());
				}
				//wj_frac
				else if(fns_fraction.first == "w_fracs_1")
				{
					w_frac_1 = fns_fraction.second->eval(args1.data());
				}
				else if(fns_fraction.first == "w_fracs_2")
				{
					w_frac_2 = fns_fraction.second->eval(args2.data());
				}
				//tt_frac
				else if(fns_fraction.first == "ttbar_fracs_1")
				{
					tt_frac_1 = fns_fraction.second->eval(args1.data());
				}
				else if(fns_fraction.first == "ttbar_fracs_2")
				{
					tt_frac_2 = fns_fraction.second->eval(args2.data());
				}
				//dy_fracs
				else if(fns_fraction.first == "dy_fracs_1")
				{
					dy_frac_1 = fns_fraction.second->eval(args1.data());
				}
				else if(fns_fraction.first == "dy_fracs_2")
				{
					dy_frac_2 = fns_fraction.second->eval(args2.data());
				}
				else
				{
					// LOG(WARNING) << "DID not find: \t \"" << fns_fraction.first << "\" LOOK INSIDE SETTINGS FAKEFACTOR OR JETTOTAUFAKESPRODUCER";
				}
			}

			real_frac_1 = dy_frac_1;
			real_frac_2 = dy_frac_2;

			double sum_of_bkg_fracs_1 = qcd_frac_1 + w_frac_1 + tt_frac_1;

			qcd_frac_1 = qcd_frac_1/(sum_of_bkg_fracs_1);
			w_frac_1 = w_frac_1/(sum_of_bkg_fracs_1);
			tt_frac_1 = tt_frac_1/(sum_of_bkg_fracs_1);

			double sum_of_bkg_fracs_2 = qcd_frac_2 + w_frac_2 + tt_frac_2;

			qcd_frac_2 = qcd_frac_2/(sum_of_bkg_fracs_2);
			w_frac_2 = w_frac_2/(sum_of_bkg_fracs_2);
			tt_frac_2 = tt_frac_2/(sum_of_bkg_fracs_2);

			inputs1[5] = qcd_frac_1;
			inputs1[6] = w_frac_1;
			inputs1[7] = tt_frac_1;

			inputs2[5] = qcd_frac_2;
			inputs2[6] = w_frac_2;
			inputs2[7] = tt_frac_2;

			for(auto  ff_comb : m_ffComb)
			{
				// Retrieve nominal fake factors
				// To see the way to call each factor/systematic visit:
				// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766
				scaleFactor.push_back(ff_comb.second->value(inputs1)*0.5);
				scaleFactor.push_back(ff_comb.second->value(inputs2)*0.5);
			}
		}
		// std::cout << "scaleFactor[" << index << "]: " << scaleFactor[index] << "\n";
		return scaleFactor[index];
	}

private:
	std::map<std::string,std::shared_ptr<FakeFactor>> m_ffComb;
	std::string m_decayChannel;
	std::string m_ff_function_variables;

protected:
	RooWorkspace *m_workspace;
	std::map<std::string,std::shared_ptr<RooFunctor>> fns_fractions;
};
