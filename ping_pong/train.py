
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:42:13 2019

@author: User
"""



from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pickle
import numpy as np 

class train_model():
		def __init__(self,tree=20):
			self.data_list=[]
			self.label_list=[]
			self.target_frame=[]
			self.scaler=StandardScaler()
			self.forest_reg = RandomForestRegressor(tree,random_state=0)
			
		
		def print_test(self):
			print(self.label_list)
		def read_file(self,datafile,player,train=0,full=0):
			d1_list=[]
			d2_list=[]#mirror
			t1_list=[]
			t2_list=[]
			l1_list=[]
			l2_list=[]
			flag=0
			key=0

			if(player=="P1"):
				key=80
			elif(player=="P2"):
				key=415
			else:
				print("wrong!!")
				
			if train==0:				
				with open(datafile,"rb") as f:
					data=pickle.load(f)
			else:
				data=datafile
			#data=list(d)#tuple to list
			ball_list=[]
			ball_list.append(list(data[0].ball))
			for i in range(1,len(data)):
				ball_list.append(list(data[i].ball))
				if((ball_list[i][1]>415 or ball_list[i][1]< 80 )and ball_list[i-1][1]!=key):
					if(ball_list[i-1][1]>80 and ball_list[i-1][1]<200):
						ball_list[i][1]=80
						flag=1
						
					elif(ball_list[i-1][1]<415 and ball_list[i-1][1]>200):
						ball_list[i][1]=415
						flag=1
						
				
				pX1=ball_list[i][0]
				pY1=ball_list[i][1]
				vX1=pX1-ball_list[i-1][0]
				vY1=pY1-ball_list[i-1][1]
				d1_list.append((pX1,pY1,vX1,vY1))
				
						
				#mirror
				pX2=195-pX1
				pY2=495-pY1
				vX2=-vX1
				vY2=-vY1
				d2_list.append((pX2,pY2,vX2,vY2))
				
				if(ball_list[i][1]==key):
					t1_list.append(i)
					#print(i)
					
				elif(ball_list[i][1]==495-key):
					t2_list.append(i)#mirror
				
				if(flag==1):
					break
			
			index1=0
			index2=0
			for j in range(1,len(data)):
		
				if(index1<len(t1_list)):
					l1_list.append(data[t1_list[index1]].ball[0])
					if(ball_list[j][1]==key):
						index1+=1
					
				if(index2<len(t2_list)):#mirror
					l2_list.append(195-data[t2_list[index2]].ball[0])
					if(ball_list[j][1]==495-key):
						index2+=1
			
			
			#d1_list=d1_list[0:len(l1_list)]
			#d2_list=d2_list[0:len(l2_list)]
			if full==0:
				cut1=0
				cut2=0
				for x in range(len(l1_list)-1,0,-1):
					if l1_list[x-1]!=l1_list[x]:
						cut1=x
						print("cut1: ",cut1)
						break
					
				for y in range(len(l2_list)-1,0,-1):
					if l2_list[y-1]!=l2_list[y]:
						cut2=y
						print("cut2: ",cut2)
						break
					
				d1_list=d1_list[cut1:len(l1_list)]
				d2_list=d2_list[cut2:len(l2_list)]
				l1_list=l1_list[cut1:len(l1_list)]
				l2_list=l2_list[cut2:len(l2_list)]
				
			else:
				d1_list=d1_list[0:len(l1_list)]
				d2_list=d2_list[0:len(l2_list)]
				
			self.data_list=self.data_list+d1_list+d2_list
			self.label_list=self.label_list+l1_list+l2_list
			return d1_list , l1_list ,d2_list,l2_list
		
		def batch(self,batch):
			self.label_list=self.label_list*batch
			self.data_list=self.data_list*batch
			
		def RandomForest(self):

			self.scaler.fit(self.data_list)
			#normalize test
			x_train_stdnorm=self.scaler.transform(self.data_list)
			self.forest_reg.fit(x_train_stdnorm,self.label_list)
		
			

		def write_file(self,RFname,SCname):
			pickle.dump(self.forest_reg,open(RFname,'wb'))
			pickle.dump(self.scaler,open(SCname,'wb'))
			


#p1 = train_model()
#p1.read_file("2019-06-19_18-41-04.pickle","P1",0,1)
#p1.batch(3)
##print("feeeeeeeeeeeeeeeeeeeeeeeee")
#p1.RandomForest()
#p1.write_file("p1rf_betta2.sav","p1sc_betta2.sav")
#pickle.dump(p1,open("P1_betta2.pickle",'wb'))
#
#p2 = train_model()
#p2.read_file("2019-06-19_18-41-04.pickle","P2",0,1)
#p2.batch(3)
#p2.RandomForest()
#p2.write_file("p2rf_betta2.sav","p2sc_betta2.sav")
#pickle.dump(p2,open("P2_betta2.pickle",'wb'))

'''
#if __name__ == '__main__':
t1P=train_model()
#t1P.read_file("2019-05-30_13-59-07.pickle","P1")
d1,l1,d2,l2=t1P.read_file("2019-06-04_21-54-21.pickle","P1")
#d1,l1,d2,l2=t1P.read_file("record06_05_09_08_03.pickle","P1")
t1P.batch(1)
t1P.RandomForest()
t1P.write_file("p1testrf.sav","p1testsc.sav")
pickle.dump(t1P,open("P1testmodel.pickle",'wb'))

t2P=train_model()
#t2P.read_file("2019-05-30_13-59-07.pickle","P2")
t2P.read_file("2019-06-04_21-54-21.pickle","P2")
t2P.batch(1)
t2P.RandomForest()
t2P.write_file("p2testrf.sav","p2testsc.sav")
pickle.dump(t2P,open("P2testmodel.pickle",'wb'))
'''