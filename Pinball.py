# 기본 제공코드는 임의 수정해도 관계 없습니다. 단, 입출력 포맷 주의
# 아래 표준 입출력 예제 필요시 참고하세요.

# 표준 입력 예제
'''
a = int(input())                        정수형 변수 1개 입력 받는 예제
b, c = map(int, input().split())        정수형 변수 2개 입력 받는 예제
d = float(input())                      실수형 변수 1개 입력 받는 예제
e, f, g = map(float, input().split())   실수형 변수 3개 입력 받는 예제
h = input()                             문자열 변수 1개 입력 받는 예제
'''

# 표준 출력 예제
'''
a, b = 6, 3
c, d, e = 1.0, 2.5, 3.4
f = "ABC"
print(a)                                정수형 변수 1개 출력하는 예제
print(b, end = " ")                     줄바꿈 하지 않고 정수형 변수와 공백을 출력하는 예제
print(c, d, e)                          실수형 변수 3개 출력하는 예제
print(f)                                문자열 1개 출력하는 예제
'''

import sys


'''
      아래의 구문은 input.txt 를 read only 형식으로 연 후,
      앞으로 표준 입력(키보드) 대신 input.txt 파일로부터 읽어오겠다는 의미의 코드입니다.
      여러분이 작성한 코드를 테스트 할 때, 편의를 위해서 input.txt에 입력을 저장한 후,
      아래 구문을 이용하면 이후 입력을 수행할 때 표준 입력 대신 파일로부터 입력을 받아올 수 있습니다.

      따라서 테스트를 수행할 때에는 아래 주석을 지우고 이 구문을 사용하셔도 좋습니다.
      아래 구문을 사용하기 위해서는 import sys가 필요합니다.

      단, 채점을 위해 코드를 제출하실 때에는 반드시 아래 구문을 지우거나 주석 처리 하셔야 합니다.
'''
sys.stdin = open("pinball.txt", "r")


dx = [-1,0,1,0]
dy =[0,1,0,-1]

T = int(input())
N = 0#int(input())
pin_map =  [[0]*N for _ in range(N)]  #초기배열   #[list(map(int,input().split()))for _ in range(N)] # 어차피 0,0 기준으로 들어오네

def inside(x,y):
    return 0<=x<N and 0<=y<N

def isCollision(x,y,direction): # 해당 방향으로 갔을때 충돌인지
    x += dx[direction]
    y+= dy[direction]
    if not inside(x,y): # 제발 부호조심
        return True
    elif pin_map[x][y] == 1 or pin_map[x][y] == 2 or pin_map[x][y] == 3 or pin_map[x][y] == 4 or pin_map[x][y] == 5: # 아 제발....
        return True
    else: return False # 충돌안함

def isEnd(x,y,i,j): # i,j 가 초기위치임!!
    if not inside(x,y): # 어차피 밖이면 안끝난거임
        return False
    elif x==i and y == j :
        return True
    elif pin_map[x][y] == -1:
        return True
    else:
        return False

def isTeleport(x,y):
    if pin_map[x][y] >=6:
        return True
    else:
        return False

def teleport(x,y): # 오버되면 이거 미리 다찾아두면 줄긴할듯
    tele = pin_map[x][y]
    for i in range(N):
        for j in range(N):
            if not (x==i and y == j) and pin_map[i][j] == tele:
                return [i,j] # 다른 웜홀 반환

def reflect(direction):
    return (direction +2)%4

def turn_reflect(direction,isLeft):
    if isLeft:
        return (direction-1)%4
    else:
        return (direction+1)%4

def collision(ball_x,ball_y,wall_x,wall_y,direction):
    sub_x = ball_x - wall_x
    sub_y = ball_y - wall_y
    if not inside(wall_x,wall_y):
        # 찐 벽이랑 만남
        direction = reflect(direction)

    elif pin_map[wall_x][wall_y] == 1:
        if (sub_x==0 and sub_y == 1): # 위치정보
            direction = turn_reflect(direction,False) # 오른쪽으로 튕김
        elif (sub_x==-1 and sub_y == 0):
            direction = turn_reflect(direction, True)  # 왼쪽으로 튕김
        else:
            direction = reflect(direction)
    elif pin_map[wall_x][wall_y] == 2:
        if (sub_x==0 and sub_y == 1): # 위치정보
            direction = turn_reflect(direction,True) # 왼쪽으로 튕김
        elif (sub_x==1 and sub_y == 0):
            direction = turn_reflect(direction, False)  # 오른쪽으로 튕김
        else:
            direction = reflect(direction)
    elif pin_map[wall_x][wall_y] == 3:
        if (sub_x==0 and sub_y == -1): # 위치정보
            direction = turn_reflect(direction,False) # 오른쪽으로 튕김
        elif (sub_x==1 and sub_y == 0):
            direction = turn_reflect(direction, True)  # 왼쪽으로 튕김
        else:
            direction = reflect(direction)
    elif pin_map[wall_x][wall_y] == 4:
        if (sub_x==-1 and sub_y == 0): # 위치정보
            direction = turn_reflect(direction,False) # 오른쪽으로 튕김
        elif (sub_x==0 and sub_y == -1):
            direction = turn_reflect(direction, True)  # 왼쪽으로 튕김
        else:
            direction = reflect(direction)
    elif pin_map[wall_x][wall_y] == 5:
        direction = reflect(direction)
    return [wall_x, wall_y, direction]  # 바깥에 나간거도 주니까 조심하기

def simulate(x,y,direction):
    start_x,start_y = x,y
    ball_x = x
    ball_y = y
    score = 0
    while(True): # 종료를 현재위치로 하면 out of range

        if inside(ball_x,ball_y) and isTeleport(ball_x, ball_y): # 텔레포트는 걍 이동으로 안침 아니면 무한이동해서
            [ball_x, ball_y] = teleport(ball_x, ball_y)

        if isCollision(ball_x,ball_y,direction): # out of range 바로 확인 해줌 얘가
            wall_x = ball_x + dx[direction]
            wall_y = ball_y + dy[direction]  # 일단 이동해본다
            score+=1 # 충돌이니까
            c = collision(ball_x,ball_y,wall_x,wall_y,direction)
            ball_x = c[0]
            ball_y = c[1]
            direction = c[2] # 여기서 나온거로 수정
        else: # 평범한 이동
            ball_x += dx[direction]
            ball_y += dy[direction]
        # 이동 하고나서 끝났는지확인
        #print(ball_x,ball_y,score)
        if isEnd(ball_x,ball_y,start_x,start_y): # collsion으로 out of range 날수도 있음
            return score





# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input()) # 계속 받아있어야해서 여기있어야하네 ---> 이것도 가기전에 외우기
    pin_map = [list(map(int, input().split())) for _ in range(N)]  # 어차피 0,0 기준으로 들어오네

    # ///////////////////////////////////////////////////////////////////////////////////


    ans = 0
    for i in range(N):
        for j in range(N):
            for k in range(4): # 4방향
                if pin_map[i][j] == 0: # 빈공간인 경우에만

                   ans = max(ans,simulate(i,j,k))

    # ///////////////////////////////////////////////////////////////////////////////////
    print(f"#{test_case} {ans}") # 이거 가기전에 한번 더 외우기!!