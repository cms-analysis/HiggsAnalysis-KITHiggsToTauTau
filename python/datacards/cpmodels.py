from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

import math

cp_xsec = PhysicsModel()

### Class that takes care of building a physics model by combining individual channels and processes together
### Things that it can do:
###   - define the parameters of interest (in the default implementation , "r")
###   - define other constant model parameters (e.g., "MH")
###   - yields a scaling factor for each pair of bin and process (by default, constant for background and linear in "r" for signal)
###   - possibly modifies the systematical uncertainties (does nothing by default)

class CPMixing(PhysicsModel):
	def __init__(self, use_mixing_angle=True, inclusive_scaling="muV_muF"):
		self.use_mixing_angle = use_mixing_angle
		self.inclusive_scaling = inclusive_scaling
		self.verbose = False

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
		
		self.modelBuilder.doVar("cpmixing[0.0,0.0,1.0]") # CP mixing angle in units of pi/2
		
		self.modelBuilder.doVar("muF[1.0,0.0,5.0]")
		self.modelBuilder.doVar("muV[1.0,0.0,5.0]")
		
		self.modelBuilder.doVar("kappa[1.0,-5.0,5.0]")
		
		self.modelBuilder.doVar("kappa_ggh[1.0,0.0,5.0]")
		self.modelBuilder.doVar("kappa_qqh[1.0,0.0,5.0]")
		self.modelBuilder.doVar("kappa_vh[1.0,0.0,5.0]")
		self.modelBuilder.doVar("kappa_tth[1.0,0.0,5.0]")
		
		if self.use_mixing_angle:
			maxmix = {
				"a_tilde" : 1.0,
				"b_tilde" : 1.0,
			}
			
			self.modelBuilder.factory_('expr::a("cos(@0*{pi}/2)", cpmixing)'.format(pi=math.pi))
			self.modelBuilder.factory_('expr::b("sin(@0*{pi}/2)", cpmixing)'.format(pi=math.pi))
			
			self.modelBuilder.factory_('expr::sm_scaling("@0*@0-@0*@1*{a_tilde}/{b_tilde}", a, b)'.format(**maxmix))
			self.modelBuilder.factory_('expr::ps_scaling("@1*@1-@0*@1*{b_tilde}/{a_tilde}", a, b)'.format(**maxmix))
			self.modelBuilder.factory_('expr::mm_scaling("@0*@1/({a_tilde}*{b_tilde})", a, b)'.format(**maxmix))
		
		else:
			#TODO: each scaling parameter is missing a factor 1/(a^2 + b^2)
			self.modelBuilder.factory_('expr::sm_scaling("1-@0-sqrt((1-@0)*@0)", cpmixing)')
			self.modelBuilder.factory_('expr::ps_scaling("@0-sqrt((1-@0)*@0)", cpmixing)')
			self.modelBuilder.factory_('expr::mm_scaling("sqrt((1-@0)*@0)", cpmixing)')
		
		for production in ["muF", "muV", "kappa", "kappa_ggh", "kappa_qqh", "kappa_vh", "kappa_tth"]:
			for decay in ["muF"]:
				self.modelBuilder.factory_('expr::{production}_{decay}("@0*@1", {production}, {decay})'.format(
						production=production, decay=decay)
				)
				for cp in ["sm_scaling", "ps_scaling", "mm_scaling"]:
					self.modelBuilder.factory_('expr::{production}_{decay}_{cp}("@0*@1*@2", {production}, {decay}, {cp})'.format(
							production=production, decay=decay, cp=cp)
					)
		
		self.modelBuilder.doSet("POI", "muF,muV,cpmixing")

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			production_decay_cp = []
			
			if self.inclusive_scaling == "muV_muF":
				if "ggh" in process.lower():
					production_decay_cp.append("muF")
				elif "qqh" in process.lower():
					production_decay_cp.append("muV")
				elif "wh" in process.lower():
					production_decay_cp.append("muV")
				elif "zh" in process.lower():
					production_decay_cp.append("muV")
				elif "tth" in process.lower():
					production_decay_cp.append("muF")
				production_decay_cp.append("muF")
			
			elif self.inclusive_scaling == "kappa":
				production_decay_cp.append("kappa")
			
			elif self.inclusive_scaling == "free":
				if "ggh" in process.lower():
					production_decay_cp.append("kappa_ggh")
				elif "qqh" in process.lower():
					production_decay_cp.append("kappa_ggh")
				elif "wh" in process.lower():
					production_decay_cp.append("kappa_vh")
				elif "zh" in process.lower():
					production_decay_cp.append("kappa_vh")
				elif "tth" in process.lower():
					production_decay_cp.append("kappa_tth")
			
			if "sm" in process.lower():
				production_decay_cp.append("sm_scaling")
			elif "ps" in process.lower():
				production_decay_cp.append("ps_scaling")
			elif "mm" in process.lower():
				production_decay_cp.append("mm_scaling")
			
			return "_".join(production_decay_cp)
		
		else:
			return 1

cp_mixing_angle = CPMixing(use_mixing_angle=True, inclusive_scaling="kappa")
cp_fa3 = CPMixing(use_mixing_angle=False, inclusive_scaling="kappa")

cp_mixing_angle_muV_muF = CPMixing(use_mixing_angle=True, inclusive_scaling="muV_muF")
cp_fa3_muV_muF = CPMixing(use_mixing_angle=False, inclusive_scaling="muV_muF")

cp_mixing_angle_kappa = CPMixing(use_mixing_angle=True, inclusive_scaling="kappa")
cp_fa3_kappa = CPMixing(use_mixing_angle=False, inclusive_scaling="kappa")

cp_mixing_angle_free = CPMixing(use_mixing_angle=True, inclusive_scaling="free")
cp_fa3_free = CPMixing(use_mixing_angle=False, inclusive_scaling="free")

