def play_B(mat1,mat2,dice):
    import copy
    
    def dice_clear(dice,i,mat):
        for j in range(0,3):
            if mat[i*3+j]==dice:
                mat[i*3+j]=0

    def cal_score(mat):
        score=0
        for i in range(0,3):
            x=mat[i*3]
            y=mat[i*3+1]
            z=mat[i*3+2]
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
                if aa[i*3+j]==0:
                    row_zero+=1
            dice=[0,0,0,0,0,0,0]#骰子点数出现的次数
            num=[0,0,0]#有多分数可以削去
            num_index=0#分数的个数
            for j in range(0,3):#将格子转换成对应骰子出现的次数
                dice[int(bb[i*3+j])]+=1
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
                if mat[i*3+j]==0:
                    row_zero+=1
                else:
                    dice[int(mat[i*3+j])]+=1
            if row_zero==2:
                max_dice=0
                for j in range(1,7):
                    if dice[j]!=0:
                        max_dice=j
                grow+=max_dice*2.4*2.4
            elif row_zero==1:
                max_dice=0
                for j in range(1,7):
                    if dice[j]!=0:
                        max_dice=j
                grow+=max_dice*2*2
            else:
                pass
        return grow

    def AI_set_dice(i,j,dice,mat1,mat2):
        aa=copy.deepcopy(mat2)
        bb=copy.deepcopy(mat1)
        bb[i*3+j]=dice
        dice_clear(dice,i,aa)
        a_score=cal_score(aa)
        b_score=cal_score(bb)
        b_risk=cal_risk(aa,bb)#b的风险
        a_risk=cal_risk(bb,aa)#a的风险
        b_grow=cal_grow(bb)
        a_grow=cal_grow(aa)
        b_a_score=b_score-a_score
        return b_a_score-b_r*(1+b_a*b_a_score/b_score)*b_risk+a_r*(1-b_a*b_a_score/b_score)*a_risk+b_g*b_grow-a_g*a_grow

        
    def AI_play(mat1,mat2,dice):#mat1作为AI，mat2作为敌对
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
                if mat1[i*3+j]==0:
                    if i==0:
                        x_i=i
                        x_j=j
                        x_sco=AI_set_dice(i,j,dice,mat1,mat2)
                    elif i==1:
                        y_i=i
                        y_j=j
                        y_sco=AI_set_dice(i,j,dice,mat1,mat2)
                    else:
                        z_i=i
                        z_j=j
                        z_sco=AI_set_dice(i,j,dice,mat1,mat2)
                    break
        if x_sco>=y_sco and x_sco>=z_sco:
            return x_i*3+x_j
        elif y_sco>=x_sco and y_sco>=z_sco:
            return y_i*3+y_j
        else:
            return z_i*3+z_j
        
    return AI_play(mat1,mat2,dice)