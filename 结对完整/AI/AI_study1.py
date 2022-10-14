from ftplib import B_CRLF
import numpy as np

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

def play_A(ownBoard, otherBoard, figure):
    import copy
    player_a = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    player_b = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    num = figure

    player_a[0][0] = ownBoard[0]
    player_a[0][1] = ownBoard[3]
    player_a[0][2] = ownBoard[6]
    player_a[1][0] = ownBoard[1]
    player_a[1][1] = ownBoard[4]
    player_a[1][2] = ownBoard[7]
    player_a[2][0] = ownBoard[2]
    player_a[2][1] = ownBoard[5]
    player_a[2][2] = ownBoard[8]

    player_b[0][0] = otherBoard[0]
    player_b[0][1] = otherBoard[3]
    player_b[0][2] = otherBoard[6]
    player_b[1][0] = otherBoard[1]
    player_b[1][1] = otherBoard[4]
    player_b[1][2] = otherBoard[7]
    player_b[2][0] = otherBoard[2]
    player_b[2][1] = otherBoard[5]
    player_b[2][2] = otherBoard[8]

    # 判定能否消除对手数字

    def judge(col, num, arch):
        for i in range(3):
            if arch[i][col] == num:
                arch[i][col] = 0
        return arch

    # 统计玩家分数 传入玩家列表 返回分数

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

    def computer(ai, player):
        get_num = int(num)
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
                col_cnt[int(copy_player[j][i])][i] += 1  # 玩家表格：值，第几列，个数++
                if copy_ai[i][j] == 0:
                    can_done[j] += 1        # 计算当前状态ai每一列可以下多少子
        # =============================================================================
        for j in range(3):
            # 如果某一列和get_num值（大于等于三）相同的>=2个，并且可以下，那就下
            if get_num >= 3 and col_cnt[int(get_num)][j] >= 2 and can_done[j] >= 1:
                for i in range(3):
                    if ai[i][j] == 0:
                        ai[i][j] = get_num
                        judge(j, get_num, player)
                        fi = i + 3 * j
                        return fi
            # 如果get_num为4、5、6，如果对面可以有得消，并且可以下，那就下
            elif get_num >= 4 and col_cnt[int(get_num)][j] >= 1 and can_done[j] >= 1:
                for i in range(3):
                    if ai[i][j] == 0:
                        ai[i][j] = get_num
                        judge(j, get_num, player)
                        fi = i + 3 * j
                        return fi
            # 检查是否4、5、6双连及以上,3三连 and 是否可下，如果有空，则留空，在其他列贪心。
            elif get_num >= 3 and (col_cnt[4][j] >= 2 or col_cnt[5][j] >= 2 or col_cnt[6][j] >= 2 or col_cnt[3][j] == 3) \
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
                                copy_player = judge(
                                    col, get_num, copy_player)
                                point = count(copy_ai)-count(copy_player)
                                if point > max_point:
                                    best_row = row
                                    best_col = col
                                    max_point = point
                ai[best_row][best_col] = get_num
                judge(best_col, get_num, player)
                fi = best_row + 3 * best_col
                return fi
            # 2222======== =
            elif get_num < 3 and (col_cnt[4][j] >= 2 or col_cnt[5][j] >= 2 or col_cnt[6][j] >= 2 or col_cnt[3][j] == 3) \
                    and can_done[0] + can_done[1] + can_done[2] > can_done[j]:
                avoid_j = j
                colmax = 0
                done_max = 0
                for col in range(0, 3):
                    if col != avoid_j:
                        if can_done[col] > done_max:
                            done_max = can_done[col]
                            colmax = col
                for i in range(0, 3):
                    if ai[i][colmax] == 0:
                        ai[i][colmax] = get_num
                        judge(colmax, get_num, player)
                        fi = i + 3 * colmax
                        return fi

            # 3333========

            elif get_num == 1 and col_cnt[1][j] >= 2 and can_done[0] + can_done[1] + can_done[2] > can_done[j]:
                avoid_j = j
                colmax = 0
                done_max = 0
                for col in range(0, 3):
                    if col != avoid_j:
                        if can_done[col] > done_max:
                            done_max = can_done[col]
                            colmax = col
                for i in range(0, 3):
                    if ai[i][colmax] == 0:
                        ai[i][colmax] = get_num
                        judge(colmax, get_num, player)
                        fi = i + 3 * colmax
                        return fi
            # 44444=========

            elif get_num == 2 and col_cnt[2][j] == 1 and can_done[0] + can_done[1] + can_done[2] > can_done[j]:
                avoid_j = j
                colmax = 0
                done_max = 0
                for col in range(0, 3):
                    if col != avoid_j:
                        if can_done[col] > done_max:
                            done_max = can_done[col]
                            colmax = col
                for i in range(0, 3):
                    if ai[i][colmax] == 0:
                        ai[i][colmax] = get_num
                        judge(colmax, get_num, player)
                        fi = i + 3 * colmax
                        return fi

            # 555555========
            elif get_num < 3 and j == 2:
                colmax = 0
                done_max = 0
                for col in range(0, 3):
                    if can_done[col] > done_max:
                        done_max = can_done[col]
                        colmax = col
                for i in range(0, 3):
                    if ai[i][colmax] == 0:
                        ai[i][colmax] = get_num
                        judge(colmax, get_num, player)
                        fi = i + 3 * colmax
                        return fi

            # 6666666666如果对面没有：(🔺🔺🔺检查🔺🔺🔺)
            elif get_num >= 3 and j == 2:
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
                fi = best_row + 3 * best_col
                return fi

    # player_a 为我方， player_b 为对方

    outputNum = computer(player_a, player_b)

    return outputNum

