import model2048

class AI2048_simpCcalc:
	def __init__(self,model):
		self.model=model
		self.model.Init()
	def CalcF(self,model):
		emptycnt=0
		ret=0;
		for x in range(4):
			for y in range(4):
				if(model.table[x][y]==0):
					emptycnt=emptycnt+1
				else:
					k=2
					if(x==0 or x==3): k=k*2
					if(y==0 or y==3): k=k*2
					ret=ret+k**model.table[x][y]
		return ret+2**emptycnt
	def run(self,draw=True):
		directs=['u','d','r','l']
		while(not self.model.CheckEnd()):
			if(draw):
				self.model.Draw()
			maxhope=0
			maxhopedir='u'
			for direct in directs:
				model_=model2048.Move(self.model,direct)
				AllSproutlist=model2048.AllSprout(model_)
				hope=0
				for pos in AllSproutlist:
					hope=hope+pos['p']*self.CalcF(pos['model'])
				if(hope>maxhope):
					maxhope=hope
					maxhopedir=direct
			self.model.Move(maxhopedir)
		if(draw):
			self.model.Draw()
		return self.model.CalcScore()

if(__name__=='__main__'):
	AI=AI2048_simpCcalc(model2048.model2048())
	AI.run()