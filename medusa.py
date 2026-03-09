import copy
import sys

sys.stdin = open("medusa.txt", "r")
from collections import deque
from pprint import pprint
N,M = map(int,input().split())
Sr,Sc,Er,Ec = map(int,input().split())
s = list(map(int,input().split()))
warriors =[]
path_map = [[[] for _ in range(N)] for _ in range(N)]
dx = [-1,1,0,0]
dy = [0,0,-1,1] # 상하좌우 순서

dx1 = [0,0,-1,1] # 좌우상하 순서 인데 걍 dx dy 바꾼거
dy1 = [-1,1,0,0]

for i in range(M): # 전사들
    warriors.append([s[2*i],s[2*i+1]])
road_map = [list(map(int,input().split())) for _ in range(N)]
rock_warriors=[]
danger_map = [[0]*N for _ in range(N)]

def distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

def inside(x,y):
    return 0<=x<N and 0<=y<N


def possible_arrive(x,y,r,c,path_map):
    queue = deque()
    queue.append([x,y])
    visit = [[0]*N for _ in range(N)]
    visit[x][y] = 1
    while(queue):
        q = queue.popleft()
        q_x, q_y = q[0],q[1]
        if q_x == r and q_y == c:
            break
        for i in range(4):
            nx = q_x + dx[i]
            ny = q_y + dy[i]
            if inside(nx,ny) and visit[nx][ny] ==0 and road_map[nx][ny] == 0:
                visit[nx][ny] = visit[q_x][q_y] + 1
                path_map[nx][ny] = copy.deepcopy(path_map[q_x][q_y]) # 진짜 변수명을 조심을하자
                if not( nx == r and ny == c):
                    path_map[nx][ny].append([nx,ny]) # 어차피 visit땜에 한번이 최대임
                queue.append([nx,ny])
    # for row in visit:
    #     print(*row)
    # print("##")
    return visit[r][c] -1 # -1 해줘서 거리를 반환시킴 초기에 1이었으니까 빼주는거 만약 반환이 -1 이면 실패한거임 찾기에
# print(Sr,Sc,Er,Ec)
# for row in road_map:
#     print(*row)
# print("----")
# print(possible_arrive(Sr,Sc,Er,Ec,path_map))
# for row in path_map:
#     print(*row)


def spread(x,y,dir1,dir2, some_map):
    loc1 = [x,y]
    loc2 = [x,y]
    for i in range(N):
        loc1[0] += dir1[0]
        loc1[1] += dir1[1]
        loc2[0] += dir2[0]
        loc2[1] += dir2[1] # 이렇게 계속해줌
        min_x = min(loc1[0],loc2[0])
        min_y = min(loc1[1], loc2[1])
        max_x = max(loc1[0], loc2[0])
        max_y = max(loc1[1], loc2[1])
        for i in range(min_x,max_x+1): # 뒤엔 무조건 +1 해줘야 맞음
            for j in range(min_y,max_y+1):
                if inside(i,j):
                    some_map[i][j] = 1

# spread(1,1,[1,1],[1,-1],danger_map)
# for row in danger_map:
#     print(*row)
# print("----")

def defense(x,y,dir1,dir2, some_map):
    loc1 = [x,y]
    loc2 = [x,y]

    for i in range(N):
        loc1[0] += dir1[0]
        loc1[1] += dir1[1]
        loc2[0] += dir2[0]
        loc2[1] += dir2[1] # 이렇게 계속해줌
        min_x = min(loc1[0],loc2[0])
        min_y = min(loc1[1], loc2[1])
        max_x = max(loc1[0], loc2[0])
        max_y = max(loc1[1], loc2[1])
        for i in range(min_x,max_x+1): # 뒤엔 무조건 +1 해줘야 맞음
            for j in range(min_y,max_y+1):
                if inside(i,j):
                    some_map[i][j] = 0

# spread(0,1,[1,1],[1,-1],danger_map)
# for row in danger_map:
#     print(*row)
# print("----")
# defense(1,2,[1,0],[1,1],danger_map)
# for row in danger_map:
#     print(*row)
# print("----")

def rock_count(dan_map, soldiers):
    count = 0
    # print("Rock_count")
    # for row in dan_map:
    #     print(*row)
    # print(soldiers)
    for s in soldiers:
        if dan_map[s[0]][s[1]] == 1:
            count +=1
    return count

