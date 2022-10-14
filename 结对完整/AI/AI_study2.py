import math
import copy
from tkinter import N
from xml.dom.expatbuilder import parseString
import pandas as pd
from turtle import clear
from unicodedata import name
import numpy as np
from numpy import random

win_num=0
b_a=0
list_name=[]
list_score=[]


def is_end(a,b):
    a_end=0
    b_end=0
    for i in range(0,3):
        for j in range(0,3):
            if a[i][j]==0:
                a_end=1
            if b[i][j]==0:
                b_end=1
    return a_end and b_end

def dice_clear(dice,i,mat):
    for j in range(0,3):
        if mat[i][j]==dice:
            mat[i][j]=0

def cal_score(mat):
    score=0
    for i in range(0,3):
        x=mat[i][0]
        y=mat[i][1]
        z=mat[i][2]
        if x==y and y==z:
            score+=x*3*3
        else:
            if x==y:
                score+=x*2*2+z
            elif y==z:
                score+=y*2*2+x
            elif x==z:
                score+=x*2*2+y
            else:
                score+=x+y+z
    return score

def cal_risk(aa,bb):#aa是敌人，bb是自己
    risk=0
    for i in range(0,3):
        row_zero=0
        for j in range(0,3):#计算风险度
            if aa[i][j]==0:
                row_zero+=1
        dice=[0,0,0,0,0,0,0]#骰子点数出现的次数
        num=[0,0,0]#有多分数可以削去
        num_index=0#分数的个数
        for j in range(0,3):#将格子转换成对应骰子出现的次数
            dice[bb[i][j]]+=1
        for j in range(1,7):
            if dice[j]:#该骰子出现过
                num[num_index]=j*dice[j]*dice[j]#骰子大小*出现次数^2
                num_index+=1
        num.sort(reverse=True)#排序
        for j in range(0,row_zero):
            risk+=num[j]
    return risk

def cal_grow(mat):
    grow=0
    for i in range(0,3):#遍历3行
        row_zero=0
        dice=[0,0,0,0,0,0,0]#骰子点数出现的次数
        for j in range(0,3):
            if mat[i][j]==0:
                row_zero+=1
            else:
                dice[mat[i][j]]+=1
        if row_zero==2:
            max_dice=0
            for j in range(1,7):
                if dice[j]!=0:
                    max_dice=j
            grow+=max_dice*2.5*2.5
        elif row_zero==1:
            max_dice=0
            for j in range(1,7):
                if dice[j]!=0:
                    max_dice=j
            grow+=max_dice*2*2
        else:
            pass
    return grow


def AI_set_dice(i,j,dice,b_r,a_r,b_g,mat1,mat2):
    aa=mat2.copy()
    bb=mat1.copy()
    bb[i][j]=dice
    dice_clear(dice,i,aa)
    a_score=cal_score(aa)
    b_score=cal_score(bb)
    b_risk=cal_risk(aa,bb)#b的风险
    a_risk=cal_risk(bb,aa)#a的风险
    b_grow=cal_grow(bb)
    b_a_score=b_score-a_score
    return b_a_score-b_r*(1+b_a*b_a_score/b_score)*b_risk+a_r*(1-b_a*b_a_score/b_score)*a_risk+b_g*b_grow
        
        
