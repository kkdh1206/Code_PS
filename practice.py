

while queue:
    size = len(queue)

    # 같은 시간대 처리
    for _ in range(size):
        x, y = queue.popleft()
        # 이동

    # 여기서 시간 증가 + 시뮬레이션
    time += 1
    dust_move()

    # 이런식으로 하면 시간대 아님 거리별로 BFS가 나눠짐