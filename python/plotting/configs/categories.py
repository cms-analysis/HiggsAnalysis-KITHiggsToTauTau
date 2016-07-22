# -*- coding: utf-8 -*-
import itertools
import pprint
import numpy as np
import copy

class CategoriesDict(object):
	def __init__(self):
		super(CategoriesDict, self).__init__()
		boosted_higgs_string = "(H_pt>100)"
		boosted_higgs_medium_string = "(H_pt>50)"
		boosted_higgs_low_string = "(H_pt>30)"
		vbf_medium_string = "(mjj>500&&jdeta>3.5)"
		vbf_loose_string = "(mjj>200&&jdeta>2)"
		jet2_string = "(njetspt30>1)"
		jet1_string = "(njetspt30>0)"
		jet0_string = "(njetspt30<1)"
		pt2_tight_string = "(pt_2>=45)"
		pt2_medium_string = "(pt_2>=35)"
		pt2_loose_string = "(pt_2>=25)"
		eta_hard_string = "jdeta>4.0"
		self.pp = pprint.PrettyPrinter(indent=4)
		self.categoriesDict = {}
		for mjj in range(0,801,100):
			for jdeta in np.linspace(0.0, 6.0, 13):
				vbf_string = ("(mjj>" + str(mjj) + ")") if mjj >0 else ""
				if(jdeta != 0):
					vbf_string += ("*" if len(vbf_string) > 0 else "" ) + "(jdeta>" + str(jdeta) + ")"
				self.categoriesDict["{analysis}{channel}vbf_" + str(mjj) + "_" + str(jdeta) + "{discriminator}"] = {
						"channel": [
							"mt_",
							"et_",
							"tt_",
							"em_"
							],
						"expressions":{
							"global":self.combine([vbf_string, jet2_string]),
							"analysis": [
								"catHtt13TeV_",
								"catMVAStudies_"
								],
							},
						"binnings":{
							"analysis": [
								"binningHtt13TeV_",
								"binningMVAStudies_"
								],
							"global":{
								"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,211,15)]),
								"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
								}
							}
						}
				self.categoriesDict["{analysis}{channel}ivbf_" + str(mjj) + "_" + str(jdeta) + "{discriminator}"] = copy.deepcopy(self.categoriesDict["{analysis}{channel}vbf_" + str(mjj) + "_" + str(jdeta) + "{discriminator}"])
				self.categoriesDict["{analysis}{channel}ivbf_" + str(mjj) + "_" + str(jdeta) + "{discriminator}"]["expressions"]["global"] = self.combine([self.invert(vbf_string), jet2_string])


		for h_pt in range(0,151,10):
			for pt_2 in range(0,101,10):
				cut_string = "(H_pt>" + str(h_pt) + ")" if h_pt > 0 else ""
				if pt_2 > 0:
					cut_string += ("*" if len(cut_string) > 0 else "" ) + "(pt_2>" + str(pt_2) + ")"
				self.categoriesDict["{analysis}{channel}1jet_" + str(h_pt) + "_" + str(pt_2) + "{discriminator}"] = {
						"channel": [
							"mt_",
							"et_",
							"tt_",
							"em_"
							],
						"expressions":{
							"global":self.combine([cut_string, jet1_string]),
							"analysis": [
								"catHtt13TeV_",
								"catMVAStudies_"
								],
							},
						"binnings":{
							"analysis": [
								"binningHtt13TeV_",
								"binningMVAStudies_"
								],
							"global":{
								"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,211,15)]),
								"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
								}
							}
						}
				self.categoriesDict["{analysis}{channel}i1jet_" + str(h_pt) + "_" + str(pt_2) + "{discriminator}"] = copy.deepcopy(self.categoriesDict["{analysis}{channel}1jet_" + str(h_pt) +"_"+ str(pt_2) + "{discriminator}"])
				self.categoriesDict["{analysis}{channel}i1jet_" + str(h_pt) + "_" + str(pt_2) +"{discriminator}"]["expressions"]["global"] = self.combine([self.invert(cut_string), jet1_string])

		for h_pt in range(0,151,10):
			for pt_2 in range(0,101,10):
				cut_string = "(H_pt>" + str(h_pt) + ")" if h_pt > 0 else ""
				if pt_2 > 0:
					cut_string += ("*" if len(cut_string) > 0 else "" ) + "(pt_2>" + str(pt_2) + ")"
				self.categoriesDict["{analysis}{channel}0jet_" + str(h_pt) + "_" + str(pt_2) + "{discriminator}"] = {
						"channel": [
							"mt_",
							"et_",
							"tt_",
							"em_"
							],
						"expressions":{
							"global":self.combine([cut_string, jet0_string]),
							"analysis": [
								"catHtt13TeV_",
								"catMVAStudies_"
								],
							},
						"binnings":{
							"analysis": [
								"binningHtt13TeV_",
								"binningMVAStudies_"
								],
							"global":{
								"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,211,15)]),
								"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
								}
							}
						}
				self.categoriesDict["{analysis}{channel}i0jet_" + str(h_pt) + "_" + str(pt_2) + "{discriminator}"] = copy.deepcopy(self.categoriesDict["{analysis}{channel}0jet_" + str(h_pt) +"_"+ str(pt_2) + "{discriminator}"])
				self.categoriesDict["{analysis}{channel}i0jet_" + str(h_pt) + "_" + str(pt_2) +"{discriminator}"]["expressions"]["global"] = self.combine([self.invert(cut_string), jet0_string])

		self.categoriesDict["{analysis}{channel}FT_InsteadQCuts{discriminator}"] = {
				"channel": [
					"mt_"
					],
				"expressions":{
					"global":"(L1_vbfggh_vs_default>=0.02)",
					"analysis":[
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
						}
					}					
				}
		self.categoriesDict["{analysis}{channel}FT_B{discriminator}"] = {
				"channel": [
					"mt_"
					],
				"expressions":{
					"global":"(L1_vbfggh_vs_default>=-1.0)*(L1_vbfggh_vs_default<-0.32)",
					"analysis":[
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
						}
					}					
				}
		self.categoriesDict["{analysis}{channel}FT_SB{discriminator}"] = {
				"channel": [
					"mt_"
					],
				"expressions":{
					"global":"(L1_vbfggh_vs_default>=-0.32)*(L2_vbfggh_vs_default<-0.30)",
					"analysis":[
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
						}
					}
				}
		self.categoriesDict["{analysis}{channel}FT_SSB{discriminator}"] = {
				"channel": [
					"mt_"
					],
				"expressions":{
					"global":"(L1_vbfggh_vs_default>=-1.0)*(L2_vbfggh_vs_default>=-0.30)*(L3_vbfggh_vs_default<-0.30)",
					"analysis":[
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
						}
					}
				}
		self.categoriesDict["{analysis}{channel}FT_SSS{discriminator}"] = {
				"channel": [
					"mt_"
					],
				"expressions":{
					"global":"(L1_vbfggh_vs_default>=-1.0)*(L2_vbfggh_vs_default>=-0.30)*(L3_vbfggh_vs_default>=-0.30)",
					"analysis":[
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)])
						}
					}
				}
		self.categoriesDict["{analysis}{channel}vbf{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([vbf_medium_string, jet2_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}ZeroJet30{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30==0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}ZeroJet20{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt20==0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}OneJet30{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30==1)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}OneJet20{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt20==1)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}TwoJet30{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30>1)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}TwoJet20{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt20>1)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}NoTwoJet20{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt20<2)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}NoTwoJet30{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30<2)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_boosted{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet1_string, self.invert(vbf_medium_string), boosted_higgs_string, pt2_tight_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_highpt2{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet1_string, self.invert(vbf_medium_string), self.invert(boosted_higgs_string), pt2_tight_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_lowpt2{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet1_string, self.invert(vbf_medium_string), self.invert(pt2_tight_string)]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_highpt2{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([self.invert(jet1_string), pt2_tight_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_lowpt2{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([self.invert(jet1_string), self.invert(pt2_tight_string)]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}vbf_tag{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet2_string, boosted_higgs_medium_string, eta_hard_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}2jet_untagged{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet2_string, self.invert(self.combine([boosted_higgs_medium_string, eta_hard_string]))]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_boost_high{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet1_string, boosted_higgs_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_boost_medium{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet1_string, self.invert(boosted_higgs_string), boosted_higgs_low_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_boost_low{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([jet1_string, self.invert(boosted_higgs_low_string)]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_nhighpt2{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([self.invert(jet1_string), pt2_tight_string]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_nlowpt2{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":self.combine([self.invert(jet1_string), self.invert(pt2_tight_string)]),
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}inclusive{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(1.0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_high{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30==0)",
					"mm_":"(pt_2>35.0)",
					"mt_":"(pt_2>35.0)",
					"et_":"(pt_2>35.0)",
					"tt_":"(pt_1>35.0)",
					"em_":"(pt_2>35.0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_low{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30==0)",
					"mm_":"(pt_2<=35.0)",
					"mt_":"(pt_2<=35.0)",
					"et_":"(pt_2<=35.0)",
					"tt_":"(pt_1<=35.0)",
					"em_":"(pt_2<=35.0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_high{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30>0)*(!((mjj>200.0)*(jdeta>2.0)))",
					"mm_":"(pt_2>35.0)",
					"mt_":"(pt_2>35.0)",
					"et_":"(pt_2>35.0)",
					"tt_":"(pt_1>35.0)",
					"em_":"(pt_2>35.0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_low{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30>0)*(!((mjj>200.0)*(jdeta>2.0)))",
					"mm_":"(pt_2<=35.0)",
					"mt_":"(pt_2<=35.0)",
					"et_":"(pt_2<=35.0)",
					"tt_":"(pt_1<=35.0)",
					"em_":"(pt_2<=35.0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}2jet_vbf{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30>1)*(mjj>200.0)*(jdeta>2.0)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_sig{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(!((0.3<=ttj_1)*(0.45<=ztt_1)*(0.8<=vbf_1)))*(njetspt30==0)",
					"mm_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"mt_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"et_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"tt_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"em_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}0jet_bkg{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(!((0.3<=ttj_1)*(0.45<=ztt_1)*(0.8<=vbf_1)))*(njetspt30==0)",
					"mm_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"mt_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"et_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"tt_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"em_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_sig{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30>0)*(!((0.3<=ttj_1)*(0.45<=ztt_1)*(0.8<=vbf_1)))",
					"mm_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"mt_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"et_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"tt_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"em_":"((0.4<=ttj_1)*(0.4<=ztt_1))",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}1jet_bkg{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(njetspt30>0)*(!((0.3<=ttj_1)*(0.45<=ztt_1)*(0.8<=vbf_1)))",
					"mm_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"mt_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"et_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"tt_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"em_":"(!((0.4<=ttj_1)*(0.4<=ztt_1)))",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		self.categoriesDict["{analysis}{channel}2jet_vbf_bdt{discriminator}"] = {
				"channel": [
					"mm_",
					"mt_",
					"et_",
					"tt_",
					"em_"
					],
				"expressions":{
					"global":"(0.3<=ttj_1)*(0.45<=ztt_1)*(0.8<=vbf_1)",
					"analysis": [
						"catHtt13TeV_",
						"catMVAStudies_"
						],
					},
				"binnings":{
					"analysis": [
						"binningHtt13TeV_",
						"binningMVAStudies_"
						],
					"global":{
						"_m_sv":" ".join([str(float(f)) for f in range(0,30,15)+range(30, 120, 10)+range(120,151,15)]),
						"_disc_1": "-1.0 "+" ".join([str(x/100.0) for x in range(-90,100,5)]) + " 1.0"
						}
					}
				}
		#print self.categoriesDict
		self.calculateBinnings()
		self.calculateExpressions()
		self.calculateDataCards()
	def calculateBinnings(self):
		self.binnings = {}
		for name, info in self.categoriesDict.iteritems():
			#print name
			channels = info["channel"]
			analysis = info["binnings"]["analysis"]
			global_keys = info["binnings"].get("global", {}).keys()
			for (channel,ana) in itertools.product(channels, analysis):
				#print channel, ana
				discriminators = global_keys
				if channel in info["binnings"].keys():
					discriminators += [x for x in info["binnings"][channel].keys() if not x in global_keys]
				for discriminator in discriminators:
					binning_string = info["binnings"].get(channel, info["binnings"]["global"]).get(discriminator, info["binnings"]["global"][discriminator])
					self.binnings[name.format(analysis=ana, channel=channel, discriminator=discriminator)]=binning_string

	def calculateDataCards(self):
		pass

	def calculateExpressions(self):
		self.expressions = {}
		for name, info in self.categoriesDict.iteritems():
			#print name
			channels = info["channel"]
			analysis = info["expressions"]["analysis"]
			global_expression = info["expressions"].get("global", "")
			for (channel,ana) in itertools.product(channels, analysis):
				expression = global_expression
				if channel in info["expressions"].keys():
					expression = self.combine([expression, info["expressions"][channel]])
				self.expressions[name.format(analysis=ana, channel=channel, discriminator="")]=expression
		#self.pp.pprint(self.expressions)

	def getExpressionsDict(self):
		return self.expressions

	def getBinningsDict(self):
		return self.binnings

	def getCategories(self, channels, prefix = True):
		Categories = {}
		placeholder=0
		for chan in channels:
			Categories[chan] = []
		for name, info in self.categoriesDict.iteritems():
			for chan in channels:
				if chan+"_" in info["channel"]:
					Categories[chan].append(name.format(analysis="", channel=(chan+"_") if prefix else "", discriminator=""))
				else:
					Categories[chan].append("placeholder{ph}".format(ph=placeholder))
					placeholder += 1
		return Categories

	def invert(self, expression):
		tmp_expression = "(" + expression + ")"
		return "(" + tmp_expression + "==0)" 

	def combine(self, strings_to_combine):
		return "(" + "*".join(strings_to_combine) + ")"
