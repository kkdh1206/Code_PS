import sys
sys.stdin = open("medusa.txt", "r")
from collections import deque
from pprint import pprint


N,M = map(int,input().split())
Sr,Sc,Er,Ec = map(int,input().split())
s_list = list(map(int,input().split()))
soldiers_loc =[]
soldiers_status = [1]*M
for m in range(M):
    ar,ac = s_list[2*m], s_list[2*m+1]
    soldiers_loc.append([ar,ac])
town_map = [list(map(int,input().split())) for _ in range(N)]
path_map = [[0]*N for _ in range(N)]
sight_map = [[False]*N for _ in range(N)]
dx = [-1,1,0,0]
dy = [0,0,-1,1]
ddx = [0,0,-1,1]
ddy = [-1,1,0,0]
# dddx = [0,0,1,-1]
# dddy = [1,-1,0,0]


def inside(x,y):
    return 0<=x<N and 0<=y<N

def distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

def init_sight():
    for i in range(N):
        for j in range(N):
            sight_map[i][j] = False

def path_exist(sr,sc,er,ec):
    visit = [[False]*N for _ in range(N)]
    visit[sr][sc] = True
    queue = deque()
    queue.append([sr,sc])
    while queue:
        q = queue.popleft()
        x,y = q[0],q[1]
        if x == er and y == ec:
            return True
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if inside(nx,ny) and not visit[nx][ny] and town_map[nx][ny] == 0:
                path_map[nx][ny] = [x,y] # 이전 위치 기록
                visit[nx][ny] = True
                queue.append([nx,ny]) # append로 해야함 insert가 아니라
    return False # 경로가 존재하지않음

def triangular(x,y,dir_1,dir_2,color):
    x1,x2,y1,y2 = x,x,y,y
    for i in range(N):
        x1 +=dir_1[0]
        y1 +=dir_1[1]
        x2 +=dir_2[0]
        y2 +=dir_2[1]
        for j in range(min(x1,x2),max(x1,x2)+1):
            for k in range(min(y1, y2), max(y1, y2) + 1):
                if inside(j,k):
                    sight_map[j][k] = color

