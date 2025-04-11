N, M, K = map(int, input().split())
arr = []
for _ in range(N):
    arr.append([[a] for a in list(map(int, input().split()))])
for i in range(N):
    for j in range(N):
        if arr[i][j] == [0]:
            arr[i][j] = []

# 총의 위치 x, y, 방향, 초기 능력치, 총
units = {}
men = [[0] * N for _ in range(N)]
for m in range(1, M+1):
    x, y, d, s = map(int, input().split())
    units[m] = [x-1, y-1, d, s, 0]
    men[x-1][y-1] = m

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


# leave(lose, ni, nj, ld, ls, lg)
def leave(idx, i, j, d, s, g):
    for p in range(4):
        ni, nj = i + dx[(d+p)%4], j + dy[(d+p)%4]
        if 0 <= ni < N and 0 <= nj < N:
            if not men[ni][nj]:
                # 여기로 이동
                # 총이 있으면 획득
                if len(arr[ni][nj]) > 0:
                    mx = max(arr[ni][nj])
                    arr[ni][nj].remove(mx)
                    g = mx
                men[ni][nj] = idx
                units[idx] = [ni, nj, (d+p)%4, s, g]
                return



point = [0] * (M+1)
for _ in range(K):
    for idx in units:
        ci, cj, cd, cs, cg = units[idx]
        # [1-1] 한 칸 이동 / 격자 벗어나면 정반대, 1칸 이동
        ni, nj = ci + dx[cd], cj + dy[cd]
        if ni < 0 or ni >= N or nj < 0 or nj >= N:
            cd = (cd+2) % 4
            ni, nj = ci + dx[cd], cj + dy[cd]
        men[ci][cj] = 0

        # [2-1] 플레이어가 없다면 => 총 획득
        if men[ni][nj] == 0:
            if len(arr[ni][nj]) > 0:         # 총이 있으면 교체 / 획득
                mx_gun = max(arr[ni][nj])
                if mx_gun > cg:
                    if cg > 0:
                        arr[ni][nj].append(cg)
                    arr[ni][nj].remove(mx_gun)
                    cg = mx_gun
            men[ni][nj] = idx
            units[idx] = [ni, nj, cd, cs, cg]

        # [2-2-1] 플레이어가 있는 경우 => 점수 획득
        else:
            t = men[ni][nj]
            ti, tj, td, ts, tg = units[t]

            if cs+cg>ts+tg or (cs+cg==ts+tg and cs>ts):
                point[idx] += (cg+cs)-(tg+ts)
                leave(t, ni, nj, td, ts, 0)

                if cg<tg:
                    if cg>0:
                        arr[ni][nj].append(cg)
                    cg = tg
                else:
                    if tg>0:
                        arr[ni][nj].append(tg)
                men[ni][nj] = idx
                units[idx] = [ni, nj, cd, cs, cg]
            else:
                point[t] += (tg+ts)-(cg+cs)
                leave(idx, ni, nj, cd, cs, 0)

                if tg<cg:
                    if tg>0:
                        arr[ni][nj].append(tg)
                    tg = cg
                else:
                    if cg>0:
                        arr[ni][nj].append(cg)
                men[ni][nj] = t
                units[t] = [ni, nj, td, ts, tg]

point.pop(0)
print(*point)