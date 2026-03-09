import sys
sys.stdin = open("castle.txt", "r")

# 입력받기
N,M,D = map(int,input().split())
enemy_map = [list(map(int, input().split())) for _ in range(N)]
# killed = [False,False,False] # 적을 잡았는지 확인용
bow = []
import copy # 맵을 복사해서 넣어야할듯
from itertools import combinations
# 공격 구현 함수
def attack(enemy_map): # 궁수별로 3번 돌리는것보다 하나에 대해 잡은지 보는게 나을듯
    count = 0 # 몇마리 잡았는지
    # killed = [False,False,False] # 여기서 매번 초기화 해줘야 겠네 -> 필요가없네 전수조사할꺼니까
    for k in range(3):
        target = [-N,-M] # 이거보다 멀수는 없음
        for i in range(N-1,-1,-1):
            for j in range(M):
                if enemy_map[i][j] != 0:
                    if distance(i,j,N,bow[k])<=D: # 행이 N임 bow는 # 무조건 1,1 기준인지 0,0 기준인지 조심하기!!
                        if distance(i,j,N,bow[k]) < distance(target[0],target[1],N,bow[k]): # j에서 최단거리가 갈
                            target = [i,j] # 타깃을 기록해둠 -> 여기서 최소값을 찾고 방향자체가 좌측에서 오는거라서
                        elif distance(i,j,N,bow[k]) == distance(target[0],target[1],N,bow[k]):
                            if j<target[1]:
                                target=[i,j]
        if target != [-N,-M]: # 초기값이 아니면
            #killed [k] = True # 누구든 일단 활은 쏨
            if enemy_map[target[0]][target[1]] == 1:
                enemy_map[target[0]][target[1]] = 2 # 곧 죽음
                count += 1
    return count
    # 거리 측정하는 함수 호출
    # 거리가 사정거리 안이면 제거
    # 이때 거리 같을때 처리
    # 동시에 공격도 가능하게 다 선택하고 나서 하면될듯
    # 반환은 죽은 숫자 그리고 선택된 애들은 지도에서 지우면 좋을듯

# 사실 적을 아래로 내리는 함수
def down(enemy_map):
    for i in range(N-1,0,-1):
        enemy_map[i] = enemy_map[i-1] # 이전 행을 가져옴
    enemy_map[0] = [0] * M

# 거리 측정하는 함수
def distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2) # 썅 오타는에바자나

# 게임 시뮬레이션 돌리는함수
# N번 시행
def game(enemy_map):
    count = 0
    for x in range(N):
        # 공격구현 함수 호출 & 몇명 죽엇는지 확인 - 공격 먼저해야함
        count += attack(enemy_map) # 잡은 놈 추가
        print (x, count)
    # 지워진 지도 바탕으로 적을 아래로 이동 함수
        down(enemy_map)
        for i in range(N): # 곧 죽을애들 업데이트
            for j in range(M):
                if enemy_map[i][j] == 2:
                    enemy_map[i][j] = 0 # 아니 좀 정신차려
    # 죽인적 리턴
    return count
# 곧죽을거 2로 두고 나중에 2로 바꿔줌

# 궁수 배치 combination 쓰면 좋을듯 똑같은 애들이니까
# combination안쓸려면 크게 순서로 제약 둬버리던가
count = 0
for i in range(M):
    for j in range(i+1,M):
        for k in range(j+1,M):
            bow=[i,j,k]
            copy_map = copy.deepcopy(enemy_map)
            count = max(count,game(copy_map))
# 최대 값 리턴
print (count)