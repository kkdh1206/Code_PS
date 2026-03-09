import sys
sys.stdin = open("input.txt", "r")


# 입력받기 split 조심
R, C, M = map(int, input().split())
# 총 M번 받음 상어

# r,c,s,d,z (위치,  속력,이동방향,크기)
sharks = [list(map(int, input().split())) for _ in range(M)]  # 이거 번호대로 갈거임
for i in range(M):
    # 1,1 기준이니 0,0변환 필요

    sharks[i][0] -= 1
    sharks[i][1] -= 1


live = [True] * M
# sharks를 바꾸며 작업할거임
sea = [[0] * C for _ in range(R)]
fisher = -1  # 초기 시작은 음수
# 방향도 1빼줘야겟네 처리할때
dx = [-1, 1, 0, 0]  # 위 아래 오른쪽 왼쪽
dy = [0, 0, 1, -1]


def inside(x, y):
    return 0 <= x < R and 0 <= y < C


def reverse(x, length):
    return length - x


def sharks_simulation(sea_map):  # 상어 바다를 미리 만들어서 넣어줘야함 - 상어번호를 넣어두자
    # 제작된 지도 바탕으로 상어 이동
    # scan해서 상어 목록 만들고 이동시키기
    for i in range(R):
        for j in range(C):
            if sea_map[i][j] != 0:
                who = sea_map[i][j] - 1
                speed = sharks[who][2]
                des = sharks[who][3]
                sea_map[i][j] = 0  # sea 초기화해줘야 복제안됨!!!!
                if live[who]:
                    swim(i, j, speed, des, who)  # 지금이러면 상어가 복제되버림

    # 지도 제작
    print(sharks)

    for i in range(M):
        if live[i]:  # 살아있는 상어만
            shark_x = sharks[i][0]
            shark_y = sharks[i][1]
            print(shark_x)
            # 여기서 잡아먹는것도 구현하자
            if sea_map[shark_x][shark_y] == 0:  # 빈킨일시
                sea_map[shark_x][shark_y] = i + 1  # 1을 더해줘야 구분이 됨 0이랑
            else:  # 상어가 있을시 서로 잡아먹기
                other = sea_map[shark_x][shark_y]
                if other == i + 1:  # 자기 자신일 경우
                    pass
                else:
                    size = sharks[i][4]
                    other_size = sharks[other - 1][4]
                    if size > other_size:  # 새로온 놈이 잡아먹음 - 자기 자신일수도 있는데 그럴경우엔 패스해줘야함
                        live[other - 1] = False  # 이전 상어 사망
                        sea_map[shark_x][shark_y] = i + 1  # 새로운 상어 등록
                    else:
                        live[i] = False  # i는 아직 더하기 전이라 바로 접근가능
                    # 이미 이전상어는 잘있음

    # 다시 다 반영해서 지도 만들어주기는 필요없음 시작할때 계속 만드니까


# def move(x,length,distance):

# 복붙하니까 자꾸 오타나는듯

def swim(x, y, speed, des, who):
    global sharks  # sharks를 여기서 수정을 해줄거임
    # 상어이동 자체를 먼저 구현
    # speed가 R,C보다 크면 걍 반복됨
    len_x, len_y = 2 * (R - 1), 2 * (C - 1)
    nx, ny = x, y
    if des == 1 or des == 2:  # 상하의 경우
        speed %= len_x  # 반복제거
        if des == 1:  # 위 -> 행을 말함
            if x - speed >= 0:
                nx = x - speed
                # 방향은 안바뀜
            elif speed <= x + R - 1:
                nx = 0 + speed - x
                des = 2
            else:
                nx = (R - 1) - (speed - x - (R - 1))  # 사실상 2R-2 까지 얼마남았나네
        else:  # 아래
            if (R - 1 - x) - speed >= 0:  # R-1 까지니까 1 빼줘야함, 거리니까 그냥 빼도됨 1안더하고
                nx = x + speed
                # 방향은 안바뀜
            elif speed <= R - 1 + (R - 1 - x):
                nx = (R - 1) - (speed - (R - 1 - x))
                des = 1
            else:
                nx = x - (2 * (R - 1) - speed)  # 부족한 만큼 위로 보냄
    else:
        speed %= len_y  # 반복제거
        if des == 4:  # 왼쪽 -> 열을 말함
            if y - speed >= 0:
                ny = y - speed
                # 방향은 안바뀜
            elif speed <= y + C - 1:
                ny = 0 + speed - y
                des = 3
            else:
                ny = (C - 1) - (speed - y - (C - 1))  # 사실상 2R-2 까지 얼마남았나네
        else:  # 오른쪽
            if (C - 1 - y) - speed >= 0:
                ny = y + speed
                # 방향은 안바뀜
            elif speed <= C - 1 + (C - 1 - y):
                ny = (C - 1) - (speed - (C - 1 - y))
                des = 4
            else:
                ny = y - (2 * (C - 1) - speed)  # 부족한 만큼 위로 보냄

        # if not inside(nx,ny): # 만약넘어가면  # !!!!! 아니 안넘어갈때로 봐야지!! 아 조건을 하하ㅏ 조건은 진짜 유심히 잘보기
    # 주석을적든
    # 수행 다 끝남
    # sharks에 반영
    sharks[who][0] = nx
    sharks[who][1] = ny
    # 올바른 방향 다시 넣어주기
    sharks[who][3] = des

    # 겹칠시 상어 잡아먹기


def catch(y, sea_map):  # 잡은 상어 크기를 반환해주자
    # y 열에서 가장 낮은 행의 상어를 잡아감

    for i in range(R):
        if sea_map[i][y] != 0:
            who = sea_map[i][y] - 1  # -1 꼭해줘야함
            # 살아있는 물고기인지 확인
            if live[who]:
                live[who] = False
                return sharks[who][4]
    return 0  # 암것도 없다는뜻


count = 0
# 초기 상어지도 만들어줘야함
for i in range(M):
    if live[i]:  # 살아있는 상어만 - 사실 다 살아있기낳ㅁ
        shark_x = sharks[i][0]
        shark_y = sharks[i][1]
        sea[shark_x][shark_y] = i + 1

for i in range(C):  ## 열을 돌아야함!!!
    # fisher +=1 # 낚시꾼이동

    count += catch(i, sea)  # 낚시
    sharks_simulation(sea)  # 상어이동

print(count)  # 잡은 상어 크기 합 반환
