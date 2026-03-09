import sys
sys.stdin = open("golem.txt", "r")


# 입력 받기
R, C, K = map(int, input().split())
golem = []
for i in range(K):
    x, y = map(int, input().split())
    golem.append([x, y])
forest = [[0] * C for _ in range(R + 3)]
# 지도로 골렘몸통은 양수 출구는 음수임 시행 횟수에따라 골렘번호가 시행횟수임
from collections import deque

dx = [1, 0, -1, 0]
dy = [0, -1, 0, 1]
dir_x = [-1, 0, 1, 0]  # 골렘 입구 표시용
dir_y = [0, 1, 0, -1]


# 회전함수 필요 - 죄측으로 갈땐 반시게로 회전 우측은 시계로 회전
def turn(x, y, for_map):  # 회전 가능한 놈들만 넣는다 가정
    if move(x, y, for_map, 1):  # 1 왼쪽
        # 왼쪽으로 이동 성공
        if move(x, y - 1, for_map, 0):
            x = x + 1
            y = y - 1
            # 회전 작업
            temp = []
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]  # 골렘 사지 이동
                temp.append(for_map[nx][ny])  # 값복사
            for i in range(4):
                #j = (i + 1) % 4  # 시계로 회전 된 값을 가져옴 -> 반시계로 회전됨 ---> 미쳣냐 가져오는게 아니잖아!!! 그냥 그 좌표로 가는거잖아 temp는 고정인데 그냥 어디 넣을지 결정이잖어
                j = (i + 3) % 4
                nx = x + dx[j]
                ny = y + dy[j]  # 골렘 사지 이동
                for_map[nx][ny] = temp.pop(0)  # 하나씩 이동해줌
            return [x, y]
        else:
            move(x, y-1, for_map, 3)  # 복구해둠
            # 여기선 아직 반환 안함

    if move(x, y, for_map, 3):
        # 오른쪽으로 이동 성공
        if move(x, y + 1, for_map, 0):
            x = x + 1
            y = y + 1
            # 회전 작업
            temp = []
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]  # 골렘 사지 이동
                temp.append(for_map[nx][ny])  # 값복사
            for i in range(4):
                j = (i + 1) % 4  # 시계로 회전 된 값을 가져옴 -> 반시계로 회전됨
                nx = x + dx[j]
                ny = y + dy[j]  # 골렘 사지 이동
                for_map[nx][ny] = temp.pop(0)  # 하나씩 이동해줌
            return [x, y]  # 중심반환
        else:
            move(x, y+1, for_map, 1)  # 복구해둠
            return False
    else:
        return False  # 돌지도 못함



def inside(x, y):
    return 0 <= x < R+3 and 0 <= y < C



def possible(x, y, for_map,k):
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if not 0 <= nx < R+3 or not 0 <= ny < C:  # 이건 진짜 들어오는지아닌지 확인 -> 회전확인도 이걸로 # not으로 할거면 or 써야지
            return False  # 이러면 실패지
        if for_map[nx][ny] != 0 and for_map[nx][ny] != k and for_map[nx][ny] != -k : # and랑 or구분잘해야함
            return False
    return True


# 우선순위는 1.하강 -> 2.서쪽 회전 -> 3.동쪽 회전
# 다하고나면 골렘에서 정령이 내려서 다른골램으로 이동하며 젤 아래로 갈수 잇는 골렘을 찾음 -> BFS구현 해야할듯?

# 골렘 이동함수 - 멈추는거 까지 멈추면 안옮기고 fALSE 반환한다던가
def move(x, y, for_map, d):  # d는 방향임 - 0 아래 1왼쪽 2 오른쪽
    temp = [for_map[x][y]]  # 중심값 저장

    if not possible(x + dx[d], y + dy[d],for_map,for_map[x][y]):  # 이동할 위치
        return False  # 이땐 멈췃으니 중심에 변화 없음
    # 아닌경우는 이동은 가능하다는 말이므로 이동 구현
    # temp로 임시로 골렘 값들 저장 (지도에 골렘은 출구 -n 가 나머진 n임)

    for_map[x][y] = 0
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]  # 골렘 사지 이동
        temp.append(for_map[nx][ny])  # 값복사
        for_map[nx][ny] = 0  # 초기화 해줌
    x = x + dx[d]
    y = y + dy[d]  # 이동함
    #print(temp)
    for_map[x][y] = temp.pop(0)  # 중심이동
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]  # 골렘 사지 이동
        for_map[nx][ny] = temp.pop(0)  # 하나씩 이동해줌

    return [x, y]


