#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

class TagAndProbeMuonPairProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "TagAndProbeMuonPairProducer";
	}
    
	enum class ValidMuonsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};
	static ValidMuonsInput ToValidMuonsInput(std::string const& validMuonsInput)
	{
		if (validMuonsInput == "uncorrected") return ValidMuonsInput::UNCORRECTED;
		else if (validMuonsInput == "corrected") return ValidMuonsInput::CORRECTED;
		else return ValidMuonsInput::AUTO;
	}

	enum class MuonID : int
	{
		NONE  = -1,
		TIGHT = 0,
		MEDIUM = 1,
		LOOSE = 2,
		VETO = 3,
		FAKEABLE = 4,
		EMBEDDING = 5
	};
	static MuonID ToMuonID(std::string const& muonID)
	{
		if (muonID == "tight") return MuonID::TIGHT;
		else if (muonID == "medium") return MuonID::MEDIUM;
		else if (muonID == "loose") return MuonID::LOOSE;
		else if (muonID == "veto") return MuonID::VETO;
		else if (muonID == "fakeable") return MuonID::FAKEABLE;
		else if (muonID == "embedding") return MuonID::EMBEDDING;
		else return MuonID::NONE;
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
			setting_type const& settings, metadata_type const& metadata) const override;
protected:
	MuonID muonID;
private:
	ValidMuonsInput validMuonsInput;
	float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const;
	bool MuonIDshortTerm = false;
	bool IsMediumMuon2016ShortTerm(KMuon* muon, event_type const& event, product_type& product) const;
	bool IsMediumMuon2016(KMuon* muon, event_type const& event, product_type& product) const;
};

class TagAndProbeElectronPairProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "TagAndProbeElectronPairProducer";
	}
    
	enum class ValidElectronsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};
	static ValidElectronsInput ToValidElectronsInput(std::string const& validElectronsInput)
	{
		if (validElectronsInput == "uncorrected") return ValidElectronsInput::UNCORRECTED;
		else if (validElectronsInput == "corrected") return ValidElectronsInput::CORRECTED;
		else return ValidElectronsInput::AUTO;
	}

	enum class ElectronID : int
	{
		INVALID = -2,
		NONE  = -1,
		MVANONTRIG = 0,
		MVATRIG = 1,
		VBTF95_VETO = 2,
		VBTF95_LOOSE = 3,
		VBTF95_MEDIUM = 4,
		VBTF95_TIGHT = 5,
		FAKEABLE = 6,
		USER  = 7,
		VETO = 8,
		LOOSE = 9,
		MEDIUM = 10,
		TIGHT = 11,
		VBTF95_LOOSE_RELAXEDVTXCRITERIA = 12,
	};
	static ElectronID ToElectronID(std::string const& electronID)
	{
		if (electronID == "mvanontrig") return ElectronID::MVANONTRIG;
		else if (electronID == "mvatrig") return ElectronID::MVATRIG;
		else if (electronID == "vbft95_veto") return ElectronID::VBTF95_VETO;
		else if (electronID == "vbft95_loose") return ElectronID::VBTF95_LOOSE;
		else if (electronID == "vbft95_loose_relaxedvtxcriteria") return ElectronID::VBTF95_LOOSE_RELAXEDVTXCRITERIA;
		else if (electronID == "vbft95_medium") return ElectronID::VBTF95_MEDIUM;
		else if (electronID == "vbft95_tight") return ElectronID::VBTF95_TIGHT;
		else if (electronID == "fakeable") return ElectronID::FAKEABLE;
		else if (electronID == "user") return ElectronID::USER;
		else if (electronID == "none") return ElectronID::NONE;
		else if (electronID == "veto") return ElectronID::VETO;
		else if (electronID == "loose") return ElectronID::LOOSE;
		else if (electronID == "medium") return ElectronID::MEDIUM;
		else if (electronID == "tight") return ElectronID::TIGHT;
		else
			LOG(FATAL) << "Could not find ElectronID " << electronID << "! If you want the ValidElectronsProducer to use no special ID, use \"none\" as argument."<< std::endl;
		return ElectronID::INVALID;
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
			setting_type const& settings, metadata_type const& metadata) const override;
protected:
	ElectronID electronID;
