import model2048

class AI2048_simpCalcSpace:
	def __init__(self,model):
		self.model=model
		self.model.Init()
	def CalcF(self,model):
		emptycnt=0
		for line in model.table:
			for gd in line:
				if(gd==0):
					emptycnt=emptycnt+1
		return model.CalcScore()+2**emptycnt
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
	N=100
	sums,maxs,mins=0,0,0
	for T in range(N):
		if(T%(N/10)==0):
			print "%d/%d"%(T,N)
		AI=AI2048_simpCalcSpace(model2048.model2048())
		s=AI.run(draw=False)
		sums=sums+s
		if(T==0):
			mins,maxs=s,s
		else:
			mins=min(mins,s)
			maxs=max(maxs,s)
	print 'min:',mins,'max:',maxs,'avg:',sums*1.0/N
