# 코드트리 빵

from collections import deque

N, M = map(int, input().split())
arr = [[2]*(N+2)] + [[2]+list(map(int, input().split()))+[2] for _ in range(N)] + [[2]*(N+2)]
stores = {}
for i in range(1, M+1):
    stores[i] = tuple(map(int, input().split()))


def bfs(si, sj, ei, ej):
    v = [[0] * (N+2) for _ in range(N+2)]
    q = deque()
    v[si][sj] = 1
    q.append((si, sj))

    while q:
        ci, cj = q.popleft()
        if (ci, cj) == (ei, ej):
            return v[ei][ej] - 1

        for di, dj in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            ni, nj = ci + di, cj + dj
            if ni < 1 or nj > N or nj < 1 or nj > N:
                continue
            if not v[ni][nj] and 0 <= arr[ni][nj] <= 1:
                v[ni][nj] = v[ci][cj] + 1
                q.append((ni, nj))
    return -1


t = 0
units = {}
while True:
    t += 1

    # [1] 가고 싶은 편의점 방향을 향해서 1칸 이동 / 최단 거리로 움직임
    n_arr = [a[:] for a in arr]
    del_lst = []
    for idx, (sx, sy) in units.items():
        ex, ey = stores[idx]
        min_dist = 400

        for dx, dy in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            nx, ny = sx + dx, sy + dy
            # [2] 편의점 도착이면 움직일 수 없는 칸 됨 / units에서 삭제
            if (nx, ny) == (ex, ey):
                n_arr[nx][ny] = 2
                del_lst.append(idx)
                break

            # 0, 1 일 때 이동 가능
            if 0 <= arr[nx][ny] <= 1:
                dist = bfs(nx, ny, ex, ey)
                if dist != -1 and dist < min_dist:
                    min_dist = dist
                    units[idx] = (nx, ny)

    for d_idx in del_lst:
        units.pop(d_idx)

    arr = n_arr

    # [3] 1분에 한 명씩 M 명의 사람이 베이스 캠프로 들어감 / 편의점과 가장 가까운 곳 / 못지나감
    n_arr = [a[:] for a in arr]
    if t <= M:
        ex, ey = stores[t]
        min_dist = 400
        for i in range(1, N+1):
            for j in range(1, N+1):
                if arr[i][j] == 1:
                    # 베이스 캠프와 편의점의 최단 거리 계산
                    # 한 번 쓴 베이스 캠프는 못 지나감
                    dist = bfs(i, j, ex, ey)
                    if dist != -1 and dist < min_dist:
                        min_dist = dist
                        units[t] = (i, j)
        n_arr[units[t][0]][units[t][1]] = 2
    arr = n_arr

    # 종료 조건 : 모두 편의점에 도착함
    if not units:
        break

print(t)