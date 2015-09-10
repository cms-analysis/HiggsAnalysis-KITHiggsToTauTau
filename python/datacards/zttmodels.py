from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

### Class that takes care of building a physics model by combining individual channels and processes together
### Things that it can do:
###   - define the parameters of interest (in the default implementation , "r")
###   - define other constant model parameters (e.g., "MH")
###   - yields a scaling factor for each pair of bin and process (by default, constant for background and linear in "r" for signal)
###   - possibly modifies the systematical uncertainties (does nothing by default)

class ZttEffAndXsec(PhysicsModel):
	def __init__(self):
		self.verbose = False
	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True
	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- Higgs Mass as other parameter ----
		self.modelBuilder.doVar("r[1,0,5]")
		self.modelBuilder.doVar("eff[1,0,2]")
		self.modelBuilder.factory_('expr::pass("@0 * @1", r, eff)')
		self.modelBuilder.factory_('expr::fail("@0 * (1 - @1)", r, eff)')
		if self.options.mass != 0:
			if self.modelBuilder.out.var("MH"):
			  self.modelBuilder.out.var("MH").removeRange()
			  self.modelBuilder.out.var("MH").setVal(self.options.mass)
			else:
			  self.modelBuilder.doVar("MH[%g]" % self.options.mass); 
		self.modelBuilder.doSet("POI","r,eff")
	def getYieldScale(self,bin,process):
		if self.DC.isSignal[process]:
			if "pass" in bin:
				return "pass"
			elif "fail" in bin:
				return "fail"
			else:
				return 1
		else:
			return 1

class ZttEff(PhysicsModel):
	def __init__(self):
		self.verbose = False
	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True
	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- Higgs Mass as other parameter ----
		self.modelBuilder.doVar("eff[1,0,2]")
		self.modelBuilder.factory_('expr::fail("(1 - @0)", eff)')
		if self.options.mass != 0:
			if self.modelBuilder.out.var("MH"):
			  self.modelBuilder.out.var("MH").removeRange()
			  self.modelBuilder.out.var("MH").setVal(self.options.mass)
			else:
			  self.modelBuilder.doVar("MH[%g]" % self.options.mass); 
		self.modelBuilder.doSet("POI","eff")
	def getYieldScale(self,bin,process):
		if self.DC.isSignal[process]:
			if "pass" in bin:
				return "eff"
			elif "fail" in bin:
				return "fail"
			else:
				return 1
		else:
			return 1


ztt_xsec = PhysicsModel()
ztt_eff = ZttEff()
ztt_eff_and_xsec = ZttEffAndXsec()

