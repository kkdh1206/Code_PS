import sys
sys.stdin = open("rudolf.txt", "r")


# 입력 받기 M개의 턴으로 동작
N,M,P,C,D = map(int,input().split())
snow = [[0]*N for _ in range(N)]
#산타는 번호대로 구현하고
santa=[0]*P # 점수
santa_life=[1]*P # 생사 스턴 -> 생 1 스턴 0 사망 -1
# 루돌프는 음수로두자
rudolf_x, rudolf_y = map(int, input().split())
santa_info =[]
for p in range(P):
    s_num, s_x,s_y = map(int, input().split())
    santa_info.append([s_num,s_x,s_y])
# 이놈들 1,1 기준인거 기억하자!

def inside(x,y):
    return 0<=x<N and 0<=y<N # 이런거 헷갈리게 설정하면 절대안됨 그냥 기본에 충실 ㄱㄱ

# 거리구하기
def distance_rudolf(r1,c1,r2,c2):
   # if abs(r1-r2) == 1 and abs(c1-c2) == 1:
    #    return 1 # 예외임
    return (r1-r2)*(r1-r2) + (c1-c2)*(c1-c2) # 정신차려 제발 함수가 오류투성이고 좀 종이에 쓸까 다음부턴

def distance(r1,c1,r2,c2):

    return (r1-r2)*(r1-r2) + (c1-c2)*(c1-c2) # 정신차려 제발 함수가 오류투성이고 좀 종이에 쓸까 다음부턴

def search_dir(x,y,isRudolf,snow_map):  # 가장 가까운거 찾아서 방향알려주는거
    # 함수 본연의 기능에 집중하자
    min_dist = N*N+N*N # 젤큰거로둠
    loc =[]
    if isRudolf:
        for i in range(N):
            for j in range(N): # 안 죽은 산타 가까운순
                if snow_map[i][j] > 0 and santa_life[snow_map[i][j]-1] != -1 and distance_rudolf(i,j,x,y) <= min_dist: # = 으로 포함을해둬서 똑같더라도 r,c순으로 더큰놈한테 이끌림
                    # 아 맞긴한데 대각선 거리는 예외적으로 1임
                    min_dist = distance_rudolf(i, j, x, y) # 아니 이걸 넣어줘얗지 하!!!!
                    loc = [i,j] # 표적

    else:
        for i in range(N):
            for j in range(N):
                if snow_map [i][j] == -1:
                    loc = [i,j]
    # 여기서 loc에 가는 가장 좋은 방향 제시 ㄹㅇ 방향만 제시할뿐 나중에 못가는거면 알려줘
    if not loc: # loc이 비엇으면
        #print(snow_map)
        #print(isRudolf)
        return False
    else:
        #print(min_dist)
        res = [loc[0]-x,loc[1]-y]  # 이렇게해서 빼주면 위치가 특정됨
        #print(res)
        if res[0] > 0: # 그걸 1 크기 애로 변신시킴
            res[0] = 1
        elif res[0] < 0:
            res[0] = -1
        else:
            res[0] = 0
        if res[1] > 0:
            res[1] = 1
        elif res[1] < 0:
            res[1] = -1
        else: res[1] = 0
        return res


# 루돌프 움직임 구성 (대각선도 가능 이동) - 가장 가까운 산타 탐색 & 이동
def rudolf(x,y,snow_map):
    santa_dir = search_dir(x,y,True,snow_map)
    #print(santa_dir)
    #print(snow_map[x][y])
    #print("~")
    #print("####")
    #print(santa_dir)
    if santa_dir: # 근처 산타가 존재하는 경우
        [nx,ny] = [x+santa_dir[0],y+santa_dir[1]] # 돌진해봄 # 리스트끼리 더할땐 걍 요서끼리 더해주자
        if snow_map[nx][ny] == 0:
            snow_map[nx][ny] = snow_map[x][y]
            snow_map[x][y] = 0 # 루톨프 이동 성공
        else:
            # 산타와 부딫힌경우 산타는 기절하고 날아감
            santa_life[snow_map[nx][ny]-1] = 0 # 기젏상황
            #print("기절 해라", snow_map[nx][ny])
            throw(nx,ny,santa_dir,C,snow_map) # nx,ny 에 있던 산타 날려버림 C는 전역변수
            # 날아갓으니 그자리 루돌프 차지
            #print(snow_map[x][y])

            snow_map[nx][ny] = -1
            snow_map[x][y] = 0 # 루톨프 이동 성공
