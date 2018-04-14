# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class TauPolarisationMva(dict):
	def __init__(self):
		self["TauPolarisationTmvaInputQuantities"] = ["rhoNeutralChargedAsymmetry_1:=TMath::Range(-2,1.0,rhoNeutralChargedAsymmetry_1)",
							"rhoNeutralChargedAsymmetry_2:=TMath::Range(-2,1.0,rhoNeutralChargedAsymmetry_2)",
							"visibleOverFullEnergySvfit_1:=TMath::Range(-1,1.0,lep1LV.E()/svfitTau1LV.E())",
							"visibleOverFullEnergySvfit_2:=TMath::Range(-1,1.0,visibleOverFullEnergySvfit_2)",
							"visibleToFullAngleSvfit_1:=TMath::Range(-1,0.1,visibleToFullAngleSvfit_1)",
							"visibleToFullAngleSvfit_2:=TMath::Range(-1,0.1,visibleToFullAngleSvfit_2)",
							"decayMode_1:=TMath::Range(-1,10,decayMode_1)",
							"decayMode_2:=TMath::Range(-1,10,decayMode_2)",
							"lep1Pt:=pt_1",
							"lep2Pt:=pt_2",
							"diLepMass:=TMath::Range(40,80,m_vis)",
							"svfitMass:=m_sv"
							]
		self["TauPolarisationTmvaMethods"] = ["BDT",
						"BDT"
						]