def make_rock(dan_map, soldiers,rocks):
    count = 0
    for s in soldiers:
        if dan_map[s[0]][s[1]] == 1:
            rocks.append([s[0],s[1]])
    return count

# print(warriors)
# print(rock_count(danger_map,warriors))

def max_spread(x,y, some_map,soldiers):
    count =0
    max_i = 0 # 최대가 되게 하는 i
    dir1=[]
    dir2=[]
    for i in range(4):
        if dx[i] == 0:
            dir1 = [dx[i]-1, dy[i]]
            dir2 = [dx[i]+1, dy[i]]
        elif dy[i] == 0:
            dir1 = [dx[i],dy[i]-1]
            dir2 = [dx[i], dy[i] + 1]
        spread_with_defense(x,y,some_map, soldiers, dir1, dir2)
        new_count = rock_count(some_map,soldiers)
        # print(new_count)
        if count < new_count: # 더 돌로 많이 하는경우
            count = new_count
            max_i = i
        # count하고 나서 초기화
        for i in range(N):
            for j in range(N):
                some_map[i][j] = 0 # 초기화
    #print(dx[max_i], dy[max_i])
    if dx[max_i] == 0:
        dir1 = [dx[max_i] - 1, dy[max_i]]
        dir2 = [dx[max_i] + 1, dy[max_i]]
    elif dy[max_i] == 0:
        dir1 = [dx[max_i], dy[max_i] - 1]
        dir2 = [dx[max_i], dy[max_i] + 1]
    spread_with_defense(x, y, some_map, soldiers, dir1, dir2) # 찐으로 최대를 한번 제대로해줌
    return count # 최대 석화 인원을 반환함


