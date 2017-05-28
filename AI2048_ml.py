# -*- coding: utf-8 -*-
"""
Created on Sun May 28 01:20:00 2017

@author: wzkdterh
"""
import sys
sys.path.append(".")
import model2048
import nn_model as nn
from random import random
from math import log

class AI2048_ml:
	def __init__(self,model):
		self.model=model
		self.model.Init()
		self.nn=nn.nn_model()
	def run(self,draw=True,train_mode=False):
		if(train_mode):
			dataxs=[]
			self.model.Init()
		directs=['u','d','r','l']
		while(not self.model.CheckEnd()):
			if(train_mode):
				dataxs.append(self.model.table)
			if(draw): self.model.Draw()
			batchxs=[]
			dirs=[]
			for direct in directs:
				model_,change=model2048.Move(self.model,direct)
				if(not change): continue
				batchxs.append(model_.table)
				dirs.append(direct)
			hopes=self.nn.run(batchxs)
			hopessum=sum(hopes)+len(hopes)
			hopes=[(x+1)/hopessum for x in hopes]
			r=random()
			for i in range(len(hopes)):
				if(r<=hopes[i]):
					self.model.Move(dirs[i])
					break
				else:
					r=r-hopes[i]
		if(train_mode): dataxs.append(self.model.table)
		if(draw): self.model.Draw()
		if(train_mode):
			Score=self.model.CalcScore()
			return dataxs,[[log(Score,2)]]*len(dataxs)
		else:
			return self.model.CalcScore()
	def getData(self):
		return self.run(draw=False,train_mode=True)
	def train(self,draw=True,Ttotal=1):
		self.nn.train(self.getData,Ttotal=Ttotal)



if(__name__=='__main__'):
	AI=AI2048_ml(model2048.model2048())
	if(sys.argv[1]=='r'):
		AI.run()
	if(sys.argv[1]=='t'):
		n=1
		if(len(sys.argv)>2):
			n=int(sys.argv[2])
		AI.train(Ttotal=n)
