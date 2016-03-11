#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/AcceptanceEfficiencyConsumer.h"

std::string AcceptanceEfficiencyConsumer::GetConsumerId() const
{
	return "AcceptanceEfficiencyConsumer";
}

void AcceptanceEfficiencyConsumer::Init(setting_type const& settings)
{
	acc_eff_hist = new TH2D("acc_eff_hist", "acc_eff_hist", 50,0.,200.,50,0.,200);
	number_of_passed_hist = new TH2D("number_of_passed_hist", "number_of_passed_hist", 50,0.,200.,50,0.,200);
	number_of_entries_hist = new TH2D("number_of_entries_hist", "number_of_entries_hist", 50,0.,200.,50,0.,200);
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
		//std::cout << event.m_genEventInfo->weight << std::endl;
		return event.m_genEventInfo->weight;
	});
	LambdaNtupleConsumer<HttTypes>::Init(settings);
}

void AcceptanceEfficiencyConsumer::ProcessFilteredEvent(event_type const& event, product_type const& product, setting_type const& settings)
{
	double PtMinus = product.m_accEffTauMinus->p4.Pt();
	double PtPlus = product.m_accEffTauPlus->p4.Pt();
	double weight = event.m_genEventInfo->weight;
	if ((PtMinus > 80 && PtPlus > 80) || weight > 0.7)
	{
		//std::cout << "PtMinus = " << PtMinus << " PtPlus = " << PtPlus << " weight = " << weight << std::endl; 
	}
	//std::cout << "Attempts passed: " << int(weight*nAttempts) << std::endl;
	for(unsigned int i = 0; i<nAttempts; ++i)
	{
		if (double(i)/double(nAttempts) < weight) number_of_passed_hist->Fill(PtMinus, PtPlus);
		number_of_entries_hist->Fill(PtMinus, PtPlus);
	}
	LambdaNtupleConsumer<HttTypes>::ProcessFilteredEvent(event, product, settings);
}

void AcceptanceEfficiencyConsumer::Finish(setting_type const& settings)
{
	LambdaNtupleConsumer::Finish(settings);
	RootFileHelper::SafeCd(settings.GetRootOutFile(), settings.GetRootFileFolder());
	acc_eff_hist->Divide(number_of_passed_hist,number_of_entries_hist,1.,1.,"B");
	number_of_passed_hist->Write();
	number_of_entries_hist->Write();
	acc_eff_hist->Write();
}
