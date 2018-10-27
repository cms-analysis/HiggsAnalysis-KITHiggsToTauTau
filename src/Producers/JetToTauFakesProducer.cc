#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/JetToTauFakesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"


JetToTauFakesProducer::~JetToTauFakesProducer()
{
}

std::string JetToTauFakesProducer::GetProducerId() const
{
	return "JetToTauFakesProducer";
}

void JetToTauFakesProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	std::map<std::string,std::vector<std::string>> ffFiles = Utility::ParseMapTypes<std::string,std::string>(Utility::ParseVectorToMap(settings.GetFakeFaktorFiles()));

	std::string ffFractionsWorkSpaceFile = settings.GetFakeFactorFractionsRooWorkspaceFile();
	fakefactormethod = settings.GetFakeFactorMethod(); //TODO change this to enumtype

	std::map<std::string,std::vector<std::string>> ff_functions = Utility::ParseMapTypes<std::string,std::string>(Utility::ParseVectorToMap((settings.GetFakeFactorRooWorkspaceFunction())));

	if (fakefactormethod == "cp2016")
	{
	//for mt/et/tt cp 2016: 
		ff_function_variables = "m_sv,pt_tt,njets,mjj,sjdphi";
	}
	else if (fakefactormethod == "cp2017")
	{
	//for mt/et/tt cp 2017: 
		ff_function_variables = "pt,njets,nbjets";
	}


	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);

	// Save some time by excluding not needed samples (e.g. HTauTau)
	m_applyFakeFactors = boost::regex_search(settings.GetNickname(), boost::regex("^(Single|MuonEG|Tau|Double|DY|TT|ST|WW|WZ|ZZ|VV)", boost::regex::icase | boost::regex::extended));
	

	
	#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
	gROOT->ProcessLine("#include <map>");
	#endif

    
	TFile f(ffFractionsWorkSpaceFile.c_str());
	m_workspace = (RooWorkspace*)f.Get("w");;
	f.Close();


	
	for(auto ff_function: ff_functions)
	{	
		fns_fractions[ff_function.first] = std::shared_ptr<RooFunctor>(
			m_workspace->function(ff_function.second[0].c_str())->functor(m_workspace->argSet(ff_function_variables.c_str())));
	}


	for(auto ffFile: ffFiles)
	{
		TFile* ffTFile = new TFile(ffFile.second.at(0).c_str(), "READ");
		FakeFactor* ff = (FakeFactor*)ffTFile->Get("ff_comb");
		m_ffComb[ffFile.first] = std::shared_ptr<FakeFactor>(ff);
		ffTFile->Close();
		delete ffTFile;
	}
	
	gDirectory = savedir;
	gFile = savefile;
}

void JetToTauFakesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings, metadata_type const& metadata) const
{
	// Fill inputs
	// to see input vector needs visit:
	// https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L9-L15

    
    bool m_isET = false, m_isMT = false, m_isTT = false; 
    if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET) m_isET = true;
    if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT) m_isMT = true;
    if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT) m_isTT = true;

    if (m_isMT || m_isET)
    {
        std::vector<double> inputs(9);
        // Tau pT 
        inputs[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();
        
        // For this quantity one has to be sure that the second lepton really is a tau
        inputs[1] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;


        // Number of Jets
        inputs[2] = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);
        
        // Visible mass
        inputs[3] = product.m_diLeptonSystem.mass();
        
        // Transverse Mass calculated from lepton and MET - needs Quantities to compute
        inputs[4] = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
        
        // Using lepton isolation over pT
        inputs[5] = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());

	//Getting the fractions for the fakefactor
	auto args = std::vector<double>{};
	double real_frac=0.; //fraction real taus

	
	
	if (fakefactormethod == "cp2016")
	{
		args.push_back(product.m_svfitResults.fittedHiggsLV->M()); // m_sv
		args.push_back(product.m_diLeptonPlusMetSystem.Pt()); //pt di-tau
		args.push_back(inputs[2]); //njets

		double mjj_ = 0.;
		double signed_jdphi_ = -9999.;
		if (product.m_diJetSystemAvailable) //dijetsyst available if njets>1 look in dijetquantitiesproducer
			{
				mjj_ = product.m_diJetSystem.mass();
				signed_jdphi_ = ROOT::Math::VectorUtil::DeltaPhi(product.m_validJets[0]->p4, product.m_validJets[1]->p4) * (product.m_validJets[0]->p4.Eta() > 0.0 ? 1.0 : -1.0);
			}

		args.push_back(mjj_); //mjj
		args.push_back(signed_jdphi_);	  //signed jdphi
	}
	else if (fakefactormethod == "cp2017")
	{
		
		args.push_back(inputs[0]); //pt tau
		args.push_back(inputs[2]); //njets
		args.push_back(0.);	  //nbjets
	}
	double qcd_frac=0.5, w_frac=0.5,tt_frac=0.;

	for(auto fns_fraction: fns_fractions)
	{
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
		else
		{
			LOG(WARNING) << "DID not find: \t \"" << fns_fraction.first << "\" LOOK INSIDE SETTINGS FAKEFACTOR OR JETTOTAUFAKESPRODUCER";
		}
	}

	real_frac = 1-qcd_frac-w_frac-tt_frac; //fraction real taus

	inputs[6] = qcd_frac;
	inputs[7] = w_frac;
	inputs[8] = tt_frac;
	/*
	std::cout << "pt tau:           " << inputs[0] << std::endl;
	std::cout << "decaymode tau:    " << inputs[1] << std::endl;
	std::cout << "njets:            " << inputs[2] << std::endl;
	std::cout << "mvis:             " << inputs[3] << std::endl;
	std::cout << "mt_1:             " << inputs[4] << std::endl;
	std::cout << "iso lepton:       " << inputs[5] << std::endl;
	std::cout << "qcd frac:         " << inputs[6] << std::endl;
	std::cout << "w frac:           " << inputs[7] << std::endl;
	std::cout << "tt frac:          " << inputs[8] << std::endl;
	*/
        for(auto  ff_comb: m_ffComb)
        {
            // Retrieve nominal fake factors
            // To see the way to call each factor/systematic visit:
            // https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766
	    double ff_nom = ff_comb.second->value(inputs);
	    //std::cout << ff_comb.first << "      :         " << ff_nom << std::endl;

            product.m_optionalWeights["fakefactorWeight_comb_inclusive_2"] = ff_nom;

            // Retrieve uncertainties
	    //wt_ff_realtau_up_1 and down_1

	    product.m_optionalWeights["fakefactorWeight_realtau_up_inclusive_2"] = ff_nom*(1.-real_frac*1.1)/(1.-real_frac);
            product.m_optionalWeights["fakefactorWeight_realtau_down_inclusive_2"] = ff_nom*(1.-real_frac*0.9)/(1.-real_frac);


            // Total systematic uncertainties on the QCD fake factor
            product.m_optionalWeights["fakefactorWeight_qcd_syst_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_syst_up");
            product.m_optionalWeights["fakefactorWeight_qcd_syst_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_syst_down");
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet0_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet0_stat_up");
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet0_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet0_stat_down");
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet1_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet1_stat_up");
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet1_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm0_njet1_stat_down");
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet0_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet0_stat_up");
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet0_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet0_stat_down");
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet1_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet1_stat_up");
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet1_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_qcd_dm1_njet1_stat_down");
            // Total systematic uncertainties on the W fake factor
            product.m_optionalWeights["fakefactorWeight_w_syst_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_syst_up");
            product.m_optionalWeights["fakefactorWeight_w_syst_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_syst_down");
            product.m_optionalWeights["fakefactorWeight_w_dm0_njet0_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm0_njet0_stat_up");
            product.m_optionalWeights["fakefactorWeight_w_dm0_njet0_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm0_njet0_stat_down");
            product.m_optionalWeights["fakefactorWeight_w_dm0_njet1_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm0_njet1_stat_up");
            product.m_optionalWeights["fakefactorWeight_w_dm0_njet1_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm0_njet1_stat_down");
            product.m_optionalWeights["fakefactorWeight_w_dm1_njet0_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm1_njet0_stat_up");
            product.m_optionalWeights["fakefactorWeight_w_dm1_njet0_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm1_njet0_stat_down");
            product.m_optionalWeights["fakefactorWeight_w_dm1_njet1_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm1_njet1_stat_up");
            product.m_optionalWeights["fakefactorWeight_w_dm1_njet1_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_w_dm1_njet1_stat_down");
            // Total systematic uncertainties on the tt fake factor
            product.m_optionalWeights["fakefactorWeight_tt_syst_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_syst_up");
            product.m_optionalWeights["fakefactorWeight_tt_syst_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_syst_down");
            product.m_optionalWeights["fakefactorWeight_tt_dm0_njet0_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm0_njet0_stat_up");
            product.m_optionalWeights["fakefactorWeight_tt_dm0_njet0_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm0_njet0_stat_down");
            product.m_optionalWeights["fakefactorWeight_tt_dm0_njet1_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm0_njet1_stat_up");
            product.m_optionalWeights["fakefactorWeight_tt_dm0_njet1_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm0_njet1_stat_down");
            product.m_optionalWeights["fakefactorWeight_tt_dm1_njet0_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm1_njet0_stat_up");
            product.m_optionalWeights["fakefactorWeight_tt_dm1_njet0_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm1_njet0_stat_down");
            product.m_optionalWeights["fakefactorWeight_tt_dm1_njet1_stat_up_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm1_njet1_stat_up");
            product.m_optionalWeights["fakefactorWeight_tt_dm1_njet1_stat_down_inclusive_2"] = ff_comb.second->value(inputs, "ff_tt_dm1_njet1_stat_down");
        }
    }
    if (m_isTT)
    {
        std::vector<double> inputs1(8);
        std::vector<double> inputs2(8);
        // Tau pT 
        inputs1[0] = product.m_flavourOrderedLeptons[0]->p4.Pt();
        inputs2[0] = product.m_flavourOrderedLeptons[1]->p4.Pt();

        inputs1[1] = product.m_flavourOrderedLeptons[1]->p4.Pt();
        inputs2[1] = product.m_flavourOrderedLeptons[0]->p4.Pt();
        
        // For this quantity one has to be sure that the second lepton really is a tau
        inputs1[2] = static_cast<KTau*>(product.m_flavourOrderedLeptons[0])->decayMode;
        inputs2[2] = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;


        // Number of Jets
        inputs1[3] = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);
        inputs2[3] = inputs1[3];
        
        // Visible mass
        inputs1[4] = product.m_diLeptonSystem.mass();
        inputs2[4] = inputs1[4];
        
        // Total Transverse Mass  - needs Quantities to compute  NOT NEEDED ANYMORE AS INPUT
	/*
        double mt_1 = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met.p4);
        double mt_2 = Quantities::CalculateMt(product.m_flavourOrderedLeptons[1]->p4, product.m_met.p4);
        double mt_tt = Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4);
        inputs1[5] = sqrt(pow(mt_tt,2)+pow(mt_1,2)+pow(mt_2,2));
        inputs2[5] = inputs1[5];*/

	auto args1 = std::vector<double>{};
	auto args2 = std::vector<double>{};

	double real_frac_1=0.; //fraction real taus
	double real_frac_2=0.; //fraction real taus

	if (fakefactormethod == "cp2016")
	{
		args1.push_back(product.m_svfitResults.fittedHiggsLV->M()); // m_sv
		args1.push_back(product.m_diLeptonPlusMetSystem.Pt()); //pt di-tau +met
		args1.push_back(inputs1[2]); //njets

		args2.push_back(product.m_svfitResults.fittedHiggsLV->M()); // m_sv
		args2.push_back(product.m_diLeptonPlusMetSystem.Pt()); //pt di-tau +met
		args2.push_back(inputs2[2]); //njets

		double mjj_ = 0.;
		double signed_jdphi_ = -9999.;
		if (product.m_diJetSystemAvailable) //dijetsyst available if njets>1 look in dijetquantitiesproducer
			{
				mjj_ = product.m_diJetSystem.mass();
				signed_jdphi_ = ROOT::Math::VectorUtil::DeltaPhi(product.m_validJets[0]->p4, product.m_validJets[1]->p4) * (product.m_validJets[0]->p4.Eta() > 0.0 ? 1.0 : -1.0);
			}

		args1.push_back(mjj_); //mjj
		args1.push_back(signed_jdphi_);	  //signed jdphi
		args2.push_back(mjj_); //mjj
		args2.push_back(signed_jdphi_);	  //signed jdphi
	}
	else if (fakefactormethod == "cp2017")
	{
		
		args1.push_back(inputs1[0]); //pt tau 1
		args1.push_back(inputs1[2]); //njets
		args1.push_back(0.);	  //nbjets
	
		args2.push_back(inputs2[0]); //pt tau 1
		args2.push_back(inputs2[2]); //njets
		args2.push_back(0.);	  //nbjets
	}

	double qcd_frac_1=1.0, w_frac_1=0.0, tt_frac_1=0.0, dy_frac_1=0.0, qcd_frac_2=1.0, w_frac_2=0.0, tt_frac_2=0.0, dy_frac_2=0.0;
	

	for(auto fns_fraction: fns_fractions)
	{
		//qcd_frac
		if(fns_fraction.first == "qcd_fracs_1")
		{
			qcd_frac_1 = fns_fraction.second->eval(args1.data());
			//std::cout << "qcd 1:    " << qcd_frac_1 << std::endl;

		}
		else if(fns_fraction.first == "qcd_fracs_2")
		{
			qcd_frac_2 = fns_fraction.second->eval(args2.data());
			//std::cout << "qcd 2:    " << qcd_frac_2 << std::endl;
		}
		//wj_frac
		else if(fns_fraction.first == "w_fracs_1")
		{
			w_frac_1 = fns_fraction.second->eval(args1.data());
			//std::cout << "w frac 1:    " << w_frac_1 << std::endl;
		}
		else if(fns_fraction.first == "w_fracs_2")
		{
			w_frac_2 = fns_fraction.second->eval(args2.data());
			//std::cout << "w frac 2:    " << w_frac_2 << std::endl;
		}
		//tt_frac
		else if(fns_fraction.first == "ttbar_fracs_1")
		{
			tt_frac_1 = fns_fraction.second->eval(args1.data());
			//std::cout << "tt frac 1:    " << tt_frac_1 << std::endl;
		}
		else if(fns_fraction.first == "ttbar_fracs_2")
		{
			tt_frac_2 = fns_fraction.second->eval(args2.data());
			//std::cout << "tt frac 2:    " << tt_frac_2 << std::endl;
		}
		//dy_fracs
		else if(fns_fraction.first == "dy_fracs_1")
		{
			dy_frac_1 = fns_fraction.second->eval(args1.data());
			//std::cout << "dy frac 1:    " << dy_frac_1 << std::endl;
		}
		else if(fns_fraction.first == "dy_fracs_2")
		{
			dy_frac_2 = fns_fraction.second->eval(args2.data());
			//std::cout << "dy frac 2:    " << dy_frac_2 << std::endl;
		}
		else
		{
			LOG(WARNING) << "DID not find: \t \"" << fns_fraction.first << "\" LOOK INSIDE SETTINGS FAKEFACTOR OR JETTOTAUFAKESPRODUCER";
		}
	}

	real_frac_1 = 1-qcd_frac_1-w_frac_1-tt_frac_1-dy_frac_1;
        real_frac_2 = 1-qcd_frac_2-w_frac_2-tt_frac_2-dy_frac_2; 


	inputs1[5] = qcd_frac_1;
	inputs1[6] = w_frac_1+ dy_frac_1;
	inputs1[7] = tt_frac_1;

	//inputs1[8] = dy_frac_1; //TODO THIS IS WHAT DANNY DOES, NOT LIKE THIS IN TWIKI


	inputs2[5] = qcd_frac_2;
	inputs2[6] = w_frac_2+ dy_frac_2;
	inputs2[7] = tt_frac_2;

	//inputs2[8] = dy_frac_2; //TODO THIS IS WHAT DANNY DOES, NOT LIKE THIS IN TWIKI

        for(auto  ff_comb: m_ffComb)
        {
            // Retrieve nominal fake factors
            // To see the way to call each factor/systematic visit:
            // https://github.com/CMS-HTT/Jet2TauFakes/blob/master/test/producePublicFakeFactors.py#L735-L766
	    double ff_nom_1 = ff_comb.second->value(inputs1) *0.5;
	    double ff_nom_2 = ff_comb.second->value(inputs2) *0.5;

	    //std::cout << "ff1:   " << ff_nom_1 << std::endl;
	    //std::cout << "ff2:   " << ff_nom_2 << std::endl;

            product.m_optionalWeights["fakefactorWeight_comb_"+ff_comb.first+"_1"] = ff_nom_1;
            product.m_optionalWeights["fakefactorWeight_comb_"+ff_comb.first+"_2"] = ff_nom_2;

	    product.m_optionalWeights["fakefactorWeight_realtau_up_inclusive_1"] = ff_nom_1*(1.-real_frac_1*1.1)/(1.-real_frac_1);
	    product.m_optionalWeights["fakefactorWeight_realtau_down_inclusive_1"] = ff_nom_1*(1.-real_frac_1*0.9)/(1.-real_frac_1);

            product.m_optionalWeights["fakefactorWeight_realtau_up_inclusive_2"] = ff_nom_2*(1.-real_frac_2*1.1)/(1.-real_frac_2);
            product.m_optionalWeights["fakefactorWeight_realtau_down_inclusive_2"] = ff_nom_2*(1.-real_frac_2*0.9)/(1.-real_frac_2);


            // Retrieve uncertainties
            // Total systematic uncertainties on the QCD fake factor
            product.m_optionalWeights["fakefactorWeight_qcd_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet0_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet0_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet0_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet0_stat_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet1_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet1_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet1_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm0_njet1_stat_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet0_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet0_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet0_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet0_stat_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet1_stat_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet1_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet1_stat_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_qcd_dm1_njet1_stat_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet0_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet0_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet0_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet0_stat_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet1_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet1_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm0_njet1_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm0_njet1_stat_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet0_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet0_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet0_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet0_stat_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet1_stat_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet1_stat_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_qcd_dm1_njet1_stat_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_qcd_dm1_njet1_stat_down") *0.5;
            // Total systematic uncertainties on the W fake factor
            product.m_optionalWeights["fakefactorWeight_w_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_w_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_w_frac_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_frac_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_w_frac_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_w_frac_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_w_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_w_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_w_frac_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_frac_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_w_frac_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_w_frac_syst_down") *0.5;
            // Total systematic uncertainties on the tt fake factor
            product.m_optionalWeights["fakefactorWeight_tt_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_tt_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_tt_frac_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_frac_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_tt_frac_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_frac_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_tt_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_tt_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_tt_frac_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_frac_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_tt_frac_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_frac_syst_down") *0.5;
            // Uncertainties for the dy FF
	    /* NOT NEEDED ANYMORE
            product.m_optionalWeights["fakefactorWeight_dy_frac_syst_up_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_dy_frac_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_dy_frac_syst_down_"+ff_comb.first+"_1"] = ff_comb.second->value(inputs1, "ff_tt_dy_frac_syst_down") *0.5;
            product.m_optionalWeights["fakefactorWeight_dy_frac_syst_up_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_dy_frac_syst_up") *0.5;
            product.m_optionalWeights["fakefactorWeight_dy_frac_syst_down_"+ff_comb.first+"_2"] = ff_comb.second->value(inputs2, "ff_tt_dy_frac_syst_down") *0.5;
	   */
	}
    }
}
