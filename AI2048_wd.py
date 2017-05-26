import model2048

class AI2048_wd:
	def __init__(self,model):
		self.model=model
		self.model.Init()
	def run(self,draw=True):
		direct=['u','r']
		cnt=0;
		if(draw):
			self.model.Draw()
		while(self.model.Move(direct[cnt])):
			if(draw):
				self.model.Draw()
			cnt=(cnt+1)%2
		return self.model.CalcScore()
