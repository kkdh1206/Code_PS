import copy
from collections import deque
import sys
from pprint import pprint
sys.stdin = open("time_machine.txt","r")
dx = [0,0,1,-1]
dy = [1,-1,0,0] # 동서남북
# 입력받기
N,M,F = map(int,input().split())
map_2D =[list(map(int,input().split())) for _ in range(N)]
east = [list(map(int,input().split())) for _ in range(M)]
west = [list(map(int,input().split())) for _ in range(M)]
south = [list(map(int,input().split())) for _ in range(M)]
north = [list(map(int,input().split())) for _ in range(M)]
top = [list(map(int,input().split())) for _ in range(M)]
wierd = []
for i in range(F):
    wierd.append(list(map(int,input().split()))) # r c d v 를 받음
map_3D = [[5]*3*M for _ in range(3*M)]
def spread(x,y,d,map_2D): # 이거 x y 값도 바꾸게 반환해야함
    if map_2D[x][y] == 0:
        map_2D[x][y] = 5
    if inside_2D(x+dx[d], y+dy[d]):
        x += dx[d]
        y+=dy[d]
        if map_2D[x][y] ==0:
            map_2D[x][y] = 5 # 이상현상 5라두자
    return [x,y]

print(wierd)
pprint(map_2D)

def reflect(x,y): # 기준을 M 으로 둠
    # 예외가 발생하지 않을듯
    if x == M and y == 0:
        return [y,x]
    if x == 0 and y == M:
        return [y,x]
    if x == 3*M and y == 2*M:
        return [y,x]
    if x == 2*M and y == 3*M:
        return [y,x]

    if abs(x-y) >= M   :
        return [3*M-1-y,3*M-1-x]
    return [y,x]

# map_3D[0][3] = -1
# [i,j] = reflect(0,3)
# map_3D[i][j] =-1
# pprint(map_3D)

def turn(some_map):
    copy_map = copy.deepcopy(some_map) # 요소를 복사해둠 영향없게
    for i in range(M):
        for j in range(M):
            some_map[i][j] = copy_map[j][M-1-i] # 반시계 회전
            # 아 배열크기가 M-1까지인걸 까먹으면안됨

# for row in east:
#     print(*row)
# turn(east)
# for row in east:
#     print(*row)

def inside_3D(x,y):
    return 0<=x<3*M and 0<=y<3*M

def inside_2D(x,y):
    return 0<=x<N and 0<=y<N

def find_wall(map_2D):
    min_i,min_j = N-1,N-1
    max_i,max_j = 0,0
    for i in range(N):
        for j in range(N):
            if map_2D[i][j] == 3:
                min_i = min(min_i,i)
                max_i = max(max_i,i)
                min_j = min(min_j, j)
                max_j = max(max_j, j)
    #return [min_i,min_j,max_i,max_j]
    x1 = min_i -1
    y1 = min_j -1

    for i in range(M+2):
        for j in range(M+2):
            if map_2D[i+x1][j+y1] == 0:
                result_x =i-1+M
                result_y = j-1+M
                if result_x <M:
                    result_x =0
                elif result_x >= 2*M:
                    result_x = 3*M-1
                else:
                    if result_y < M:
                        result_y = 0
                    elif result_y >= 2 * M:
                        result_y = 3 * M - 1
                return [result_x,result_y,x1+i,y1+j]

#print(find_wall(map_2D))

# print(find_wall(map_2D))
#
# def find_exit(map_3D): # 사실 2D를 조사해야함
#     east_exit = False
#     west_exit = False
#     south_exit = False
#     north_exit = False
#     locate = -1
#     x1,y1,x2,y2 = find_wall(map_3D)
#     x1 -=1
#     y1 -=1
#     x2 +=1
#     y2 +=1
#     if inside_2D(x1,y1) and inside_2D(x2,y2):
#     for i in range((N-M)//2  ,(N+M)//2 ,1): # +1 안하는게맞음
#         if map_3D[i][(N+M)//2] == 0 : # 동쪽
#             east_exit = True
#             locate = i
#         elif map_3D[i][(N-M)//2-1] == 0: # 서쪽
#             west_exit = True
#             locate = i
#         elif map_3D[(N+M)//2][i] == 0: # 남쪽
#             south_exit = True
#             locate = i
#         elif map_3D[(N-M)//2][i] == 0: # 북쪽
#             north_exit = True
#             locate = i
#     i = locate
#     if east_exit:
#         return [i-(N-M)//2+M,3*M-1] # 방향이 아니라 위치 바로 줄수 있을듯 이렇게 기준을 M 으로 바꾸고
#     elif west_exit:
#         return [i-(N-M)//2+M,0] # 방향이 아니라 위치 바로 줄수 있을듯 이렇게 기준을 M 으로 바꾸고
#     elif south_exit:
#         return [3*M-1,i-(N-M)//2+M] # 방향이 아니라 위치 바로 줄수 있을듯 이렇게 기준을 M 으로 바꾸고
#     elif north_exit:
#         return [0,i-(N-M)//2+M] # 방향이 아니라 위치 바로 줄수 있을듯 이렇게 기준을 M 으로 바꾸고

