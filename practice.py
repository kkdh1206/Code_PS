
arr.sort()          # 원본 변경
b = sorted(arr)     # 새 리스트
arr.sort(reverse=True)
sorted(arr, reverse=True)

arr = [[2,1], [1,3], [2,0]]

b = sorted(arr, key=lambda x: (x[0], -x[1])) # lambda는 이렇게 key= 을 까먹으면안됨

print(b)

zip으로 묶어서 정렬ㄹ하는것도 배우기

from collections import deque

queue = deque()
queue.append((sx, sy))
visit[sx][sy] = 0

time = 0

while queue:
    size = len(queue) # 그렇지 이렇게 크기를 미리 들어두고 그만큼 밑에서 for문으로 그것만 처리하고 다시온느거지

    # 1. 같은 시간대 노드 처리 - 크기파악해서 걔네만 돌ㄹ림
    for _ in range(size):
        x, y = queue.popleft() # 하나꺼내고

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d] # 뒤에 달아주고 하는데 이전에는 계속 이걸반복이었다면 size = len(queue) 만큼 계속 이걸 함

            if not inside(nx, ny):  # 이런 조건들확인하고
                continue
            if visit[nx][ny] != -1: 
                continue
            if map[nx][ny] == 벽: 
                continue

            # ⭐ 이동 (append 여기 있음)
            visit[nx][ny] = visit[x][y] + 1
            queue.append((nx, ny)) # 그다음 세대를 달아주면됨

    # 2. 시간 흐름 (딱 한 번)
    time += 1

    # 3. 시뮬레이션 (먼지, 불, 물 등)
    dust_move()

    from collections import deque

    q = deque()
    q.append(start)
    visited = set([start])

    dist = 0

    while q:
        size = len(q)  # 현재 거리 레벨 크기

        for _ in range(size):
            x = q.popleft()

            # 여기서 x는 거리 dist에 있는 노드

            for nx in graph[x]:
                if nx not in visited:
                    visited.add(nx)
                    q.append(nx)

        dist += 1