def spread_with_defense(x, y, some_map, soldiers, dir_1,dir_2):
    spread(x, y, dir_1, dir_2, some_map)
    for s in soldiers:
        if some_map[s[0]][s[1]] == 1:  # 석화가 된경우에만 처리함 순서는 상관없을듯
            dir_x = s[0] - x
            dir_y = s[1] - y
            if dir_x == 0:
                dir1 = [0, dir_y // abs(dir_y)]  # 부호만 남김
                defense(s[0], s[1], dir1, dir1, some_map)
            elif dir_y == 0:
                dir1 = [dir_x // abs(dir_x), 0]  # 부호만 남김
                defense(s[0], s[1], dir1, dir1, some_map)
            # 이제 대각선인경우
            elif abs(dir_x) == abs(dir_y):  # 찐 대각선인경우
                dir1 = [dir_x // abs(dir_x), dir_y // abs(dir_y)]  # 단위행렬로 살림
                dir3_x = dir_1[0] + dir_2[0]
                dir3_y = dir_1[1] + dir_2[1]
                dir2 = [dir3_x // 2, dir3_y // 2]
                defense(s[0], s[1], dir1, dir2, some_map)
            else:  # 방향 두개인경우
                if dir_x > 0 and dir_y > 0:
                    if abs(dir_x) > abs(dir_y):
                        dir1 = [1, 1]
                        dir2 = [1, 0]
                        defense(s[0], s[1], dir1, dir2, some_map)
                    else:
                        dir1 = [1, 1]
                        dir2 = [0, 1]
                        defense(s[0], s[1], dir1, dir2, some_map)
                elif dir_x < 0 and dir_y > 0:
                    if abs(dir_x) > abs(dir_y):
                        dir1 = [-1, 1]
                        dir2 = [-1, 0]
                        defense(s[0], s[1], dir1, dir2, some_map)
                    else:
                        dir1 = [-1, 1]
                        dir2 = [0, 1]
                        defense(s[0], s[1], dir1, dir2, some_map)
                elif dir_x > 0 and dir_y < 0:
                    if abs(dir_x) > abs(dir_y):
                        dir1 = [1, -1]
                        dir2 = [1, 0]
                        defense(s[0], s[1], dir1, dir2, some_map)
                    else:
                        dir1 = [1, -1]
                        dir2 = [0, -1]
                        defense(s[0], s[1], dir1, dir2, some_map)
                elif dir_x < 0 and dir_y < 0:
                    if abs(dir_x) > abs(dir_y):
                        dir1 = [-1, -1]
                        dir2 = [-1, 0]
                        defense(s[0], s[1], dir1, dir2, some_map)
                    else:
                        dir1 = [-1, -1]
                        dir2 = [0, -1]
                        defense(s[0], s[1], dir1, dir2, some_map)
    # print("====")
    # for row in some_map:
    #     print(*row)
    # print("====")

# print(warriors)
#print(max_spread(0,2, danger_map,warriors))


def warrior_move(x,y,tar_x,tar_y):
    dist = distance(x,y,tar_x,tar_y)
    fin_x = x
    fin_y = y  # 초기에는 처음 위치둠 여차하면 안움직이기위해서
    if [x,y] not in rock_warriors:
        for i in range(4):
            nx = x+dx[i]
            ny = y+dy[i]
            if inside(nx,ny) and danger_map[nx][ny] == 0  and dist > distance(nx,ny,tar_x,tar_y): # 위험지대, 격자외부가 아니고 더 가까운 곳이 있으면
                dist = distance(nx,ny,tar_x,tar_y)
                fin_x = nx
                fin_y = ny
    return [fin_x,fin_y] # 움직일 위치 반환 만약 안움직이면 그냥 그위치 그대로겟지

def warrior_move2(x,y,tar_x,tar_y):
    dist = distance(x,y,tar_x,tar_y)
    fin_x = x
    fin_y = y  # 초기에는 처음 위치둠 여차하면 안움직이기위해서
    if [x,y] not in rock_warriors:
        for i in range(4):
            nx = x+dy[i] # dx dy 바꿈
            ny = y+dx[i]
            if inside(nx,ny) and danger_map[nx][ny] == 0  and dist > distance(nx,ny,tar_x,tar_y): # 위험지대, 격자외부가 아니고 더 가까운 곳이 있으면
                dist = distance(nx,ny,tar_x,tar_y)
                fin_x = nx
                fin_y = ny
    return [fin_x,fin_y] # 움직일 위치 반환 만약 안움직이면 그냥 그위치 그대로겟지


#print(warrior_move(1,3,0,2))

turn = possible_arrive(Sr,Sc,Er,Ec,path_map)
if turn == -1:
    print(-1)
else:
    path = path_map[Er][Ec]
    # print(turn)
    # print(path)
    # pprint(road_map)
    for t in range(turn-1): # 총 turn-1번 진행됨 왜냐면 걍 마지막은 0 반환할거라서
        rock = 0
        warrior_legth = 0
        attack_count = 0
        nx,ny = path[t][0], path[t][1]
        while([nx,ny] in warriors): # 있을때 삭제를 해야지 - 메두사가 움직이며 전사 잡음
            warriors.remove([nx,ny])

        for i in range(N):
            for j in range(N):
                danger_map[i][j] = 0

        rock = max_spread(nx,ny,danger_map,warriors)
        make_rock(danger_map,warriors,rock_warriors)
        # print(warriors)
        # print(rock_warriors)
        # print(nx,ny)
        # for row in danger_map:
        #     print(*row)
        # print("----")
        for w in warriors:
            w_nx,w_ny = warrior_move(w[0],w[1],nx,ny)
            if not (w[0] == w_nx and w_ny == w[1]):
                warrior_legth +=1
                w[0] = w_nx
                w[1] = w_ny # 이동했으면 이동
                if w[0] == nx and ny == w[1]:
                    attack_count +=1
        while [nx,ny] in warriors:
            warriors.remove([nx,ny])
        #print(warriors)
        for w in warriors:
            #print("b",w, len(warriors))
            w_nx, w_ny = warrior_move2(w[0], w[1], nx, ny)
            #print("a", w_nx,w_ny)
            if not (w[0] == w_nx and w_ny == w[1]):
                warrior_legth += 1
                w[0] = w_nx
                w[1] = w_ny  # 이동했으면 이동
                if w[0] == nx and ny == w[1]:
                    attack_count +=1
        while [nx,ny] in warriors:
            warriors.remove([nx,ny])
        # print(warriors)
        # print("---")
        print(warrior_legth,rock,attack_count)
        rock_warriors = [] # 풀어줌 돌에서
    print (0)







