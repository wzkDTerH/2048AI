import model2048

class AI2048_wasd:
	def __init__(self,model):
		self.model=model
		self.model.Init()
	def run(self,draw=True):
		direct=['u','r','d','l']
		cnt=0;
		if(draw):
			self.model.Draw()
		while(self.model.Move(direct[cnt])):
			if(draw):
				self.model.Draw()
			cnt=(cnt+1)%4
		return self.model.CalcScore()

if(__name__=='__main__'):
	AI=AI2048_wasd(model2048.model2048())
	AI.run()
