# 루돌프의 반란

N, M, P, C, D = map(int, input().split())
# 루돌프 위치
ri, rj = map(int, input().split())

# 위치 x, y, 포인트
arr = [[0] * (N+2) for _ in range(N+2)]
santa = {}
for _ in range(P):
    pn, sr, sc = map(int, input().split())
    santa[pn] = [sr, sc]
    arr[sr][sc] = pn

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]


def in_range(x, y):
    if x < 1 or x > N or y < 1 or y > N:
        return False
    else:
        return True


def distance(x1, y1, x2, y2):
    return (x1-x2)**2 + (y1-y2)**2


# def dfs(v, sx, sy, sd):
#     nx, ny = sx + dx[sd], sy + dy[sd]
#     ns = arr[sx][sy]
#
#     if in_range(nx, ny):
#         if arr[nx][ny] > 0:
#             v[nx][ny] = ns
#             santa[ns] = [nx, ny]
#             return dfs(v, nx, ny, sd)
#         else:
#             return v
#
#     else:
#         if arr[sx][sy] > 0:
#             dead = arr[sx][sy]
#             santa.pop(dead)
#         return v


def dfs(v, sx, sy, sd):
    nx, ny = sx + dx[sd], sy + dy[sd]
    ns = arr[sx][sy]
    if not in_range(nx, ny):
        if arr[sx][sy] > 0:
            dead = arr[sx][sy]
            santa.pop(dead)
        return v

    v[nx][ny] = ns
    santa[ns] = [nx, ny]

    if arr[nx][ny] > 0:
        return dfs(v, nx, ny, sd)
    else:
        return v




def collide(sx, sy, sd, n, push):
    global arr

    point[push] += n
    arr[sx][sy] = 0
    tset = set()

    # 밀려난 산타 위치 (narr, santa) 업데이트 / 기절 산타 업데이트
    x, y = sx + dx[sd] * n, sy + dy[sd] * n
    if not in_range(x, y):              # 격자 밖으로 나감
        santa.pop(push)
    else:
        if arr[x][y] != 0:
            narr = [a[:] for a in arr]
            arr = dfs(narr, x, y, sd)       # 새로운 arr로 업데이트
        arr[x][y] = push
        santa[push] = [x, y]
        tset.add(push)
    return tset


point = [0] * (P+1)     # 점수 기록용
stset = set()       # 기절한 산타 번호 기록
for _ in range(M):
    # [0] 산타 위치 정렬하기
    temp = sorted(santa.items(), key=lambda x: x[1][1], reverse=True)
    temp.sort(key=lambda x: x[1][0], reverse=True)
    santa = {x[0]: x[1] for x in temp}

    n_stset = set()     # 다음 턴을 위한 기절 산타 기록

    # [1] 루돌프 움직이기: 모든 산타와 거리 비교
    mn_dist = 2501
    mn_santa = 31
    ei, ej = 51, 51
    for idx in santa:
        si, sj = santa[idx]
        dist = distance(si, sj, ri, rj)
        if mn_dist > dist:
            mn_dist = dist
            mn_santa = idx
            ei, ej = si, sj

    # [1-1] 루돌프 한 칸 이동
    nxt_dist = 2501
    nri, nrj = 51, 51           # 새로운 루돌프 위치
    rd = 9                     # 루돌프 이동해온 방향 기록
    for idx in range(8):
        ni, nj = ri + dx[idx], rj + dy[idx]
        if in_range(ni, nj):
            dist = distance(ei, ej, ni, nj)
            if dist < nxt_dist:
                nxt_dist = dist
                nri, nrj, rd = ni, nj, idx
    ri, rj = nri, nrj

    # [3] 충돌 (루돌프 -> 산타)
    if arr[ri][rj] > 0:
        # 새로운 루돌프 위치에 산타가 있으면 충돌
        rset = collide(ri, rj, rd, C, arr[ri][rj])
        n_stset = n_stset.union(rset)

    # [2] 산타의 움직임 => 같은 산타가 있는 칸으로 못감 (arr 업뎃 필요)
    for idx in range(1, P+1):
        if idx in stset:        # 기절한 산타이면 넘어감
            continue
        if idx in n_stset:
            continue
        if not idx in santa:
            continue

        si, sj = santa[idx]
        arr[si][sj] = 0                 # 현재 위치에서 표시 없애기
        cur_dist = distance(si, sj, ri, rj)
        nsi, nsj, sd = si, sj, 9
        for i in (0, 2, 4, 6):          # 상 우 하 좌 우선순위
            ni, nj = si + dx[i], sj + dy[i]
            if not in_range(ni, nj):    # 범위 내
                continue
            if arr[ni][nj]:             # 이 칸에 다른 산타 있으면 xxx
                continue
            dist = distance(ni, nj, ri, rj)
            if cur_dist > dist:         # 이전 위치보다 더 가까워져야 이동함
                cur_dist = dist
                nsi, nsj = ni, nj
                sd = i

        # [3] 충돌 (산타 -> 루돌프)
        if (nsi, nsj) == (ri, rj) and sd < 9:      # 충돌 시, 산타 위치 다시 바뀜
            sset = collide(nsi, nsj, (sd+4)%8, D, idx)
            n_stset = n_stset.union(sset)
        else:                           # 충돌 x, 산타 위치 여기서 고정
            arr[nsi][nsj] = idx
            santa[idx] = [nsi, nsj]

    stset = n_stset

    # 종료 조건: 모든 산타 탈락
    if not santa:
        break

    # 탈락 하지 않은 산타에게 1점 추가
    for idx in santa:
        point[idx] += 1

point.pop(0)
print(*point)