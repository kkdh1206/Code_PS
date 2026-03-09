import sys
from collections import deque

# PyPy3 제출 필수
input = sys.stdin.readline
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def bfs_get_distances(start_node_idx, all_nodes, n, m, grid):
    sx, sy = all_nodes[start_node_idx]

    # 목표 지점들의 좌표를 딕셔너리로 매핑 {(r,c): index}
    # 이렇게 하면 BFS 돌면서 좌표만으로 몇 번째 식당인지 바로 알 수 있음
    target_map = {}
    for i, (r, c) in enumerate(all_nodes):
        target_map[(r, c)] = i

    # 결과 저장용 리스트 (거리값만 저장, -1로 초기화)
    # 크기가 매우 작음 (최대 21개)
    dists = [-1] * len(all_nodes)
    dists[start_node_idx] = 0

    # 방문 체크 배열 (BFS 함수 안에서만 쓰고 버림 -> 메모리 절약)
    visited = [[-1] * m for _ in range(n)]
    visited[sx][sy] = 0

    q = deque([(sx, sy)])

    # 찾은 타겟 개수 (자기 자신 포함 1개로 시작)
    found_count = 1
    target_total = len(all_nodes)

    while q:
        x, y = q.popleft()
        d = visited[x][y]

        # 1. 큐에서 꺼낸 좌표가 목표물(식당) 중 하나라면 거리 기록
        if (x, y) in target_map:
            idx = target_map[(x, y)]
            if dists[idx] == -1:
                dists[idx] = d
                found_count += 1
                # 모든 타겟을 다 찾았으면 BFS 즉시 종료 (시간 최적화)
                if found_count == target_total:
                    return dists

        # 2. 상하좌우 이동
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] != 'X' and visited[nx][ny] == -1:
                    visited[nx][ny] = d + 1
                    q.append((nx, ny))

    return dists


def main():
    try:
        line = input().split()
        if not line: return
        n, m = map(int, line)
        grid = [input().strip() for _ in range(n)]
    except ValueError:
        return

    pts = []
    start = None

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'K':
                pts.append((i, j))

    # 식당 5개 미만이면 불가능
    if len(pts) < 5:
        print(-1)
        return

    # 관리해야 할 모든 지점: [Start, K1, K2, ..., Kn]
    nodes = [start] + pts
    total_nodes = len(nodes)

    # 1. 인접 행렬(Adjacency Matrix) 생성
    # adj[i][j] : nodes[i]와 nodes[j] 사이의 거리
    # 맵 전체가 아니라, 숫자값만 저장하므로 메모리 매우 적게 씀
    adj = []

    for i in range(total_nodes):
        # i번째 노드에서 다른 모든 노드까지의 거리 리스트를 받아옴
        dists_from_i = bfs_get_distances(i, nodes, n, m, grid)
        adj.append(dists_from_i)

    # 2. DP 수행
    # 우리는 nodes[0](Start)에서 출발.
    # 식당은 nodes[1] ~ nodes[total_nodes-1] (총 num_k 개)

    num_k = len(pts)
    # dp[(visited_mask, last_visited_index)] = min_cost
    # 식당 인덱스를 0 ~ num_k-1 로 사용하여 비트마스크

    current_dp = {}

    # Start -> 첫 번째 식당 방문 초기화
    for i in range(num_k):
        dist = adj[0][i + 1]  # Start(0) -> i번째 식당(i+1)
        if dist != -1:
            current_dp[(1 << i, i)] = dist

    # 총 5개의 식당을 방문해야 함 (이미 1개 방문했으니 4번 더 반복)
    for step in range(4):
        next_dp = {}
        if not current_dp:
            break

        for state, cost in current_dp.items():
            mask, last_k_idx = state

            # 현재 식당(last_k_idx) -> 다음 식당(next_k_idx)
            # nodes 리스트 기준 인덱스는 (idx + 1) 임을 주의
            u_node_idx = last_k_idx + 1

            for next_k_idx in range(num_k):
                # 이미 방문한 식당 패스
                if mask & (1 << next_k_idx):
                    continue

                v_node_idx = next_k_idx + 1
                dist = adj[u_node_idx][v_node_idx]

                if dist == -1:  # 이동 불가
                    continue

                new_mask = mask | (1 << next_k_idx)
                new_cost = cost + dist

                if (new_mask, next_k_idx) not in next_dp or new_cost < next_dp[(new_mask, next_k_idx)]:
                    next_dp[(new_mask, next_k_idx)] = new_cost

        current_dp = next_dp

    if not current_dp:
        print(-1)
    else:
        print(min(current_dp.values()))


if __name__ == "__main__":
    main()