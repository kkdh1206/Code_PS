import sys
sys.stdin = open("rudolf.txt", "r")


# -----------------------------------------------
# ※ 문제 규칙에 맞춘 구현 코드에 학습용 주석 추가 ※
#   - 동작‧로직은 절대 수정하지 않음
#   - 최상단 TL;DR 요약 문자열 제거
#   - Santa.__repr__ 메서드 삭제
# -----------------------------------------------

# 8 방향 델타: 0~3 = 상‧우‧하‧좌(산타 전용 우선순위),
#              4~7 = 대각선(루돌프 전용까지 포함)
dxy = [
    (-1, 0),  (0, 1),  (1, 0),  (0, -1),   # 상, 우, 하, 좌
    (-1, -1), (-1, 1), (1, -1), (1, 1)     # ↖, ↗, ↙, ↘
]

# -------------------------------------------------
# 헬퍼 함수
# -------------------------------------------------
def in_range(r, c):
    """격자 (r, c)가 0 ≤ r,c < N 안인가?"""
    return 0 <= r < N and 0 <= c < N

def distance(r1, c1, r2, c2):
    """문제 정의 거리: (Δr)^2 + (Δc)^2"""
    return (r1 - r2) ** 2 + (c1 - c2) ** 2

# -------------------------------------------------
# 산타 클래스
# -------------------------------------------------
class Santa:
    def __init__(self, num, r, c):
        self.num = num           # 산타 번호(0‑index)
        self.r, self.c = r, c    # 현재 위치
        self.fainted_turn = 0    # 이 턴까지 기절 (turn > fainted_turn 이면 정상)
        self.is_out = False      # 격자 밖 탈락?
        self.score = 0           # 누적 점수

    # -------------------------------------------------
    # 산타를 dir_num 방향으로 dist 칸 이동시키는 재귀 함수
    #   - 연쇄 밀림, 탈락 처리 포함
    # -------------------------------------------------
    def move(self, dir_num, dist):
        if dist == 0:
            return

        nr = self.r + dxy[dir_num][0] * dist
        nc = self.c + dxy[dir_num][1] * dist

        # 격자 밖 → 탈락
        if not in_range(nr, nc):
            self.is_out = True
            A[self.r][self.c] = None
            return

        # 착지 칸에 다른 산타가 있으면 1칸 추가 밀어내기(연쇄)
        if A[nr][nc] is not None:
            other_santa = santa_list[A[nr][nc]]
            other_santa.move(dir_num, 1)

        # 실제 위치 갱신
        A[self.r][self.c] = None
        self.r, self.c = nr, nc
        A[nr][nc] = self.num

    # 루돌프와 제곱 거리
    def distance(self, rudolph):
        return distance(self.r, self.c, rudolph[0], rudolph[1])

    # 현재 턴에 기절 상태인가?
    def is_fainted(self):
        return self.fainted_turn >= turn


# -------------------------------------------------
# 입력 & 초기화
# -------------------------------------------------
N, M, P, C, D = map(int, input().split())

# 루돌프 위치(0‑index)
R = tuple(map(lambda x: int(x) - 1, input().split()))

# 산타 정보
santa_list = [None] * P
for _ in range(P):
    num, r, c = map(int, input().split())
    santa_list[num - 1] = Santa(num - 1, r - 1, c - 1)

# 격자: None = 빈칸, -1 = 루돌프, 0~P‑1 = 산타 번호
A = [[None] * N for _ in range(N)]
A[R[0]][R[1]] = -1
for idx, s in enumerate(santa_list):
    A[s.r][s.c] = idx

