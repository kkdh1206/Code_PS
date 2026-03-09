import sys
sys.stdin = open("mineral.txt", "r")


# 입력
from collections import deque
R,C = map(int,input().split())
cave = [list(map(str,input().strip())) for _ in range(R)]
N = int(input())
height = list(map(int,input().split()))
#for h in height:
#    h = R-h # 이거 무조건 해줘야함!!! 조심하기 입력 적을때도 주석으로 조심해야할 부분 적어주기!! -> 와 좀 제발 조심하자 R에서 빼야지!! N이라고 익숙한문자라 속지말자
for i in range(len(height)):
    height[i] = R- height[i] # 아니 이렇게해야 반영이 되네 저렇게 h 로 받아오면 주소로 접근하는게 아니라 스칼라 값만 가져와서 값바꿔도 반영이 안됨!!!!!
turn = True # 왼 -> 오
di = [-1,1,0,0]
dj = [0,0,1,-1]
def inside(x,y):
    return 0<=x<R and 0<=y<C
# 막대기 이동하며 부딫히고 사라지는 로직
def shoot(cave_map,h,turn):
    if turn:
        for i in range(C):
            if cave_map[h][i] == 'x': # h높이에서 왼 -> 오 로 이동 --> 소문자 x임!! 문자 잘보거나 복붙을 해오자
                cave_map[h][i] = '.' # 부서짐 처리!!! 이거 까먹으면 안되지
                return [h,i]
    else:
        for i in range(C-1,-1,-1):
            if cave_map[h][i] == 'x': # h높이에서 오->왼 으로 이동
                cave_map[h][i] = '.'  # 부서짐 처리!!! 이거 까먹으면 안되지
                return [h,i] # 부서지는 위치 반환
    # 없으면 반환안함

# 같은 미네랄 덩어리를 움직이는게 관건일듯 -> 덩어리를 찾아내자 그리고 덩어리가 2개로 떨어질수도 있겟네 흠

# 부서져서 미네랄이 아래로 떨어지는 로직 -> 한칸씩 갈필욘 없고 아래로 하나씩 이동하면서 미네랄이있거나 바닥이면 그 좌표를 반환
def broken(cave_map,blocks): # 가장 아래위치 블록들 -> 몇칸 아래로 떨어질지 반환하기
    length = R # 가장 길게 고정 -> 다시 손바줘야함
    blocks_set = set(map(tuple, blocks))  # {(x,y), (x,y), ...}
    for b in blocks:
        x = b[0]
        y = b[1]
        for i in range(x + 1, R):  # x-> R 로 떨어짐 # 하 지는 빼야지 체크할때 아래로 떨어질건데 지도 미네랄이라서 체크걸리네
            if (i, y) not in blocks_set and cave_map[i][y] == 'x': # GPT한테 도움받은거 그냥 리스트 탐색하면 시간복잡도 오래걸리니 set으로 바꿔서 하라고 함
            #if not [i,y] in blocks and cave_map[i][y] == 'x': # 미네랄을 만남 # 아니 지꺼에 자꾸 걸리면 안되제!!!!!
                length = min(length, i-x-1) # i전 까지 떨어진거니까
                #print("len")
                #print(length)
        length = min (length, R-1-x) # 찐바닥에 닿은경우도 처리해줘야함

    return length

def fall(cave_map,blocks,length):
    for b in blocks: # 다지우고 다이동
        cave_map[b[0]][b[1]] = '.' # 다지움
    for b in blocks: # 채움
        #print (b[0], length)
        cave_map[b[0]+length][b[1]] = 'x' # 다채움 다 같은 거리 이동



def cluster(cave_map,x,y): # x,y에 해당하는 블록의 덩어리를 조사함
    mineral = deque()
    result = deque()
    mineral.append([x,y])
    # result.append([x,y])
    visit = [[0]*C for _ in range(R)] # 반복 막기 위함
    visit[x][y] =1
    while mineral:
        m = mineral.popleft()
        i,j = m[0],m[1]
        if cave_map[i][j] == 'x':
            result.append([i, j])  # 결과에 추가함
            # print([i,j])
        for k in range(4):
            ni = i+di[k]
            nj = j+dj[k]
            if inside(ni,nj) and cave_map[ni][nj] == 'x' and visit[ni][nj] == 0: # 미네랄로만 이동
                visit[ni][nj] =1 # 방문함
                mineral.append([ni,nj]) # 이거 추가 까먹으면 어카냐
    return result

def exist(blocks):
    #while blocks:
    for b in blocks:
        # b = blocks.popleft() 하 여기서 빼버리면 어카냐 미친 그럼 다 날아가자너
        if b[0] == R-1: # 땅바닥에 닿아있는지 조사
            return False
    return True

from pprint import pprint
# 나중에 잘린거 볼때는 클러스터로 뽑고 h 위에있는것들 떨어트리면 될듯
for k in range (N):
    h = height[k] # 이번에 던지는 높이
    if k %2 == 0: # k에 따라서 방향 뒤바뀌게 설정 이때 0부터 시작함을 잊으면 안됨
        turn = True
    else:
        turn = False
    # 막대기 발사
    block = shoot(cave,h,turn) # 부서진 위치 받아옴
    #print(block)
    #print(cave)
    if not block: # 부서진데 없으면
        continue
    # 벽 부서지는 위치 및 부수기
    # 위치 기준으로 클러스터 확인
    # 아 위에만하는게 아니라 사방을 다 조사해줘야겠네!!!
    for a in range(4):
        if not inside(block[0]+di[a], block[1] + dj[a]): # 밖에 나가버리는경우
            continue
        minerals = cluster(cave,block[0]+di[a],block[1]+dj[a]) # 클러스터 확인  -> 아니지 부서질칸 바로윗칸만 확인하면되지 왜냐면 위에칸만 떨어질거니까 이게 아래랑 연결되있는지 보면될듯 이 위에가 없으면 부서졋다고 떨어질일이없음
        if not minerals:
            continue
        isBroken = exist(minerals) # block 의 높이에 해당하는게 있으면 클러스터에 그럼 안부서짐
        #print(minerals)
        #print(isBroken)
        #pprint(cave)
        if isBroken:
            length = broken(cave,minerals) # 얼마나 떨어져야하는지
            #print(length)
            fall(cave, minerals, length)

    # 위쪽 클러스터들 분리됫는지 확인 -> 근데 사실상 한칸 사라지는건데 위에는 무조건 1덩어리지 않을까
    # 아래로 떨어트림
pprint(cave)

for row in cave:
    print("".join(row)) #-> GPT한테 도움받은거 이렇게 출력해라고한다1! 출력형식도 좀 연습을 할필요가있을듯하다!!
