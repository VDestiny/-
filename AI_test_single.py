import pandas as pd
from turtle import clear
from unicodedata import name
import numpy as np

win_num=0
list_name=[]
list_score=[]

def is_end(a,b):
    a_end=0
    b_end=0
    for i in range(1,4):
        for j in range(1,4):
            if a[i][j]==0:
                a_end=1
            if b[i][j]==0:
                b_end=1
    return a_end and b_end

def dice_clear(dice,i,mat):
    for j in range(1,4):
        if(mat[i][j]==dice):
            mat[i][j]=0;

def cal_score(mat):
    score=0
    for i in range(1,4):
        x=mat[i][1]
        y=mat[i][2]
        z=mat[i][3]
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

def cal_risk(aa,bb):
    risk=0
    for i in range(1,4):
        row_zero=0
        for j in range(1,4):#计算风险度
            if aa[i][j]==0:
                row_zero+=1
        dice=[0,0,0,0,0,0,0]#骰子点数出现的次数
        num=[0,0,0]#有多分数可以削去
        num_index=0#分数的个数
        for j in range(1,4):#将格子转换成对应骰子出现的次数
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
    for i in range(1,4):#遍历3行
        row_zero=0
        dice=[0,0,0,0,0,0,0]#骰子点数出现的次数
        for j in range(1,4):
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
    return b_a_score-b_r*b_risk+a_r*a_risk+b_g*b_grow
        
        
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
    for i in range(1,4):#搜索前三行
        for j in range(1,4):#搜索第i行
            if mat1[i][j]==0:
                if i==1:
                    x_i=i
                    x_j=j
                    x_sco=AI_set_dice(i,j,dice,b_r,a_r,b_g,mat1,mat2)
                elif i==2:
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


def play(b_r,a_r,b_g):#游戏开始
    a=np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    b=np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    while is_end(a,b):#判断是否结束
        #AI(A)投骰子
        dice=np.random.randint(1,7,1)
        AI_play(dice,0.3,0.3,0.2,a,b)
        print("A玩家投掷的骰子点数是：")
        print(dice)
        print("A:")
        print(a)
        print("B:")
        print(b)
        if is_end()==0:
            break
        #AI(B)投骰子
        dice=np.random.randint(1,7,1)
        AI_play(dice,b_r,a_r,b_g,b,a)
        print("B玩家投掷的骰子点数是：")
        print(dice)
        print("A:")
        print(a)
        print("B:")
        print(b)
        if is_end()==0:
            break
    if cal_score(b)>=cal_score(a):
        return 1
    else:
        return 0


def main():
    win_num=0
    for l in range(1,2):
        if play(0.4,0.4,0.1)==1:
            win_num+=1
    print(win_num)
             
if __name__ == '__main__':
    main()