private:
	ValidElectronsInput validElectronsInput;
	std::string electronIDName;
	double electronMvaIDCutEB1;
	double electronMvaIDCutEB2;
	double electronMvaIDCutEE;
	bool IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const;
};
/*
template<class TLepton>
class TagAndProbeGenLeptonProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	TagAndProbeGenLeptonProducer(std::vector<TLepton>* event_type::*leptons,
				     std::vector<std::shared_ptr<TLepton>> product_type::*leptons_corrected,
				     std::vector<TLepton*> product_type::*validleptons,
				     std::vector<TLepton*> product_type::*genleptons) :
			ProducerBase<HttTypes>(),
			m_leptons(leptons),
			m_leptons_corrected(leptons_corrected),
			m_validleptons(validleptons),
			m_genleptons(genleptons)
	{
	}
	
	virtual std::string GetProducerId() const override {
		return "TagAndProbeGenLeptonProducer";
	}
    
	enum class ValidLeptonsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};

	ValidLeptonsInput ToValidLeptzonsInput(std::string const& validLeptonsInput)
	{
		if (validLeptonsInput == "uncorrected") return ValidLeptonsInput::UNCORRECTED;
		else if (validLeptonsInput == "corrected") return ValidLeptonsInput::CORRECTED;
		else return ValidLeptonsInput::AUTO;
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
	}
	
	virtual void Produce(event_type const& event, product_type& product,
					setting_type const& settings, metadata_type const& metadata) const override
	{
		assert(*m_leptons);
		bool IsData = settings.GetInputIsData();
		if(IsData) return;
		// select input source
		std::vector<TLepton*> leptons;
		if ((validLeptonsInput == ValidLeptonsInput::AUTO && (m_leptons_corrected->size() > 0)) || (validLeptonsInput == ValidLeptonsInput::CORRECTED))
		{
			leptons.resize(m_leptons_corrected->size());
			size_t leptonIndex = 0;
			for (typename std::vector<std::shared_ptr<TLepton> >::iterator lepton = m_leptons_corrected->begin();
			     lepton != m_leptons_corrected->end(); ++lepton)
			{
				leptons[leptonIndex] = lepton->get();
				++leptonIndex;
			}
		}
		else
		{
			leptons.resize((*m_leptons)->size());
			size_t leptonIndex = 0;
			for (typename std::vector<TLepton>::iterator lepton = (*m_leptons)->begin(); lepton != (*m_leptons)->end(); ++lepton)
			{
				leptons[leptonIndex] = &(*lepton);
				++leptonIndex;
			}
		}
		//loop over leptons
		for (typename std::vector<TLepton*>::iterator lepton = leptons.begin(); lepton != leptons.end(); ++lepton)
		{
			m_validleptons->push_back(*lepton); //needed for ValidLEptonsFilter
			
			//filter
			if (
				(*lepton)->p4.Pt() > 10.0 &&
				std::abs((*lepton)->p4.Eta()) < 2.5
			){
				m_genleptons->push_back(*lepton);
			}
		}
	}
	ValidLeptonsInput validLeptonsInput;
private:
	std::vector<TLepton>* event_type::*m_leptons;
	std::vector<std::shared_ptr<TLepton>> product_type::*m_leptons_corrected;
	std::vector<TLepton*> product_type::*m_validleptons;
	std::vector<TLepton*> product_type::*m_genleptons;
};

class TagAndProbeGenElectronProducer: public TagAndProbeGenLeptonProducer<KElectron> {
public:
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	enum class ValidLeptonsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};
	
	virtual std::string GetProducerId() const override;
	TagAndProbeGenElectronProducer();
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
};

class TagAndProbeGenMuonProducer: public TagAndProbeGenLeptonProducer<KMuon> {
public:
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	enum class ValidLeptonsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};
	
	virtual std::string GetProducerId() const override;
	TagAndProbeGenMuonProducer();
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
};

class TagAndProbeGenTauProducer: public TagAndProbeGenLeptonProducer<KTau> {
public:
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	enum class ValidLeptonsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};
	
	virtual std::string GetProducerId() const override;
	TagAndProbeGenTauProducer();
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
};
*/
class TagAndProbeGenElectronProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "TagAndProbeGenElectronProducer";
	}
    
	enum class ValidElectronsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};

	ValidElectronsInput ToValidElectronsInput(std::string const& validElectronsInput)
	{
		if (validElectronsInput == "uncorrected") return ValidElectronsInput::UNCORRECTED;
		else if (validElectronsInput == "corrected") return ValidElectronsInput::CORRECTED;
		else return ValidElectronsInput::AUTO;
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
		validElectronsInput = ToValidElectronsInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidElectronsInput())));
	}
	
	virtual void Produce(event_type const& event, product_type& product,
					setting_type const& settings, metadata_type const& metadata) const override
	{
		assert(event.m_electrons);
		bool IsData = settings.GetInputIsData();
		if(IsData) return;
		// select input source
		std::vector<KElectron*> electrons;
		if ((validElectronsInput == ValidElectronsInput::AUTO && (product.m_correctedElectrons.size() > 0)) || (validElectronsInput == ValidElectronsInput::CORRECTED))
		{
			electrons.resize(product.m_correctedElectrons.size());
			size_t electronIndex = 0;
			for (std::vector<std::shared_ptr<KElectron> >::iterator electron = product.m_correctedElectrons.begin();
			     electron != product.m_correctedElectrons.end(); ++electron)
			{
				electrons[electronIndex] = electron->get();
				++electronIndex;
			}
		}
		else
		{
			electrons.resize(event.m_electrons->size());
			size_t electronIndex = 0;
			for (KElectrons::iterator electron = event.m_electrons->begin(); electron != event.m_electrons->end(); ++electron)
			{
				electrons[electronIndex] = &(*electron);
				++electronIndex;
			}
		}
		//loop over electrons
		for (typename std::vector<KElectron*>::iterator electron = electrons.begin(); electron != electrons.end(); ++electron)
		{
			product.m_validElectrons.push_back(*electron); //needed for ValidLEptonsFilter
			
			//filter
			if (
				(*electron)->p4.Pt() > 10.0 &&
				std::abs((*electron)->p4.Eta()) < 2.5
			){
				product.m_TagAndProbeGenElectrons.push_back(*electron);
			}
		}
	}
	
