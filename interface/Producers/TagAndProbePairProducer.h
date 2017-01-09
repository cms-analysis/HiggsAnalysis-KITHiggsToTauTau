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
        bool IsMediumMuon2016ShortTerm(KMuon* muon, event_type const& event, product_type& product) const;
};