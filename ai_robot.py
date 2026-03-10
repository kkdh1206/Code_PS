import sys
from collections import deque
sys.stdin = open("input.txt")
import pprint

N,K,L = map(int,input().split())
dirt_map = [list(map(int,input().split())) for _ in range(N)]
robot_loc = [0]*K
robot_set = set()
# robot_dir = [0]*K
for k in range(K):
    rx,ry = map(int,input().split())
    robot_loc[k] = [rx-1,ry-1] # 좌표 통일화
    robot_set.add((rx-1,ry-1))
dx = [-1,0,0,1]
dy = [0,-1,1,0]

dir_x = [0,1,0,-1]
dir_y = [1,0,-1,0]

# 아 리스트 순회하면 시간복잡도 개터지니까 항상 set으로 관리를 하자


def inside(x,y):
    return 0<=x<N and 0<=y<N

def stack(some_map):
    for i in range(N):
        for j in range(N):
            if some_map[i][j] >0:
                some_map[i][j] +=5

def spread(some_map): # 동시에해야해서 한번에 더해야함
    temp_map = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if some_map[i][j] == 0:
                for k in range(4):
                    ni = i + dx[k]
                    nj = j + dy[k]
                    if inside(ni,nj) and some_map[ni][nj] >0:
                        temp_map[i][j] += some_map[ni][nj] # 주변꺼를 더해줌
    for i in range(N):
        for j in range(N):
            some_map[i][j] += temp_map[i][j]//10
    # pprint.pprint(temp_map)
#
# def move_robot():
#     for k in range(K):
#         [r_x,r_y] = robot_loc[k]
#         if dirt_map[r_x][r_y] >0:
#             continue # 이미 잘 도착해있는 케이스
#         visit = [[False]*N for _ in range(N)]
#         queue = deque()
#         queue.append([r_x,r_y])
#         visit[r_x][r_y] = True
#         found = False
#         while queue and not found: # 먼지에 도착하기 전까지
#             q = queue.popleft()
#             x,y = q[0],q[1]
#             # if k == 2:
#                 # print("fefff")
#                 # print(x, y)
#             for i in range(4):
#
#                 nx = x + dx[i]
#                 ny = y + dy[i]
#                 # if k == 2: print(nx, ny)
#                 if inside(nx,ny) and not visit[nx][ny] and not dirt_map[nx][ny]<0 and not (nx,ny) in robot_set: # 벽,로봇있는곳은 가면 안되니까
#                     # 여기서 시간복잡도 터진듯
#
#                     visit[nx][ny] = True # 이제 방문을 했음
#                     queue.append([nx, ny]) # queue인지 q인지 조심하기!!!
#                     if dirt_map[nx][ny] >0:
#                         found = True
#                         robot_loc[k] = [nx,ny] # nx,ny 로 이동
#                         robot_set.remove((r_x,r_y))
#                         robot_set.add((nx,ny))
#                         # print(k)
#                         # robot_dir[k] = i # 이러면 i 반대방향이겠지 실제 방향은
#                         break # 이 for 문 종료
def move_robot():
    for k in range(K):
        r_x, r_y = robot_loc[k]

        # 이미 먼지 위에 있으면 이동 안 함
        if dirt_map[r_x][r_y] > 0:
            continue

        visit = [[False]*N for _ in range(N)]
        queue = deque()
        queue.append((r_x, r_y))
        visit[r_x][r_y] = True

        found = False

        while queue:
            size = len(queue)
            candidates = []

            for _ in range(size):
                x, y = queue.popleft()

                # 현재 위치가 먼지면 후보에 추가
                if dirt_map[x][y] > 0:
                    candidates.append((x, y))

                for i in range(4):
                    nx = x + dx[i]
                    ny = y + dy[i]

                    if not inside(nx, ny):
                        continue
                    if visit[nx][ny]:
                        continue
                    if dirt_map[nx][ny] < 0:  # 물건
                        continue
                    if (nx, ny) in robot_set:
                        continue

                    visit[nx][ny] = True
                    queue.append((nx, ny))

            # 같은 거리에서 먼지 발견했다면
            if candidates:
                candidates.sort()  # 행 → 열 우선
                nx, ny = candidates[0]

                # robot_set 갱신
                robot_set.remove((r_x, r_y))
                robot_set.add((nx, ny))

                robot_loc[k] = [nx, ny]
                found = True
                break

# def sum_clean(x,y,direct): # x,y는 inside 줘야지 그래도
#     sum = dirt_map[x][y]
#     for i in range(4):
#         nx = x +dir_x[i]
#         ny = y +dir_y[i]
#         if inside(nx,ny):
#             sum += dirt_map[ny][ny]
#     # 다더해진상태
#     if inside(x-direct[0],y-direct[1]):
#         sum -= dirt_map[x-direct[0]][y-direct[1]]
#     return sum

def clean(i,j): # 최대 20까지 청소
    # if i==5 and j==4:
    #     print(dirt_map[i][j])
    if dirt_map[i][j] >20:
        dirt_map[i][j] -=20
    elif dirt_map[i][j] >0:
        dirt_map[i][j] = 0

def cleaning():
    for k in range(K):
        [rx, ry] = robot_loc[k]
        clean(rx,ry) # 원래자리 청소
        max_dirt = 0
        max_dir = 0
        for i in range(4):
            nx = rx + dir_x[i]
            ny = ry +dir_y[i]
            nx1 = rx + dir_x[(i+1)%4]
            ny1 = ry + dir_y[(i+1)%4]
            nx2 = rx + dir_x[(i+3)%4]
            ny2 = ry + dir_y[(i+3)%4]
            local = 0
            if inside(nx,ny) and dirt_map[nx][ny] > 0:
                local += min(20,dirt_map[nx][ny])
            if inside(nx1,ny1) and dirt_map[nx1][ny1]>0:
                local += min(20,dirt_map[nx1][ny1])
            if inside(nx2,ny2) and dirt_map[nx2][ny2]>0:
                local += min(20,dirt_map[nx2][ny2])
            if local > max_dirt:
                max_dirt = local
                max_dir = i # 이방향 뺀게 젤작음
        # 청소방향 알았으니 청소
        i = max_dir
        nx = rx + dir_x[i]
        ny = ry + dir_y[i]
        nx1 = rx + dir_x[(i + 1) % 4] # 아 방향은 무조건 나머지로 해야지 몫이 아니라!!!
        ny1 = ry + dir_y[(i + 1) % 4]
        nx2 = rx + dir_x[(i + 3) % 4]
        ny2 = ry + dir_y[(i + 3) % 4]
        # if k == 2:
        #     print(dir_y[(i + 1) % 4])
        #     print(dir_y[(i + 3) % 4])
        #     print((i + 1) // 4)
        if inside(nx, ny):
            clean(nx,ny)
        if inside(nx1, ny1):
            clean(nx1,ny1)
        if inside(nx2, ny2):
            clean(nx2,ny2)
        # pprint.pprint(dirt_map)
        # print("-------")

def sum_dirt():
    sum = 0
    for i in range(N):
        for j in range(N):
            if dirt_map[i][j]>0:
                sum += dirt_map[i][j]
    return sum


for i in range(L):
    if sum_dirt() == 0:
        break

    move_robot()
    # print(robot_loc)
    cleaning()
    # pprint.pprint(dirt_map)
    # print("-----")
    stack(dirt_map)
    # for row in dirt_map:
    #     print(*row)
    # print("-----")
    spread(dirt_map)
    print(sum_dirt())

    # for row in dirt_map:
    #     print(*row)


