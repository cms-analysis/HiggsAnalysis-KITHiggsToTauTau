
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/UnitConverter.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsCPinTauDecays/ImpactParameter/interface/ImpactParameter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/IsomorphicMappingProducer.h"

#include <fstream>

std::string IsomorphicMappingProducer::GetProducerId() const
{
	return "IsomorphicMappingProducer";
}

void IsomorphicMappingProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	m_isData = settings.GetInputIsData();

	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);

	std::string ip_r_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/nominal/IP_1_R__.root");
	std::string ip_phi_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/nominal/IP_1_Phi__.root");
	std::string ip_theta_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/nominal/IP_1_Theta__.root");
	std::string ip_r_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/nominal/IP_2_R__.root");
	std::string ip_phi_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/nominal/IP_2_Phi__.root");
	std::string ip_theta_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/nominal/IP_2_Theta__.root");

	TFile inputFile_ip1_r(ip_r_str_1.c_str(), "READ");
	ip_1_r_isomap = static_cast<TGraph*>(inputFile_ip1_r.Get("isomap"));
	inputFile_ip1_r.Close();

	TFile inputFile_ip1_theta(ip_theta_str_1.c_str(), "READ");
	ip_1_theta_isomap = static_cast<TGraph*>(inputFile_ip1_theta.Get("isomap"));
	inputFile_ip1_theta.Close();

	TFile inputFile_ip1_phi(ip_phi_str_1.c_str(), "READ");
	ip_1_phi_isomap = static_cast<TGraph*>(inputFile_ip1_phi.Get("isomap"));
	inputFile_ip1_phi.Close();

	TFile inputFile_ip2_r(ip_r_str_2.c_str(), "READ");
	ip_2_r_isomap = static_cast<TGraph*>(inputFile_ip2_r.Get("isomap"));
	inputFile_ip2_r.Close();

	TFile inputFile_ip2_theta(ip_theta_str_2.c_str(), "READ");
	ip_2_theta_isomap = static_cast<TGraph*>(inputFile_ip2_theta.Get("isomap"));
	inputFile_ip2_theta.Close();

	TFile inputFile_ip2_phi(ip_phi_str_2.c_str(), "READ");
	ip_2_phi_isomap = static_cast<TGraph*>(inputFile_ip2_phi.Get("isomap"));
	inputFile_ip2_phi.Close();

	std::string iprPV_r_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPV/IPrPV_1_R__.root");
	std::string iprPV_phi_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPV/IPrPV_1_Phi__.root");
	std::string iprPV_theta_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPV/IPrPV_1_Theta__.root");
	std::string iprPV_r_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPV/IPrPV_2_R__.root");
	std::string iprPV_phi_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPV/IPrPV_2_Phi__.root");
	std::string iprPV_theta_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPV/IPrPV_2_Theta__.root");

	TFile inputFile_iprPV1_r(iprPV_r_str_1.c_str(), "READ");
	iprPV_1_r_isomap = static_cast<TGraph*>(inputFile_iprPV1_r.Get("isomap"));
	inputFile_iprPV1_r.Close();

	TFile inputFile_iprPV1_theta(iprPV_theta_str_1.c_str(), "READ");
	iprPV_1_theta_isomap = static_cast<TGraph*>(inputFile_iprPV1_theta.Get("isomap"));
	inputFile_iprPV1_theta.Close();

	TFile inputFile_iprPV1_phi(iprPV_phi_str_1.c_str(), "READ");
	iprPV_1_phi_isomap = static_cast<TGraph*>(inputFile_iprPV1_phi.Get("isomap"));
	inputFile_iprPV1_phi.Close();

	TFile inputFile_iprPV2_r(iprPV_r_str_2.c_str(), "READ");
	iprPV_2_r_isomap = static_cast<TGraph*>(inputFile_iprPV2_r.Get("isomap"));
	inputFile_iprPV2_r.Close();

	TFile inputFile_iprPV2_theta(iprPV_theta_str_2.c_str(), "READ");
	iprPV_2_theta_isomap = static_cast<TGraph*>(inputFile_iprPV2_theta.Get("isomap"));
	inputFile_iprPV2_theta.Close();

	TFile inputFile_iprPV2_phi(iprPV_phi_str_2.c_str(), "READ");
	iprPV_2_phi_isomap = static_cast<TGraph*>(inputFile_iprPV2_phi.Get("isomap"));
	inputFile_iprPV2_phi.Close();

	std::string iprPVBS_r_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPVBS/IPrPVBS_1_R__.root");
	std::string iprPVBS_phi_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPVBS/IPrPVBS_1_Phi__.root");
	std::string iprPVBS_theta_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPVBS/IPrPVBS_1_Theta__.root");
	std::string iprPVBS_r_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPVBS/IPrPVBS_2_R__.root");
	std::string iprPVBS_phi_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPVBS/IPrPVBS_2_Phi__.root");
	std::string iprPVBS_theta_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/refitPVBS/IPrPVBS_2_Theta__.root");

	TFile inputFile_iprPVBS1_r(iprPVBS_r_str_1.c_str(), "READ");
	iprPVBS_1_r_isomap = static_cast<TGraph*>(inputFile_iprPVBS1_r.Get("isomap"));
	inputFile_iprPVBS1_r.Close();

	TFile inputFile_iprPVBS1_theta(iprPVBS_theta_str_1.c_str(), "READ");
	iprPVBS_1_theta_isomap = static_cast<TGraph*>(inputFile_iprPVBS1_theta.Get("isomap"));
	inputFile_iprPVBS1_theta.Close();

	TFile inputFile_iprPVBS1_phi(iprPVBS_phi_str_1.c_str(), "READ");
	iprPVBS_1_phi_isomap = static_cast<TGraph*>(inputFile_iprPVBS1_phi.Get("isomap"));
	inputFile_iprPVBS1_phi.Close();

	TFile inputFile_iprPVBS2_r(iprPVBS_r_str_2.c_str(), "READ");
	iprPVBS_2_r_isomap = static_cast<TGraph*>(inputFile_iprPVBS2_r.Get("isomap"));
	inputFile_iprPVBS2_r.Close();

	TFile inputFile_iprPVBS2_theta(iprPVBS_theta_str_2.c_str(), "READ");
	iprPVBS_2_theta_isomap = static_cast<TGraph*>(inputFile_iprPVBS2_theta.Get("isomap"));
	inputFile_iprPVBS2_theta.Close();

	TFile inputFile_iprPVBS2_phi(iprPVBS_phi_str_2.c_str(), "READ");
	iprPVBS_2_phi_isomap = static_cast<TGraph*>(inputFile_iprPVBS2_phi.Get("isomap"));
	inputFile_iprPVBS2_phi.Close();

	std::string ipHel_r_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/Helnominal/IPHel_1_R__.root");
	std::string ipHel_phi_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/Helnominal/IPHel_1_Phi__.root");
	std::string ipHel_theta_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/Helnominal/IPHel_1_Theta__.root");
	std::string ipHel_r_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/Helnominal/IPHel_2_R__.root");
	std::string ipHel_phi_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/Helnominal/IPHel_2_Phi__.root");
	std::string ipHel_theta_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/Helnominal/IPHel_2_Theta__.root");

	TFile inputFile_ipHel1_r(ipHel_r_str_1.c_str(), "READ");
	ipHel_1_r_isomap = static_cast<TGraph*>(inputFile_ipHel1_r.Get("isomap"));
	inputFile_ipHel1_r.Close();

	TFile inputFile_ipHel1_theta(ipHel_theta_str_1.c_str(), "READ");
	ipHel_1_theta_isomap = static_cast<TGraph*>(inputFile_ipHel1_theta.Get("isomap"));
	inputFile_ipHel1_theta.Close();

	TFile inputFile_ipHel1_phi(ipHel_phi_str_1.c_str(), "READ");
	ipHel_1_phi_isomap = static_cast<TGraph*>(inputFile_ipHel1_phi.Get("isomap"));
	inputFile_ipHel1_phi.Close();

	TFile inputFile_ipHel2_r(ipHel_r_str_2.c_str(), "READ");
	ipHel_2_r_isomap = static_cast<TGraph*>(inputFile_ipHel2_r.Get("isomap"));
	inputFile_ipHel2_r.Close();

	TFile inputFile_ipHel2_theta(ipHel_theta_str_2.c_str(), "READ");
	ipHel_2_theta_isomap = static_cast<TGraph*>(inputFile_ipHel2_theta.Get("isomap"));
	inputFile_ipHel2_theta.Close();

	TFile inputFile_ipHel2_phi(ipHel_phi_str_2.c_str(), "READ");
	ipHel_2_phi_isomap = static_cast<TGraph*>(inputFile_ipHel2_phi.Get("isomap"));
	inputFile_ipHel2_phi.Close();

	std::string ipHelrPV_r_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPV/IPHelrPV_1_R__.root");
	std::string ipHelrPV_phi_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPV/IPHelrPV_1_Phi__.root");
	std::string ipHelrPV_theta_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPV/IPHelrPV_1_Theta__.root");
	std::string ipHelrPV_r_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPV/IPHelrPV_2_R__.root");
	std::string ipHelrPV_phi_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPV/IPHelrPV_2_Phi__.root");
	std::string ipHelrPV_theta_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPV/IPHelrPV_2_Theta__.root");

	TFile inputFile_ipHelrPV1_r(ipHelrPV_r_str_1.c_str(), "READ");
	ipHelrPV_1_r_isomap = static_cast<TGraph*>(inputFile_ipHelrPV1_r.Get("isomap"));
	inputFile_ipHelrPV1_r.Close();

	TFile inputFile_ipHelrPV1_theta(ipHelrPV_theta_str_1.c_str(), "READ");
	ipHelrPV_1_theta_isomap = static_cast<TGraph*>(inputFile_ipHelrPV1_theta.Get("isomap"));
	inputFile_ipHelrPV1_theta.Close();

	TFile inputFile_ipHelrPV1_phi(ipHelrPV_phi_str_1.c_str(), "READ");
	ipHelrPV_1_phi_isomap = static_cast<TGraph*>(inputFile_ipHelrPV1_phi.Get("isomap"));
	inputFile_ipHelrPV1_phi.Close();

	TFile inputFile_ipHelrPV2_r(ipHelrPV_r_str_2.c_str(), "READ");
	ipHelrPV_2_r_isomap = static_cast<TGraph*>(inputFile_ipHelrPV2_r.Get("isomap"));
	inputFile_ipHelrPV2_r.Close();

	TFile inputFile_ipHelrPV2_theta(ipHelrPV_theta_str_2.c_str(), "READ");
	ipHelrPV_2_theta_isomap = static_cast<TGraph*>(inputFile_ipHelrPV2_theta.Get("isomap"));
	inputFile_ipHelrPV2_theta.Close();

	TFile inputFile_ipHelrPV2_phi(ipHelrPV_phi_str_2.c_str(), "READ");
	ipHelrPV_2_phi_isomap = static_cast<TGraph*>(inputFile_ipHelrPV2_phi.Get("isomap"));
	inputFile_ipHelrPV2_phi.Close();

	std::string ipHelrPVBS_r_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPVBS/IPHelrPVBS_1_R__.root");
	std::string ipHelrPVBS_phi_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPVBS/IPHelrPVBS_1_Phi__.root");
	std::string ipHelrPVBS_theta_str_1 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPVBS/IPHelrPVBS_1_Theta__.root");
	std::string ipHelrPVBS_r_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPVBS/IPHelrPVBS_2_R__.root");
	std::string ipHelrPVBS_phi_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPVBS/IPHelrPVBS_2_Phi__.root");
	std::string ipHelrPVBS_theta_str_2 = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/HelrPVBS/IPHelrPVBS_2_Theta__.root");

	TFile inputFile_ipHelrPVBS1_r(ipHelrPVBS_r_str_1.c_str(), "READ");
	ipHelrPVBS_1_r_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS1_r.Get("isomap"));
	inputFile_ipHelrPVBS1_r.Close();

	TFile inputFile_ipHelrPVBS1_theta(ipHelrPVBS_theta_str_1.c_str(), "READ");
	ipHelrPVBS_1_theta_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS1_theta.Get("isomap"));
	inputFile_ipHelrPVBS1_theta.Close();

	TFile inputFile_ipHelrPVBS1_phi(ipHelrPVBS_phi_str_1.c_str(), "READ");
	ipHelrPVBS_1_phi_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS1_phi.Get("isomap"));
	inputFile_ipHelrPVBS1_phi.Close();

	TFile inputFile_ipHelrPVBS2_r(ipHelrPVBS_r_str_2.c_str(), "READ");
	ipHelrPVBS_2_r_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS2_r.Get("isomap"));
	inputFile_ipHelrPVBS2_r.Close();

	TFile inputFile_ipHelrPVBS2_theta(ipHelrPVBS_theta_str_2.c_str(), "READ");
	ipHelrPVBS_2_theta_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS2_theta.Get("isomap"));
	inputFile_ipHelrPVBS2_theta.Close();

	TFile inputFile_ipHelrPVBS2_phi(ipHelrPVBS_phi_str_2.c_str(), "READ");
	ipHelrPVBS_2_phi_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS2_phi.Get("isomap"));
	inputFile_ipHelrPVBS2_phi.Close();

	gDirectory = savedir;
	gFile = savefile;

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIP_1).x() != -999) ? RMPoint( (product.m_calibIP_1).x(), (product.m_calibIP_1).y(), (product.m_calibIP_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIP_2).x() != -999) ? RMPoint( (product.m_calibIP_2).x(), (product.m_calibIP_2).y(), (product.m_calibIP_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPrPV_1).x() != -999) ? RMPoint( (product.m_calibIPrPV_1).x(), (product.m_calibIPrPV_1).y(), (product.m_calibIPrPV_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPrPV_2).x() != -999) ? RMPoint( (product.m_calibIPrPV_2).x(), (product.m_calibIPrPV_2).y(), (product.m_calibIPrPV_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPrPVBS_1).x() != -999) ? RMPoint( (product.m_calibIPrPVBS_1).x(), (product.m_calibIPrPVBS_1).y(), (product.m_calibIPrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPrPVBS_2).x() != -999) ? RMPoint( (product.m_calibIPrPVBS_2).x(), (product.m_calibIPrPVBS_2).y(), (product.m_calibIPrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHel_1).x() != -999) ? RMPoint( (product.m_calibIPHel_1).x(), (product.m_calibIPHel_1).y(), (product.m_calibIPHel_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHel_2).x() != -999) ? RMPoint( (product.m_calibIPHel_2).x(), (product.m_calibIPHel_2).y(), (product.m_calibIPHel_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPV_1).x() != -999) ? RMPoint( (product.m_calibIPHelrPV_1).x(), (product.m_calibIPHelrPV_1).y(), (product.m_calibIPHelrPV_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPV_2).x() != -999) ? RMPoint( (product.m_calibIPHelrPV_2).x(), (product.m_calibIPHelrPV_2).y(), (product.m_calibIPHelrPV_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPVBS_1).x() != -999) ? RMPoint( (product.m_calibIPHelrPVBS_1).x(), (product.m_calibIPHelrPVBS_1).y(), (product.m_calibIPHelrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPVBS_2).x() != -999) ? RMPoint( (product.m_calibIPHelrPVBS_2).x(), (product.m_calibIPHelrPVBS_2).y(), (product.m_calibIPHelrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	// CP-related quantities
	// IP-Method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCP", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPHelrPVBS;
	});
	// Combined Method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPComb", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPComb;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMerged", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMerged;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedHelrPVBS;
	});


}

void IsomorphicMappingProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	if (!m_isData){
		assert(event.m_vertexSummary);
		assert(product.m_flavourOrderedLeptons.size() >= 2);

		// initialization of TVector3 objects
		//FIXME These Vectors are only needed for the helical approach
		TVector3 IPPlus;
		TVector3 IPMinus;
		TVector3 IPPlusHel;
		TVector3 IPMinusHel;
		TVector3 IPPlusrPV;
		TVector3 IPMinusrPV;
		TVector3 IPPlusHelrPV;
		TVector3 IPMinusHelrPV;
		TVector3 IPPlusrPVBS;
		TVector3 IPMinusrPVBS;
		TVector3 IPPlusHelrPVBS;
		TVector3 IPMinusHelrPVBS;

		IPPlus.SetXYZ(-999,-999,-999);
		IPMinus.SetXYZ(-999,-999,-999);
		IPPlusHel.SetXYZ(-999,-999,-999);
		IPMinusHel.SetXYZ(-999,-999,-999);
		IPPlusrPV.SetXYZ(-999,-999,-999);
		IPMinusrPV.SetXYZ(-999,-999,-999);
		IPPlusHelrPV.SetXYZ(-999,-999,-999);
		IPMinusHelrPV.SetXYZ(-999,-999,-999);
		IPPlusrPVBS.SetXYZ(-999,-999,-999);
		IPMinusrPVBS.SetXYZ(-999,-999,-999);
		IPPlusHelrPVBS.SetXYZ(-999,-999,-999);
		IPMinusHelrPVBS.SetXYZ(-999,-999,-999);

		product.m_calibIP_1.SetXYZ(-999, -999, -999);
		product.m_calibIP_2.SetXYZ(-999, -999, -999);
		product.m_calibIPrPV_1.SetXYZ(-999, -999, -999);
		product.m_calibIPrPV_2.SetXYZ(-999, -999, -999);
		product.m_calibIPrPVBS_1.SetXYZ(-999, -999, -999);
		product.m_calibIPrPVBS_2.SetXYZ(-999, -999, -999);
		product.m_calibIPHel_1.SetXYZ(-999, -999, -999);
		product.m_calibIPHel_2.SetXYZ(-999, -999, -999);
		product.m_calibIPHelrPV_1.SetXYZ(-999, -999, -999);
		product.m_calibIPHelrPV_2.SetXYZ(-999, -999, -999);
		product.m_calibIPHelrPVBS_1.SetXYZ(-999, -999, -999);
		product.m_calibIPHelrPVBS_2.SetXYZ(-999, -999, -999);



		// reconstructed leptons
		KLepton* recoParticle1 = product.m_flavourOrderedLeptons.at(0);
		KLepton* recoParticle2 = product.m_flavourOrderedLeptons.at(1);
		KLepton* chargedPart1  = product.m_chargeOrderedLeptons.at(0);
		KLepton* chargedPart2  = product.m_chargeOrderedLeptons.at(1);
		KTrack trackP = chargedPart1->track; // in case of tau_h, the track of the lead. prong is saved in the KTau track member
		KTrack trackM = chargedPart2->track;
		RMFLV momentumP = ((chargedPart1->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart1)->chargedHadronCandidates.at(0).p4 : chargedPart1->p4);
		RMFLV momentumM = ((chargedPart2->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart2)->chargedHadronCandidates.at(0).p4 : chargedPart2->p4);

		// Defining CPQuantities object to use variables and functions of this class
		CPQuantities cpq;
		// ImpactParameter ip;

		// ---------
		// Calibration of IPs (nominal PV)
		// ---------

		product.m_calibIP_1.SetMagThetaPhi(ip_1_r_isomap->Eval(product.m_recoIP1.Mag()),
					ip_1_theta_isomap->Eval(product.m_recoIP1.Theta()),
					ip_1_phi_isomap->Eval(product.m_recoIP1.Phi())
		);

		// product.m_calibIP_2.SetMagThetaPhi(ip_2_r_isomap->Eval(product.m_recoIP2.Mag()),
		// 			ip_2_theta_isomap->Eval(product.m_recoIP2.Theta()),
		// 			ip_2_phi_isomap->Eval(product.m_recoIP2.Phi())
		// );

		product.m_calibIPHel_1.SetMagThetaPhi(ipHel_1_r_isomap->Eval(product.m_recoIPHel_1.Mag()),
					ipHel_1_theta_isomap->Eval(product.m_recoIPHel_1.Theta()),
					ipHel_1_phi_isomap->Eval(product.m_recoIPHel_1.Phi())
		);

		// product.m_calibIPHel_2.SetMagThetaPhi(ipHel_2_r_isomap->Eval(product.m_recoIPHel_2.Mag()),
		// 			ipHel_2_theta_isomap->Eval(product.m_recoIPHel_2.Theta()),
		// 			ipHel_2_phi_isomap->Eval(product.m_recoIPHel_2.Phi())
		// );

		// ---------
		// Calculation of phi*cp with calibrated IPs
		// ---------

		// Calculate the phi*cp by taking the ipvectors from the helical approach as arguments
		if (recoParticle1->getHash() == chargedPart1->getHash()){
			IPPlus  = product.m_calibIP_1;
			IPMinus = product.m_calibIP_2;
			IPPlusHel  = product.m_calibIPHel_1;
			IPMinusHel = product.m_calibIPHel_2;
		} else {
			IPPlus  = product.m_calibIP_2;
			IPMinus = product.m_calibIP_1;
			IPPlusHel  = product.m_calibIPHel_2;
			IPMinusHel = product.m_calibIPHel_1;
		}
		product.m_calibPhiStarCP= cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlus, IPMinus, "reco");
		product.m_calibPhiStarCPHel = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHel, IPMinusHel, "reco");

		// ---------
		// comb-method
		// ---------
		KTau* recoTau1 = static_cast<KTau*>(recoParticle1);
		KTau* recoTau2 = static_cast<KTau*>(recoParticle2);
		if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET || recoTau2->decayMode == 1){

			product.m_calibPhiStarCPComb    = cpq.CalculatePhiStarCPComb(product.m_calibIP_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_calibPhiStarCPCombHel = cpq.CalculatePhiStarCPComb(product.m_calibIPHel_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

			product.m_calibPhiStarCPCombMerged    = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPComb, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			product.m_calibPhiStarCPCombMergedHel = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombHel, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

		}  // if et or mt ch.

		if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
			KTau* recoTau1 = static_cast<KTau*>(recoParticle1);

			// tau1->rho, tau2->a
			if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
				product.m_calibPhiStarCPComb    = cpq.CalculatePhiStarCPComb(product.m_calibIP_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
				product.m_calibPhiStarCPCombHel = cpq.CalculatePhiStarCPComb(product.m_calibIPHel_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());

				product.m_calibPhiStarCPCombMerged    = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPComb, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_calibPhiStarCPCombMergedHel = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHel, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			} // tau1->rho, tau2->a

			// tau1->a, tau2->rho
			if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
				product.m_calibPhiStarCPComb    = cpq.CalculatePhiStarCPComb(product.m_calibIP_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_calibPhiStarCPCombHel = cpq.CalculatePhiStarCPComb(product.m_calibIPHel_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

				product.m_calibPhiStarCPCombMerged = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPComb, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_calibPhiStarCPCombMergedHel = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHel, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			} // tau1->a, tau2->rho

		}  // if tt ch.




		if (product.m_refitPV != nullptr){
			product.m_calibIPrPV_1.SetMagThetaPhi(iprPV_1_r_isomap->Eval(product.m_recoIPrPV_1.Mag()),
						iprPV_1_theta_isomap->Eval(product.m_recoIPrPV_1.Theta()),
						iprPV_1_phi_isomap->Eval(product.m_recoIPrPV_1.Phi())
			);
			// product.m_calibIPrPV_2.SetMagThetaPhi(iprPV_2_r_isomap->Eval(product.m_recoIPrPV_2.Mag()),
			// 			iprPV_2_theta_isomap->Eval(product.m_recoIPrPV_2.Theta()),
			// 			iprPV_2_phi_isomap->Eval(product.m_recoIPrPV_2.Phi())
			// );

			product.m_calibIPrPVBS_1.SetMagThetaPhi(iprPVBS_1_r_isomap->Eval(product.m_recoIPrPVBS_1.Mag()),
							iprPVBS_1_theta_isomap->Eval(product.m_recoIPrPVBS_1.Theta()),
							iprPVBS_1_phi_isomap->Eval(product.m_recoIPrPVBS_1.Phi())
			);
			// product.m_calibIPrPVBS_2.SetMagThetaPhi(iprPVBS_2_r_isomap->Eval(product.m_recoIP2.Mag()),
			// 				iprPVBS_2_theta_isomap->Eval(product.m_recoIPrPVBS_2.Theta()),
			// 				iprPVBS_2_phi_isomap->Eval(product.m_recoIPrPVBS_2.Phi())
			// );

			product.m_calibIPHelrPV_1.SetMagThetaPhi(ipHelrPV_1_r_isomap->Eval(product.m_recoIPHelrPV_1.Mag()),
						ipHelrPV_1_theta_isomap->Eval(product.m_recoIPHelrPV_1.Theta()),
						ipHelrPV_1_phi_isomap->Eval(product.m_recoIPHelrPV_1.Phi())
			);
			// product.m_calibIPHelrPV_2.SetMagThetaPhi(ipHelrPV_2_r_isomap->Eval(product.m_recoIPHelrPV_2.Mag()),
			// 			ipHelrPV_2_theta_isomap->Eval(product.m_recoIPHelrPV_2.Theta()),
			// 			ipHelrPV_2_phi_isomap->Eval(product.m_recoIPHelrPV_2.Phi())
			// );

			product.m_calibIPHelrPVBS_1.SetMagThetaPhi(ipHelrPVBS_1_r_isomap->Eval(product.m_recoIPHelrPVBS_1.Mag()),
							ipHelrPVBS_1_theta_isomap->Eval(product.m_recoIPHelrPVBS_1.Theta()),
							ipHelrPVBS_1_phi_isomap->Eval(product.m_recoIPHelrPVBS_1.Phi())
			);
			// product.m_calibIPHelrPVBS_2.SetMagThetaPhi(ipHelrPVBS_2_r_isomap->Eval(product.m_recoIP2.Mag()),
			// 				ipHelrPVBS_2_theta_isomap->Eval(product.m_recoIPHelrPVBS_2.Theta()),
			// 				ipHelrPVBS_2_phi_isomap->Eval(product.m_recoIPHelrPVBS_2.Phi())
			// );
			if (recoParticle1->getHash() == chargedPart1->getHash()){
				IPPlusrPV  = product.m_calibIPrPV_1;
				IPMinusrPV = product.m_calibIPrPV_2;
				IPPlusrPVBS  = product.m_calibIPrPVBS_1;
				IPMinusrPVBS = product.m_calibIPrPVBS_2;
				IPPlusHelrPV  = product.m_calibIPHelrPV_1;
				IPMinusHelrPV = product.m_calibIPHelrPV_2;
				IPPlusHelrPVBS  = product.m_calibIPHelrPVBS_1;
				IPMinusHelrPVBS = product.m_calibIPHelrPVBS_2;
			} else {
				IPPlusrPV  = product.m_calibIPrPV_2;
				IPMinusrPV = product.m_calibIPrPV_1;
				IPPlusrPVBS  = product.m_calibIPrPVBS_2;
				IPMinusrPVBS = product.m_calibIPrPVBS_1;
				IPPlusHelrPV  = product.m_calibIPHelrPV_2;
				IPMinusHelrPV = product.m_calibIPHelrPV_1;
				IPPlusHelrPVBS  = product.m_calibIPHelrPVBS_2;
				IPMinusHelrPVBS = product.m_calibIPHelrPVBS_1;
			}
			product.m_calibPhiStarCPrPV = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusrPV, IPMinusrPV, "reco");
			product.m_calibPhiStarCPrPVBS = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusrPVBS, IPMinusrPVBS, "reco");
			product.m_calibPhiStarCPHelrPV = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPV, IPMinusHelrPV, "reco");
			product.m_calibPhiStarCPHelrPVBS = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPVBS, IPMinusHelrPVBS, "reco");

			// ---------
			// comb-method - with refitted PV
			// ---------
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET || recoTau2->decayMode == 1){
				KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

				product.m_calibPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_calibIPrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_calibPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_calibIPrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_calibPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

				product.m_calibPhiStarCPCombMergedrPV      = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombrPV, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_calibPhiStarCPCombMergedrPVBS    = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombrPVBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_calibPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombHelrPV, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombHelrPVBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			}
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
				// tau1->rho, tau2->a
				if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
					product.m_calibPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_calibIPrPV_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
					product.m_calibPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_calibIPrPVBS_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
					product.m_calibPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPV_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
					product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());

					product.m_calibPhiStarCPCombMergedrPV      = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedrPVBS    = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}
				// tau1->a, tau2->rho
				if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
					product.m_calibPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_calibIPrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
					product.m_calibPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_calibIPrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
					product.m_calibPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
					product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

					product.m_calibPhiStarCPCombMergedrPV      = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedrPVBS    = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}

			}  // if tt ch.

		} // if refitPV exists
	} // is not data
	else{
		product.m_calibIP_1 = product.m_recoIP1;
		product.m_calibIP_2 = product.m_recoIP2;
		product.m_calibIPrPV_1 = product.m_recoIPrPV_1;
		product.m_calibIPrPV_2 = product.m_recoIPrPV_2;
		product.m_calibIPrPVBS_1 = product.m_recoIPrPVBS_1;
		product.m_calibIPrPVBS_2 = product.m_recoIPrPVBS_2;
		product.m_calibIPHel_1 = product.m_recoIPHel_1;
		product.m_calibIPHel_2 = product.m_recoIPHel_2;
		product.m_calibIPHelrPV_1 = product.m_recoIPHelrPV_1;
		product.m_calibIPHelrPV_2 = product.m_recoIPHelrPV_2;
		product.m_calibIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1;
		product.m_calibIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;

		product.m_calibPhiStarCP                   = product.m_recoPhiStarCP;
		product.m_calibPhiStarCPHel                = product.m_recoPhiStarCPHel;
		product.m_calibPhiStarCPrPV                = product.m_recoPhiStarCPrPV;
		product.m_calibPhiStarCPHelrPV             = product.m_recoPhiStarCPHelrPV;
		product.m_calibPhiStarCPrPVBS              = product.m_recoPhiStarCPrPVBS;
		product.m_calibPhiStarCPHelrPVBS           = product.m_recoPhiStarCPHelrPVBS;
		product.m_calibPhiStarCPComb               = product.m_recoPhiStarCPComb;
		product.m_calibPhiStarCPCombMerged         = product.m_recoPhiStarCPCombMerged;
		product.m_calibPhiStarCPCombrPV            = product.m_recoPhiStarCPCombrPV;
		product.m_calibPhiStarCPCombMergedrPV      = product.m_recoPhiStarCPCombMergedrPV;
		product.m_calibPhiStarCPCombrPVBS          = product.m_recoPhiStarCPCombrPVBS;
		product.m_calibPhiStarCPCombMergedrPVBS    = product.m_recoPhiStarCPCombMergedrPVBS;
		product.m_calibPhiStarCPCombHel            = product.m_recoPhiStarCPCombHel;
		product.m_calibPhiStarCPCombMergedHel      = product.m_recoPhiStarCPCombMergedHel;
		product.m_calibPhiStarCPCombHelrPV         = product.m_recoPhiStarCPCombHelrPV;
		product.m_calibPhiStarCPCombMergedHelrPV   = product.m_recoPhiStarCPCombMergedHelrPV;
		product.m_calibPhiStarCPCombHelrPVBS       = product.m_recoPhiStarCPCombHelrPVBS;
		product.m_calibPhiStarCPCombMergedHelrPVBS = product.m_recoPhiStarCPCombMergedHelrPVBS;
	}
}