# 기절산타관리 산타 큐나 리스트 필요 -> 기절,탈락상태,그리고 점수 나타내는 리스트 ㄱㄱ

# 산타 움직이는 로직
def santa_move(x,y,rudolf_dir,snow_map): # 걸어서 산타만나면 아무것도 안하고 걸어서 없으면 걸어가고 루돌프 만나면 튕김
    [nx,ny] = [x+rudolf_dir[0],y+rudolf_dir[1]] # 단방향이니 일단 이동 바로해봄
    if snow_map[nx][ny] == 0: # 비어있을때
        snow_map[nx][ny], snow_map[x][y] = snow_map[x][y], snow_map[nx][ny]
        # 산타이동
        return True
    elif snow_map[nx][ny] <0: # 루돌프 만날때
        # 얘도 기절해야하는듯 기절먼저먹이고 죽으면 죽여
        santa_life[snow_map[x][y] - 1] = 0
        snow_map[nx][ny] = snow_map[x][y] # 일단 산타를 넣어주고
        snow_map[x][y] = 0
        #print(rudolf_dir)

        throw(nx,ny,[-x for x in rudolf_dir],D,snow_map) # 루돌프 자리에서 부터 D 칸 반대방향으로 튕겨나감
        snow_map[nx][ny] =-1 # 산타 날린후에 루돌프 복구

        #pprint(snow_map)
        #print("@@@@@")

        # 리스트 음수 바로 안된다함 이렇게 쓰는거 알아두자
        return True
    return False # 안움직인경우


# 산타이동 구현(산타번호도 있는듯) 산타도 루돌프와 가까워지는 방향으로 이동 ㅋㅋ - 항상 가까워 져야지만 이동
# 산타는 상하좌우만 이동가능
def santa_simulate(x,y,snow_map,r_loc): #<-----------------------여기가 문제따!!!!
    rudolf_dir = search_dir(x,y,False,snow_map) # 현재 루돌프로 가는 방향 탐색
    #print(snow_map)
    if abs(rudolf_dir[0]) + abs(rudolf_dir[1]) == 1:
        if santa_move(x,y,rudolf_dir,snow_map):
            return True # 산타가 움직인 경우
    elif abs(rudolf_dir[0]) + abs(rudolf_dir[1]) == 2:
        # 상우하좌 순서
        final_dir =[0,0]
        min_dist = distance(x,y,r_loc[0],r_loc[1])
        if rudolf_dir[0] == -1:
            if  distance(r_loc[0],r_loc[1],x-1,y) < min_dist and snow_map[x-1][y] == 0 : # 정신차리자 산타는 다 숫자다르자나
                min_dist = distance(r_loc[0],r_loc[1],x-1,y)
                final_dir = [-1,0]
        if rudolf_dir[1] == 1: # tlqkf elif면 당연히 못가지 qudtls아
            if distance(r_loc[0],r_loc[1],x,y+1) < min_dist and snow_map[x][y+1] == 0:
                min_dist = distance(r_loc[0], r_loc[1], x, y+1) # 복사하고 수정 똑바로 다하자
                final_dir = [0, 1]
        if rudolf_dir[0] == 1:
            #print("!!!!!!!!!")
            #print(rudolf_dir)
            if distance(r_loc[0],r_loc[1],x+1,y) < min_dist and snow_map[x+1][y] == 0:
                min_dist = distance(r_loc[0], r_loc[1], x + 1, y)
                final_dir = [1, 0]
        if rudolf_dir[1] == -1:
            #print("!!!!!!!!!")
            if distance(r_loc[0],r_loc[1],x,y-1) < min_dist and snow_map[x][y-1] == 0:
                min_dist = distance(r_loc[0], r_loc[1], x , y-1)
                final_dir = [0, -1]
        #print(santa_life)
        #print(snow_map[x][y],final_dir, rudolf_dir, min_dist)
        if min_dist <distance(x,y,r_loc[0],r_loc[1]):

            #print(min_dist)
            if santa_life[snow_map[x][y] -1 ] == 1:
                #print(snow_map[x][y], final_dir, rudolf_dir, santa_life[snow_map[x][y] - 1])
                #print("AAA")
                santa_move(x,y,final_dir,snow_map)
                #pprint(snow_map)
                #print("****")
                return True
        return False
    return False # 산타 꼼짝안함
