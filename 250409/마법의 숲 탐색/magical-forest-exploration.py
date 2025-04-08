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


def can_go_down(cr, cc):
    cr, cc = cr + 1, cc
    flag = True
    for dr, dc in ((1, 0), (0, -1), (0, 1)):
        nr, nc = cr + dr, cc + dc
        if nr > R + 2:          # 범위 초과
            flag = False
            continue
        if arr[nr][nc] != 0:    # 빈 칸이 아닐 때
            flag = False
    return flag


def can_go_left(cr, cc):
    flag = True
    for dr, dc in ((-1, -1), (0, -2), (1, -1), (1, -2), (2, -1)):
        nr, nc = cr + dr, cc + dc
        if nr > R + 2 or nc < 1:
            flag = False
            continue
        if arr[nr][nc] != 0:
            flag = False
    return flag


def can_go_right(cr, cc):
    flag = True
    for dr, dc in ((-1, 1), (0, 2), (1, 1), (1, 2), (2, 1)):
        nr, nc = cr + dr, cc + dc
        if nr > R + 2 or nc > C:
            flag = False
            continue
        if arr[nr][nc] != 0:
            flag = False
    return flag


def down(sr, sc, sd):
    # 아래로 한 칸
    if can_go_down(sr, sc):
        return down(sr+1, sc, sd)
    # 왼쪽 회전 아래로 한 칸
    elif can_go_left(sr, sc):
        return down(sr+1, sc-1, (sd+3)%4)
    # 오른쪽 회전 아래로 한 칸
    elif can_go_right(sr, sc):
        return down(sr+1, sc+1, (sd+1)%4)
    else:       # 더 이상 움직이지 못할 때
        return sr, sc, sd


result = 0
for idx, (ci, di) in enumerate(orders):
    # [1] 숲 탐색: 아래 / 왼 / 오 -> 반복

    tr, tc, td = down(1, ci, di)

    # RESET 조건 ) 골렘의 몸 일부가 벗어난 상태 -> 배열 비우고, 다음 골렘으로 넘어감
    if tr < 4:
        arr = [[0] * (C + 2) for _ in range(R + 3)]
        continue

    # [2] 정령 이동
    # [2-1] 골렘 표시하기 / 상하좌우
    arr[tr][tc] = (idx + 1)
    for d in range(4):
        # 출구이면 - 붙여서 표기
        nr, nc = tr + dx[d], tc + dy[d]
        if d == td:
            arr[nr][nc] = -(idx + 1)
        else:
            arr[nr][nc] = (idx + 1)

    # [2-2] bfs로 가장 낮은 위치 찾기

    depth = bfs(tr, tc)
    result += (depth - 2)

print(result)