# 골렘 회전함수 죄측 우측 제작 - 출구 돌리는게 중요

# 내려서 최하층으로 내려갈수 있는 행을 반환하는 함수
def walk(x, y, for_map):
    max_x = x
    # bfs 할땐 무조건 visit 만들기
    visit = [[0] * C for _ in range(R + 3)]
    visit[x][y] = 1
    queue = deque()
    queue.append([x, y])
    while queue:
        q = queue.popleft() # popleft로 해야 bfs가 된다함 사실 dfs로 탐색해도 상관없음
        #print(for_map)
        for i in range(4):
            nx = q[0] + dx[i]
            ny = q[1] + dy[i]
            #print(nx,ny,R+3,C)
            # print(max_x, inside(nx, ny) , visit[nx][ny] == 0 , for_map[nx][ny] != 0)

            if inside(nx, ny) and visit[nx][ny] == 0 and for_map[nx][ny] != 0:
                # 이러면 queue에 넣을 조건을 이제 봐주면 됨 근데 출구인지는 봐줘야함
                if for_map[q[0]][q[1]] > 0:
                    if for_map[nx][ny] == for_map[q[0]][q[1]] or for_map[nx][ny] == - for_map[q[0]][q[1]]:  # 같은 골렘인 경우
                        queue.append([nx, ny])
                        visit[nx][ny] = 1  # 이거 항상 조심해주기 append 하면 뒤에 visit 설정하기
                        max_x = max(max_x, nx)  # 둘중에 최대비교
                        #print(max_x, ny)
                else:  # 출구인 경우
                    # 출구면 주변에 아무데나 갈수 있음 어차피 0인 곳은 걸럿으니
                    queue.append([nx,ny])
                    visit[nx][ny] = 1
                    max_x = max(max_x, nx)
                    #print(max_x,ny)

    return max_x


# 위의 3개를 합쳐서 하나의 골렘을 다 제어하는 함수 만들기
def simulate(x, y, for_map):  # 초기 골렘의 위치를 받음 -> 이걸 K번 시행할거임
    isBreak = False
    while not isBreak:
       # pprint (for_map)
       # print("-----")
        where = move(x, y, for_map, 0)  # 아래로 갈수 있으면 이동
        if where: # 이동된걸 넣어줘야지
            #old_where = where
            x,y = where[0],where[1]
            continue
        where = turn(x, y, for_map)
        if where:  # 아래로 못가면 이번엔 회전
            #old_where = where
            x,y = where[0], where[1]
            continue
        else:  # 회전도 못함
            isBreak = True
   # pprint(for_map)
    #print("!!")
    m_x, m_y = x,y
    #print(x,y)
    if m_x < 4:
        for i in range(R + 3):
            for j in range(C):
                for_map[i][j] = 0  # 초기화
        return 0
    else:
        return walk(m_x, m_y, for_map) - 2  # 행을 반환 -> 3을 더 붙였으니까!!


# 골렘 제작함수
def make_golem(y, d, k, for_map):  # k로 골렘의 숫자 설정
    for_map[1][y] = k
    for i in range(4):
        nx = 1 + dir_x[i]
        ny = y + dir_y[i]
        #print(for_map)
        for_map[nx][ny] = k
        if i == d:
            for_map[nx][ny] = -k  # 입구 뚫어줌


# 이 함수를 호출해서 종료 할때 까지 호출

# 배열 3칸늘려서 3칸 못들어간놈은 빼내는 함수도 필요 -> 더이상 못들어가면 골렘을 모두 비우는 작업 수행
# 이때 골렘은 튀어나간 골렘 다음부터 수행 튀어 나온경우는 정령의 위치는 고려하지 않음
from pprint import pprint
result = 0
for i in range(K):
    g = golem[i]
    # 지도에 골렘표시하기!
    make_golem(g[0]-1, g[1], i + 1, forest)  # 골렘 번호는 1부터
    #pprint(forest)
    #print("----")
    result += simulate(1, g[0]-1, forest)  # simulate 실행
   # print(result)

# 출력 : 정령의 최종위치 행번호의 합
print(result)