#print(find_exit(map_2D))


    # 위치반환


# 여기서 출구 위치 찍어두기

time = 0
turn(east)
turn(north)
turn(north)
turn(west)
turn(west)
turn(west)

isEscape = False

for i in range(M):
    for j in range(M):
        map_3D [i][j+M] = north[i][j]
        map_3D [i+2*M][j+M] = south[i][j]
        map_3D[i +M][j] = west[i][j]
        map_3D[i + M][j+2*M] = east[i][j]
        map_3D[i + M][j+M] = top[i][j] # 값가져온거라 참조문제는 없을듯
# 지도 제작완료
[exit_x , exit_y, exit_2D_x, exit_2D_y]= find_wall(map_2D)
map_3D[exit_x][exit_y] = 4 # 탈출구 찾아서
# 여기서 visit 값을 time 저장을 한번하기
for i in range(4):
    nx = dx[i] + exit_2D_x
    ny = dy[i] + exit_2D_y
    if map_2D[nx][ny] == 3:
        exit_2D_x = nx
        exit_2D_y = ny
        break
pprint(map_3D)
time_x, time_y = 0,0
for i in range(3*M):
    for j in range(3*M):
        if map_3D[i][j] ==2 :
            time_x =i
            time_y = j


# BFS 하기
# Reflect 이동 반영해서
queue = deque()
visit = [[0]*3*M for _ in range(3*M)]
path = [[0]*3*M for _ in range(3*M)]
queue.append([time_x,time_y])
visit[time_x][time_y] = 1
while queue:
    q = queue.popleft()
    for i in range(4):
        nx = q[0] + dx[i]
        ny = q[1] + dy[i]
        if inside_3D(nx,ny) and visit[nx][ny] == 0 and map_3D[nx][ny] != 1: # 장애물 아닐때
            visit[nx][ny] =1
            if map_3D[nx][ny] == 5:
                visit[nx][ny] = 1
                nx,ny = reflect(q[0],q[1]) # 이전 좌표 reflect
                if visit[nx][ny] == 0 and map_3D[nx][ny] != 1:
                    visit[nx][ny] = 1
                    path[nx][ny] = path[q[0]][q[1]] + 1  # 한칸씩 더해줌
                    queue.append([nx, ny])
            else:
                path[nx][ny] = path[q[0]][q[1]] + 1 # 한칸씩 더해줌
                queue.append([nx,ny])
            if map_3D[nx][ny] == 4: # 탈출시
                queue = deque() # 빈거로 나둬버림
print("======")
pprint(path)
print("======")
for i in range(3*M):
    for j in range(3*M):
        if map_3D[i][j] ==4 and path[i][j] !=0:
            isEscape = True
            time = path[i][j]
print(time)
if not isEscape:
    print(-1)
else:
    print(time)
    for w in wierd:
        [r, c, d, v]=w
        for i in range(time // v):  # for 문으로 각각의 v에 대해 해야할듯
            [r, c] = spread(r, c, d,map_2D)

    queue = deque()
    visit = [[0] * N for _ in range(N)]
    path = [[0] * N for _ in range(N)]
    # print(exit_2D_x,exit_2D_y)
    queue.append([exit_2D_x,exit_2D_y])
    while (queue):
        # 타임머신 이동 구현 visit 안한곳으로
        q = queue.popleft()

        for w in wierd:
            [r, c, d, v] = w
            if (time+path[q[0]][q[1]]+1) % v == 0:  # for 문으로 각각의 v에 대해 해야할듯 v 횟수일때
                [r, c] = spread(r, c, d,map_2D)

        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            if inside_2D(nx, ny) and visit[nx][ny] == 0 and (map_2D[nx][ny] ==0 or map_2D[nx][ny] ==4) :  # 장애물, 위험물질아닐때
                visit[nx][ny] = 1
                print(q)
                path[nx][ny] = path[q[0]][q[1]] + 1  # 한칸씩 더해줌
                queue.append([nx,ny])
                if map_2D[nx][ny] == 4:  # 탈출시
                    queue = deque()  # 빈거로 나둬버림


    pprint(path)
    pprint(map_2D)

    is_exit = False
    for i in range(N):
        for j in range(N):
             if visit[i][j] == 1 and map_2D[i][j] == 4:
                is_exit = True
                time += path[i][j]
    # print(time)
    if is_exit:
        print(time)
    else:
        print(-1)


