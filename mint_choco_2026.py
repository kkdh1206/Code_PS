import sys
from collections import deque

sys.stdin = open("mint_choco.txt","r")

N,T = map(int,input().split())

F = [[0]*N for _ in range(N)]
for i in range(N):
    letter = input()
    for j in range(len(letter)):
        F[i][j] = set(letter[j]) # set으로 관리해서 더하고 빼기 쉽게

B = [list(map(int, input().split())) for _ in range(N)]

defense = set()
king = [] # 정렬필요함
dx = [-1,1,0,0]
dy = [0,0,-1,1]

def inside(x,y):
    return 0<=x<N and 0<=y<N

def prey():
    for i in range(N):
        for j in range(N):
            B[i][j] +=1

def one_charge(x,y,visited):
    queue = deque()
    color = F[x][y]
    group = []
    queue.append([x,y])
    group.append([x, y])
    visited[x][y] = True # 이전엔 무조건 False만 왔을거임
    while queue:
        q = queue.popleft()
        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            if inside(nx,ny) and not visited[nx][ny] and F[nx][ny] == color: # 색 같고 방문안했고 안에있는거
                visited[nx][ny] = True
                queue.append([nx,ny])
                group.append([nx,ny])
    # 이러면 group잘 묶어옴
    group.sort(key = lambda x: (-B[x[0]][x[1]], x[0], x[1])) # 신앙큰순 행작은순 열작은순
    for g in range(1,len(group)):
        [i,j] = group[g]
        B[i][j] -= 1 # 1빼줌
        B[group[0][0]][group[0][1]] += 1 # 1더해줌
    return group[0] # 젤 대장 반환

def charging():
    visited = [[False]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                k = one_charge(i,j,visited)
                king.append(k)

def shoot(i,j,P,color,dir_num): # 재귀문으로 색깔도 같이 넣어주기
    if not inside(i,j):
        return # 종료
    if P == 0:
        return # power가 0이라도 할거없음 <--- 이거안하면 오염만되버림
    if F[i][j] == color:
        shoot(i+dx[dir_num],j+dy[dir_num],P,color,dir_num) # 바로 이동시킴
    # if P == 0:
    #     return # power가 0이라도 할거없음 <--- 이거안하면 오염만되버림
    else:
        local_power = B[i][j]
        defense.add((i,j)) # 공격당했으니 표시 <--- 타입이 리스트는 바뀌는거라서 안된다고함 튜플만들어가짐 - set에는 변하지 않는 값만 들어갈수 있기 때문
        if local_power < P: # 강한전파일때
            B[i][j] +=1 # 1더해짐
            F[i][j] = color # 색깔 바뀜
            shoot(i + dx[dir_num], j + dy[dir_num], P - local_power - 1, color, dir_num)
            # if P-local_power-1>0: # 이거 해줘야 에러안생김 0 이되면 문제가생기나봐
            #     shoot(i + dx[dir_num], j + dy[dir_num], P-local_power-1, color, dir_num)
        else: # 약한전파일때
            B[i][j] += P # P만큼 증가
            F[i][j] = color | F[i][j] # set을 더해버림 <------ set끼리 더할땐 | (or)이라고 한다
            # shoot안함 끝났으니까

def propagation():
    king.sort(key=lambda x:(len(F[x[0]][x[1]]), -B[x[0]][x[1]], x[0], x[1])) # 단일, 이중, 삼중 그룹순이라서 색 개수로 오름차순조짐 그리고 신앙 내림차순, 행 열 오름차순
    for k in king:
        if not ((k[0],k[1]) in defense): # defense가 아닌애면 발사시작 <-- set에 tuple을 검색함 있는지 없는지
            dir_num = B[k[0]][k[1]]%4
            power = B[k[0]][k[1]]
            B[k[0]][k[1]] = 1  # 에너지 미리 소진 왜냐면 shoot에 영향을 줄수도있으니까
            shoot(k[0],k[1], power-1, F[k[0]][k[1]], dir_num)


def check_sum():
    result=[0,0,0,0,0,0,0]
    for i in range(N):
        for j in range(N):
            if F[i][j] == {"T","C","M"}:
                result[0] += B[i][j]
            elif F[i][j] == {"T","C"}:
                result[1] += B[i][j]
            elif F[i][j] == {"T","M"}:
                result[2] += B[i][j]
            elif F[i][j] == {"C","M"}:
                result[3] += B[i][j]
            elif F[i][j] == {"M"}:
                result[4] += B[i][j]
            elif F[i][j] == {"C"}:
                result[5] += B[i][j]
            elif F[i][j] == {"T"}:
                result[6] += B[i][j]
    return result

for t in range(T):
    king = []
    defense = set()  # 이거 초기화
    prey() # 아침시간
    charging() # 점심시간
    propagation() # 저녁시간
    print(*check_sum())