def sight(Mx,My,dir_1,dir_2):
    count =0
    triangular(Mx, My, dir_1,dir_2,True)
    for s in range(len(soldiers_loc)):
        if soldiers_status[s] == 1 and sight_map[soldiers_loc[s][0]][soldiers_loc[s][1]]:
            dir_3 = [(dir_1[0]+dir_2[0])//2, (dir_1[1]+dir_2[1])//2]
            dir_4 =[0,0]
            if dir_3[0]!=0: # x축방향임
                if My > soldiers_loc[s][1]:
                    dir_4 = [dir_3[0],-1]
                elif My < soldiers_loc[s][1]:
                    dir_4 = [dir_3[0],1]
                else:
                    dir_4 =dir_3

            elif dir_3[1]!=0:
                if Mx > soldiers_loc[s][0]:
                    dir_4 = [-1,dir_3[1]]
                elif Mx < soldiers_loc[s][0]:
                    dir_4 = [1,dir_3[1]]
                else:
                    dir_4 =dir_3
            triangular(soldiers_loc[s][0], soldiers_loc[s][1], dir_3, dir_4, False)
    for s in range(len(soldiers_loc)):
        if soldiers_status[s] == 1 and sight_map[soldiers_loc[s][0]][soldiers_loc[s][1]]:
            # soldiers_status[s] = 0 # 석화상태
            count +=1
    #         print(soldiers_loc[s][0],soldiers_loc[s][1])
    # print(Mx,My)
    # print(count)
    return count

def soldier_move(Mr,Mc):
    dead, move =0,0
    for s in range(len(soldiers_loc)):
        if soldiers_status[s] == 1:
            res_x,res_y = soldiers_loc[s][0], soldiers_loc[s][1]
            min_dist = distance(Mr,Mc, res_x,res_y)
            for i in range(4):
                nx, ny = soldiers_loc[s][0] +dx[i], soldiers_loc[s][1]+dy[i]
                if inside(nx,ny) and not sight_map[nx][ny] and distance(nx,ny,Mr,Mc)< min_dist:
                    min_dist = distance(nx,ny,Mr,Mc)
                    res_x,res_y = nx,ny
                    # soldiers_loc[s][0], soldiers_loc[s][1] = res_x,res_y
                    # move +=1
                    if nx == Mr and ny == Mc: # 메두사랑 닿음
                        dead +=1
                        soldiers_status[s] = -1 # 사망
            if res_x != soldiers_loc[s][0] or res_y != soldiers_loc[s][1]:
                move +=1
                soldiers_loc[s][0], soldiers_loc[s][1] = res_x, res_y
    return [dead,move]

def soldier_move2(Mr,Mc):
    dead, move =0,0
    for s in range(len(soldiers_loc)):
        if soldiers_status[s] == 1:
            res_x,res_y = soldiers_loc[s][0], soldiers_loc[s][1]
            min_dist = distance(Mr,Mc, res_x,res_y)
            for i in range(4):
                nx, ny = soldiers_loc[s][0] +ddx[i], soldiers_loc[s][1]+ddy[i]
                if inside(nx,ny) and not sight_map[nx][ny] and distance(nx,ny,Mr,Mc)< min_dist:
                    min_dist = distance(nx,ny,Mr,Mc)
                    res_x,res_y = nx,ny

                    # move +=1
                    if nx == Mr and ny == Mc: # 메두사랑 닿음
                        dead +=1
                        soldiers_status[s] = -1 # 사망
            if res_x != soldiers_loc[s][0] or res_y != soldiers_loc[s][1]:
                move +=1
                soldiers_loc[s][0], soldiers_loc[s][1] = res_x, res_y
    return [dead,move]

if(path_exist(Sr,Sc,Er,Ec)):
    path_list = deque()
    x,y = Er,Ec
    # path_list.append([x,y])
    while x!= Sr or y!=Sc: # 아 부정을 하면 조심하기 and를 부정하면 or이다
        path_list.append([x, y])
        [x,y] = path_map[x][y]

    for p in range(len(path_list)-1,0,-1): # 마지막 도착한건 뽑을 필요가 없음
        [x,y] = path_list.pop()
        # print(x,y)
        for s in range(len(soldiers_loc)): # 메두사가 공격
            if soldiers_status[s] == 1 and soldiers_loc[s][0] == x and soldiers_loc[s][1] == y:
                soldiers_status[s] = -1 # 석화상태
        dir_1 =[-1,-1]
        dir_2 =[-1,1]
        init_sight()
        rock_count = sight(x,y,[-1,-1],[-1,1])
        init_sight()
        if sight(x, y, [1, -1], [1, 1])> rock_count:
            init_sight()
            rock_count = sight(x, y, [1, -1], [1, 1])
            dir_1=[1,-1]
            dir_2=[1,1]
        init_sight()
        if sight(x, y, [-1, -1], [1, -1])> rock_count:
            init_sight()
            rock_count = sight(x, y, [-1, -1], [1, -1])
            dir_1=[-1,-1]
            dir_2=[1,-1]
        init_sight()
        if sight(x, y, [-1, 1], [1, 1])> rock_count:
            init_sight()
            rock_count = sight(x, y, [-1, 1], [1, 1])
            dir_1=[-1,1]
            dir_2=[1,1]
        init_sight()
        rock_count = sight(x,y,dir_1,dir_2)

        for s in range(len(soldiers_loc)): # 석화상태 적용해주기
            if soldiers_status[s] == 1 and sight_map[soldiers_loc[s][0]][soldiers_loc[s][1]]:
                soldiers_status[s] = 0 # 석화상태
        # print(soldiers_loc)
        [dead, move] = soldier_move(x,y)
        [dead2, move2] = soldier_move2(x, y)# 2번이동
        # print(soldiers_status)
        for s in range(len(soldiers_status)):
            if soldiers_status[s] == 0: # 기절 풀어주기
                soldiers_status[s] = 1
        init_sight()

        print(move+move2, rock_count, dead+dead2)
        # print(x,y)
        # print(soldiers_loc)

    print(0)
else:
    print(-1)