def is_end(a,b):
    is_a=1
    is_b=1
    for i in range(0,9):
        if a[i]==0:
            is_a=0
        if b[i]==0:
            is_b=0
    return is_a or is_b

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

def printf(a,b):
    print("A:")
    for i in range(0,3):
        print(str(a[i*3])+' '+str(a[i*3+1])+' '+str(a[i*3+2]))
    print("B:")
    for i in range(0,3):
        print(str(b[i*3])+' '+str(b[i*3+1])+' '+str(b[i*3+2]))
    print('\=======================================/')

def play():
    a=[0,0,0,0,0,0,0,0,0]
    b=[0,0,0,0,0,0,0,0,0]
    while 1:
        dice=np.random.randint(1,7,1)
        pos=int(play_A(a,b,dice))
        a[pos]=dice
        dice_clear(dice,int(pos/3),b)
        if is_end(a,b):
            break
        
        
        dice=np.random.randint(1,7,1)
        pos=int(play_B(b,a,dice))
        b[pos]=dice
        dice_clear(dice,int(pos/3),a)
        if is_end(a,b):
            break

    if cal_score(a)>cal_score(b):
        return 1
    else :
        return 0

b_r=0.12
a_r=0.12
b_g=0.08
a_g=0.08
b_a=0.7         
def main():
    n=1000
    f=open('url_part','w', encoding='utf-8')
    for i in range(1,7):
        for j in range(1,7):
            for k in range(1,7):
                for l in range(1,7):
                    for o in range(5,16):
                        b_r=i*0.05
                        a_r=j*0.05
                        b_g=k*0.05
                        a_g=l*0.05
                        b_a=o*0.1 
                        aa=0
                        bb=0
                        for m in range(1,n+1):
                            if play()==1:
                                aa+=1
                            else:
                                bb+=1
                        f.write(str(b_r)+'\n')
                        f.write(str(a_r)+'\n')
                        f.write(str(b_g)+'\n')
                        f.write(str(a_g)+'\n')
                        f.write(str(b_a)+'\n')
                        f.write(str(bb/n)+'\n'+'\n')
                        print(aa/n)
                        print(bb/n)
    f.close()

if __name__ == "__main__":
    main()