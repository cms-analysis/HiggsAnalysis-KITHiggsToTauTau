
#pragma once

#include <cstdint>
#include <cassert>

#include <boost/algorithm/string/predicate.hpp>

#include <TTree.h>
#include <Math/Vector4D.h>
#include <Math/Vector4Dfwd.h>

#include "Artus/Core/interface/EventBase.h"
#include "Artus/Core/interface/ProductBase.h"
#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/Configuration/interface/SettingsBase.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/RootFileHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

#include "Kappa/DataFormats/interface/Kappa.h"
#include <boost/regex.hpp>


class TagAndProbeMuonPairConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override;
	
	void Init(setting_type const& settings, metadata_type& metadata) override;

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override;

	void Finish(setting_type const& settings, metadata_type const& metadata) override;


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	bool usedMuonIDshortTerm = false;
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Short_Term_Medium_Muon_Definitio
	bool IsMediumMuon2016ShortTerm(KMuon* muon) const;
	bool IsMediumMuon2016(KMuon* muon) const;
};


class TagAndProbeElectronPairConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override;
	
	void Init(setting_type const& settings, metadata_type& metadata) override;

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override;

	void Finish(setting_type const& settings, metadata_type const& metadata) override;


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	std::string electronIDName;
	double electronMvaIDCutEB1;
	double electronMvaIDCutEB2;
	double electronMvaIDCutEE;
	bool IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const;
};


class TagAndProbeGenTauConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override;
	
	void Init(setting_type const& settings, metadata_type& metadata) override;

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override;

	void Finish(setting_type const& settings, metadata_type const& metadata) override;


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	bool oldTauDMs;
	bool IsTauIDRecommendation13TeV(KTau* tau, event_type const& event, bool const& oldTauDMs, bool const& isAOD=false) const;
};


class TagAndProbeGenMuonConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override;
	
	void Init(setting_type const& settings, metadata_type& metadata) override;

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override;

	void Finish(setting_type const& settings, metadata_type const& metadata) override;


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	bool usedMuonIDshortTerm = false;
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Short_Term_Medium_Muon_Definitio
	bool IsMediumMuon2016ShortTerm(KMuon* muon) const;
	bool IsMediumMuon2016(KMuon* muon) const;
};


class TagAndProbeGenElectronConsumer: public ConsumerBase<HttTypes> {

public:
	typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > RMFLV;

	std::string GetConsumerId() const override;
	
	void Init(setting_type const& settings, metadata_type& metadata) override;

	void ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata ) override;

	void Finish(setting_type const& settings, metadata_type const& metadata) override;


private:
	TTree* m_tree = nullptr;
	std::map <std::string, bool> BoolQuantities;
	std::map <std::string, int> IntQuantities;
	std::map <std::string, float> FloatQuantities;
	std::string electronIDName;
	double electronMvaIDCutEB1;
	double electronMvaIDCutEB2;
	double electronMvaIDCutEE;
	bool IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const;
};