# -------------------------------------------------
# 루돌프 이동 함수
# -------------------------------------------------
def move_rudolph():
    global R

    # 1) 가장 가까운 산타 선택 (거리, r desc, c desc)
    selected_santa = None
    for s in santa_list:
        if s.is_out:
            continue
        if (selected_santa is None or
            (s.distance(R), -s.r, -s.c) <
            (selected_santa.distance(R), -selected_santa.r, -selected_santa.c)):
            selected_santa = s

    # 2) 8 방향 중 타깃에 더 가까워지는 1칸 선택
    selected_dir_num = -1
    min_distance = selected_santa.distance(R)
    for dir_num, (dr, dc) in enumerate(dxy):
        nr, nc = R[0] + dr, R[1] + dc
        if in_range(nr, nc) and distance(nr, nc,
                                         selected_santa.r, selected_santa.c) < min_distance:
            min_distance = distance(nr, nc, selected_santa.r, selected_santa.c)
            selected_dir_num = dir_num
    assert selected_dir_num != -1, "No valid direction found for Rudolph"

    # 3) 실제 전진
    nr = R[0] + dxy[selected_dir_num][0]
    nc = R[1] + dxy[selected_dir_num][1]

    # 충돌 발생 시 처리 (루돌프가 먼저 움직였으므로 C점, C칸 밀림)
    if A[nr][nc] is not None:
        s = santa_list[A[nr][nc]]
        s.fainted_turn = turn + 1
        s.score += C
        s.move(selected_dir_num, C)

    # 격자 업데이트
    A[R[0]][R[1]] = None
    R = (nr, nc)
    A[nr][nc] = -1

# -------------------------------------------------
# 산타 이동 함수 (한 명)
# -------------------------------------------------
def move_santa(santa: Santa):
    # 이동 후보: 상우하좌 중 격자 안 + (빈칸 or 루돌프)
    min_distance = santa.distance(R)
    selected_dir_num = -1
    for dir_num, (dr, dc) in enumerate(dxy[:4]):  # 상우하좌
        nr, nc = santa.r + dr, santa.c + dc
        if in_range(nr, nc) and (A[nr][nc] is None or A[nr][nc] == -1):
            if distance(nr, nc, R[0], R[1]) < min_distance:
                min_distance = distance(nr, nc, R[0], R[1])
                selected_dir_num = dir_num

    # 가까워질 수 있는 칸이 없으면 정지
    if selected_dir_num == -1:
        return

    nr = santa.r + dxy[selected_dir_num][0]
    nc = santa.c + dxy[selected_dir_num][1]

    # ① 빈칸 → 1칸 이동
    if A[nr][nc] is None:
        santa.move(selected_dir_num, 1)
    # ② 루돌프 칸 → 산타 주도 충돌 (D점, 반대방향 D칸 밀림)
    else:
        santa.fainted_turn = turn + 1
        santa.score += D
        santa.move((selected_dir_num + 2) % 4, D - 1)

# -------------------------------------------------
# 메인 루프
# -------------------------------------------------
from pprint import pprint
def main():
    global turn
    B=[[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j]:

                if A[i][j]>=0:
                    B[i][j] = A[i][j] + 1
                else:
                    B[i][j] = -1
            else:
                B[i][j] = 0
    print(A)
    for turn in range(1, M + 1):
        pprint(B)
        #pprint(A)
        #print("---")
        # 1. 루돌프 이동
        move_rudolph()
        for i in range(N):
            for j in range(N):
                if not A[i][j]:
                    B[i][j] = 0
                elif A[i][j] > 0:
                    B[i][j] = A[i][j] + 1
                else:
                    B[i][j] = -1
        pprint(B)
        print("===")
        # 2. 산타 이동 (번호 순, 기절/탈락 제외)
        for s in santa_list:
            if not s.is_out and not s.is_fainted():
                move_santa(s)

        # 3. 생존 산타 1점 보너스
        is_all_out = True
        for s in santa_list:
            if not s.is_out:
                s.score += 1
                is_all_out = False

        # 4. 전원 탈락 시 조기 종료
        if is_all_out:
            break

    # 최종 점수 출력
    print(*[s.score for s in santa_list])

# -------------------------------------------------
main()
