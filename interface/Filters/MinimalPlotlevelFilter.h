
#pragma once

#include "Artus/Core/interface/FilterBase.h"
#include <algorithm>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"


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
class MinimalPlotlevelFilter: public FilterBase<HttTypes> 
{
public:
	typedef std::function<float(event_type const&, product_type const&)> float_extractor_lambda;
	
	virtual std::string GetFilterId() const override {
			return "MinimalPlotlevelFilter";
	}
	
	void Init(setting_type const& settings, metadata_type& metadata) override
	{
		FilterBase<HttTypes>::Init(settings, metadata);
		// construct extractors vector
		m_ExpressionQuantities.clear();
		m_ExpressionNames.clear();
		for (std::vector<std::string>::const_iterator quantity = (settings.GetPlotlevelFilterExpressionQuantities)().begin();
			quantity != (settings.GetPlotlevelFilterExpressionQuantities)().end(); ++quantity)
		{
			bool variable_found = false;
			if (metadata.m_commonFloatQuantities.count(*quantity) > 0)
			{
				m_ExpressionQuantities.push_back(SafeMap::Get(metadata.m_commonFloatQuantities, *quantity));
				m_ExpressionNames.push_back(*quantity);
				LOG(DEBUG) << "\t" << *quantity << " is used as floatQuantity";
				variable_found = true;
			}
			else{ if(metadata.m_commonIntQuantities.count(*quantity) > 0)
			{
				m_ExpressionQuantities.push_back(SafeMap::Get(metadata.m_commonIntQuantities, *quantity));
				m_ExpressionNames.push_back(*quantity);
				LOG(DEBUG) << "\t" << *quantity << " is used as intQuantity";
				variable_found = true;
			}
			else{ if (metadata.m_commonBoolQuantities.count(*quantity) > 0)
			{
				m_ExpressionQuantities.push_back(SafeMap::Get(metadata.m_commonBoolQuantities, *quantity));
				m_ExpressionNames.push_back(*quantity);
				LOG(DEBUG) << "\t" << *quantity << " is used as boolQuantity";
				variable_found = true;
			}}}
			if (not variable_found)
			{
				LOG(WARNING) << "Could not parse a given variable. If you know what you are doing those subexpressions containing this variable will return true if you follow this instructions!";
				LOG(WARNING) << "comment out line 73 to 78, this will make this comment disappear!";
				LOG(FATAL) << "The lines above give a hint how to solve this problem. ExpressionParser only supports float, int and bool quantities and none of them matched your variable: " << *quantity;
			}
		}
// 		if(m_ExpressionNames.size() < settings.GetPlotlevelFilterExpressionQuantities().size())
	}
	
	template<typename T>
	void removeSubstrs(typename std::basic_string<T>& s,char p) const
	{
		typename std::basic_string<T>::size_type n = 1;
		for (typename std::basic_string<T>::size_type i = s.find(p); i != typename std::basic_string<T>().npos; i = s.find(p))
		{
			s.erase(i, n);
		}
	}
	
	bool evaluateSubExpression(std::string& expression, event_type const& event, product_type const& product, setting_type const& settings) const
	{
		bool OrIn = boost::algorithm::contains(expression, "||");
		bool back = false;
		if(OrIn)
		{
			LOG_N_TIMES(1,DEBUG) << "Subexpression contains || -> split and calculate subsubexpressions";
			std::vector<std::string> substrings;
			boost::algorithm::split(substrings, expression, boost::algorithm::is_any_of("||"));
			std::transform(substrings.begin(), substrings.end(), substrings.begin(),
					[](std::string s) { return boost::algorithm::trim_copy(s); });
			for (uint it = 0; it < substrings.size(); ++it)
				{
					std::string sexp = substrings[it];
					// substrings contains always on empty string after the splitting.
					// We need to skip this substring since the code fails otherwise.
					if(sexp == "")
						continue;
					LOG_N_TIMES(1,DEBUG) << "subexpression is " << sexp << " use || operation";
					back = back || evaluateSubExpression(sexp, event, product, settings);
				}
			return back;
		}
		else
		{
			LOG_N_TIMES(1,DEBUG) << "no further splitting of Substring, calculate expression " << expression;
			std::vector<std::string> substrings;
			boost::algorithm::split(substrings, expression, boost::algorithm::is_any_of(" "));
			std::transform(substrings.begin(), substrings.end(), substrings.begin(),
					[](std::string s) { return boost::algorithm::trim_copy(s); });
			for (unsigned int it = 0; it < substrings.size(); it++)
				{
					removeSubstrs(substrings[it], ')');
					removeSubstrs(substrings[it], '(');
				}
			uint position = 999;
			for(uint itstr = 0; itstr < m_ExpressionNames.size(); ++itstr)
			{
				if (substrings[0] == m_ExpressionNames[itstr])
				{
					position = itstr;
					break;
				}
			}
			if(position == 999){
				LOG(WARNING) << "Variable " << substrings[0] << " not found!";
				LOG(WARNING) << "Variable used in expression was not found in variable list, you might want to check if variable is already produced when this filter is run.";
				LOG(WARNING) << "If you are 100% sure that this variable is filled apropriatly and wiht a random number during runtime, you might comment out lines 138 to 141 and run again!";
				LOG(FATAL) << "expression " << expression << " was evaluated to " << true;
				return true;
			}
			double variable = (m_ExpressionQuantities[position])(event, product);
			float static_value = boost::lexical_cast<float>(substrings[2]);
			LOG_N_TIMES(1,DEBUG) << expression << " variable: " << m_ExpressionNames[position] << " = " << variable;
			std::string relation = substrings[1];
			if(relation == ">"){
				back = variable > static_value;
				LOG_N_TIMES(1,DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else if(relation == "<"){
				back = variable < static_value;
				LOG_N_TIMES(1,DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else if(relation == ">="){
				back = variable >= static_value;
				LOG_N_TIMES(1,DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else if(relation == "<="){
				back = variable <= static_value;
				LOG_N_TIMES(1,DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else
				LOG(FATAL) << "\tcould not parse relation sign " << relation;
			return true;
		}
	}
	virtual bool DoesEventPass(event_type const& event,
		product_type const& product, setting_type const& settings, metadata_type const& metadata) const override
		{
			(m_SubExpressions).clear();
			std::vector<std::string> temp_string;
			std::string temp_str = settings.GetPlotlevelFilterExpression();
			boost::algorithm::split(temp_string, temp_str, boost::algorithm::is_any_of("*"));
			std::transform(temp_string.begin(), temp_string.end(), temp_string.begin(),
						[](std::string s) { return boost::algorithm::trim_copy(s); });
			for(std::vector<std::string>::const_iterator pb = temp_string.begin(); pb != temp_string.end(); ++pb)
			{
				(m_SubExpressions).push_back(*pb);
			}
			bool back = true;
			for (uint it = 0; it < (m_SubExpressions).size(); ++it)
				{
					std::string sexp = (m_SubExpressions)[it];
					LOG_N_TIMES(1,DEBUG) << "\tevaluate subexpression " << sexp;
					back = back && evaluateSubExpression(sexp, event, product, settings);
				}
			return back;
		}

private:
	std::vector<float_extractor_lambda> m_ExpressionQuantities;
	std::vector<std::string> m_ExpressionNames;
	mutable std::vector<std::string> m_SubExpressions;
};