# 날아가는 함수
def throw(x,y,direct,dist,snow_map): # 여기서 연쇄적으로 날아가는거 까지 처리해주기!! 점수도 같이
# 점수 추가하는거 여기에 넣어야할듯!! global로 하든해서
    #score += dist # 날아간만큼 더해짐 왜냐면 루돌프 혹은 산타에 의해서 움직일수 있기 때문
    #isRudolf = False

    who = snow_map[x][y] -1 # 지금 날아가는 산타 번호 -1
    # if snow_map[x][y] < -1: # 루돌프가 나왔으면 이건 여기로 오는 산타가 날아가는거임
    #     #isRudolf = True
    #     who = snow_map[x][y] -1
    #     old_x = x + direct[0] # 아 튕기는거니까 무조건 플러스지 이미 그 위치에서 온거니까
    #     old_y = y + direct[1]
    #     #print(x,y)
    #     #print(direct)
    #     who = snow_map[old_x][old_y]-1
    if dist == -1:
        dist = 1
    else:
        santa[who] += dist  # 날아간 거리만큼 점수 더함
    # direct는 방향 리스트임
    nx = x+ dist*direct[0]
    ny = y+dist*direct[1]
    if inside(nx,ny):
        if snow_map[nx][ny] == 0: # 움직인 자리에 없는경우
            snow_map[nx][ny] = snow_map[x][y] # 이동시킴
            snow_map[x][y] = 0 # 없애줌 이전껀

            return True
            # success
        else : # 또다른 산타가 있는경우
            temp = snow_map[x][y]
            snow_map[x][y] = 0 # 이동 함
            # 연쇄 구현
            throw(nx,ny,direct,-1,snow_map) # 1만큼 밀림 그동안 nx,ny는 보장 되있음 아직 다 하고나서 바뀜
            # 여기서 점수를 빼주자 맞춰주기 위해서
            #santa[snow_map[nx][ny] -1] -=1 # 한번빼줘
            #print("temp=", temp, nx,ny)
            #print(snow_map[nx][ny])
            snow_map[nx][ny] = temp # 이동 도착
            #print(snow_map[nx][ny])
            return True
    else:
        santa_life[who] = -1 # 사망
        # 사망처리도 해줘야함 실제로없애는 작업
        snow_map[x][y] = 0
        return False # fail -> 이경우는 산타가 장외 탈락임

