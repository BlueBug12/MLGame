"""
場景大小：200 x 500
球：5 x 5，移動速度 (± 5, ± 5)。初始位置 (100, 100)，初始移動速度 (5, 5)，也就是一開始往右下角移動
平台：50 x 5，移動速度 (± 5, 0)。初始位置 (75, 400)
磚塊：25 x 10。初始位置依關卡而定
"""

import pingpong.communication as comm
import train
from pingpong.communication import (
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

import pickle
import time

def ml_loop(side: str):
	all_infor=[]
	game=[]
	ans=[]
	pre=[]
	e=[]
	err=0
	ball_pos = (82, 107)
	platform_pos2P = (80, 420)

	#zipname='v1.zip'
	#filepath=os.path.join(os.path.dirname(__file__),zipname)
	#z = zipfile.ZipFile(filepath,'r')
	#m1_path = z.extract('newrf.sav')
	#s1_path = z.extract('newsc.sav')
	#z.close()

	#p12 = train_model()
	m = pickle.load(open('p1rf_betta2.sav', 'rb'))
	s = pickle.load(open('p1sc_betta2.sav', 'rb'))
	comm.ml_ready()

    # 3. Start an endless loop.
	while True:

		# 3.1. Receive the scene information sent from the game process.
		scene_info = comm.get_scene_info()
		all_infor.append(scene_info)

		a1 = scene_info.ball[0]
		a2 = scene_info.ball[1]
		a3 = a1 - ball_pos[0]
		a4 = a2 - ball_pos[1]
		a5 = scene_info.platform_1P[0]
		#a6 = scene_info.platform_2P[0]
		#a7 = a6 - platform_pos2P[0]
		#input = [(a1, a2, a3, a4,a6,a7,scene_info.frame)]
		input = [(a1, a2, a3, a4)]
		
		#print(input)
		#std_input=m.scaler.transform(input)
		std_input = s.transform(input)
		pre_pos = m.predict(std_input)-20
		#print(pre_pos)
		#print("1P: ",scene_info.ball[0] - pre_pos[0]-20,input)
		if(scene_info.ball[1]==80):
			e.append(scene_info.ball[0] - pre_pos[0]-20)
			ans.append(scene_info.ball[0])
			pre.append(pre_pos[0]+20)
			if(scene_info.ball[0]!=pre_pos[0]+20):
				print("1P: ",scene_info.ball[0] - pre_pos[0]-20)
				err+=abs(scene_info.ball[0] - pre_pos[0]-20)
			#print("1P: ",scene_info.ball[0],'vs',pre_pos[0]+20)
			#act.append(scene_info.ball[0])
			#pre.append(pre_pos+20)
			#minus.append(scene_info.ball[0]-int(pre_pos[0])-20)
		
		if scene_info.status == GameStatus.GAME_1P_WIN or \
		scene_info.status == GameStatus.GAME_2P_WIN:
			# Do something updating or reseting stuff
			
			# 3.2.1 Inform the game process that
			#       the ml process is ready for the next round# save game data
			
			path="C:/Users/User/Desktop/ping pong/MLGame-master/"
			with open(path+"game_result.pickle","rb") as d:
				game=pickle.load(d)
			with open(path+"P1_betta2.pickle","rb") as f:
				model=pickle.load(f)
				
			model.read_file(all_infor,"P1",1,0)
			model.RandomForest()
			model.write_file(path+"p1rf_betta2.sav",path+"p1sc_betta2.sav")
			pickle.dump(model,open(path+"P1_betta2.pickle",'wb'))
			
			m = pickle.load(open('p1rf_betta2.sav', 'rb'))
			s = pickle.load(open('p1sc_betta2.sav', 'rb'))
			
			game.append((scene_info.frame,scene_info.ball_speed,scene_info.status,err))
			pickle.dump(game,open(path+"game_result.pickle",'wb'))
			

			pre=[]
			e=[]
			ans=[]
			all_infor=[]
			err=0
			comm.ml_ready()
			continue

		if (pre_pos==a5):
			pass
			#comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)

		elif (pre_pos <a5):
			comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)

		else:
			comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
		
		ball_pos = scene_info.ball
		#platform_pos2P = scene_info.platform_2P
