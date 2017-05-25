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

if(__name__=='__main__'):
	N=100
	sums,maxs,mins=0,0,0
	for T in range(N):
		AI=AI2048_wd(model2048.model2048())
		s=AI.run(False)
		sums=sums+s
		if(T==0):
			mins,maxs=s,s
		else:
			mins=min(mins,s)
			maxs=max(maxs,s)
	print 'min:',mins,'max:',maxs,'avg:',sums*1.0/N