def simulation(snow_map): # 턴제에 기절도 고려 하고 기절된애 복구도해주고
    santa_loc = [0]*P # 매번 그냥 산타 위치를 탐색해서 넣어주자 하나 하고 계속 탐색은 너무 비효율적

    r_loc =[]
    for i in range(N):
        for j in range(N):
            if snow_map[i][j] > 0:
                #print(snow_map)
                #print(P)
                #print(snow_map[i][j]-1)
                if santa_life[snow_map[i][j]-1] == -1:
                    snow_map[i][j] = 0
                else:
                    santa_loc[snow_map[i][j]-1] = [i,j] # -1해준이유는 0,0기반으로 변경
            elif snow_map[i][j] == -1:
                r_loc = [i,j]
    # 루돌프 먼저 움직임
    if r_loc:
        rudolf(r_loc[0],r_loc[1],snow_map)
        #print("))))))")
        #pprint(snow_map)
        #print("end rudolf")


    for i in range(N):
        for j in range(N):
            if snow_map[i][j] == -1:
                r_loc = [i,j]
    # 산타 개시 살아있는거만 기절안하고
    #print(santa_life)
    if santa_loc: # 산타 있다면
        #print(santa_loc)
        #print("@@@@")
        for p in range(P):
            if santa_life[p] == 1: # 살아있는 산타
                # print(p)
                for i in range(N):  # 바꾸고 나서도 갱신을 해ㅑ잊씨발 ㅏ라다ㅏ  -> 아 설마 튕기고 난 이후의 연쇄이후에 좌표가 업데이트 안되서 문제가 될수도??!!
                    for j in range(N):
                        if snow_map[i][j] > 0:
                            # print(snow_map)
                            # print(P)
                            # print(snow_map[i][j]-1)
                            if santa_life[snow_map[i][j] - 1] == -1:
                                snow_map[i][j] = 0
                            else:
                                santa_loc[snow_map[i][j] - 1] = [i, j]  # -1해준이유는 0,0기반으로 변경
                        elif snow_map[i][j] == -1:
                            r_loc = [i, j]
                santa_simulate(santa_loc[p][0],santa_loc[p][1],snow_map,r_loc)
    #print("------")

    #pprint(snow_map)
    #print("+++++++")
    #print("end santa")
    # 기절 복구
   #print(santa_life)
    #print(santa)
    for p in range(P):
        if santa_life[p] != -1:
            santa[p] +=1 # 1점씩 점수증가
        if santa_life[p] == 0: # 기절한놈들
            santa_life[p] = 3 # 기절중간
        elif santa_life[p] == 3: # 제발 elif if 실수 그만
            santa_life[p] = 1 # 살아남
    #pprint(snow_map)
# snow 생성해줘야함 input에 따라서
snow[rudolf_x-1][rudolf_y-1] = -1 # 루돌프 지정 -1 해준건 1,1 기준인거 0,0 으로 변환
for p in range(P):
    [s_num,s_x, s_y] = santa_info[p]
    snow[s_x-1][s_y-1] = s_num # 1부터 시작해서 ㄱㅊ할듯

from pprint import pprint
for i in range(M): # M번 수행
   #("Turn", i+1)
    #print(santa_life)
    #print(santa)
    #print("!!!!!")
    #pprint(snow)
    simulation(snow)
    #pprint(snow)
    #print("=======")
    #print(santa)ㄴ
    #print(santa_life)
   # 아니 지도 업데이트 언제할지도 무척 중요하다!!!!!!!!!!! -> 뭔갈할때 넣을때 제발 한버더 신중하게 생각해서 해보자!!!

   # 연쇄로 인해서 움직인 산타가 반영이 안되서 해맸음
   # 이거 먼가 디버깅으로 찾을순있긴한데 12시간정도 걸리니까 앞으로는
   # 그냥 짤때 좀더 더 생각해보고 신중하게 넣자
   # 아님 어디서 입력을 받을지 A4에 그림을 그리자!!!!!!!!제 발 ㅂㄹㄷㅈ너무힘들어ㅓㅓㅓㅓ


print(*santa)

# 충돌함수 구현
# 루돌프 -> 산타 충돌하면 C만큼점수얻고 C만큼 밀려남 루돌프가 이동한 방향ㅇ으로
# 산타 -> 루돌프 면 D만큼 점수얻고 산타가 이동한 반대 방향으로 D만큼 밀림
# 충돌함수에 점수함수 & 튕기는함수 필요함
# 게임판 밖으로 나가면 산타 탈락
# 튕길때는 그냥 바로 그 위치로감 추다충돌없이 근데 산타랑 합쳐지면 상호작용있음

# 상호작용 원래있던 산타는 1칸 해당방향으로 밀려남 연쇄적임

# 기절 k+1턴까지 기절 즉 1번턴 쉼 - 근데 턴은 루돌프 산타 한번씩움직이는게 한번 턴임

# 탈락안한 산타1점씩 추가