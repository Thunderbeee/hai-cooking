import pandas as pd
from tqdm import tqdm
import numpy as np
import json
import ast

def get_dat(file):
    dat = pd.read_csv(file)
    dat = dat.loc[:,["ResponseId", "round_1_states", "round_2_states", 
                    "round_3_states", "round_4_states", "round_5_states", "round_6_states"]]
    dat = dat.dropna().reset_index().iloc[:,1:]
    return  dat

def get_state12(dat):
    # 0~chef, 1~sou_chef, 2~server
    # 99 ~ available, 100 ~ finished
    final12 = pd.DataFrame()
    for round in ["round_1_states", "round_2_states"]:
        print(f"    generating {round}")
        out = pd.DataFrame()
        ID = dat["ResponseId"]
        for kim in tqdm(np.arange(len(ID))):
            zzx = pd.DataFrame(json.loads(dat[round][kim]))
            chef_order = [state[0]["order_index"] for state in zzx["worker_states"]]
            chef_task = [state[0]["task"] for state in zzx["worker_states"]]
            chef_left_ticks = [state[0]["ticks"] for state in zzx["worker_states"]]

            sou_chef_order = [state[1]["order_index"] for state in zzx["worker_states"]]
            sou_chef_task = [state[1]["task"] for state in zzx["worker_states"]]
            sou_chef_left_ticks = [state[1]["ticks"] for state in zzx["worker_states"]]

            server_order = [state[2]["order_index"] for state in zzx["worker_states"]]
            server_task = [state[2]["task"] for state in zzx["worker_states"]]
            server_left_ticks = [state[2]["ticks"] for state in zzx["worker_states"]]

            ticks = np.arange(len(chef_order))

        # t01, order 0, task 1, 12 in total 
            t00 = ["available"] * len(ticks)
            t01 = ["unavailable"] * len(ticks)
            t02 = ["unavailable"] * len(ticks)

            t10 = ["available"] * len(ticks)
            t11 = ["unavailable"] * len(ticks)
            t12 = ["unavailable"] * len(ticks)

            t20 = ["available"] * len(ticks)
            t21 = ["unavailable"] * len(ticks)
            t22 = ["unavailable"] * len(ticks)

            t30 = ["available"] * len(ticks)
            t31 = ["unavailable"] * len(ticks)
            t32 = ["unavailable"] * len(ticks)

            matrix = [[t00, t01, t02], [t10, t11, t12], [t20, t21, t22], [t30, t31, t32]]

            i = 0
            for i in np.arange(len(ticks)):
                order_chef = chef_order[i]
                task_chef = chef_task[i]
                if order_chef != None and task_chef != None:
                    matrix[order_chef][task_chef][i] = "chef"

                    for jisoo in np.arange(2):
                        if task_chef == jisoo and chef_left_ticks[i] == 1:
                            new1 = matrix[order_chef][jisoo+1][:i+1]
                            new2 = ["available"]*(len(ticks) - i - 1)
                            matrix[order_chef][jisoo+1] = new1 + new2

                    for mmy in np.arange(3):
                        if task_chef == mmy and chef_left_ticks[i] == 1:
                            new1 = matrix[order_chef][mmy][:i+1]
                            new2 = ["finished"]*(len(ticks) - i - 1)
                            matrix[order_chef][mmy] = new1 + new2

                order_sou_chef = sou_chef_order[i]
                task_sou_chef = sou_chef_task[i]
                if order_sou_chef != None and task_sou_chef != None:
                    matrix[order_sou_chef][task_sou_chef][i] = "sou_chef"

                    for jisoo in np.arange(2):
                        if task_sou_chef == jisoo and sou_chef_left_ticks[i] == 1:
                            new1 = matrix[order_sou_chef][jisoo+1][:i+1]
                            new2 = ["available"]*(len(ticks) - i - 1)
                            matrix[order_sou_chef][jisoo+1] = new1 + new2


                    for mmy in np.arange(3):
                        if task_sou_chef == mmy and sou_chef_left_ticks[i] == 1:
                            new1 = matrix[order_sou_chef][mmy][:i+1]
                            new2 = ["finished"]*(len(ticks) - i - 1)
                            matrix[order_sou_chef][mmy] = new1 + new2


                order_server = server_order[i]
                task_server = server_task[i]
                if order_server != None and task_server != None:
                    matrix[order_server][task_server][i] = "server"

                    for jisoo in np.arange(2):
                        if task_server == jisoo and server_left_ticks[i] == 1:
                            new1 = matrix[order_server][jisoo+1][:i+1]
                            new2 = ["available"]*(len(ticks) - i - 1)
                            matrix[order_server][jisoo+1] = new1 + new2

                    for mmy in np.arange(3):
                        if task_server == mmy and server_left_ticks[i] == 1:
                            new1 = matrix[order_server][mmy][:i+1]
                            new2 = ["finished"]*(len(ticks) - i - 1)
                            matrix[order_server][mmy] = new1 + new2


            player = pd.DataFrame()
            player["ID"] = [ID[kim]] * len(ticks)
            player["round"] = [round] * len(ticks)
            player["chef_order"] = chef_order
            player["chef_task"] = chef_task
            player["chef_left_ticks"] = chef_left_ticks
            player["sou_chef_order"] = sou_chef_order
            player["sou_chef_task"] = sou_chef_task
            player["sou_chef_left_ticks"] = sou_chef_left_ticks
            player["server_order"] = server_order
            player["server_task"] = server_task
            player["server_left_ticks"] = server_left_ticks
            player["ticks"] = ticks
            player["order0_task0"] = matrix[0][0]
            player["order0_task1"] = matrix[0][1]
            player["order0_task2"] = matrix[0][2]
            player["order1_task0"] = matrix[1][0]
            player["order1_task1"] = matrix[1][1]
            player["order1_task2"] = matrix[1][2]
            player["order2_task0"] = matrix[2][0]
            player["order2_task1"] = matrix[2][1]
            player["order2_task2"] = matrix[2][2]
            player["order3_task0"] = matrix[3][0]
            player["order3_task1"] = matrix[3][1]
            player["order3_task2"] = matrix[3][2]

            out = pd.concat([out, player])
        final12 = pd.concat([final12, out])

    return final12