def AI_play(dice,b_r,a_r,b_g,mat1,mat2):#mat1作为AI，mat2作为敌对
    x_i=0 
    x_j=0 
    x_sco=-9999
    y_i=0
    y_j=0
    y_sco=-9999
    z_i=0
    z_j=0
    z_sco=-9999
    for i in range(0,3):#搜索前三行
        for j in range(0,3):#搜索第i行
            if mat1[i][j]==0:
                if i==0:
                    x_i=i
                    x_j=j
                    x_sco=AI_set_dice(i,j,dice,b_r,a_r,b_g,mat1,mat2)
                elif i==1:
                    y_i=i
                    y_j=j
                    y_sco=AI_set_dice(i,j,dice,b_r,a_r,b_g,mat1,mat2)
                else:
                    z_i=i
                    z_j=j
                    z_sco=AI_set_dice(i,j,dice,b_r,a_r,b_g,mat1,mat2)
                break
    if x_sco>=y_sco and x_sco>=z_sco:
        mat1[x_i][x_j]=dice
        dice_clear(dice,x_i,mat2)
    elif y_sco>=x_sco and y_sco>=z_sco:
        mat1[y_i][y_j]=dice
        dice_clear(dice,y_i,mat2)
    else:
        mat1[z_i][z_j]=dice
        dice_clear(dice,z_i,mat2)


# 检查游戏是否结束
def check(player):
    count = 0
    for i in player:
        for j in i:
            if j == 0:
                count += 1
    if count == 0:
        return True
    else:
        return False


# 判定能否消除对手数字
def judge(col, num, arch):
    for i in range(3):
        if arch[i][col] == num:
            arch[i][col] = 0
    return arch

def count(player):
    sum = 0
    count_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for i in range(3):
        count_dict[int(player[int(i)][0])] += 1
    for key in count_dict.keys():
        sum += int(key) * count_dict[key] * count_dict[key]
    count_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for i in range(3):
        count_dict[int(player[int(i)][1])] += 1
    for key in count_dict.keys():
        sum += int(key) * count_dict[key] * count_dict[key]
    count_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for i in range(3):
        count_dict[int(player[int(i)][2])] += 1
    for key in count_dict.keys():
        sum += int(key) * count_dict[key] * count_dict[key]
    return sum


