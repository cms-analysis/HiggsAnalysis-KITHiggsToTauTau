
#pragma once

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


/** Filter for exclusively defined event category.
 *  Required config tag:
 *  - Category
 */
class EventCategoryFilter: public FilterBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetFilterId() const override {
            return "EventCategoryFilter";
    }
    
	virtual void Init(setting_type const& settings) override;

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
	                           setting_type const& settings) const override;


private:
	HttEnumTypes::EventCategory m_eventCategory;

};


