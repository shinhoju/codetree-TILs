# 마법의 숲 탐색

from collections import deque

R, C, K = map(int, input().split())

# c, d (골렘이 출발하는 열 / 골렘의 출구 방향)
orders = []
for _ in range(K):
    orders.append(tuple(map(int, input().split())))

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

arr = [[0] * (C+2) for _ in range(R+3)]


def down(c):
    r = 1
    for mul in range(1, R+2):
        nr = r + mul                        # 중앙 한 칸 내려옴
        # 조건 확인: 아랫쪽 3칸 빈 칸인지 체크
        # for dr, dc in ((1, -1), (1, 1), (1, 0)):
        for dr, dc in ((0, -1), (0, 1), (1, 0)):
            nnr, nnc = nr + dr, c + dc      # 아랫쪽 칸 좌표
            if nnr > (R+2):     # 맨 마지막 행 / 아랫쪽 칸이 빈 칸이 아님 -> 중앙이 내려오면 안됨
                return nr - 1, c

            if arr[nnr][nnc] != 0:
                return nr - 1, c
    return -1                               # 예외 처리 필요


def left(r, c, d):
    # 골렘 위치 / 출구 방향
    cur_r, cur_c, cur_d = r, c, d
    for _ in range(C*2):
        nc = cur_c - 1          # 중앙 왼쪽 이동
        # 조건 확인: 왼쪽 3칸이 빈 칸인지 체크
        for dr, dc in ((-1, 0), (0, -1), (1, 0)):
            nnr, nnc = cur_r + dr, nc + dc
            if nnc < 1:                 # 범위 벗어나면 더 이상 이동하면 안됨
                return cur_r, cur_c, cur_d
            if arr[nnr][nnc] != 0:      # 빈 칸이 아니면 가면 안됨
                return cur_r, cur_c, cur_d

        # 3 칸 모두 빈 칸인 경우 ) 아래로 한 칸 내리기
        nr = cur_r + 1
        for dr, dc in ((0, -1), (1, 0)):
            nnr, nnc = nr + dr, nc + dc
            if nnr > R + 2:
                return cur_r, cur_c, cur_d
            if arr[nnr][nnc] != 0:
                return cur_r, cur_c, cur_d

        # 2 칸 모두 빈 칸인 경우 ) 내려갈 수 있음 -> 중앙 내리기, 출구 회전
        cur_r, cur_c, cur_d = nr, nc, (cur_d+3) % 4
    return -1       # 예외 처리


def right(r, c, d):
    # 골렘 위치 / 출구 방향
    cur_r, cur_c, cur_d = r, c, d
    for _ in range(C*2):
        nc = cur_c + 1          # 중앙 오른쪽 이동
        # 조건 확인: 왼쪽 3칸이 빈 칸인지 체크
        for dr, dc in ((1, 0), (0, 1), (-1, 0)):
            nnr, nnc = cur_r + dr, nc + dc
            if nnc > C:                 # 범위 벗어나면 더 이상 이동하면 안됨
                return cur_r, cur_c, cur_d
            if arr[nnr][nnc] != 0:      # 빈 칸이 아니면 가면 안됨
                return cur_r, cur_c, cur_d

        # 3 칸 모두 빈 칸인 경우 ) 아래로 한 칸 내리기
        nr = cur_r + 1
        for dr, dc in ((1, 0), (0, -1)):
            nnr, nnc = nr + dr, nc + dc
            if nnr > R + 2:
                return cur_r, cur_c, cur_d
            if arr[nnr][nnc] != 0:
                return cur_r, cur_c, cur_d

        # 2 칸 모두 빈 칸인 경우 ) 내려갈 수 있음 -> 중앙 내리기, 출구 회전
        cur_r, cur_c, cur_d = nr, nc, (cur_d+1) % 4
    return -1       # 예외 처리


def bfs(sx, sy):
    v = [[False] * (C+2) for _ in range(R+3)]
    q = deque()
    v[sx][sy] = True
    q.append((sx, sy))

    while q:
        cx, cy = q.popleft()

        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if 3 <= nx <= R + 2 and 0 < ny <= C:
                if not v[nx][ny] and arr[nx][ny] != 0:
                    # 현재 칸이 출구 칸이면 아뭍따 이동 가능
                    if arr[cx][cy] < 0:
                        v[nx][ny] = True
                        q.append((nx, ny))
                    # 현재 칸이 출구 칸이 아니면 자기 골룸 내 이동 가능 / 다른 골렘 x
                    elif arr[cx][cy] > 0:
                        if abs(arr[nx][ny]) == abs(arr[cx][cy]):
                            v[nx][ny] = True
                            q.append((nx, ny))

    for i in range(R+2, -1, -1):
        for j in range(1, C+1):
            if v[i][j]:
                return i

    return -1           # 예외 처리




result = 0
for idx, (ci, di) in enumerate(orders):
    # [1] 숲 탐색: 아래 / 왼 / 오
    down_r, down_c = down(ci)
    left_r, left_c, left_d = left(down_r, down_c, di)
    right_r, right_c, right_d = right(left_r, left_c, left_d)

    # RESET 조건 ) 골렘의 몸 일부가 벗어난 상태 -> 배열 비우고, 다음 골렘으로 넘어감
    if right_r < 4:
        arr = [[0] * (C+2) for _ in range(R+3)]
        continue

    # [2] 정령 이동
    # [2-1] 골렘 표시하기 / 상하좌우
    arr[right_r][right_c] = (idx+1)
    for d in range(4):
        # 출구이면 - 붙여서 표기
        nr, nc = right_r + dx[d], right_c + dy[d]
        if d == right_d:
            arr[nr][nc] = -(idx+1)
        else:
            arr[nr][nc] = (idx+1)

    # [2-2] bfs로 가장 낮은 위치 찾기

    depth = bfs(right_r, right_c)
    result += (depth - 2)

print(result)