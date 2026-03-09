import sys
sys.stdin = open("rudolf.txt", "r")
from pprint import pprint
# 저번에 짠건 300 줄이니까 더 짧게 짜보자

N,M,P,C,D = map(int,input().split())
r_x,r_y = map(int,input().split())
r_x-=1
r_y-=1
snow_map = [[0]*N for _ in range(N)]
snow_map[r_x][r_y] = -1 # 루돌프 표시
santa_loc =[0]*P
for p in range(P):
    num, s_x,s_y = map(int,input().split())
    snow_map[s_x-1][s_y-1] = num # 산타 번호 표시, 위치는 1빼줘야함
    santa_loc[num-1] = [s_x-1,s_y-1]
santa_life =[1]*P
santa_score = [0] *P

s_nx =[-1,0,1,0]
s_ny = [0,1,0,-1]
r_nx =[1,1,1,0,0,-1,-1,-1]
r_ny = [1,0,-1,1,-1,1,0,-1]

def inside(x,y):
    return 0<=x<N and 0<=y<N

def distance(r1,c1,r2,c2):
    return (r1-r2)*(r1-r2) + (c1-c2)*(c1-c2)

def scan(x,y): # 루돌프 기준으로 젤 가까운 산타 찾음
    dis = float('inf')
    res_x,res_y =0,0
    for i in range(N-1,-1,-1):
        for j in range(N-1,-1,-1):
            if snow_map[i][j]>0: # 산타 숫자는 바뀜
                if dis > distance(i,j,x,y):
                    dis = distance(i,j,x,y)
                    res_x, res_y = i,j
    return (res_x,res_y)

def s2s_collision(s_x,s_y,dir_x,dir_y,santa):
    santa2 = snow_map[s_x][s_y] # 기존에 있던 산타
    snow_map[s_x][s_y] = santa # 일단 알박기
    santa_loc[santa-1] = [s_x,s_y] # 위치 기록
    s_x += dir_x
    s_y += dir_y
    if not inside(s_x,s_y):
        santa_life[santa2-1] = -1 # 사망
    elif snow_map[s_x][s_y] >0: # 다른 산타인경우
        s2s_collision(s_x,s_y,dir_x,dir_y,santa2) # 한번더
    else: # 빈자리인 경우
         snow_map[s_x][s_y]= santa2
         santa_loc[santa2 - 1] = [s_x, s_y]  # 위치 기록

def s2r_collision(s_x,s_y,r_x,r_y):
    santa = snow_map[s_x][s_y]
    santa_score[santa-1] += D # 1빼줘야함
    snow_map[s_x][s_y] = 0 # 산타 삭제
    # print(s_x,s_y)
    dir_x =s_x-r_x
    dir_y =s_y-r_y
    s_x += dir_x*(D-1)
    s_y += dir_y * (D - 1)
    # print(s_x, s_y)
    santa_life[santa - 1] = 0  # 기절
    if not inside(s_x,s_y):
        santa_life[santa-1] = -1
    elif snow_map[s_x][s_y] != 0:
        s2s_collision(s_x,s_y,dir_x,dir_y,santa)
    else:
        snow_map[s_x][s_y] = santa # 산타 이동해둠
        santa_loc[santa - 1] = [s_x, s_y]  # 위치 기록
    # pprint(snow_map)

def r2s_collision(r_x,r_y,s_x,s_y):
    santa = snow_map[s_x][s_y]
    santa_score[santa - 1] += C # 1빼줘야함
    snow_map[r_x][r_y] = 0
    snow_map[s_x][s_y] = -1  # 산타 자리에 루돌프
    dir_x =s_x-r_x
    dir_y =s_y-r_y
    s_x += dir_x*C
    s_y += dir_y * C
    santa_life[santa - 1] = 0  # 기절
    # print(santa_life)
    if not inside(s_x, s_y):
        santa_life[santa - 1] = -1
    elif snow_map[s_x][s_y] != 0:
        s2s_collision(s_x, s_y, dir_x, dir_y, santa)
    else:
        snow_map[s_x][s_y] = santa  # 산타 이동해둠
        santa_loc[santa - 1] = [s_x, s_y]  # 위치 기록

def s_move(num,r_x,r_y):
    [s_x, s_y] = santa_loc[num]
    # print(num + 1, s_x, s_y)
    min_dis = distance(s_x, s_y, r_x, r_y)
    res_x, res_y = s_x, s_y
    for i in range(4):
        nx = s_x + s_nx[i]
        ny = s_y + s_ny[i]
        if inside(nx, ny) and snow_map[nx][ny] <= 0 and min_dis > distance(nx, ny, r_x, r_y):
            # 루돌프거나 빈자리만 이동
            res_x, res_y = nx, ny  # 가만히있는거랑 다같을수는 없을걸
            min_dis = distance(nx, ny, r_x, r_y)
    if snow_map[res_x][res_y] == -1:
        s2r_collision(s_x, s_y, r_x, r_y)  # 당장은 이동안시키고 그냥 바로 충돌함수 하면 이동까지 해줌
    else:
        snow_map[s_x][s_y] = 0  # 기존 위치 삭제
        snow_map[res_x][res_y] = num + 1  # 이동 (무조건 1을 더해줘야함!!!)
        santa_loc[num] = [res_x, res_y]  # 기록
        # print(num + 1, res_x, res_y)

def r_move():
    global r_x,r_y
    (s_x,s_y) = scan(r_x,r_y)
    min_dis =float('inf')
    res_x,res_y = 0,0
    for i in range(8):
        nx = r_x + r_nx[i]
        ny = r_y + r_ny[i]
        if inside(nx, ny) and min_dis > distance(nx, ny, s_x, s_y):
            # 갈수있는 자리 찾음
            res_x, res_y = nx, ny  # 가만히있는거랑 다같을수는 없을걸
            min_dis = distance(nx, ny, s_x, s_y)
    if snow_map[res_x][res_y] >0:
        r2s_collision(r_x,r_y,res_x,res_y)
    else:
        snow_map[r_x][r_y] = 0
        snow_map[res_x][res_y] = -1  # 산타 자리에 루돌프
    r_x,r_y = res_x,res_y


for m in range(M):
    # pprint(snow_map)
    # print(santa_life)
    r_move()
    done = True
    for p in range(P):
        if santa_life[p] == 1:# 아 이걸 안하면 다음턴에서 기절 회복해야하는데 이번턴에 회복해버리네 루돌프가 박으면
            s_move(p,r_x,r_y)
    # 다하고 나서 점수 더해야함 왜냐면 산타끼리 부딫힐수도있으니까

    for p in range(P):
        if santa_life[p] != -1:
            santa_score[p] += 1 # 살아있으면 점수증가
            done = False
            if santa_life[p] == 0:
                santa_life[p] =2
            elif santa_life[p] == 2: # 한턴은 기절된상황
                santa_life[p] = 1
    if done:
        break
    #print(*santa_score)

print(*santa_score) # 공백으로 출력