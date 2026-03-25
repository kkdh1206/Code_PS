import sys
from collections import deque
sys.stdin = open("ancient.txt","r")


K,M = map(int,input().split())
treasure_map = [list(map(int,input().split())) for _ in range(5)]
prepare_queue = deque()
prepare_list = list(map(int,input().split())) # M개있음
for m in range(M):
    prepare_queue.append(prepare_list[m]) # 하나씩 큐로 만들어서 입력해둠 쓰기 편하게


dx = [0,0,1,-1]
dy = [1,-1,0,0]

def inside(x,y):
    return 0<=x<5 and 0<=y<5

def rotate_3x3(some_map,x,y): # 좌측위라고 생각 x,y를
    temp_map = [[0]*5 for _ in range(5)] # 딥카피인지 뭔지 그런거 개념 좀 공부해야할듯
    for i in range(5):
        for j in range(5):
            temp_map[i][j] = some_map[i][j]

    for i in range(3):
        for j in range(3):
            temp_map[x+i][y+j] = some_map[x+2-j][y+i] # 시계회전 내부에서만 돌아야함! - 이런건 테스트해서 어느방향인지 잘확인해보기

    return temp_map # 이래도 밖에서 이거 주소 가르키면 소멸안됨

def how_much_this(some_map,x,y,visited): # BFS 정석좀 외우자 -- 그 길이별로 나눠서 하는게 정석일건데
    queue = deque()
    visited[x][y] = True
    num = some_map[x][y]
    queue.append([x,y])
    count = 1
    while queue:
        q = queue.popleft()
        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            if inside(nx,ny) and not visited[nx][ny] and some_map[nx][ny] == num: # 같은거면
                visited[nx][ny] = True
                queue.append([nx,ny]) # 추가 - 아 BFS 실수하지말기진짜
                count +=1 # 1증가
    if count >=3:
        return count # 3이상이면 유물
    else:
        return 0
def delete_treasure(some_map,x,y,visited): # 지우는 함수
    queue = deque()
    visited[x][y] = True
    num = some_map[x][y]
    some_map[x][y] = 0
    queue.append([x,y])
    while queue:
        q = queue.popleft()
        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            if inside(nx,ny) and not visited[nx][ny] and some_map[nx][ny] == num: # 같은거면
                visited[nx][ny] = True
                some_map[nx][ny] = 0
                queue.append([nx,ny])

def how_much_these(some_map):
    visited = [[False]*5 for _ in range (5)]
    count = 0
    for i in range(5):
        for j in range(5):
            if not visited[i][j]: # 방문안된거면
                a =  how_much_this(some_map,i,j,visited)
                count += a
    return count # 이러면 유물 가치가 나옴

def best_price(some_map): # 어디서 회전한게 젤좋은지 확인
    max_price = -1
    max_map = [] # i,j,회전수
    for k in range(1,4): # 어차피 안돌린거에서는 안나오긴할거임 k는 회전횟수임
        for j in range(3): # 회전수 다음에는 열작은순서 2인이유는 3x3을 돌리는거고 좌측상단 가르키는거라
            for i in range(3): # 다음은 행작은게 먼저  <------------------------------------- 아니 이런실수는 에바지 !!! 하 무조건 범위확인 철저히!!! 당연히 0~4까지니까 3x3을 넣으려면 2까지 되야하니까 2,3,4 하려고 range(2)라했는데
                                                                                        # 생각해보면 range(3)이 2까지가고 range(2)는 1까지 감!!!! 하,,, 진짜 이것땜에 30분 날림 
                for l in range(k): # k회만큼 회전
                    some_map = rotate_3x3(some_map,i,j)
                price = how_much_these(some_map)
                for l in range(4-k):  # k회만큼 회전
                    some_map = rotate_3x3(some_map, i, j) # 복구작업
                if price == max_price:
                    print(i,j,k,max_price)
                if price > max_price: # 더 크다면
                    print(i,j,k,price,"@@@")
                    max_price = price
                    # print(price)
                    max_map = [i,j,k,max_price] # i,j에 k번회전이 젤큼
    print(max_map, '!!!')
    return max_map # max_price는 나중에 진짜 제거시에해주면됨

def pick_treasure(max_var,some_map):
    [i,j,k,price] = max_var
    for l in range(k):  # k회만큼 회전
        # for row in some_map:
        #     print(*row)
        # print("------")
        some_map[:] = rotate_3x3(some_map, i, j) # 아 이러면 some_map이 변수이름이 다르기때문에 [:] 로해주든 global로 treasure_map을 바로 바꾸든해야함
        # for row in treasure_map:
        #     print(*row)

    visited = [[False] * 5 for _ in range(5)]
    count = 0
    delete_queue = deque()
    for i in range(5):
        for j in range(5):
            if not visited[i][j]:  # 방문안된거면
                a = how_much_this(treasure_map, i, j, visited)
                if a>=3:
                    delete_queue.append([i,j])
                    count += a # 유물 가치
    visited = [[False] * 5 for _ in range(5)] # 다시 초기화
    while delete_queue:
        d =delete_queue.popleft()
        delete_treasure(treasure_map,d[0],d[1],visited) # 다 지워버리기
    return count

def refill(some_map):
    for j in range(5):
        for i in range(4,-1,-1): # 열번호 작고 행번호 큰순이라 먼저함
            if some_map[i][j] == 0:
                q = prepare_queue.popleft()
                some_map[i][j] = q



# treasure_map = rotate_3x3(treasure_map,1,1)
# delete_treasure(treasure_map,1,1,[[False] * 5 for _ in range(5)])
# max_map = best_price(treasure_map)
# print(max_map)
# one_round_price = pick_treasure(max_map,treasure_map)
# refill(treasure_map)
# for row in treasure_map:
#     print(*row)
# print(how_much_these(treasure_map))
result = []
for k in range(K):
    count = 0
    # 탐사진행
    max_map = best_price(treasure_map)
    # 탐사 유물획득 및 삭제
    round_price = max_map[3]
    if round_price == 0:
        break # 더이상 유물 없을때
    while round_price>0: # 더이상 유물 안나올때까지 계속 복원
        round_price = pick_treasure(max_map,treasure_map)
        count += round_price
    # 탐사지 복원
    #     print(k)
    #     for row in treasure_map:
    #         print(*row)
        print("-----")
        refill(treasure_map)
    # 유물 추가획득 확인용
        max_map = [0,0,0,0] # 아무것도 앞으로 안돌림

    result.append(count)
print(*result)



