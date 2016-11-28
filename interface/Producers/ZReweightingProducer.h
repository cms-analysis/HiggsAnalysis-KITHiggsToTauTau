
#pragma once

#include <TH3.h>
//#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>

/**
   \brief ZReweightingProducer
   Config tags:
   - Fill me with something meaningful

*/

//class ZReweightingProducer : public KappaProducerBase {
class ZReweightingProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
	m_applyReweighting = false;
	m_isDY = boost::regex_search(settings.GetNickname(), boost::regex("DY.?JetsToLLM(10|50|150)", boost::regex::icase | boost::regex::extended));
        TDirectory *savedir(gDirectory);
        TFile *savefile(gFile);
        TString cmsswBase = TString( getenv ("CMSSW_BASE") );
        TFile * zReweightingFile = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/zReweighting/reweighting_rebinned_wEmptyBinFix.root");
	if(boost::regex_search(settings.GetRootFileFolder(), boost::regex("(em|mm)_jecUncNom_tauEs(Nom|Up|Down)", boost::regex::icase | boost::regex::extended)))
	{
        m_zReweightingHist = (TH3D*)zReweightingFile->Get("rweight_3d_EM_noMET");
	m_applyReweighting = true;
	}
	if(boost::regex_search(settings.GetRootFileFolder(), boost::regex("et_jecUncNom_tauEs(Nom|Up|Down)", boost::regex::icase | boost::regex::extended)))
	{
        m_zReweightingHist = (TH3D*)zReweightingFile->Get("rweight_3d_ET_noMET");
	m_applyReweighting = true;
	}
	if(boost::regex_search(settings.GetRootFileFolder(), boost::regex("mt_jecUncNom_tauEs(Nom|Up|Down)", boost::regex::icase | boost::regex::extended)))
	{
        m_zReweightingHist = (TH3D*)zReweightingFile->Get("rweight_3d_MT_noMET");
	m_applyReweighting = true;
	}
	if(boost::regex_search(settings.GetRootFileFolder(), boost::regex("tt_jecUncNom_tauEs(Nom|Up|Down)", boost::regex::icase | boost::regex::extended)))
	{
        m_zReweightingHist = (TH3D*)zReweightingFile->Get("rweight_3d_TT_noMET");
	m_applyReweighting = true;
	}
        gDirectory = savedir;
        gFile = savefile;
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
	TH3D* m_zReweightingHist = 0;
	bool m_applyReweighting;
	bool m_isDY;

};
