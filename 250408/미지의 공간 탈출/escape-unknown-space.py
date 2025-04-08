# 미지의 공간 탈출

from collections import deque

N, M, F = map(int, input().split())
space = []
for _ in range(N):
    space.append(list(map(int, input().split())))

# 동 서 남 북 윗면
wall = []
for _ in range(5):
    temp = []
    for _ in range(M):
        temp.append(list(map(int, input().split())))
    wall.append(temp)

eff = []
for _ in range(F):
   eff.append(list(map(int, input().split())))


def find_3d_start():
    for i in range(M):
        for j in range(M):
            if wall[4][i][j] == 2:
                # 타임 머신 위치 반환
                return 4, i, j


def find_2d_end():
    for i in range(N):
        for j in range(N):
            if space[i][j] == 4:
                return i, j


def find_wall_2d():
    for i in range(N):
        for j in range(N):
            if space[i][j] == 3:
                return i, j


def find_exit_3d_2d():
    # 2d에서 시간의 벽 위치 찾기 / 2d bfs 시작점
    wi, wj = find_wall_2d()
    si_2d, sj_2d = 20, 20
    for i in range(wi - 1, wi + M + 1):
        for j in range(wj - 1, wj + M + 1):
            if space[i][j] == 0:
                si_2d, sj_2d = i, j

    # 3d에서 시간의 벽 위치 찾기 / 3d bfs 끝나는 점 / k, x, y 알아야 함
    ek_3d, ei_3d, ej_3d = 5, 20, 20
    if sj_2d == wj + M:     # 동쪽인 경우
        ek_3d = 0
        ei_3d, ej_3d = M - 1, (wi + M - 1) - si_2d
    elif sj_2d == wj - 1:
        ek_3d = 1
        ei_3d, ej_3d = M - 1, si_2d - wi
    elif si_2d == wi + M:
        ek_3d = 2
        ei_3d, ej_3d = M - 1, sj_2d - wj
    else:
        ek_3d = 3
        ei_3d, ej_3d = M - 1, (wj + M - 1) - sj_2d

    return si_2d, sj_2d, ek_3d, ei_3d, ej_3d


def bfs_3d(sk, sx, sy, ek, ex, ey):
    left = {0: 2, 1: 3, 2: 1, 3: 0}
    right = {0: 3, 1: 2, 2: 0, 3: 1}

    v = [[[0] * M for _ in range(M)] for _ in range(5)]
    q = deque()
    v[sk][sx][sy] = 1
    q.append((sk, sx, sy))

    while q:
        ck, cx, cy = q.popleft()

        # 종료 조건: end 위치에 도달
        if (ck, cx, cy) == (ek, ex, ey):
            return v[ck][cx][cy]

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nk, nx, ny = ck, cx + dx, cy + dy

            # 범위 벗어나는 경우
            if nx < 0:          # 위로 벗어날 때
                if ck == 0:
                    nk, nx, ny = 4, M-1-cy, M-1
                elif ck == 1:
                    nk, nx, ny = 4, cy, 0
                elif ck == 2:
                    nk, nx, ny = 4, M-1, cy
                elif ck == 3:
                    nk, nx, ny = 4, 0, M-1-cy
                else:
                    nk, nx, ny = 3, 0, M-1-cy

            elif nx >= M:         # 아래로 벗어날 때
                if ck == 4:
                    nk, nx, ny = 2, 0, cy
                else:
                    # 윗면 제외, 아래로 벗어날 수 없음
                    continue

            elif ny < 0:          # 왼쪽으로 벗어날 때
                if ck == 4:
                    nk, nx, ny = 1, 0, cx
                else:
                    nk, nx, ny = left[ck], cx, M-1

            elif ny >= M:           # 오른쪽으로 벗어날 때
                if ck == 4:
                    nk, nx, ny = 0, 0, M-1-cx
                else:
                    nk, nx, ny = right[ck], cx, 0

            # bfs 실행
            if not v[nk][nx][ny] and wall[nk][nx][ny] == 0:
                v[nk][nx][ny] = v[ck][cx][cy] + 1
                q.append((nk, nx, ny))

    # end 위치에 도달하지 못하면
    return -1


def bfs_2d(sx, sy, ex, ey, d_3d):
    v = [[0] * N for _ in range(N)]
    q = deque()
    v[sx][sy] = d_3d
    q.append((sx, sy))

    while q:
        cx, cy = q.popleft()
        if (cx, cy) == (ex, ey):
            return v[cx][cy]

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < N and 0 <= ny < N:
                if not v[nx][ny] and space[nx][ny] > v[cx][cy] + 1 > 1:
                    v[nx][ny] = v[cx][cy] + 1
                    q.append((nx, ny))
    return -1


# 각종 위치 찾기 > 타임 머신 위치, 시간의 벽 출구(3d, 2d), 탈출구
sk_3d, sx_3d, sy_3d = find_3d_start()
ex_2d, ey_2d = find_2d_end()
sx_2d, sy_2d, ek_3d, ex_3d, ey_3d = find_exit_3d_2d()

# 3d bfs 실행
dist_3d = bfs_3d(sk_3d, sx_3d, sy_3d, ek_3d, ex_3d, ey_3d)

# 시간 이상 현상 확산 시키기
for i in range(N):
    for j in range(N):
        if space[i][j] == 0:
            space[i][j] = 401
        if space[i][j] == 3:
            space[i][j] = 1
        if space[i][j] == 4:
            space[i][j] = 401

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

for sr, sc, d, v in eff:
    space[sr][sc] = 1

    for mul in range(1, 22):
        nr, nc = sr + dx[d] * mul, sc + dy[d] * mul
        if nr < 0 or nr >= N or nc < 0 or nc >= N:
            break

        if space[nr][nc] == 1:
            break

        if space[nr][nc] == 401:
            space[nr][nc] = v * mul

# 2d bfs 실행
dist_2d = bfs_2d(sx_2d, sy_2d, ex_2d, ey_2d, dist_3d)
print(dist_2d)