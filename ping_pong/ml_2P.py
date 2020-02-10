"""
場景大小：200 x 500
球：5 x 5，移動速度 (± 5, ± 5)。初始位置 (100, 100)，初始移動速度 (5, 5)，也就是一開始往右下角移動
平台：50 x 5，移動速度 (± 5, 0)。初始位置 (75, 400)
磚塊：25 x 10。初始位置依關卡而定
"""

import pingpong.communication as comm
from pingpong.communication import (
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)
#import train_model
import pickle
import time
#import train
def ml_loop(side: str):

	err=0
	all_infor=[]
	ball_pos = (82, 107)
	#plateform_pos = (70, 400)

	#zipname='v1.zip'
	#filepath=os.path.join(os.path.dirname(__file__),zipname)
	#z = zipfile.ZipFile(filepath,'r')
	#m1_path = z.extract('newrf.sav')
	#s1_path = z.extract('newsc.sav')
	#z.close()


	m = pickle.load(open('p2rf_betta2.sav', 'rb'))
	s = pickle.load(open('p2sc_betta2.sav', 'rb'))
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
		a5 = scene_info.platform_2P[0]
		input = [(a1, a2, a3, a4)]

		std_input = s.transform(input)
		pre_pos = m.predict(std_input)-20
		
		#print("2P: ",scene_info.ball[0] - pre_pos[0]-20,input)
		if(scene_info.ball[1]==415):
			if(scene_info.ball[0]!=pre_pos[0]+20):
				print("2P: ",scene_info.ball[0] - pre_pos[0]-20)
				err+=abs(scene_info.ball[0] - pre_pos[0]-20)

		
		if scene_info.status == GameStatus.GAME_1P_WIN or \
		scene_info.status == GameStatus.GAME_2P_WIN:
			

			path="C:/Users/User/Desktop/ping pong/MLGame-master/"
			with open(path+"P2_betta2.pickle","rb") as f:
				model=pickle.load(f)
			model.read_file(all_infor,"P2",1,0)
			model.RandomForest()
			model.write_file(path+"p2rf_betta2.sav",path+"p2sc_betta2.sav")
			pickle.dump(model,open(path+"P2_betta2.pickle",'wb'))
			m = pickle.load(open('p2rf_betta2.sav', 'rb'))
			s = pickle.load(open('p2sc_betta2.sav', 'rb'))
			print("2p error: ",err)
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
