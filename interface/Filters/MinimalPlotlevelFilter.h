
#pragma once

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Filter with lightweight expression parser
 *  Required config tag:
 *  - PlotlevelFilterExpressionQuantities  -> List of variable names to be used in expression
 *  - PlotevelFilterExpression  -> Expression to be applied
 * Hint:
 * - Use * for connecting subexpressions with AND
 * - You are allowd to use || for OR statements
 * - Syntax:
 * - Always write [variable] [relation] [static value]
 * - You must insert one space between relation signs and value/variable BUT none between * or ||
 * (pt_1 < 40||pt_2 > 50)*(mjj > 250)
 *
 */
// template<class HttTypes>
class MinimalPlotlevelFilter : public FilterBase<HttTypes> 
{
public:
	typedef std::function<float(event_type const&, product_type const&)> float_extractor_lambda;
	
	virtual std::string GetFilterId() const override;
	
	void Init(setting_type const& settings, metadata_type& metadata) override;
	
	template<typename T>
	void RemoveSubstrs(typename std::basic_string<T>& s,char p) const
	{
		typename std::basic_string<T>::size_type n = 1;
		for (typename std::basic_string<T>::size_type i = s.find(p); i != typename std::basic_string<T>().npos; i = s.find(p))
		{
			s.erase(i, n);
		}
	}
	
	bool EvaluateSubExpression(std::string& expression, event_type const& event, product_type const& product, setting_type const& settings) const;
	
	virtual bool DoesEventPass(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::vector<float_extractor_lambda> m_ExpressionQuantities;
	std::vector<std::string> m_ExpressionNames;
	mutable std::vector<std::string> m_SubExpressions;
};
