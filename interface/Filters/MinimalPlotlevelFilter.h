
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
class MinimalPlotlevelFilter: public FilterBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	typedef std::function<float(event_type const&, product_type const&)> float_extractor_lambda;

	MinimalPlotlevelFilter(){}

	virtual std::string GetFilterId() const override {
            return "MinimalPlotlevelFilter";
    }

	void Init(setting_type const& settings) override
	{
		FilterBase<HttTypes>::Init(settings);
		// construct extractors vector
		m_ExpressionQuantities.clear();
		m_ExpressionNames.clear();
		for (std::vector<std::string>::const_iterator quantity = (settings.GetPlotlevelFilterExpressionQuantities)().begin();
			 quantity != (settings.GetPlotlevelFilterExpressionQuantities)().end(); ++quantity)
		{
// 			std::vector<std::string> splitted;
// 			boost::algorithm::split(splitted, *quantity, boost::algorithm::is_any_of(":="));
// 			std::transform(splitted.begin(), splitted.end(), splitted.begin(),
// 					  [](std::string s) { return boost::algorithm::trim_copy(s); });
// 			std::string *quantity = splitted.front();

			if (LambdaNtupleConsumer<HttTypes>::GetFloatQuantities().count(*quantity) > 0)
			{
				m_ExpressionQuantities.push_back(SafeMap::Get(LambdaNtupleConsumer<HttTypes>::GetFloatQuantities(), *quantity));
				m_ExpressionNames.push_back(*quantity);
				LOG(DEBUG) << "\t" << *quantity << " is used as floatQuantity";
			}
			else if(LambdaNtupleConsumer<HttTypes>::GetIntQuantities().count(*quantity) > 0)
			{
				m_ExpressionQuantities.push_back(SafeMap::Get(LambdaNtupleConsumer<HttTypes>::GetIntQuantities(), *quantity));
				m_ExpressionNames.push_back(*quantity);
				LOG(DEBUG) << "\t" << *quantity << " is used as intQuantity";
			}
			else if (LambdaNtupleConsumer<HttTypes>::GetBoolQuantities().count(*quantity) > 0)
			{
				m_ExpressionQuantities.push_back(SafeMap::Get(LambdaNtupleConsumer<HttTypes>::GetBoolQuantities(), *quantity));
				m_ExpressionNames.push_back(*quantity);
				LOG(DEBUG) << "\t" << *quantity << " is used as boolQuantity";
			}
// 			else
// 			{
// 				LOG(FATAL) << "ExpressionParser currently only supports float-type and int-type and bool input variables! " << *quantity;
// 			}
		}
		/*std::vector<std::string> temp_string;
		std::string temp_str = settings.GetPlotlevelFilterExpression();
		boost::algorithm::split(temp_string, temp_str, boost::algorithm::is_any_of("*"));
		std::transform(temp_string.begin(), temp_string.end(), temp_string.begin(),
					[](std::string s) { return boost::algorithm::trim_copy(s); });
		for(std::vector<std::string>::const_iterator pb = temp_string.begin(); pb != temp_string.end(); ++pb)
		{
			(m_SubExpressions).push_back(*pb);
		}*/
		if(m_ExpressionNames.size() < settings.GetPlotlevelFilterExpressionQuantities().size())
			LOG(WARNING) << "Could not parse a given Variables, subexpressions containing this variable will return true!";
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
			LOG(DEBUG) << "Subexpression contains || -> split and calculate subsubexpressions";
			std::vector<std::string> substrings;
			boost::algorithm::split(substrings, expression, boost::algorithm::is_any_of("||"));
			std::transform(substrings.begin(), substrings.end(), substrings.begin(),
					[](std::string s) { return boost::algorithm::trim_copy(s); });

			for (uint it = 0; it < substrings.size(); ++it)
				{
					std::string sexp = substrings[it];
					LOG(DEBUG) << "subexpression is " << sexp << " use || operation";
					back = back || evaluateSubExpression(sexp, event, product, settings);
				}
			return back;
		}
		else
		{
			LOG(DEBUG) << "no further splitting of Substring, calculate expression " << expression;
			std::vector<std::string> substrings;
			boost::algorithm::split(substrings, expression, boost::algorithm::is_any_of(" "));
			std::transform(substrings.begin(), substrings.end(), substrings.begin(),
					[](std::string s) { return boost::algorithm::trim_copy(s); });
			for (int it = 0; it < 3; it++)
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
				LOG_N_TIMES(5, WARNING) << "Variable " << substrings[0] << " not found!";
				LOG_N_TIMES(5, WARNING) << "Variable used in expression was not found in variable list, you might want to check if variable is already produced when this filter is run.";
				LOG_N_TIMES(5, WARNING) << "expression " << expression << " was evaluated to " << true;
				return true;
			}
			double variable = (m_ExpressionQuantities[position])(event, product);
			float static_value = boost::lexical_cast<float>(substrings[2]);
			LOG(DEBUG) << expression << " variable: " << m_ExpressionNames[position] << " = " << variable;
			std::string relation = substrings[1];
			if(relation == ">"){
				back = variable > static_value;
				LOG(DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else if(relation == "<"){
				back = variable < static_value;
				LOG(DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else if(relation == ">="){
				back = variable >= static_value;
				LOG(DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else if(relation == "<="){
				back = variable <= static_value;
				LOG(DEBUG) << "\tExpression " << expression << " was evaluated to " << back;
				return back;}
			else
				LOG(WARNING) << "\tcould not parse relation sign " << relation;
			return true;
		}
	}
		virtual bool DoesEventPass(event_type const& event,
		product_type const& product, setting_type const& settings) const override
		{
// 			if(m_ExpressionNames.size() < settings.GetPlotlevelFilterExpressionQuantities().size())
// 				return true;
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
					LOG(DEBUG) << "\tevaluate subexpression " << sexp;
					back = back && evaluateSubExpression(sexp, event, product, settings);
				}
			return back;
		}

private:
	std::vector<float_extractor_lambda> m_ExpressionQuantities;
	std::vector<std::string> m_ExpressionNames;
	mutable std::vector<std::string> m_SubExpressions;

};