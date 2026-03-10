import sys
import pprint
sys.stdin = open("delivery.txt", "r")


# 아 함수 하나하나 좀 테스트 해가면서 하자

N,M = map(int,input().split())
box_list = []
box_loc = []
box_status= [True]*M
input_list = []
box_map =[[0]*N for _ in range (N)]

def inside(x,y):
    return 0<=x<N and 0<=y<N

def under_exist(x,y,w,h): # 이동 가능한지 보는거임 아래로
    if not inside(x+h, y): # not인지 뭔지 조심하기
        return True
    for i in range(y,y+w):
        if box_map[x+h][i] !=0:
            return True
    return False # 모두 다 통과한경우 아래 이동 가능하고 모두 0일때

def move_down(t):
    [h,w,c,k] = box_list[t]
    [x,y,p] = box_loc[t] # 좌측 상단 위치
    if not under_exist(x,y,w,h):
        box_loc[t] = [x+1,y,t] # 이동시킴
        for i in range(y, y + w):
            box_map[x][i] = 0 # 젤위에 비우기
            box_map[x + h][i] = k # 젤 아래 채우기
        return True
    else:
        return False

def falling():
    combined = list(zip(box_loc,box_list)) # zip에는 바로 정렬할수없다고함 물론 list를 해줘야함
    combined.sort(key = lambda x:(-x[0][0] - x[1][0])) # x+h값이 높은순으로 정렬
    # print(combined)
    for i in range(0,M): # 이거 아래순서대로 떨어져야하는데 아래에서 부터 falling
        t = combined[i][0][2]
        if box_status[t]:
            while move_down(t):
                pass

def is_blank(t,is_left):
    x,y = box_loc[t][0], box_loc[t][1]
    h,w = box_list[t][0], box_list[t][1]
    if is_left:
        for i in range(x,x+h):
            for j in range(0,y):
                if box_map[i][j]!= 0:
                    return False
        return True
    else:
        for i in range(x,x+h):
            for j in range(y+w,N):
                if box_map[i][j]!= 0:
                    return False
        return True

def take_out(is_left):
    for t in range (M):
        if box_status[t]:
            if is_blank(t,is_left):
                x, y = box_loc[t][0], box_loc[t][1]
                [h,w,c,k] = box_list[t]
                for i in range(x, x + h):
                    for j in range(y, y+w):
                        box_map[i][j] = 0 # 빼줌
                box_status[t] = False # 상자 이제 없으니까
                return k # 뽑힌거 택배 반환
    return False # 이제 뺄게 더이상 없을때

def is_finish():
    for t in range(M):
        if box_status[t] == True:
            return False # 안끝남
    return True

def make_box(c,w,h,k):
    for i in range(0,h):
        for j in range(c,c+w): # 미리c를 1빼둬서 바로 넣어도됨
            box_map[i][j] = k

for m in range(M):
    k,h,w,c = map(int,input().split())
    box_list.append([h,w,c-1,k]) # 박스 번호 저장
    box_loc.append([0,c-1,k]) # 여기에는 내림차순으로 정렬했을때 순번 저장
    input_list.append([k,m])

box_list.sort(key= lambda x: (x[3]))
box_loc.sort(key =lambda x: (x[2]))
input_list.sort(key =lambda x: (x[0]))

for j in range(len(box_loc)):
    box_loc[j][2] = j  # 이렇게 실제 순번
    input_list[j][0] = j # 순번 예쁘게 그림

input_list.sort(key =lambda x: (x[1])) # 다시 순서복구

# 맵 만들때 falling이나 함수써서만들기
# 초기 짐내려오는것
# print(input_list)
for i in range(len(input_list)):
    t = input_list[i][0]
    [h,w,c,k] = box_list[t]
    make_box(c,w,h,k)
    while(move_down(t)): # 여기서 falling쓰면 falling x,y 가 처음 젤위에있는상태라 이상해짐
        pass
is_left = True # 초기에 왼쪽
# pprint.pprint(box_map)
while(not is_finish()):
    print(take_out(is_left))
    falling()
    is_left = not is_left # 계속 뒤집어줌