private:
	ValidElectronsInput validElectronsInput;
};

class TagAndProbeGenMuonProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "TagAndProbeGenMuonProducer";
	}
    
	enum class ValidMuonsInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};

	ValidMuonsInput ToValidMuonsInput(std::string const& validMuonsInput)
	{
		if (validMuonsInput == "uncorrected") return ValidMuonsInput::UNCORRECTED;
		else if (validMuonsInput == "corrected") return ValidMuonsInput::CORRECTED;
		else return ValidMuonsInput::AUTO;
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
		validMuonsInput = ToValidMuonsInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidMuonsInput())));
	}
	
	virtual void Produce(event_type const& event, product_type& product,
					setting_type const& settings, metadata_type const& metadata) const override
	{
		assert(event.m_muons);
		bool IsData = settings.GetInputIsData();
		if(IsData) return;
		// select input source
		std::vector<KMuon*> muons;
		if ((validMuonsInput == ValidMuonsInput::AUTO && (product.m_correctedMuons.size() > 0)) || (validMuonsInput == ValidMuonsInput::CORRECTED))
		{
			muons.resize(product.m_correctedMuons.size());
			size_t muonIndex = 0;
			for (std::vector<std::shared_ptr<KMuon> >::iterator muon = product.m_correctedMuons.begin();
			     muon != product.m_correctedMuons.end(); ++muon)
			{
				muons[muonIndex] = muon->get();
				++muonIndex;
			}
		}
		else
		{
			muons.resize(event.m_muons->size());
			size_t muonIndex = 0;
			for (KMuons::iterator muon = event.m_muons->begin(); muon != event.m_muons->end(); ++muon)
			{
				muons[muonIndex] = &(*muon);
				++muonIndex;
			}
		}
		//loop over muons
		for (typename std::vector<KMuon*>::iterator muon = muons.begin(); muon != muons.end(); ++muon)
		{
			product.m_validMuons.push_back(*muon); //needed for ValidLEptonsFilter
			
			//filter
			if (
				(*muon)->p4.Pt() > 10.0 &&
				std::abs((*muon)->p4.Eta()) < 2.5
			){
				product.m_TagAndProbeGenMuons.push_back(*muon);
			}
		}
	}
	
private:
	ValidMuonsInput validMuonsInput;
};

class TagAndProbeGenTauProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "TagAndProbeGenTauProducer";
	}
    
	enum class ValidTausInput : int
	{
		AUTO = 0,
		UNCORRECTED = 1,
		CORRECTED = 2,
	};

	ValidTausInput ToValidTausInput(std::string const& validTausInput)
	{
		if (validTausInput == "uncorrected") return ValidTausInput::UNCORRECTED;
		else if (validTausInput == "corrected") return ValidTausInput::CORRECTED;
		else return ValidTausInput::AUTO;
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
		validTausInput = ToValidTausInput(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetValidTausInput())));
	}
	
	virtual void Produce(event_type const& event, product_type& product,
					setting_type const& settings, metadata_type const& metadata) const override
	{
		assert(event.m_taus);
		bool IsData = settings.GetInputIsData();
		if(IsData) return;
		// select input source
		std::vector<KTau*> taus;
		if ((validTausInput == ValidTausInput::AUTO && (product.m_correctedTaus.size() > 0)) || (validTausInput == ValidTausInput::CORRECTED))
		{
			taus.resize(product.m_correctedTaus.size());
			size_t tauIndex = 0;
			for (std::vector<std::shared_ptr<KTau> >::iterator tau = product.m_correctedTaus.begin();
			     tau != product.m_correctedTaus.end(); ++tau)
			{
				taus[tauIndex] = tau->get();
				++tauIndex;
			}
		}
		else
		{
			taus.resize(event.m_taus->size());
			size_t tauIndex = 0;
			for (KTaus::iterator tau = event.m_taus->begin(); tau != event.m_taus->end(); ++tau)
			{
				taus[tauIndex] = &(*tau);
				++tauIndex;
			}
		}
		//loop over taus
		for (typename std::vector<KTau*>::iterator tau = taus.begin(); tau != taus.end(); ++tau)
		{
			product.m_validTaus.push_back(*tau); //needed for ValidLEptonsFilter
			
			//filter
			if (
				(*tau)->p4.Pt() > 10.0 &&
				std::abs((*tau)->p4.Eta()) < 2.5
			){
				product.m_TagAndProbeGenTaus.push_back(*tau);
			}
		}
	}
	
private:
	ValidTausInput validTausInput;
};
