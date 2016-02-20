#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/AcceptanceEfficiencyConsumer.h"

std::string AcceptanceEfficiencyConsumer::GetConsumerId() const
{
	return "AcceptanceEfficiencyConsumer";
}

void AcceptanceEfficiencyConsumer::Init(setting_type const& settings)
{
	acc_eff_hist = new TH2F("acc_eff_hist", "acc_eff_hist", 50,0.,100.,50,0.,100);
	number_of_passed_hist = new TH2F("number_of_passed_hist", "number_of_passed_hist", 50,0.,100.,50,0.,100);
	number_of_entries_hist = new TH2F("number_of_entries_hist", "number_of_entries_hist", 50,0.,100.,50,0.,100);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("PtTauMinus",[](event_type const& event, product_type const& product)
	{
		return product.m_accEffTauMinus->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("PtTauPlus",[](event_type const& event, product_type const& product)
	{
		return product.m_accEffTauPlus->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("accEfficiency",[](event_type const& event, product_type const& product)
	{
		std::cout << event.m_genEventInfo->weight << std::endl;
		return event.m_genEventInfo->weight;
	});
	LambdaNtupleConsumer<HttTypes>::Init(settings);
}

void AcceptanceEfficiencyConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings)
{
	double PtMinus = product.m_accEffTauMinus->p4.Pt();
	double PtPlus = product.m_accEffTauPlus->p4.Pt();
	double weight = event.m_genEventInfo->weight;
	std::cout << "Attempts passed: " << int(weight*nAttempts) << std::endl;
	for(int i = 0; i<int(weight*nAttempts); ++i)
	{
		number_of_passed_hist->Fill(PtMinus, PtPlus);
	}
	for(unsigned int i = 0; i<nAttempts; ++i)
	{
		number_of_entries_hist->Fill(PtMinus, PtPlus);
	}
	acc_eff_hist->Divide(number_of_passed_hist,number_of_entries_hist,1.,1.,"B");
	LambdaNtupleConsumer<HttTypes>::ProcessFilteredEvent(event, product, settings);
}

void AcceptanceEfficiencyConsumer::Finish(setting_type const& settings)
{
	LambdaNtupleConsumer::Finish(settings);
	RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
	number_of_passed_hist->Write();
	number_of_entries_hist->Write();
	acc_eff_hist->Write();
}
