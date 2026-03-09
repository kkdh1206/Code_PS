import sys
import pprint
sys.stdin = open("delivery.txt","r")
from collections import deque
N ,M = map(int,input().split())
containers=[0]*100
container_map = [[0]*N for _ in range(N)]
max_cus_num = 0
for m in range(M): 
    k,h,w,c = map(int,input().split())
    max_cus_num = max(max_cus_num, k)
    min_x = 0 # top_x 뭐이렇게 했던거같은데 , lefty랑 left_y 둘다있었는데
    max_x = w-1
    min_y = c-1
    max_y = c-1+h-1
    containers[k-1] = [min_x, max_x, min_y, max_y]

def stack(some_array):

    for k in range(len(some_array)):
        if some_array[k] !=0:
            [min_x, max_x, min_y, max_y] = some_array[k]
            movement = 0
            while inside(max_x + 1+movement,0) and all_zero_array(container_map[max_x + 1+movement][min_y:min_y + 1]):
                movement += 1
            for i in range(min_x + movement, max_x + 1 + movement):
                for j in range(min_y, max_y + 1):
                    container_map[i][j] = k + 1  # 색을 칠해줌




def gravity():
    for i in range(N - 1, -1, -1):
        bottom_array = bottom(container_map[i])
        if bottom_array:
            for b in bottom_array:
                if all_zero(b, i + 1):
                    move_down(b, i)



def bottom(some_array):
    old = 0
    box = []
    result = []
    for s in some_array:
        if s !=0:
            if old == s:
                box.append(s)
            else:
                if box:
                    result.append(box)
                box=[s]
    return result



def all_zero(some_array,i):
    if not inside(some_array[0],i):
        return False
    for s in some_array:
        if container_map[i][s] != 0:
            return False
    return True

def all_zero_array(some_array):
    for s in some_array:
        if s != 0:
            return False
    return True


def inside (x,y):
    return 0<=x<N and 0<=y<N

def move_down(some_array,i):
    color = 0
    for s in some_array:
        color =container_map[i][s]
        container_map[i][s] = 0
    for s in some_array:
        container_map[i+1][s] = color

    pprint.pprint(container_map)

def locate(cus_num):
    min_x = N
    max_x = 0
    min_y = N
    max_y = 0
    if cus_num == 0:
        return False
    isExist = False
    for i in range(N):
        for j in range(N):
            if container_map [i][j] == cus_num:
                min_x = min(min_x,i)
                max_x = max(max_x, i)
                min_y = min(min_y, j)
                max_y = max(max_y, j)
                isExist = True

    if isExist:
        return [min_x,max_x,min_y,max_y]
    else:
        return False

def can_move_carrier(some_array,is_left):
    [min_x, max_x, min_y, max_y] = some_array
    if is_left ==-1:
        for i in range(min_x,max_x+1):
            for j in range(0,min_y):
                if container_map[i][j] != 0:
                    return False
        return True
    else:
        for i in range(min_x,max_x+1):
            for j in range(max_y+1,N):
                if container_map[i][j] != 0:
                    return False
        return True

def select_carrier(some_array):
    [min_x, max_x, min_y, max_y] = some_array
    color = container_map[min_x][min_y]
    for i in range(min_x,max_x+1):
        for j in range(min_y, max_y+1):
            container_map[i][j]=0
    return color


print(containers)
stack(containers)
pprint.pprint(container_map)

locate_map = deque()
for m in range(max_cus_num):
    l = locate(m)
    if l:
        locate_map.append(l)
turn = -1
while locate_map:
    for l in locate_map:
        if can_move_carrier(l,turn):
            s = select_carrier(l)
            print(locate_map)
            # print(s)
            # pprint.pprint(container_map)
            for _ in range(N):
                gravity()
            pprint.pprint(container_map)
            locate_map = deque()
            for m in range(max_cus_num):
                l = locate(m)
                if l:
                    locate_map.append(l)
            print(s)

    turn = -turn





