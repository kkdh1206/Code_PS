# 로직 이랑 함수 종이에 구현하는데 1시간 15분 소요


from collections import deque
import copy
import sys
import pprint
sys.stdin = open("bacteria.txt", "r")

N,Q= map(int,input().split())
num = 1 # 미생물번호
small_map = [[0] * N for _ in range(N)]

dx = [1,-1,0,0]
dy = [0,0,1,-1]


def inside(x,y):
    return 0<=x<N and 0<=y<N

def isOne(x,y,some_map): # 웬만하면 계수는 x,y 그리고 iteration은  i,j 로하자
    queue = deque()
    color = some_map[x][y]
    visit = [[0]*N for _ in range(N)]
    visit[x][y] = 1
    queue.append([x,y])
    while(queue):
        q = queue.popleft()
        for k in range(4):
            nx = q[0] + dx[k]
            ny = q[1] + dy[k]
            if inside(nx,ny) and visit[nx][ny] == 0 and some_map[nx][ny] == color: # 같은 color인 놈을 모두 visit 처리하는중 <--- 아 제발 당연히 bfs 걍외워 미친놈아
                visit[nx][ny] = 1
                queue.append([nx,ny])
    for i in range(N):
        for j in range(N):
            if visit[i][j] == 0 and some_map[i][j] == color: # 방문안된 같은 색
                return False
    return True # 다 통과하면 한 덩어리

def largest(num, some_map):
    large = [0]*num # 총 이때까지 나온 미생물개수임
    for i in range(N):
        for j in range(N):
            if some_map[i][j]>0: # 디버깅이 빨라지든 이런걸 안틀리던 둘중하나를해야함
                large[some_map[i][j]-1] +=1 # 여기에 저장을해줌 # 아 이럴수가 이런오류가 있을수가.....
    result = -1 # 더이상 없으면 -1 로 반환하게 둠
    max_num = 0
    for i in range(num):
        if max_num < large[i]:
            max_num = large[i]
            result = i # 사실 이게 필요한거임 -> 자연스레 같은 크기면 i 가 작은값이 결정됨
    print(large)
    return result+1 # 1 더해줘서 복구함 -> 만약 이게 0이 나오면 실제로 남은건 없는거임 아니면 색을 반환함

def kill(color, some_map):
    for i in range(N):
        for j in range(N):
            if some_map[i][j] == color:
                some_map[i][j] = 0 # 0 으로 초기화 시켜버림

def together(some_map):

    t_set = set()
    for i in range(N):
        old = 0
        for j in range(N):
            if old>0 and some_map[i][j] >0 and old !=some_map[i][j]: # 둘다 0이 아니고 이전거랑 다른경우
                #print(old, some_map[i][j])
                if old > some_map[i][j]:
                    t_set.add((some_map[i][j],old)) # 오름차순 정렬
                else: t_set.add((old,some_map[i][j]))
            old = some_map[i][j]
    for j in range(N):
        old = 0 # 아 줄바뀌면 바뀌어야지
        for i in range(N):
            if old>0 and some_map[i][j] >0 and old !=some_map[i][j]: # 둘다 0이 아니고 이전거랑 다른경우
                #print(old, some_map[i][j])
                if old > some_map[i][j]:
                    t_set.add((some_map[i][j],old)) # 오름차순 정렬
                else: t_set.add((old,some_map[i][j])) # 와 set에는 튜플넣어야함 왜냐면 리스트는 못들어간단다
            old = some_map[i][j]
    # 가로 세로로 모두 다함
    return t_set

def scoring(color1,color2,some_map):
    area_c1 = 0
    area_c2 = 0
    for i in range(N):
        for j in range(N):
            if some_map[i][j] == color1:
                area_c1 +=1
            elif some_map[i][j] == color2:
                area_c2 +=1
    return area_c1*area_c2

def insert_bacteria(r1,r2,c1,c2,color,some_map):
    for i in range(r1,r2,1):
        for j in range(c1,c2,1): # 더하기 1 빼야함 왜냐면 좌표라서 칸이 아니라서 그럼
            #print(i,j)
            some_map[i][j] = color # 걍 무시하고 덮음

