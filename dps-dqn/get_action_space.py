import numpy as np
#ratio:[0.1,1]
#f_pump:[25,45] f_tower:[25,45]
action_all = []
for ratio_10 in range(1,11):
    for f_pump in range(25,51):
        for f_tower in range(25,51):
            action_all.append([ratio_10/10,f_pump,f_tower])
print(len(action_all))
action_all = np.array(action_all)
np.save("action_all_6760",action_all)
print(action_all[504])