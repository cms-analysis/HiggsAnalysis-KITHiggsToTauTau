from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

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
		self.modelBuilder.doVar("CV[1.0,0.0,5.0]")
		self.modelBuilder.doVar("CF[1.0,0.0,5.0]")
		self.modelBuilder.doVar("alpha[0.0,0.0,1.572]") #cp mixing angle from 0 to pi/2
		self.modelBuilder.factory_('expr::cosalpha("cos(@1)", alpha)')
		self.modelBuilder.factory_('expr::sinalpha("sin(@1)", alpha)')

		self.modelBuilder.doSet("POI","alpha")

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			if "sm" in process.lower():
				return "cosalpha*cosalpha"
			elif "ps" in process.lower():
				return "sinalpha*sinalpha"
			elif "mm" in process.lower():
				return "sinalpha*sinalpha"
			else:
				return "r"
		else:
			return 1

cp_mixing = CPMixing()
