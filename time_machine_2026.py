import sys
from collections import deque
sys.stdin =open("time_machine.txt","r")

# 1. 주사위 모양으로 위쪽 지도 만듬 - 지도 돌려가며 합침 - 나머지 빈공간 -1 로 두고 -1 나오면 이동하는 함수 해줘야함
# 2. 2D지도에서 어디가 출구인지 잘보고 찍음
# 3. 그 지도에 임시 출구 5 만듬 그래서 나가는 경로 BFS로 찾음
# 4. 이후에 2D환경으로와서 이어서 게속 진행해야하는데 그전에 시간먼지 이동 시켜둠
# 5. BFS로 또 최단거리 탐색함
#
# 처음 입력받고 333으로 모여있는 시간벽쪽주변 돌면서
import pprint
dx = [0,0,1,-1]
dy = [1,-1,0,0]

N,M,F = map(int,input().split())

Dim2_map = [list(map(int,input().split())) for _ in range(N)]


east =[list(map(int,input().split())) for _ in range(M)]
west=[list(map(int,input().split())) for _ in range(M)]
south=[list(map(int,input().split())) for _ in range(M)]
north=[list(map(int,input().split())) for _ in range(M)]
top=[list(map(int,input().split())) for _ in range(M)]

dusts =[0]*F
for i in range(F):
    dusts[i] = list(map(int,input().split()))

build_map = [[0]*3*M for _ in range(3*M)]


# 필요함수 - 테스트 먼저 하고 그리고 합치기 각 작은 함수부터 테스트 ㄱㄱ
def inside(x,y,n): # 나가는거 아닌지 감시
    return 0<=x<n and 0<=y<n

def rotate_map(some_map): # 시계방향 혹은 반시계방향으로 회전 만듬 - 반시계로 만듬
    temp_map = [[0]*M for _ in range(M)]
    for i in range(M):
        for j in range(M):
            temp_map[i][j] = some_map[j][M-1-i] # 이러면 반시계방향으로 가져와지겠네
    return temp_map # 반환안할거면 이거 사라질수도있지않나 이런거 개념 잘알아야할듯
A = [[1,2,3],[4,5,6],[7,8,9]]
# B = rotate_map(A)
# for row in B:
#     print(*row)

def teleport(x,y): # 주사위 모양 지도에서 제대로 이동 보장하기 위함 y=x, y=-x 에서 대칭시킴
    if (x>1.5*M and y>1.5*M) or (x<1.5*M and y<1.5*M):
        return (y,x)
    else:
        return (3*M-1-y,3*M-1-x) # 점대칭하고 x=y 대칭

# print(teleport(2,5))

def time_dust_move(x,y,d): # 시간황사 움직이는거
    Dim2_map[x][y] = 6
    nx = x + dx[d]
    ny = y + dy[d]
    if inside(nx,ny,N) and Dim2_map[nx][ny] == 0: # 빈공간에서만 확산
        return [nx,ny] # 다음 황사 위치
    else:
        return [x,y]
def search_middle_exit(x,y,some_map):# 3333 으로 이뤄진곳을 찾고 그주변에 출구가 어느편에있는지 4가지 케이스로 나눠서 위치를 동서남북 알려준이후에 몇번째인지 알려주기
    for i in range(x-1,x+M+1):
        for j in range(y-1,y+M+1):
            if some_map[i][j] == 0:
                if i == x-1: # 북
                    gap = y+M-1-j
                    north[M-1][gap] = 5
                elif i == x+M: # 남
                    gap = j-y
                    south[M-1][gap] = 5
                elif j == y-1 : # 서
                    gap = i-x
                    west[M-1][gap] = 5
                elif j == y+M: # 동
                    gap = x+M-1 - i
                    # print(gap)
                    # print(i, j)
                    east[M-1][gap] = 5
                return [i,j]
def search():
    for i in range(N):
        for j in range(N):
            if Dim2_map[i][j] == 3:
                middle_x,middle_y = search_middle_exit(i,j,Dim2_map)
                return [middle_x,middle_y]
[middle_x,middle_y] = search()
# for row in east:
#     print(*row)
# print("-----")
# for row in west:
#     print(*row)
# print("-----")
# for row in south:
#     print(*row)
# print("-----")
# for row in north:
#     print(*row)

Dim3_map = [[-1]*3*M for _ in range(3*M)]
for i in range(M):
    for j in range(M):
        Dim3_map[i+M][j+M] = top[i][j]