def get_state36(dat):
    # 0~chef, 1~sou_chef, 2~server
    # 99 ~ available, 100 ~ finished
    final36 = pd.DataFrame()
    for round in ["round_3_states", "round_4_states", "round_5_states", "round_6_states"]:
        print(f"    generating {round}")
        out = pd.DataFrame()
        ID = dat["ResponseId"]
        for kim in tqdm(np.arange(len(ID))):
            zzx = pd.DataFrame(json.loads(dat[round][kim]))

            sou_chef_order = [state[0]["order_index"] for state in zzx["worker_states"]]
            sou_chef_task = [state[0]["task"] for state in zzx["worker_states"]]
            sou_chef_left_ticks = [state[0]["ticks"] for state in zzx["worker_states"]]

            server_order = [state[1]["order_index"] for state in zzx["worker_states"]]
            server_task = [state[1]["task"] for state in zzx["worker_states"]]
            server_left_ticks = [state[1]["ticks"] for state in zzx["worker_states"]]

            ticks = np.arange(len(sou_chef_order))

            # t01, order 0, task 1, 12 in total 
            t00 = ["available"] * len(ticks)
            t01 = ["unavailable"] * len(ticks)
            t02 = ["unavailable"] * len(ticks)

            t10 = ["available"] * len(ticks)
            t11 = ["unavailable"] * len(ticks)
            t12 = ["unavailable"] * len(ticks)

            t20 = ["available"] * len(ticks)
            t21 = ["unavailable"] * len(ticks)
            t22 = ["unavailable"] * len(ticks)

            t30 = ["available"] * len(ticks)
            t31 = ["unavailable"] * len(ticks)
            t32 = ["unavailable"] * len(ticks)

            matrix = [[t00, t01, t02], [t10, t11, t12], [t20, t21, t22], [t30, t31, t32]]

            i = 0
            for i in np.arange(len(ticks)):

                order_sou_chef = sou_chef_order[i]
                task_sou_chef = sou_chef_task[i]
                if order_sou_chef != None and task_sou_chef != None:
                    matrix[order_sou_chef][task_sou_chef][i] = "sou_chef"

                    for jisoo in np.arange(2):
                        if task_sou_chef == jisoo and sou_chef_left_ticks[i] == 1:
                            new1 = matrix[order_sou_chef][jisoo+1][:i+1]
                            new2 = ["available"]*(len(ticks) - i - 1)
                            matrix[order_sou_chef][jisoo+1] = new1 + new2


                    for mmy in np.arange(3):
                        if task_sou_chef == mmy and sou_chef_left_ticks[i] == 1:
                            new1 = matrix[order_sou_chef][mmy][:i+1]
                            new2 = ["finished"]*(len(ticks) - i - 1)
                            matrix[order_sou_chef][mmy] = new1 + new2


                order_server = server_order[i]
                task_server = server_task[i]
                if order_server != None and task_server != None:
                    matrix[order_server][task_server][i] = "server"

                    for jisoo in np.arange(2):
                        if task_server == jisoo and server_left_ticks[i] == 1:
                            new1 = matrix[order_server][jisoo+1][:i+1]
                            new2 = ["available"]*(len(ticks) - i - 1)
                            matrix[order_server][jisoo+1] = new1 + new2

                    for mmy in np.arange(3):
                        if task_server == mmy and server_left_ticks[i] == 1:
                            new1 = matrix[order_server][mmy][:i+1]
                            new2 = ["finished"]*(len(ticks) - i - 1)
                            matrix[order_server][mmy] = new1 + new2


            player = pd.DataFrame()
            player["ID"] = [ID[kim]] * len(ticks)
            player["round"] = [round] * len(ticks)
            player["sou_chef_order"] = sou_chef_order
            player["sou_chef_task"] = sou_chef_task
            player["sou_chef_left_ticks"] = sou_chef_left_ticks
            player["server_order"] = server_order
            player["server_task"] = server_task
            player["server_left_ticks"] = server_left_ticks
            player["ticks"] = ticks
            player["order0_task0"] = matrix[0][0]
            player["order0_task1"] = matrix[0][1]
            player["order0_task2"] = matrix[0][2]
            player["order1_task0"] = matrix[1][0]
            player["order1_task1"] = matrix[1][1]
            player["order1_task2"] = matrix[1][2]
            player["order2_task0"] = matrix[2][0]
            player["order2_task1"] = matrix[2][1]
            player["order2_task2"] = matrix[2][2]
            player["order3_task0"] = matrix[3][0]
            player["order3_task1"] = matrix[3][1]
            player["order3_task2"] = matrix[3][2]

            out = pd.concat([out, player])
        final36 = pd.concat([final36, out])

    return final36

def get_state(args):
    dat = get_dat(args.file)
    return pd.concat([get_state12(dat), get_state36(dat)])
    

