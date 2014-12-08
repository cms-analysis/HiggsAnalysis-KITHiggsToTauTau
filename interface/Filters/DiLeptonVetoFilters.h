
#pragma once

#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


/** Abstract filter for Veto of dileptons
 */
template<class TLepton>
class DiLeptonVetoFilterBase: public FilterBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	enum class VetoMode : int
	{
		NONE  = -1,
		VETO_OS_KEEP_SS = 0,
		VETO_SS_KEEP_OS = 1,
		VETO_OS_VETO_SS = 2,
		KEEP_OS_KEEP_SS = 2,
	};
	static VetoMode ToVetoMode(std::string const& vetoMode)
	{
		if (vetoMode == "veto_os_keep_ss") return VetoMode::VETO_OS_KEEP_SS;
		else if (vetoMode == "veto_ss_keep_os") return VetoMode::VETO_SS_KEEP_OS;
		else if (vetoMode == "veto_os_veto_ss") return VetoMode::VETO_OS_VETO_SS;
		else if (vetoMode == "keep_os_keep_ss") return VetoMode::KEEP_OS_KEEP_SS;
		else return VetoMode::NONE;
	}
	
	DiLeptonVetoFilterBase(std::vector<TLepton*> product_type::*leptons,
						   std::string (setting_type::*GetDiLeptonVetoMode)(void) const) :
		m_leptons(leptons),
		GetDiLeptonVetoMode(GetDiLeptonVetoMode)
	{
	}					
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE
	{
		FilterBase<HttTypes>::Init(settings);
	
		vetoMode = ToVetoMode(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.*GetDiLeptonVetoMode)())));
	}

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
							   setting_type const& settings) const ARTUS_CPP11_OVERRIDE
	{
		if ((vetoMode == VetoMode::KEEP_OS_KEEP_SS) ||
		    (vetoMode == VetoMode::NONE) ||
		    ((product.*m_leptons).size() < 2))
		{
			return true;
		}
		else
		{
			int nPosLeptons = 0;
			int nNegLeptons = 0;
		
			for (typename std::vector<TLepton*>::const_iterator lepton = (product.*m_leptons).begin();
				 lepton != (product.*m_leptons).end(); ++lepton)
			{
				if ((int)((*lepton)->charge()) > 0)
				{
					++nPosLeptons;
				}
				else
				{
					++nNegLeptons;
				}
			
				if ((
						((nPosLeptons > 0) && (nNegLeptons > 0))
						&&
						((vetoMode == VetoMode::VETO_OS_KEEP_SS) || (vetoMode == VetoMode::VETO_OS_VETO_SS))
					)
					||
					(
						((nPosLeptons > 1) || (nNegLeptons > 1))
						&&
						((vetoMode == VetoMode::VETO_SS_KEEP_OS) || (vetoMode == VetoMode::VETO_OS_VETO_SS))
					)
				)
				{
					return false;
				}
			}
		
			return true;
		}
	}


private:
	std::vector<TLepton*> product_type::*m_leptons;
	std::string (setting_type::*GetDiLeptonVetoMode)(void) const;
	
	VetoMode vetoMode;

};


/** Filter for Veto of DiVetoElectrons
 *  Required config tag:
 *  - DiVetoElectronVetoMode
 */
class DiVetoElectronVetoFilter : public DiLeptonVetoFilterBase<KElectron> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
			return "DiVetoElectronVetoFilter";
	}
	
	DiVetoElectronVetoFilter();
};


/** Filter for Veto of DiVetoMuons
 *  Required config tag:
 *  - DiVetoMuonVetoMode
 */
class DiVetoMuonVetoFilter : public DiLeptonVetoFilterBase<KMuon> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
			return "DiVetoMuonVetoFilter";
	}
	
	DiVetoMuonVetoFilter();
};

