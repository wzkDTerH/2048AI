from random import randint,random
from copy import deepcopy
class model2048:
	def __init__(self):
		self.table=[[0 for i in range(4)] for j in range(4)]
		self.Score=0
		pass

	def Sprout(self,gen={1:0.9,2:0.1},cnt=1):
		empty_cnt=0
		for line in self.table:
			for gd in line:
				if(gd==0):
					empty_cnt=empty_cnt+1
		cnt=min(cnt,empty_cnt)
		gen_sum=sum([gen[p] for p in gen])
		for p in gen: gen[p]=gen[p]/gen_sum
		for t in range(cnt):
			x,y=randint(0,3),randint(0,3)
			while(self.table[x][y]!=0):
				x,y=randint(0,3),randint(0,3)
			r=random()
			for p in gen:
				if(r<=gen[p]):
					self.table[x][y]=p
					break
				r=r-gen[p]
		self.CalcScore()

	def Init(self):
		self.__init__()
		self.Sprout(gen={1:1.0},cnt=2)

	def Draw(self):
		print '='*41
		for line in self.table:
			print '|',
			for gd in line:
				if(gd==0):
					print " "*7,'|',
				else:
					print "%7d"%(2**gd),'|',
			print '\n','='*41
		print "Score = ",self.Score

	def CalcScore(self):
		self.Score=0
		for line in self.table:
			for gd in line:
				if(gd!=0):
					self.Score=self.Score+2**gd

	def _Trun(self,x):
		x=x%4
		for T in range(x):
			temp=[[0 for i in range(4)] for j in range(4)]
			for i in range(4):
				for j in range(4):
					temp[j][3-i]=self.table[i][j]
			self.table=deepcopy(temp)
	def CheckEnd(self):
		for i in range(4):
			for j in range(4):
				if(self.table[i][j]==0):
					return False
		for i in range(4):
			for j in range(3):
				if(self.table[i][j]==self.table[i][j+1]):
					return False
		for i in range(3):
			for j in range(4):
				if(self.table[i][j]==self.table[i+1][j]):
					return False
		return True

	def Move(self,direct,sprout=True):
		if(self.CheckEnd()): return False
		directmap={'l':0,'d':1,'r':2,'u':3}
		self._Trun(directmap[direct])
		for l in range(len(self.table)):
			line=self.table[l]
			temp=[]
			for gd in line:
				if(gd!=0):
					temp.append(gd)
			i=0
			while(i<len(temp)-1):
				if(temp[i]==temp[i+1]):
					temp[i]=temp[i]+1
					del temp[i+1]
				i=i+1
			while(len(temp)<4):
				temp.append(0)
			self.table[l]=deepcopy(temp)
		self._Trun(4-directmap[direct])
		self.Sprout()
		self.CalcScore()


if(__name__=='__main__'):
	model=model2048()
	model.Init()
	model.Draw()
	while(True):
		if(model.CheckEnd()):
			print "End!!!"
			exit()
		key=raw_input("Input key:")
		if(key=='e' or key=='q'):exit()
		directmap={'w':'u','a':'l','s':'d','d':'r'}
		try:
			model.Move(directmap[key])
		except:
			pass
		model.Draw()
	pass