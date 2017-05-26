import getopt, sys
import model2048

def main(N=100,args=[]):
	if(len(args)==0):
		opts, args = getopt.getopt(sys.argv[1:], "n:")
		for opt,arg in opts:
			if(opt=='-n'):
				N=int(arg)
	if(len(args)==0):
		print "python checker.py [-n number(default=100)] AI_NAME\n"
		exit()
	result=[]
	for arg in args:
		AIname=arg.split('.')[0]
		print "AI robot:",AIname
		exec("import %s"%(AIname))
		sums,maxs,mins=0,0,0
		it=float(N)/10
		itcnt=0
		for T in range(N):
			if(T>=itcnt):
				print "%d/%d  %0.2f%%"%(T,N,T*100.0/N)
				itcnt=itcnt+it
			AI2048=eval("%s.%s"%(AIname,AIname))
			AI=AI2048(model2048.model2048())
			s=AI.run(False)
			sums=sums+s
			if(T==0):
				mins,maxs=s,s
			else:
				mins=min(mins,s)
				maxs=max(maxs,s)
		print 'name:',AIname,'min:',mins,'max:',maxs,'avg:',sums*1.0/N
		ret={'name':AIname,'min':mins,'max':maxs,'avg':sums*1.0/N}
		result.append(ret)
		print '='*60
	return result

if __name__ == "__main__":
	main()