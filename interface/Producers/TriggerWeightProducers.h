
#pragma once

#include "TMath.h"

#include "../HttTypes.h"


/** Producer for the Trigger weights using the functions and paramters provided by the Htt group
 *      See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Data_MC_correction_factors
 *
 *  Required config tags:
 *  - <Electron|Muon|Tau>TriggerTurnOnParamtersData (vector of doubles, length 5)
 *  - <Electron|Muon|Tau>TriggerTurnOnParamtersMc (vector of doubles, length 5)
 *
 *  This is an abstract base class for the implementations for electrons, muons and taus below.
 */
template<class TLepton>
class TriggerWeightProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "trigger_weight";
	}
	
	TriggerWeightProducer(std::vector<TLepton*> product_type::*validLeptons,
	                      std::string weightName) :
		ProducerBase<HttTypes>(),
		m_validLeptonsMember(validLeptons),
		m_weightName(weightName)
	{
	}

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE
	{
		double triggerWeight = 1.0;
		// loop over all valid leptons of this flavour (should be one or two)
		for (typename std::vector<TLepton*>::const_iterator lepton = (product.*m_validLeptonsMember).begin();
		     lepton != (product.*m_validLeptonsMember).end(); ++lepton)
		{
			// weight = efficiency in data / efficiency in MC
			double efficiencyData = Efficiency((*lepton)->p4.Pt(), m_m0Data, m_sigmaData, m_alphaData, m_nData, m_normData);
			double efficiencyMc = Efficiency((*lepton)->p4.Pt(), m_m0Mc, m_sigmaMc, m_alphaMc, m_nMc, m_normMc);
			triggerWeight *= (efficiencyData / efficiencyMc);
		}
		product.m_weights[m_weightName] = triggerWeight;
	}

protected:

	// function that lets this producer work as both a global and a local producer
	void Initialise(std::vector<double> const& hltTriggerTurnOnParamtersData,
	                std::vector<double> const& hltTriggerTurnOnParamtersMc,
	                std::string leptonName)
	{
		// initialise parameters for data
		if (hltTriggerTurnOnParamtersData.size() < 5) {
			LOG(FATAL) << "Too few (" << hltTriggerTurnOnParamtersData.size()
			           << " instead of 5) parameters specified via config tag \""
			           << leptonName << "TriggerTurnOnParamtersData\"!";
		}
		else if (hltTriggerTurnOnParamtersData.size() > 5) {
			LOG(WARNING) << "Too many (" << hltTriggerTurnOnParamtersData.size()
			             << " instead of 5) parameters specified via config tag \""
			             << leptonName << "TriggerTurnOnParamtersData\"! Only the first ones are taken.";
		}
	
		m_m0Data = hltTriggerTurnOnParamtersData[0];
		m_sigmaData = hltTriggerTurnOnParamtersData[1];
		m_alphaData = hltTriggerTurnOnParamtersData[2];
		m_nData = hltTriggerTurnOnParamtersData[3];
		m_normData = hltTriggerTurnOnParamtersData[4];
	
		// initialise parameters for MC
		if (hltTriggerTurnOnParamtersMc.size() < 5) {
			LOG(FATAL) << "Too few (" << hltTriggerTurnOnParamtersMc.size()
			           << " instead of 5) parameters specified via config tag \""
			           << leptonName << "TriggerTurnOnParamtersMc\"!";
		}
		else if (hltTriggerTurnOnParamtersMc.size() > 5) {
			LOG(WARNING) << "Too many (" << hltTriggerTurnOnParamtersMc.size()
			             << " instead of 5) parameters specified via config tag \""
			             << leptonName << "TriggerTurnOnParamtersMc\"! Only the first ones are taken.";
		}
	
		m_m0Mc = hltTriggerTurnOnParamtersMc[0];
		m_sigmaMc = hltTriggerTurnOnParamtersMc[1];
		m_alphaMc = hltTriggerTurnOnParamtersMc[2];
		m_nMc = hltTriggerTurnOnParamtersMc[3];
		m_normMc = hltTriggerTurnOnParamtersMc[4];
	}


private:
	std::vector<TLepton*> product_type::*m_validLeptonsMember;
	std::string m_weightName;
	
	double m_m0Data;
	double m_sigmaData;
	double m_alphaData;
	double m_nData;
	double m_normData;
	
	double m_m0Mc;
	double m_sigmaMc;
	double m_alphaMc;
	double m_nMc;
	double m_normMc;

	/** Trigger turn-on parametrisation
	 *  Code taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2012#ETau_MuTau_trigger_turn_on_Joshu
	 *  Parameter m seems to mean pt
	 */
	double Efficiency(double m, double m0, double sigma, double alpha, double n, double norm) const
	{
		const double sqrtPiOver2 = 1.2533141373;
		const double sqrt2 = 1.4142135624;
		double sig = fabs((double) sigma);
		double t = (m - m0)/sig;
		if (alpha < 0.0) t = -t;
		double absAlpha = fabs(alpha/sig);
		double a = TMath::Power(n/absAlpha, n)*exp(-0.5*absAlpha*absAlpha);
		double b = absAlpha - n/absAlpha;
		double ApproxErf;
		double arg = absAlpha / sqrt2;
		if (arg > 5.0) ApproxErf = 1;
		else if (arg < -5.) ApproxErf = -1;
		else ApproxErf = TMath::Erf(arg);
		double leftArea = (1 + ApproxErf) * sqrtPiOver2;
		double rightArea = ( a * 1/TMath::Power(absAlpha - b, n-1)) / (n - 1);
		double area = leftArea + rightArea;
		if( t <= absAlpha )
		{
			arg = t / sqrt2;
			if(arg > 5.) ApproxErf = 1;
			else if (arg < -5.) ApproxErf = -1;
			else ApproxErf = TMath::Erf(arg);
			return norm * (1 + ApproxErf) * sqrtPiOver2 / area;
		}
		else
		{
			return norm * (leftArea + a * (1.0/TMath::Power(t-b, n-1.0) - 1.0/TMath::Power(absAlpha - b, n-1.0)) / (1.0 - n)) / area;
		}
	}
};


class ElectronTriggerWeightProducer: public TriggerWeightProducer<KDataElectron> {
public:
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "electron_trigger_weight";
	}
	
	ElectronTriggerWeightProducer() : TriggerWeightProducer<KDataElectron>(&product_type::m_validElectrons,
		                                                                   "electronTriggerWeight")
	{
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE
	{
		this->Initialise(settings.GetElectronTriggerTurnOnParamtersData(),
		                 settings.GetElectronTriggerTurnOnParamtersMc(), "Electron");
	}
};


class MuonTriggerWeightProducer: public TriggerWeightProducer<KDataMuon> {
public:
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "muon_trigger_weight";
	}
	
	MuonTriggerWeightProducer() : TriggerWeightProducer<KDataMuon>(&product_type::m_validMuons,
		                                                           "muonTriggerWeight")
	{
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE
	{
		this->Initialise(settings.GetMuonTriggerTurnOnParamtersData(),
		                 settings.GetMuonTriggerTurnOnParamtersMc(), "Muon");
	}
};


class TauTriggerWeightProducer: public TriggerWeightProducer<KDataPFTau> {
public:
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tau_trigger_weight";
	}
	
	TauTriggerWeightProducer() : TriggerWeightProducer<KDataPFTau>(&product_type::m_validTaus,
		                                                           "tauTriggerWeight")
	{
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE
	{
		this->Initialise(settings.GetTauTriggerTurnOnParamtersData(),
		                 settings.GetTauTriggerTurnOnParamtersMc(), "Tau");
	}
};

