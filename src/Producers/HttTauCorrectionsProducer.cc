
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <TRandom3.h>

#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTauCorrectionsProducer.h"

#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

#include "TauPOG/TauIDSFs/interface/TauIDSFTool.h"

void HttTauCorrectionsProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	TauCorrectionsProducer::Init(settings, metadata);

	tauEnergyCorrection = ToTauEnergyCorrection(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(static_cast<HttSettings const&>(settings).GetTauEnergyCorrection())));
}

void HttTauCorrectionsProducer::AdditionalCorrections(KTau* tau, event_type const& event,
                                                      product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	TauCorrectionsProducer::AdditionalCorrections(tau, event, product, settings, metadata);

	double normalisationFactor = 1.0;

	KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
	KLepton* originalLepton = product.m_originalLeptons.find(tau) != product.m_originalLeptons.end() ? const_cast<KLepton*>(product.m_originalLeptons.at(tau)) : tau;
	if (settings.GetUseUWGenMatching())
	{
		genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
	}
	else
	{
		KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons);
		if (genParticle)
			genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
		else
			genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
	}

	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#TauES_and_decay_mode_scale_facto
	if (tauEnergyCorrection == TauEnergyCorrection::SUMMER2013)
	{
		// http://cmslxr.fnal.gov/lxr/source/DataFormats/TauReco/interface/PFTau.h#035
		if (tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero)
		{
			normalisationFactor = 0.88;
		}
		else if (tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero || tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng2PiZero)
		{
			tau->p4 = tau->p4 * (1.012);
// 			tau->p4 = tau->p4 * (1.015 + 0.001 * std::min(std::max(tau->p4.Pt() - 45.0, 0.0), 10.0));
		}
		else if (tau->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero)
		{
			tau->p4 = tau->p4 * (1.012);
// 			tau->p4 = tau->p4 * (1.012 + 0.001 * std::min(std::max(tau->p4.Pt() - 32.0, 0.0), 18.0));
		}
	}
	else if (tauEnergyCorrection == TauEnergyCorrection::NEWTAUID)
	{
		tau->p4 = tau->p4 * (1.01);
	}
	else if (tauEnergyCorrection == TauEnergyCorrection::SMHTT2016 || tauEnergyCorrection == TauEnergyCorrection::SMHTT2017)
	{
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY) // correct tau->had energy scale
		{
			float tauEnergyCorrectionOneProng = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProng();
			float tauEnergyCorrectionOneProngPiZeros = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZeros();
			float tauEnergyCorrectionThreeProng = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProng();
			float tauEnergyCorrectionThreeProngPiZeros = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngPiZeros();

			//float tauEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionShift();
			float tauEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngShift();
			float tauEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZerosShift();
			float tauEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngShift();
			float tauEnergyCorrectionThreeProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngPiZerosShift();

			if (tau->decayMode == 0)// && tauEnergyCorrectionOneProng != 1.0)
			{
				if (tauEnergyCorrectionOneProngShift != 0.0)
				{
					tauEnergyCorrectionOneProng += tauEnergyCorrectionOneProngShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauEnergyCorrectionOneProng:    " << tauEnergyCorrectionOneProng << std::endl;
				tau->p4 = tau->p4 * tauEnergyCorrectionOneProng;
				product.m_weights["tauTrackReconstructionEfficiencyWeight"] = static_cast<HttSettings const&>(settings).GetTauTrackReconstructionEfficiencyWeightOneProng();
			}
			else if ((tau->decayMode == 1 || tau->decayMode == 2))// && tauEnergyCorrectionOneProngPiZeros != 1.0)
			{
				if (tauEnergyCorrectionOneProngPiZerosShift != 0.0)
				{
					tauEnergyCorrectionOneProngPiZeros += tauEnergyCorrectionOneProngPiZerosShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauEnergyCorrectionOneProngPiZeros:    " << tauEnergyCorrectionOneProngPiZeros << std::endl;
				tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPiZeros;
				product.m_weights["tauTrackReconstructionEfficiencyWeight"] = static_cast<HttSettings const&>(settings).GetTauTrackReconstructionEfficiencyWeightOneProngPiZeros();
			}
			else if (tau->decayMode == 10)// && tauEnergyCorrectionThreeProng != 1.0)
			{
				if (tauEnergyCorrectionThreeProngShift != 0.0)
				{
					tauEnergyCorrectionThreeProng += tauEnergyCorrectionThreeProngShift;
					//TODO cached svfit cache, has to rerun
				}

				LOG(DEBUG) << "tauEnergyCorrectionThreeProng:    " << tauEnergyCorrectionThreeProng << std::endl;
				tau->p4 = tau->p4 * tauEnergyCorrectionThreeProng;
				product.m_weights["tauTrackReconstructionEfficiencyWeight"] = static_cast<HttSettings const&>(settings).GetTauTrackReconstructionEfficiencyWeightThreeProng();
			}
			else if(tauEnergyCorrection == TauEnergyCorrection::SMHTT2017 && tau->decayMode >= 11)// && tauEnergyCorrectionThreeProngPiZeros != 1.0)
			{
				if (tauEnergyCorrectionOneProngShift != 0.0)
				{
					tauEnergyCorrectionThreeProngPiZeros += tauEnergyCorrectionThreeProngPiZerosShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tau decay mode 11 and 2017";
				tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngPiZeros;
				product.m_weights["tauTrackReconstructionEfficiencyWeight"] = static_cast<HttSettings const&>(settings).GetTauTrackReconstructionEfficiencyWeightThreeProngPiZeros();
			}

			if(tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				LOG(DEBUG) << "byTightIsolationMVArun2017v2DBoldDMwLT2017: " << tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata);
				product.m_weights["tauIDEfficiencyWeight"] = static_cast<HttSettings const&>(settings).GetTauIDEfficiencyWeightTight();
			}
			else if(tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byVLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				LOG(DEBUG) << "byVLooseIsolationMVArun2017v2DBoldDMwLT2017: " << tau->getDiscriminator("byVLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata);
				LOG(DEBUG) << "byTightIsolationMVArun2017v2DBoldDMwLT2017: " << tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata);
				product.m_weights["tauIDEfficiencyWeight"] = static_cast<HttSettings const&>(settings).GetTauIDEfficiencyWeightVLoose();
			}
		}
		else if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)) // correct mu->tau fake energy scale
		{
			float tauMuonFakeEnergyCorrectionOneProng = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProng();
			float tauMuonFakeEnergyCorrectionOneProngPiZeros = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngPiZeros();
			float tauMuonFakeEnergyCorrectionThreeProng = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionThreeProng();

			//float tauMuonFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionShift();
			float tauMuonFakeEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngShift();
			float tauMuonFakeEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngPiZerosShift();
			float tauMuonFakeEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionThreeProngShift();
			if (tau->decayMode == 0) //&& tauMuonFakeEnergyCorrectionOneProng != 1.0
			{
				if (tauMuonFakeEnergyCorrectionOneProngShift != 0.0)
				{
					tauMuonFakeEnergyCorrectionOneProng += tauMuonFakeEnergyCorrectionOneProngShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauMuonFakeEnergyCorrectionOneProng:    " << tauMuonFakeEnergyCorrectionOneProng << std::endl;
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProng;
			}
			else if ((tau->decayMode == 1 || tau->decayMode == 2)) //&& tauMuonFakeEnergyCorrectionOneProngPiZeros != 1.0
			{
				if (tauMuonFakeEnergyCorrectionOneProngPiZerosShift != 0.0)
				{
					tauMuonFakeEnergyCorrectionOneProngPiZeros += tauMuonFakeEnergyCorrectionOneProngPiZerosShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauMuonFakeEnergyCorrectionOneProngPiZeros:    " << tauMuonFakeEnergyCorrectionOneProngPiZeros << std::endl;
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProngPiZeros;
			}
			else if (tau->decayMode == 10 && tauMuonFakeEnergyCorrectionThreeProng != 1.0)
			{
				if (tauMuonFakeEnergyCorrectionThreeProngShift != 0.0)
				{
					tauMuonFakeEnergyCorrectionThreeProng += tauMuonFakeEnergyCorrectionThreeProngShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauMuonFakeEnergyCorrectionThreeProng:    " << tauMuonFakeEnergyCorrectionThreeProng << std::endl;
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionThreeProng;
			}
		}
		else if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)) // correct e->tau fake energy scale
		{
			float tauElectronFakeEnergyCorrectionOneProng = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProng();
			float tauElectronFakeEnergyCorrectionOneProngPiZeros = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZeros();
			float tauElectronFakeEnergyCorrectionThreeProng = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionThreeProng();

			//float tauElectronFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionShift();
			float tauElectronFakeEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngShift();
			float tauElectronFakeEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZerosShift();
			float tauElectronFakeEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionThreeProngShift();

			if (tau->decayMode == 0) // && tauElectronFakeEnergyCorrectionOneProng != 1.0
			{
				if (tauElectronFakeEnergyCorrectionOneProngShift != 0.0)
				{
					tauElectronFakeEnergyCorrectionOneProng += tauElectronFakeEnergyCorrectionOneProngShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauElectronFakeEnergyCorrectionOneProng:    " << tauElectronFakeEnergyCorrectionOneProng << std::endl;
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProng;
			}
			else if ((tau->decayMode == 1 || tau->decayMode == 2) ) //&& tauElectronFakeEnergyCorrectionOneProngPiZeros != 1.0
			{
				if (tauElectronFakeEnergyCorrectionOneProngPiZerosShift != 0.0)
				{
					tauElectronFakeEnergyCorrectionOneProngPiZeros += tauElectronFakeEnergyCorrectionOneProngPiZerosShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauElectronFakeEnergyCorrectionOneProngPiZeros:    " << tauElectronFakeEnergyCorrectionOneProngPiZeros << std::endl;
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngPiZeros;
			}
			else if (tau->decayMode == 10) // && tauElectronFakeEnergyCorrectionThreeProng != 1.0
			{
				if (tauElectronFakeEnergyCorrectionThreeProngShift != 0.0)
				{
					tauElectronFakeEnergyCorrectionThreeProng += tauElectronFakeEnergyCorrectionThreeProngShift;
					//TODO cached svfit cache, has to rerun
				}
				LOG(DEBUG) << "tauElectronFakeEnergyCorrectionThreeProng:    " << tauElectronFakeEnergyCorrectionThreeProng << std::endl;
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionThreeProng;
			}
		}
	}
	else if (tauEnergyCorrection == TauEnergyCorrection::LEGACY2017)
	{
		bool isShiftUp = static_cast<HttSettings const&>(settings).GetIsShiftUp();
		bool isNominal = static_cast<HttSettings const&>(settings).GetIsNominal();
		float TauEnergyCorrectionShift = 1.0;

		TDirectory *savedir(gDirectory);
		TFile *savefile(gFile);

		std::string TauEnergyCorrectionFilename         = "$CMSSW_BASE/src/TauAnalysisTools/TauIDSFs/data/TauES_dm_DeepTau2017v2p1VSjet_2017ReReco.root";
		std::string TauEnergyCorrectionFilename_ptgt100 = "$CMSSW_BASE/src/TauAnalysisTools/TauIDSFs/data/TauES_dm_DeepTau2017v2p1VSjet_2017ReReco_ptgt100.root";

		TFile* TauEnergyCorrectionFile         = new TFile(TauEnergyCorrectionFilename.c_str(), "READ");
		TFile* TauEnergyCorrectionFile_ptgt100 = new TFile(TauEnergyCorrectionFilename_ptgt100.c_str(), "READ");


		std::string histoname = "tes";
		TH1F* TauEnergyCorrectionHist         =  static_cast<TH1F*>(TauEnergyCorrectionFile->Get(histoname.c_str()));
		TauEnergyCorrectionHist->SetDirectory(nullptr);
		TH1F* TauEnergyCorrectionHist_ptgt100 =  static_cast<TH1F*>(TauEnergyCorrectionFile_ptgt100->Get(histoname.c_str()));
		TauEnergyCorrectionHist_ptgt100->SetDirectory(nullptr);

		TauEnergyCorrectionFile->Close();
		TauEnergyCorrectionFile_ptgt100->Close();

		gDirectory = savedir;
		gFile = savefile;

		// Definitions of pt_high and pt_low taken from https://github.com/cms-tau-pog/TauIDSFs/blob/master/python/TauIDSFTool.py
		double pt_high = 170;
		double pt_low = 34;

		int dm = (tau->decayMode!=11?tau->decayMode:10);
		int bin = TauEnergyCorrectionHist->GetBin(dm); // DM=11 is treated the same as DM=10
		float tes = 1.0;

		double err = 0.0;
		double err_high = 0.0;
		double err_low  = 0.0;
		int bin_high = 0;
		if(genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY && (dm == 0 || dm == 1 || dm == 10))
		{
			tes = TauEnergyCorrectionHist->GetBinContent(bin);
			if (tau->p4.Pt() >= pt_high)
			{
				bin_high = TauEnergyCorrectionHist_ptgt100->GetBin(dm);
				err      = TauEnergyCorrectionHist_ptgt100->GetBinError(bin_high);
			} // high pt
			else if (tau->p4.Pt() > pt_low)
			{
				bin_high = TauEnergyCorrectionHist_ptgt100->GetBin(dm);
				err_high = TauEnergyCorrectionHist_ptgt100->GetBinError(bin_high);
				err_low  = TauEnergyCorrectionHist->GetBinError(bin);
				err      = err_low + (err_high - err_low) / (pt_high - pt_low) * (tau->p4.Pt() - pt_low);
			} // interpolate between high and low pt
			else
			{
				err = TauEnergyCorrectionHist->GetBinError(bin);
			} // low pt
		}

		if (isNominal)
		{
			TauEnergyCorrectionShift = tes;
		}
		else
		{
			if (isShiftUp)
			{
				TauEnergyCorrectionShift = tes + err;
			}
			else
			{
				TauEnergyCorrectionShift = tes - err;
			}
		}

		tau->p4 = tau->p4 * TauEnergyCorrectionShift;
	}
	else if (tauEnergyCorrection == TauEnergyCorrection::MSSMHTT2016)
	{
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)
		{
			if (tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProng();
			}
			else if (tau->decayMode == 1)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZeros();
			}
			else if (tau->decayMode == 10)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProng();
			}
		}
		// correct e->tau fake energy scale
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)
		{
			if (tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProng();
			}
			else if (tau->decayMode == 1)
			{
				tau->p4 = tau->p4 * static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZeros();
			}
		}
	}
	else if (tauEnergyCorrection != TauEnergyCorrection::NONE)
	{
		LOG(FATAL) << "Tau energy correction of type " << Utility::ToUnderlyingValue(tauEnergyCorrection) << " not yet implemented!";
	}
	/* if no objection this is wrong and will be deleted
	// -------------------------------------
	// tau energy scale shifts
	float tauEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionShift();
	float tauEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngShift();
	float tauEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionOneProngPiZerosShift();
	float tauEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauEnergyCorrectionThreeProngShift();
	// inclusive
	if (tauEnergyCorrectionShift != 1.0)
	{
		tau->p4 = tau->p4 * tauEnergyCorrectionShift;

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionShift;
	}
	// 1-prongs only
	if (tauEnergyCorrectionOneProngShift != 1.0 && tau->decayMode == 0)
	{
		tau->p4 = tau->p4 * tauEnergyCorrectionOneProngShift;

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES_1PRONG;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionOneProngShift;
	}
	// 1-prong+pi0s only
	if (tauEnergyCorrectionOneProngPiZerosShift != 1.0 && (tau->decayMode == 1 || tau->decayMode == 2))
	{
		tau->p4 = tau->p4 * tauEnergyCorrectionOneProngPiZerosShift;

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES_1PRONGPI0S;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionOneProngPiZerosShift;
	}
	// 3-prongs only
	if (tauEnergyCorrectionThreeProngShift != 1.0 && tau->decayMode == 10)
	{
		tau->p4 = tau->p4 * tauEnergyCorrectionThreeProngShift;

		// settings for (cached) Svfit calculation
		(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ES_3PRONG;
		(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionThreeProngShift;
	}
	// -------------------------------------
	// electron->tau fake energy scale shifts
	float tauElectronFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionShift();
	float tauElectronFakeEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngShift();
	float tauElectronFakeEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionOneProngPiZerosShift();
	float tauElectronFakeEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauElectronFakeEnergyCorrectionThreeProngShift();
	if (tauElectronFakeEnergyCorrectionShift != 1.0 ||
		tauElectronFakeEnergyCorrectionOneProngShift != 1.0 ||
		tauElectronFakeEnergyCorrectionOneProngPiZerosShift != 1.0 ||
		tauElectronFakeEnergyCorrectionThreeProngShift != 1.0)
	{
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU))
		{
			// inclusive
			if (tauElectronFakeEnergyCorrectionShift != 1.0)
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionShift;
			}
			// 1-prongs only
			if (tauElectronFakeEnergyCorrectionOneProngShift != 1.0 && tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES_1PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauElectronFakeEnergyCorrectionOneProngShift;
			}
			// 1-prong+pi0s only
			if (tauElectronFakeEnergyCorrectionOneProngPiZerosShift != 1.0 && (tau->decayMode == 1 || tau->decayMode == 2))
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionOneProngPiZerosShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES_1PRONGPI0S;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauElectronFakeEnergyCorrectionOneProngPiZerosShift;
			}
			// 3-prongs only
			if (tauElectronFakeEnergyCorrectionThreeProngShift != 1.0 && tau->decayMode == 10)
			{
				tau->p4 = tau->p4 * tauElectronFakeEnergyCorrectionThreeProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_ELECTRON_FAKE_ES_3PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauElectronFakeEnergyCorrectionThreeProngShift;
			}
		}
	}
	// -------------------------------------
	// muon->tau fake energy scale shifts
	float tauMuonFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionShift();
	float tauMuonFakeEnergyCorrectionOneProngShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngShift();
	float tauMuonFakeEnergyCorrectionOneProngPiZerosShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionOneProngPiZerosShift();
	float tauMuonFakeEnergyCorrectionThreeProngShift = static_cast<HttSettings const&>(settings).GetTauMuonFakeEnergyCorrectionThreeProngShift();
	if (tauMuonFakeEnergyCorrectionShift != 1.0 ||
		tauMuonFakeEnergyCorrectionOneProngShift != 1.0 ||
		tauMuonFakeEnergyCorrectionOneProngPiZerosShift != 1.0 ||
		tauMuonFakeEnergyCorrectionThreeProngShift != 1.0)
	{
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU))
		{
			// inclusive
			if (tauMuonFakeEnergyCorrectionShift != 1.0)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauEnergyCorrectionShift;
			}
			// 1-prongs only
			if (tauMuonFakeEnergyCorrectionOneProngShift != 1.0 && tau->decayMode == 0)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES_1PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauMuonFakeEnergyCorrectionOneProngShift;
			}
			// 1-prong+pi0s only
			if (tauMuonFakeEnergyCorrectionOneProngPiZerosShift != 1.0 && (tau->decayMode == 1 || tau->decayMode == 2))
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionOneProngPiZerosShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES_1PRONGPI0S;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauMuonFakeEnergyCorrectionOneProngPiZerosShift;
			}
			// 3-prongs only
			if (tauMuonFakeEnergyCorrectionThreeProngShift != 1.0 && tau->decayMode == 10)
			{
				tau->p4 = tau->p4 * tauMuonFakeEnergyCorrectionThreeProngShift;

				// settings for (cached) Svfit calculation
				(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_MUON_FAKE_ES_3PRONG;
				(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauMuonFakeEnergyCorrectionThreeProngShift;
			}
		}
	}
	// -------------------------------------

	*/

	// jet->tau fake energy scale shifts
	float tauJetFakeEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetTauJetFakeEnergyCorrection();
	if (tauJetFakeEnergyCorrectionShift != 0.0)
	{
		if (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_FAKE)
		{
			// maximum shift of 40% for pt > 200 GeV
			double shift = tau->p4.Pt() < 200. ? 0.2 * tau->p4.Pt() / 100. : 0.4;

			tau->p4 = tau->p4 * (1 - tauJetFakeEnergyCorrectionShift * shift);

			// settings for (cached) Svfit calculation
			(static_cast<HttProduct&>(product)).m_systematicShift = HttEnumTypes::SystematicShift::TAU_JET_FAKE_ES;
			(static_cast<HttProduct&>(product)).m_systematicShiftSigma = tauJetFakeEnergyCorrectionShift;
		}
	}
	(static_cast<HttProduct&>(product)).m_tauEnergyScaleWeight[tau] = normalisationFactor;
		float randomTauEnergySmearing = static_cast<HttSettings const&>(settings).GetRandomTauEnergySmearing();

	if (randomTauEnergySmearing != 0.0)
	{
		double r;
		TRandom *r3 = new TRandom3();
		r3->SetSeed(event.m_eventInfo->nEvent);
		r = (1.0+r3->Gaus(0,randomTauEnergySmearing));
		tau->p4 = tau->p4 * r;
	}
}
