#pragma once

#include "../HttTypes.h"
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

class TagAndProbeMuonPairProducer: public ProducerBase<HttTypes> {
public:

        typedef typename HttTypes::event_type event_type;
        typedef typename HttTypes::product_type product_type;
        typedef typename HttTypes::setting_type setting_type;
        
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
        
        virtual void Init(setting_type const& settings) override;
        
        virtual void Produce(event_type const& event, product_type& product,
                        setting_type const& settings) const override;
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

        typedef typename HttTypes::event_type event_type;
        typedef typename HttTypes::product_type product_type;
        typedef typename HttTypes::setting_type setting_type;
        
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
        
        virtual void Init(setting_type const& settings) override;
        
        virtual void Produce(event_type const& event, product_type& product,
                        setting_type const& settings) const override;
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