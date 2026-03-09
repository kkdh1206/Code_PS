import sys
from collections import deque
from pprint import pprint
sys.stdin = open("mint_choco.txt","r")

dx = [-1,1,0,0]
dy = [0,0,-1,1]

N,T = map(int,input().split())

F = [list(map(set,input().strip())) for _ in range (N)]
pprint(F)
B = [list(map(int,input().split())) for _ in range (N)]
visit_map = [[False]*N for _ in range(N)]
attacked_map = [[False]*N for _ in range(N)]
crowd =[]
result = [0,0,0,0,0,0,0] # 마지막 결과내는 놈으로 순서대로 민초우,민초,민우,초우,우,초,민 숫자임

# set으로 색 관리할거임

def inside(x,y):
    return 0<=x<N and 0<=y<N


def total():
    result_list = [0, 0, 0, 0, 0, 0,0] # 계속 새 객체 만들어서 ㄱㅊ
    for i in range(N):
        for j in range(N):
            if F[i][j] == {'M', 'C', 'T'}:
                result_list[0] +=B [i][j]
            elif F[i][j] == {'C', 'T'}:
                result_list[1] +=B [i][j]
            elif F[i][j] == {'M', 'T'}:
                result_list[2] +=B [i][j]
            elif F[i][j] == {'M', 'C'}:
                result_list[3] +=B [i][j]
            elif F[i][j] == {'M'}:
                result_list[4] +=B [i][j]
            elif F[i][j] == {'C'}:
                result_list[5] +=B [i][j]
            elif F[i][j] == {'T'}:
                result_list[6] +=B [i][j]
    return result_list

def gather_energy(king_x,king_y): # 에너지 모아주는 함수
    queue = deque()
    visit = [[0]*N for _ in range(N)]
    queue.append([king_x,king_y])
    color  = F[king_x][king_y]  # king의 색과 같은 친구들을 뽑아서 주변 무리에서 에너지 모을거임

    #print(F[1][3])
    while queue:
       # print("while1")
        q=queue.popleft()
        x = q[0]
        y = q[1]
        visit[x][y] =1
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if inside(nx,ny) and visit[nx][ny] == 0 and F[nx][ny] == color: # 색같고 안나가고 방문도 안했으면
                B[nx][ny] -=1
                B[king_x][king_y] +=1
                queue.append([nx,ny]) # 추가
                visit[nx][ny] =1 # 방문 표시


def make_crowd(x,y,some_map): # 집단 뽑아내는 함수 x,y가 속한 집단 뽑음 효율 구려도 ㄱㅊ을듯
    queue = deque()
    queue.append([x, y])
    color = F[x][y]  # 색과 같은 친구들을 뽑아서 주변 무리 찾기
    max_i, max_j = x, y
    if some_map[x][y]:
        return False # 만들거 없다 표시
   #print(F[1][3])
    while queue:
     #   print("while2")
      #  print(queue)
        q = queue.popleft()
        x = q[0]
        y = q[1]

        some_map[x][y] = True # 방문했으니까 표시
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if inside(nx, ny) and (not some_map[nx][ny]) and F[nx][ny] == color:  # 색같고 안나가고 방문도 안했으면
                queue.append([nx, ny])  # 추가
                some_map[nx][ny] = True  # 방문 표시
                max_i,max_j = detemine_king(nx,ny,max_i,max_j)

    return [max_i,max_j]


def detemine_king(i,j,max_i,max_j): # 왕을 하나 뽑아내는 함수 군중 다주면 함
    max_power = B[max_i][max_j]
    king_candidate = [max_i,max_j]
    power = B[i][j]
    if power > max_power:
        king_candidate = [i,j]  # 이걸로 대체해줌
    elif power == max_power:
        if max_i > i:  # 행이 더작을때
            king_candidate = [i,j]   # 이걸로 대체해줌
        elif i == max_i:  # 행이 같을때
            if max_j > j:  # 열이 더작을때
                king_candidate = [i,j]   # 이걸로 대체해줌
    return king_candidate


def spread(x,y,power,color): # 전도하는거 함수 한번에 대해서 x,y가 전파되는곳임
    new_power = B[x][y]
    attacked_map[x][y] = True # 공격당했으니 기록
    if power > new_power: # 강한전파
        F[x][y] = color # 덮어씀
        power -= (new_power+1)
        B[x][y] +=1 # 여기가 new_power라서 여기에 1더해줌
    else: # 약한전파
        F[x][y] = F[x][y] | color # 색을 더해줌 set은 반환값이 없어서 이렇게해야한다!!
        B[x][y] +=power
        power =0
    return power # 남은 파워 리턴해줌