def computer(get_num, ai, player):
    # =============================================================================
    copy_ai = copy.deepcopy(ai)  # 复制一份原表格
    copy_player = copy.deepcopy(player)
    col_cnt = [[0, 0, 0], [0, 0, 0], [0, 0, 0],
               [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    can_done = [0, 0, 0]
    # =============================================================================
    # 设置col_cnt\can_done
    for i in range(3):
        for j in range(3):
            col_cnt[copy_player[j][i]][i] += 1  # 玩家表格：值，第几列，个数++
            if copy_ai[i][j] == 0:
                can_done[j] += 1        # 计算当前状态ai每一列可以下多少子
    # =============================================================================
    if get_num >= 3:
        for j in range(3):
            # 如果某一列和get_num值（大于等于三）相同的>=2个，并且可以下，那就下
            if col_cnt[get_num][j] >= 2 and can_done[j] >= 1:
                for i in range(3):
                    if ai[i][j] == 0:
                        ai[i][j] = get_num
                        judge(j, get_num, player)
                        return ai
            # 如果get_num为4、5、6，如果对面可以有得消，并且可以下，那就下
            elif get_num >= 4 and col_cnt[get_num][j] >= 1 and can_done[j] >= 1:
                for i in range(3):
                    if ai[i][j] == 0:
                        ai[i][j] = get_num
                        judge(j, get_num, player)
                        return ai
            # 检查是否4、5、6双连及以上,3三连 and 是否可下，如果有空，则留空，在其他列贪心。
            elif col_cnt[4][j] >= 2 or col_cnt[5][j] >= 2 or col_cnt[6][j] >= 2 or col_cnt[3] == 3 \
                    and can_done[0] + can_done[1] + can_done[2] > can_done[j]:  # 上次编辑地
                max_point = -162  # 最离谱分差
                best_row = 0
                best_col = 0
                for row in range(3):
                    for col in range(3):
                        if col != j:
                            if ai[row][col] != 0:
                                continue
                            else:
                                copy_ai = copy.deepcopy(ai)  # 复制一份原表格
                                copy_player = copy.deepcopy(player)
                                copy_ai[row][col] = get_num
                                copy_player = judge(col, get_num, copy_player)
                                point = count(copy_ai)-count(copy_player)
                                if point > max_point:
                                    best_row = row
                                    best_col = col
                                    max_point = point
                ai[best_row][best_col] = get_num
                judge(best_col, get_num, player)
                return ai

            # 如果对面没有：(🔺🔺🔺检查🔺🔺🔺)
            else:
                max_point = -162  # 最离谱分差
                best_row = 0
                best_col = 0
                for row in range(3):
                    for col in range(3):
                        if ai[row][col] != 0:
                            continue
                        else:
                            copy_ai = copy.deepcopy(ai)  # 复制一份原表格
                            copy_player = copy.deepcopy(player)
                            copy_ai[row][col] = get_num
                            copy_player = judge(col, get_num, copy_player)
                            point = count(copy_ai)-count(copy_player)
                            if point > max_point:
                                best_row = row
                                best_col = col
                                max_point = point
                ai[best_row][best_col] = get_num
                judge(best_col, get_num, player)
                return ai
    elif get_num < 3:
        jmax = 0
        done_max = 0
        # 选择空最多的落子
        for j in range(3):
            if can_done[j] > done_max:
                done_max = can_done[j]
                jmax = j
        for i in range(3):
            if ai[i][jmax] == 0:
                ai[i][jmax] = get_num
                judge(jmax, get_num, player)
                return ai


def play(b_r,a_r,b_g):#游戏开始
    a=np.array([[0,0,0],[0,0,0],[0,0,0]])
    b=np.array([[0,0,0],[0,0,0],[0,0,0]])
    while 1:#判断是否结束
        #AI(B)投骰子
        a=a.T
        dice=np.random.randint(1,7,1)
        AI_play(dice,b_r,a_r,b_g,b,a)
        a=a.T
        # print("B玩家的骰子是"+str(dice))
        # a=a.T
        # print(a)
        # print(b)
        # a=a.T
        a.T
        if is_end(a,b)==0:
            break
        a.T
        #AI(A)投骰子
        b=b.T
        dice=np.random.randint(1,7,1)
        computer(int(dice),a,b)
        b=b.T
        # print("A玩家的骰子是"+str(dice))
        # a=a.T
        # print(a)
        # print(b)
        # a=a.T
        a.T
        if is_end(a,b)==0:
            break
        a.T
    a=a.T
    if cal_score(b)>cal_score(a):
        return 1
    else:
        return 0


def main():
    win_rate=0.555
    T=10
    n=2000
    x=0.083
    y=0.155
    z=0.083
    n_b_a=1.177
    f=open('url_part','w', encoding='utf-8')
    while T:
        for k in range(1,61):
            a=0
            b=0
            n_x=x+0.001*np.random.randint(-9,10,1)
            n_y=y+0.001*np.random.randint(-9,10,1)
            n_z=z+0.001*np.random.randint(-9,10,1)
            b_a=n_b_a+0.001*np.random.randint(-9,10,1)
            for l in range(1,int(n+1)):
                if play(n_x,n_y,n_z)==1:
                    b+=1
                else:
                    a+=1
            print(n_x)
            print(n_y)
            print(n_z)
            print(b_a)
            print("a:"+str(a/n))
            print("b:"+str(b/n))
            n_win_rate=b/n
            if b/n>0.57:
                f.write(parseString(b/n))
                f.write(parseString(n_x))
                f.write(parseString(n_y))
                f.write(parseString(n_z))
                f.write(parseString(b_a))
            if n_win_rate>win_rate:
                x=n_x
                y=n_y
                z=n_z
                n_b_a=b_a
                win_rate=n_win_rate
            else :
                m=random.rand()
                print(math.exp(-(win_rate-n_win_rate)/T*1000))
                if m<=math.exp(-(win_rate-n_win_rate)/T*1000):
                    x=n_x
                    y=n_y
                    z=n_z
                    n_b_a=b_a
                    win_rate=n_win_rate
        T-=1
if __name__ == '__main__':
    main()