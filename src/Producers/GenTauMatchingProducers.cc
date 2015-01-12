
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauMatchingProducers.h"


std::string RecoElectronGenTauMatchingProducer::GetProducerId() const {
	return "RecoElectronGenTauMatchingProducer";
}

RecoElectronGenTauMatchingProducer::RecoElectronGenTauMatchingProducer() :
	GenTauMatchingProducerBase<KDataElectron>(&product_type::m_genTauMatchedElectrons,
	                                          &product_type::m_validElectrons,
	                                          &product_type::m_invalidElectrons,
	                                          RecoElectronGenTauMatchingProducer::TauDecayMode::E,
	                                          &setting_type::GetDeltaRMatchingRecoElectronsGenTau,
	                                          &setting_type::GetInvalidateNonGenTauMatchingRecoElectrons)
{
}


std::string RecoMuonGenTauMatchingProducer::GetProducerId() const {
	return "RecoMuonGenTauMatchingProducer";
}

RecoMuonGenTauMatchingProducer::RecoMuonGenTauMatchingProducer() :
	GenTauMatchingProducerBase<KDataMuon>(&product_type::m_genTauMatchedMuons,
	                                      &product_type::m_validMuons,
	                                      &product_type::m_invalidMuons,
	                                      RecoMuonGenTauMatchingProducer::TauDecayMode::M,
	                                      &setting_type::GetDeltaRMatchingRecoMuonGenTau,
	                                      &setting_type::GetInvalidateNonGenTauMatchingRecoMuons)
{
}


std::string RecoTauGenTauMatchingProducer::GetProducerId() const {
	return "RecoTauGenTauMatchingProducer";
}

RecoTauGenTauMatchingProducer::RecoTauGenTauMatchingProducer() :
	GenTauMatchingProducerBase<KDataPFTau>(&product_type::m_genTauMatchedTaus,
	                                       &product_type::m_validTaus,
	                                       &product_type::m_invalidTaus,
	                                       RecoTauGenTauMatchingProducer::TauDecayMode::T,
	                                       &setting_type::GetDeltaRMatchingRecoTauGenTau,
	                                       &setting_type::GetInvalidateNonGenTauMatchingRecoTaus)
{
}

