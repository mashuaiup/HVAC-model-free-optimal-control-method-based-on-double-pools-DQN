from big_Chiller_Model import big_Chiller_group_Model
from small_Chiller_Model import  small_Chiller_group_Model
# import sys
# sys.path.append("state_array_CLs_Twet.npy")
'''
这边包含了两个相同型号的大冷机和一个小冷机
模型需要传入的参数就是系统冷负荷和Twet
还要做一个序列控制来解决冷机开启的数量，现在的问题就是这个序列控制是写在模型里面还是外边。如果放在模型外边的话，强化学习在学的时候可能小冷机不会被开启、
这样的话优化哦那个孩子多那个最控制动作就设置为:000,这样会比较合适。不加序列控制。这边序列控制还是的加上去，这样就可以使用全部的数据了
现在就是说对CL进行一个判断。将这个判断单独放在一个地方。
模型相当于环境
'''
import numpy as np
class model:
    def __init__(self):
        self.index = 0
        self.CLs = np.load("state_array_CLs_Twet_431.npy")
        self.Tchwr = 12
        self.c_p=4.2
        self.density_water =1000
        self.F_chw=1000
        self.Tchwr_bigchiller = 12
    def step(self,action):

        big_chiller = big_Chiller_group_Model(self.CLs[self.index],self.Tchwr_bigchiller,action)
        small_chiller = small_Chiller_group_Model(self.CLs[self.index],self.Tchwr_bigchiller,action)

        P_big_challer_two,P_big_tower_two,P_big_pump_two,Tchwr_bigchiller,Tcwr_big,Tcws_big  = big_chiller.get_P()
        P_small_challer,P_small_tower,P_small_pump,Tchwr_smallchiller,Tcwr_small,Tcws_small = small_chiller.get_P()

        if ((P_big_challer_two+P_big_tower_two+P_big_pump_two) + (P_small_challer + P_small_tower + P_small_pump)) == 0:
            R = 0
        else:

            R = (self.CLs[self.index][0])/((P_big_challer_two+P_big_tower_two+P_big_pump_two)+(P_small_challer + P_small_tower + P_small_pump))

        self.index += 1
        self.Tchwr_bigchiller = (Tchwr_bigchiller*2+Tchwr_smallchiller)/3

        Done = False
        if self.index >= len(self.CLs)-1:
            Done = True

        S_ = self.CLs[self.index]
        return S_,R,Done,P_big_challer_two,P_big_tower_two,P_big_pump_two,P_small_challer,P_small_tower,P_small_pump,Tcwr_big,Tcwr_small,Tcws_big,Tcws_small
    def reset(self):
        self.index = 0
        self.Tchwr_bigchiller = 12
        return self.CLs[self.index]
if __name__=="__main__":
    # pass
    state = np.load("state_array_CLs_Twet.npy")
    print(state.shape)

    model = model()
    for ratio in range(50,100,5):
        for action0 in range(35,50,1):
            for action1 in range(35, 50, 1):
                S_, R, Done = model.step([ratio/100, action0, action0, action1, action1,[1,0,1]])
                print(R)