def one_possible(color,old_map,new_map,move_x,move_y): #  <---- 이거 완료하면됨
    for i in range(N):
        for j in range(N):
            if old_map[i][j] == color:
                nx = i + move_x
                ny = j + move_y
                if not (inside(nx,ny) and new_map[nx][ny] == 0): # 비어있고 가능하지않으면
                    return False
    return True

def is_possible(color,old_map,new_map):
    if old_map == [[0]*N for _ in range(N)]:
        return False # 애초에 바꿀거도 존재하지 않ㄴ아서 바로 종료시킴
    min_x =N-1
    min_y =N-1
    max_x = 0
    max_y = 0
    possible = False
    for i in range(N):
        for j in range(N):
            if old_map[i][j] == color:
                if min_x > i:
                    min_x = i
                if min_y > j:
                    min_y = j
                if max_x < i:
                    max_x = i
                if max_y < j:
                    max_y = j
    left_x = 0 - min_x # 이만큼 더하면 0으로 이동
    down_y = 0 - min_y # 이 위치들이 저기로 이동해야해서 이만큼 각각 더해져야함
    right_x = N-1 - max_x
    up_y = N-1 - max_y # 이만큼 더하면 끝으로 이동
    move_x =0
    move_y = 0
    for i in range(left_x,right_x+1,1): # +1은 해줘야함 그전에 멈춰버리니까
        for j in range(down_y, up_y+1,1):
            if not possible and one_possible(color,old_map,new_map,i,j): # 지금 불가능한 상태이고 one_possible일때 기록함
                possible = True # 성공함 심지어 가장 i, j 가 작은놈으로
                move_x = i
                move_y = j
    if possible: # 성공했다면 실제로 이동
        for i in range(N):
            for j in range(N):
                if old_map[i][j] == color:
                    nx = i + move_x
                    ny = j + move_y
                    if inside(nx, ny) and new_map[nx][ny] == 0: # 아싯팔 제발 조건 제대로!! 맞는지 확인
                        new_map[nx][ny] = color # 색칠해주고
                        old_map[i][j] = 0 # 이전껀 지워줌
    # 이동후 성공여부 반환
    return possible

def simulate(r1,r2,c1,c2,some_map,num):
    result = 0
    new_some_map = [[0]*N for _ in range(N)]
    insert_bacteria(r1,r2,c1,c2,num,some_map) # 넣고
    #print(num)


    # 잠만 여기서 kill 도해줘야지 옮기기전에
    for i in range(N):
        for j in range(N):
            if some_map[i][j] !=0: # 0이 아닌경우 다른게 있는지 걍보자 중복하면 어때 아 시간복잡도 에바긴한데 줄이면여기 좀 줄여봐
                if not isOne(i,j,some_map): # not인지 아닌지 잘봐야함
                    kill(some_map[i][j],some_map)
    # pprint.pprint(some_map)
    # print("!!!")

    l = largest(num, some_map)
    while l > 0 : # some_map이 비거나 옮기는게 실패할동안 옮김
        #pprint.pprint(new_some_map)
        # print("---")
        #print(l)
        #pprint.pprint(some_map)
        if not is_possible(l,some_map,new_some_map): # 아니 실패하면 멈춰야지 --> 근데 지금 값이 안바뀌는듯 new_some_map 이
            kill(l,some_map) # 이전맵에서 어차피 불가능한거면 데려오지도 못하는데 삭제
            l = largest(num, some_map)
            continue # 아니 실패하면 끝날게 아니라 더 작은걸 넣어봐야지!!!
        l = largest(num, some_map)
    #pprint.pprint(new_some_map)
    # 인접뽑고 점수
    t_set = together(new_some_map)
    for t in t_set:
        color1 = t[0]
        color2 = t[1]
        add_result = scoring(color1,color2,new_some_map)
        #print(color1,color2,add_result)
        result += add_result
    some_map[:] = copy.deepcopy(new_some_map) # 값복사로 넘겨줌 다시 맵에 쓸수 있게
    #pprint.pprint(some_map)
    return result

for i in range(Q):
    num = i+1 # 여기서 num을 설정해둠
    r1,c1,r2,c2 = map(int,input().split())
    score = simulate(r1,r2,c1,c2,small_map,num)
   # pprint.pprint(small_map)
    print(score)
    #print("----")

