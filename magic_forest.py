import sys
from collections import  deque

sys.stdin = open("magic_forest.txt", "r")

R,C,K = map(int,input().split())
forest = [[0]*C for _ in range(R+3)]
# for i in range(R):
#     row = list(map(int,input().split()))
#     forest[i+3] = row # 이렇게 넣어줌
dx = [-1,0,1,0]
dy = [0,1,0,-1]

# 중앙을 1 입구3개를 2 출구 1개를 3 이라두자

def inside(x,y):
    return 0<=x<R+3 and 0<=y<C # 위에서 생성해서 가야하니까

def can_go(x,y,d):
    x += dx[d]
    y += dy[d]
    if inside(x+1,y) and inside(x-1,y) and inside(x,y-1) and inside(x,y+1):
        return forest[x+1][y] == 0 and forest[x-1][y] == 0 and forest[x][y-1] == 0 and forest[x][y+1] ==0
        # 0은 빈공간이고 하나는 1 즉 중심부라서 괜찮음 항상 겹치는건 바깥부분임 2,3 인곳
    else:
        return False


def turn(x,y,is_left):
    if is_left:
        temp = forest[x-1][y]
        forest[x-1][y] = forest[x][y+1]
        forest[x][y+1] = forest[x+1][y]
        forest[x+1][y] = forest[x][y-1]
        forest[x][y-1] = temp
    else: # 오른쪽 돌기
        temp = forest[x - 1][y]
        forest[x - 1][y] = forest[x][y - 1]
        forest[x][y - 1] = forest[x + 1][y]
        forest[x + 1][y] = forest[x][y + 1]
        forest[x][y + 1] = temp

def spirit_simul(x,y):
    max_x = x # 처음 이걸 저장해둠 그리고 반환할때는 지금 3 더해진 상태라 반환은 3 빼줘야함
    visit = [[False]*C for _ in range(R+3)]
    visit[x][y] = True
    queue = deque()
    queue.append([x,y])
    while queue:
        q = queue.popleft()
        max_x = max(max_x, q[0]) # q[0] 중에 젤큰게 x중에 젤큰거임
        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            if inside(nx,ny) and not visit[nx][ny] and forest[nx][ny] != 0: # 일단 갈수있고 방문안한곳 + 골렘바깥이 아닌곳
                if forest[q[0]][q[1]] == 1: # 출발위치가 중앙일때
                    queue.append([nx,ny])
                    visit[nx][ny] = True # 중앙에서는 어디든 갈수 있음

                elif forest[q[0]][q[1]] == 2: # 출발위치가 입구일때
                    if forest[nx][ny] == 1: # 입구에서는 중앙으로 밖에 못감 왜냐면 애초에 출구랑 붙어있는거면 다른 골렘 출구임 입구도 마찬가지고
                        queue.append([nx, ny])
                        visit[nx][ny] = True  # 중앙에서는 어디든 갈수 있음
                elif forest[q[0]][q[1]] == 3: # 출발위치가 출구일때
                    queue.append([nx, ny])
                    visit[nx][ny] = True  # 출구에서는 어디든 갈수 있음
    return max_x-3 +1 # 마지막에 3 빼줘야 올바른 값이 나옴 그리고 정확한 행은 맞는데 거기 번호는 1 더해줘야함

def reset(): # 초기화
    for i in range(R+3):
        for j in range(C):
            forest[i][j] = 0

def insert(nx,ny,data):
    (top, down, left, right, middle) = data
    forest[nx-1][ny] = top
    forest[nx+1][ny] = down
    forest[nx][ny-1] = left
    forest[nx][ny+1] = right
    forest[nx][ny] = middle

def delete_and_save(nx,ny):
    top = forest[nx - 1][ny]
    down = forest[nx + 1][ny]
    left = forest[nx][ny - 1]
    right = forest[nx][ny + 1]
    middle = forest[nx][ny]
    forest[nx - 1][ny] = 0
    forest[nx + 1][ny] = 0
    forest[nx][ny - 1] = 0
    forest[nx][ny + 1] = 0
    forest[nx][ny] = 0
    return (top,down,left,right,middle)


def golem_simul(y,d): # 여기서 y는 행렬이 아니라 1시작
    result = 0
    loc_x = 1
    loc_y = y - 1
    forest[loc_x-1][loc_y] = 2
    forest[loc_x][loc_y-1] = 2
    forest[loc_x+1][loc_y] = 2
    forest[loc_x][loc_y+1] = 2
    forest[loc_x][loc_y] = 1
    nx = loc_x + dx[d]
    ny = loc_y + dy[d]
    forest[nx][ny] = 3 # 출구 설정

    # for row in forest:
    #     print(*row)

    while True:
        data = delete_and_save(loc_x,loc_y) # 잠시 빼놓고 고민
        if can_go(loc_x,loc_y,2): # 아래로 이동
            loc_x += 1  # 아래로 한칸 이동
            insert(loc_x,loc_y,data)
            continue # 성공하면 다시 while로 다시 처음부터 실행

        elif can_go(loc_x,loc_y,3) and can_go(loc_x,loc_y-1,2): # 왼쪽으로 이동
            loc_x +=1
            loc_y -=1 # 왼쪽으로 이동
            insert(loc_x,loc_y,data)
            turn(loc_x,loc_y,True)
            continue # 성공하면 다시 while로 다시 처음부터 실행

        elif can_go(loc_x,loc_y,1) and can_go(loc_x,loc_y+1,2): # 오른쪽으로 이동
            loc_x +=1
            loc_y +=1 # 오른쪽으로 이동
            insert(loc_x,loc_y,data)
            turn(loc_x,loc_y,False)
            continue # 성공하면 다시 while로 다시 처음부터 실행

        else:
            insert(loc_x, loc_y, data) # 삭제하면 안됨 나둬야함
            break # 다 실패시에 멈춤

    if loc_x>3: # 3보다 크면 (4이상이면) spirit simul 실행
        result = spirit_simul(loc_x,loc_y)
    else:
        reset() # loc_x가 3보다 작거나 같으면 이건 반영안하고 다 비워줌

    return result

result = 0
for k in range(K):
    y,d = map(int,input().split())
    result += golem_simul(y,d)
    # for row in forest:
    #     print(*row)
    # print("------")
print(result)
# print(spirit_simul(4,1))

# for row in forest:
#     print(*row)
# print("------")
# turn(1,1,True)
# for row in forest:
#     print(*row)
# print(can_go(2,2,0))
# print(can_go(1,4,1))
# print(can_go(2,2,2))
# print(can_go(2,2,3))