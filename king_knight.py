import sys

sys.stdin = open("king_knight.txt", "r")

L,N,Q = map(int,input().split())
dx = [-1,0,1,0]
dy = [0,1,0,-1]

trap_map = [list(map(int,input().split())) for _ in range(L)]
start_health = []
knights =[]
for i in range(N):
    r,c,h,w,k = map(int,input().split())
    knights.append([r-1,c-1,h,w,k]) # 1,1 기준이라서
    start_health.append(k)
order =[]
for q in range(Q):
    i,d = map(int,input().split())
    order.append([i,d]) # 명령저장

knights_map = [[0]*L for _ in range(L)]

for n in range(N):
    [r,c,h,w,k] = knights[n]
    for i in range(r,r+h):
        for j in range(c,c+w):
            knights_map[i][j] = n+1 # 0->1 로 시작을 바꿔줌

def inside(x,y):
    return 0<=x<L and 0<=y<L

def is_wall(who,d): # True가 뜨면 가면안되는거임
    # 여기 input i는 명령의 i임
    other = set()
    [r,c,h,w,k] = knights[who-1]
    r += dx[d]
    c += dy[d] # 이동해줌
    for i in range(r, r + h):
        for j in range(c, c + w):
            if not inside(i,j):
                return True # 밖으로 나가면 걍 wall임
            elif trap_map[i][j] == 2:
                return True # 이동시킨곳에 wall이 있으면

    for i in range(r, r + h):
        for j in range(c, c + w):
            # print(knights_map[i][j], who)
            if knights_map[i][j] != 0 and knights_map[i][j] != who: # 자기자신이나 빈곳이 아니면 xxxx -> and로 해야지 동시에 만족해야하니까
                other.add(knights_map[i][j]) # knight 저장
    # print(other)
    for o in other:
        if is_wall(o,d): # 실행함 만약 여기서 True가 뜨면 True반환 안되니까
            return True # 바로 is_wall반환하면 안됨 왜냐면 밀리는 자식이 여러개일수도있는데 그러면 하나만 False되도 큰일나버림

    return False # 전체 문제가 다 없으면

def remove(num):
    for i in range(L):
        for j in range(L):
            if knights_map[i][j] == num:
                knights_map[i][j] = 0 # 지워줌

def push(num, d): # 이건 무조건 움직이는거 기준임
    other = set()
    [r, c, h, w, k] = knights[num - 1]
    for i in range(r, r + h):
        for j in range(c, c + w):
            if knights_map[i][j] == num: # 이미 다른곳에 의해 밀린부분은 신경안써줘도 되니까
                knights_map[i][j] = 0
    r += dx[d]
    c += dy[d]
    for i in range(r, r + h):
        for j in range(c, c + w):
            if knights_map[i][j] != 0:  # 0말고 다른게있으면 밀기
                other.add(knights_map[i][j])
            knights_map[i][j] = num  # 상관없이 이걸로 채움
            if trap_map[i][j] == 1: # 함정이있는곳
                k-=1 # 체력감소
    knights[num - 1] = [r, c, h, w, k] # 여기도 업데이트 k도 바뀐거 반영되서 업뎃 됨
    for o in other:
        push(o,d) # 연쇄 push

    # 죽은 말은 안움직이게해줘야함 -> 이건 move 이후에 지우기
    return

def move(num,d):
    if not is_wall(num,d): # 움직일수있다면 - 못움직이면 못밈 애초에 push에서도 안움직이는거 하나라도 있으면 시작을안함
        other = set()
        [r,c,h,w,k] = knights[num-1]
        for i in range(r, r + h):
            for j in range(c, c + w):
                knights_map[i][j] = 0
        r += dx[d]
        c += dy[d]
        knights[num - 1] = [r, c, h, w, k] # 바뀐거 업데이트 여기는 k변화 없음
        for i in range(r, r + h):
            for j in range(c, c + w):
                if knights_map[i][j] != 0:  # 0말고 다른게있으면 밀기
                    other.add(knights_map[i][j])
                knights_map[i][j] = num # 상관없이 이걸로 채움
        for o in other:
            push(o,d) # 연쇄 push

for o in order:
    if knights[o[0]-1][4]<=0: # 이미죽은경우 무시 - 보통 답이 틀리면 어떤게 엣지케이스일지 어떤걸 고려안했을지 생각해봐라 보통 일반거 통과햇으면 평범은 통과되는데 뭔가 죽거나 이럴때 안되게해야하는데 처리안했을가능성이 크다
        # 아 제발 조건 < 인지 <=인지 제대로 보기 어디까지 해줘야할지 조건 정확히 하는게 정말중요하다!!!
        continue
    else:
        move(o[0], o[1])
        for k in range(N):
            if knights[k][4] <= 0:  # 죽으면
                remove(k + 1)  # 실제 번호를 넣어줌
    # for row in knights_map:
    #     print(*row)
    # print("~~~~")
    # print(knights)
final_health = 0
for k in range(N):
    if knights[k][4] > 0:
        final_health +=(start_health[k] - knights[k][4])
print(final_health)

# knights = [[0,0,2,2,1],[0,2,1,1,1]]
# N=2
# knights_map = [[0]*L for _ in range(L)]
# for n in range(N):
#     [r,c,h,w,k] = knights[n]
#     for i in range(r,r+h):
#         for j in range(c,c+w):
#             knights_map[i][j] = n+1 # 0->1 로 시작을 바꿔줌
# for row in knights_map:
#     print(*row)
# print("~~~~~")
# move(1,1)
# for row in knights_map:
#     print(*row)
#
# print(knights)

