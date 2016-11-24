from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

class HiggsCPInitialstate(PhysicsModel):
	def __init__(self):
		self.verbose = False

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True


	def doParametersOfInterest(self):
		self.modelBuilder.doVar("alpha[0,0,1]")
		self.modelBuilder.factory_('expr::sm("(1-@0)", alpha)')
		self.modelBuilder.factory_('expr::ps("@0", alpha)')


	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			if "sm" in process.lower() and "ggh" in process.lower():
				return "sm"
			elif "ps" in process.lower() and "ggh" in process.lower():
				return "ps"


HiggsCPI=HiggsCPInitialstate()			



