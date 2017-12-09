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
	def __init__(self):
		self.verbose = False

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
		
		maxmix = {
			"a_tilde" : 1.0,
			"b_tilde" : 1.0,
		}
		
		self.modelBuilder.doVar("muV[1.0,0.0,5.0]")
		self.modelBuilder.doVar("muF[1.0,0.0,5.0]")
		self.modelBuilder.doVar("alpha_over_pi_half[0.0,0.0,1.0]") # cp mixing angle from 0 to pi/2
		self.modelBuilder.factory_('expr::cosalpha("cos(@1*{pi}/2)", alpha_over_pi_half)'.format(pi=math.pi))
		self.modelBuilder.factory_('expr::sinalpha("sin(@1*{pi}/2)", alpha_over_pi_half)'.format(pi=math.pi))
		self.modelBuilder.factory_('expr::a("@1", cosalpha)')
		self.modelBuilder.factory_('expr::b("@1", sinalpha)')
		self.modelBuilder.factory_('expr::sm_scaling("@1*@1-@1*@2*{a_tilde}/{b_tilde}", a, b)'.format(**maxmix))
		self.modelBuilder.factory_('expr::ps_scaling("@2*@2-@1*@2*{b_tilde}/{a_tilde}", a, b)'.format(**maxmix))
		self.modelBuilder.factory_('expr::mm_scaling("@1*@2/({a_tilde}*{b_tilde})", a, b)'.format(**maxmix))

		self.modelBuilder.doSet("POI", "alpha_over_pi_half, muV, muV")

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			signal_scaling = ["muF"]
			
			if "ggh" in process.lower():
				signal_scaling.append("muF")
			elif "qqh" in process.lower():
				signal_scaling.append("muV")
			else:
				pass # TODO
			
			if "sm" in process.lower():
				signal_scaling.append("sm_scaling")
			elif "ps" in process.lower():
				signal_scaling.append("ps_scaling")
			elif "mm" in process.lower():
				signal_scaling.append("mm_scaling")
			
			return "*".join(signal_scaling)
		
		else:
			return 1

cp_mixing = CPMixing()