def shoot(x,y): # 전도하는거 spread 써서 완성한 함수 X,y는 왕의좌표임
    color = F[x][y] # set으로 받아오겠네
    power = B[x][y] -1 # 1 은 남겨줘야함
    B[x][y] =1 # 1남겨줌
    dir_x = dx[(power+1) %4]
    dir_y = dy[(power+1) %4]
    # 방향은 한번만 정해짐
    while power>0:
        #print("while3")
        x += dir_x
        y += dir_y
        if not inside(x,y):
            break # 나가면 그먄
        # print("!!!")
        # print(color)
        # print(F[x][y])
        # print(x,y)
        # print("!!!")
        if F[x][y] != color:
            power = spread(x,y,power,color)
            # print("!!")


 # 로그를 보는거 보단 때론 코드를 보며 어디가 틀렸는지 찾는게 빠를수도있다.
 # 시간복잡도를 최대한줄여라.. 불필요한 2번계산은 시간초과나버린다. -> 합칠수 있으면 함수는 따로하되, 함수안에서 호출해서 중복 탐색을하지말도록 분업할것이지 일을 두번하게 하지말라.
 # 결국 알고리즘을 짤때가 제일 중요하구나...


#
# pprint(F)
# for row in B:
#     print(*row)
# print(make_king([make_crowd(3,0,visit_map)]))
# shoot(1,1) # 무조건 문자를 넣어야함
# print("----")
# for row in B:
#     print(*row)
# pprint(F)

def color_strength(color):
    if color == {'T'}:
        return 100
    elif color == {'C'}:
        return 100
    elif color == {'M'}:
        return 100
    elif color == {'C','M'}:
        return 40
    elif color == {'M','T'}:
        return 40
    elif color == {'T','C'}:
        return 40
    elif color == {'T', 'C', 'M'}:
        return 4



for _ in range(T):
    for i in range(N):
        for j in range(N):
            B[i][j] +=1 # 1씩 증가시킴
    # print("----")
    # for row in B:
    #     print(*row)
    # pprint(F)
    # print("=====")
    kings=[]
    # crowd 모으고
    for i in range(N):
        for j in range(N):
            if not visit_map[i][j]:  # 방문안하몀ㄴ
                new_king = make_crowd(i, j,visit_map)
                if new_king: # 존재한다면
                    kings.append(new_king)

    # # king 선정
    # for c in crowd:
    #     kings = make_king(crowd)
    # print (kings)
    for k in kings:
        gather_energy(k[0], k[1])
    while(kings):
        #print("while4")
        # 가장 강한 왕 뽑기 -> 색도 고려해야함
        # print("kings = ", kings)
        # pprint(attacked_map)
        strongest_color = -1
        strongest_power = -1
        selected = []
        for k in kings:
            power = B[k[0]][k[1]]
            color = F[k[0]][k[1]]
            if not attacked_map[k[0]][k[1]]: # 공격당한거면 안됨
                if color_strength(color) > strongest_color:
                    selected = k
                    strongest_color = color_strength(color) # 현재 가장 우선순위인 색을 저장해둠
                    strongest_power = power
                    # print(color)
                elif color_strength(color) == strongest_color:
                    if power > strongest_power: # 처음엔 power -1 이라 무조건 더쎔
                        # print(power)
                        selected = k # 선택됨
                        strongest_power = power
                    elif power == strongest_power:# 힘이 같을때
                        if selected[0] > k[0]: # 행이 더 작음
                            selected = k
                        elif selected[0] == k[0] and selected[1] > k[1]: # 열이 더작을때
                            selected = k

        # print(kings)
        # print(selected)
        # print(strongest_color)
        # print(strongest_power)
        if selected: # selected가 존재하면
            # print("----")
            # for row in B:
            #     print(*row)
            # pprint(F)
            # print("=====")
            # print("----")
            # for row in B:
            #     print(*row)
            # print("=====")
            shoot(selected[0], selected[1])  # 전도 시작
            kings.remove(selected) # 기존에 있던 왕에서 삭제
            # print("----")
            # for row in B:
            #     print(*row)
            # pprint(F)
            # print("=====")
        else:
            break # 더이상 선택안되면 끝난거
    # attacked 된 킹들 삭제
    # attacked 초기화
    # visit_map도 초기화?
    for i in range(N):
        for j in range(N):
            visit_map[i][j] = False
            attacked_map[i][j] = False

    print(*total()) # 출력

#result = [0,0,0,0,0,0,0] # 다시 초기화