east = rotate_map(east)
north = rotate_map(rotate_map(north))
west = rotate_map(rotate_map(rotate_map(west)))
# 지도 제작
for i in range(M):
    for j in range(M):
        Dim3_map[i+M][j+2*M] = east[i][j]
for i in range(M):
    for j in range(M):
        Dim3_map[i+M][j] = west[i][j]
for i in range(M):
    for j in range(M):
        Dim3_map[i][j+M] = north[i][j]
for i in range(M):
    for j in range(M):
        Dim3_map[i+2*M][j+M] = south[i][j]

# for row in Dim3_map:
#     print(*row)

# BFS로 이동하는건 각자 짜줘야함 왜냐면 이동 로직이 좀 달라서
def BFS_3D():
    t_x, t_y = 0, 0
    for i in range(M):
        for j in range(M):
            if top[i][j] == 2:
                t_x = i + M  # 타임머신 위치
                t_y = j + M
    queue = deque()
    visit = [[-1] * 3 * M for _ in range(3 * M)]
    queue.append([t_x, t_y])
    visit[t_x][t_y] = 0
    while queue:
        q = queue.popleft()
        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            if inside(nx, ny, 3 * M):
                if Dim3_map[nx][ny] == -1:  # telesport해야할수도있으니까
                    #print(nx,ny)
                    nx, ny = teleport(q[0], q[1]) # 이전꺼를 해줘야지
                    #print(nx, ny)
                if visit[nx][ny] == -1 and (Dim3_map[nx][ny] == 0 or Dim3_map[nx][ny] == 5):  # 더확실히 하려면 nx,ny 로 나온게 -1 이면안됨
                    visit[nx][ny] = visit[q[0]][q[1]] + 1
                    queue.append([nx,ny]) # 정신차리자 아니면 while이거는 차라리 외우든가
                    if Dim3_map[nx][ny] == 5:  # 목적지 도착
                        return visit[nx][ny] # 가는데 걸리는시간

def BFS_2D():
    t_x, t_y = middle_x, middle_y
    queue = deque()
    visit = [[-1] * N for _ in range(N)]
    queue.append([t_x, t_y])
    visit[t_x][t_y] = 0
    time = 0
    while queue:
        q = queue.popleft()
        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            if inside(nx, ny, N):
                # 여기에 dust 움직이는게 반영이 안됨 <--------
                if visit[nx][ny] == -1 and (Dim2_map[nx][ny] == 0 or Dim2_map[nx][ny] == 4): # 가기전에 해줘야함 황사가 먼저임
                    if visit[q[0]][q[1]] +1 > time:  # 이전보다 커진다면 증가하면
                        time = visit[q[0]][q[1]] + 1  # 그 다음 시간에 대해서 맵 정렬 <---- 이게 중요함 같은 시간에 대해서 정렬하면안됨 문제잘읽기
                        for f in range(F):  # 황사 이동해줌
                            [r, c, d, v] = dusts[f]
                            if (time + phase1_time) % v == 0:  # phase1_time에서 시간이 저만큼흐른다면
                                # print(time)
                                [r, c] = time_dust_move(r, c, d)
                                dusts[f] = [r, c, d, v]

                        # print(time)
                if visit[nx][ny] == -1 and (Dim2_map[nx][ny] == 0 or Dim2_map[nx][ny] == 4):  # 더확실히 하려면 nx,ny 로 나온게 -1 이면안됨
                    visit[nx][ny] = visit[q[0]][q[1]] + 1
                    queue.append([nx,ny]) # 정신차리자 아니면 while이거는 차라리 외우든가

                    if Dim2_map[nx][ny] == 4:  # 목적지 도착
                        # for row in visit:
                        #     print(*row)
                        return visit[nx][ny] # 가는데 걸리는시간


# print(dusts)
t = BFS_3D()
if t:
    #print(t)
    phase1_time = t + 1 # 한칸 더 나와야하니까 Middle으로
    for f in range(F):  # 황사 이동해줌
        [r, c, d, v] = dusts[f]
        num = phase1_time // v
        for i in range(num + 1):  # 왜냐면 초기 위치 찍는것은 해줘야하니까
            [r, c] = time_dust_move(r, c, d)
        dusts[f] = [r, c, d, v]
    # print(dusts)
    if Dim2_map[middle_x][middle_y] == 6:
        print(-1)
        # 종료
    else:
        phase2_time = BFS_2D()
        if phase2_time:
            print(phase1_time + phase2_time)
        else:
            print(-1)

else:
    print(-1)