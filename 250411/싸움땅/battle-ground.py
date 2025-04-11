# 싸움땅

N, M, K = map(int, input().split())
arr = []
for _ in range(N):
    arr.append([[a] for a in list(map(int, input().split()))])

v = [[False] * N for _ in range(N)]

# x, y, d, s
units = {}
for m in range(1, M+1):
    x, y, d, s = map(int, input().split())
    units[m] = [x-1, y-1, d, s]
    v[x-1][y-1] = True

# 초기 체력 저장
init_power = [0]
for idx in range(1, M+1):
    init_power.append(units[idx][3])

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def in_range(i, j):
    if i < 0 or i >= N or j < 0 or j >= N:
        return False
    else:
        return True


# nx, ny, nd = move(idx)
def move(idx):
    si, sj, sd, _ = units[idx]
    ni, nj = si + dx[sd], sj + dy[sd]
    if in_range(ni, nj):
        return ni, nj, sd
    else:       # 범위 벗어날 때
        nd = (sd + 2) % 4
        ni, nj = si + dx[nd], sj + dy[nd]
        return ni, nj, nd


# lose_x, lose_y, lose_d = lose_move(lose)
def lose_move(idx):
    si, sj, sd, _ = units[idx]
    ni, nj = si + dx[sd], sj + dy[sd]

    # 다른 플레이어가 있거나 / 격자 범위 밖인 경우 => 90도 회전, 빈 칸이 보이면 이동

    if in_range(ni, nj):
        if v[ni][nj]:
            for plus in range(1, 4):
                ni, nj = si + dx[(sd + plus) % 4], sj + dy[(sd + plus) % 4]
                if not v[ni][nj]:
                    v[ni][nj] = True
                    return ni, nj, (sd + plus) % 4
        else:
            return ni, nj, sd
    else:
        for plus in range(1, 4):
            ni, nj = si + dx[(sd + plus) % 4], sj + dy[(sd + plus) % 4]
            if not v[ni][nj]:
                v[ni][nj] = True
                return ni, nj, (sd + plus) % 4
                return ni, nj, (sd+plus)%4


def get_gun(idx):
    # 이미 총을 가지고 있는 상태 => 칸의 총들 + 내 총 비교 후 고르기
    # 총이 없는 상태 => 칸의 총들 비교 후 고르기
    # units 업데이트 => init_power + 고른 총 공격력

    ci, cj, cd, cs = units[idx]

    if arr[ci][cj] == [0]:          # 현재 칸에 총이 없음 => 바로 종료
        return

    else:
        compares = []
        if cs > init_power[idx]:    # 이미 총을 가지고 있는 상태
            compares.append(cs-init_power[idx])

        for gun in arr[ci][cj]:
            compares.append(gun)

        if len(compares) == 1:
            units[idx] = [ci, cj, cd, init_power[idx]+compares[0]]
            arr[ci][cj] = [0]
        else:
            mx_gun = max(compares)
            units[idx] = [ci, cj, cd, init_power[idx]+mx_gun]
            compares.remove(mx_gun)
            arr[ci][cj] = compares

            # arr[ci][cj].remove(mx_gun)
    return


point = [0] * (M+1)
for _ in range(K):
    # [1] 한 칸 이동
    for idx in units:
        ux, uy, ud, us = units[idx]
        nx, ny, nd = move(idx)

        v[ux][uy] = False
        v[nx][ny] = True

        flag = False
        for tidx in units:
            tx, ty, td, ts = units[tidx]
            if (tx, ty) == (nx, ny) and tidx != idx:        # 이동한 칸에 다른 플레이어 있는 경우
                flag = True
                if ts != us:                # 총 공격력이 큰 놈이 이김
                    win = tidx if ts > us else idx
                    lose = idx if win == tidx else tidx
                else:       # 총 공격력이 같은 경우 => 초기 능력치 비교
                    win = tidx if init_power[tidx] > init_power[idx] else idx
                    lose = idx if win == tidx else tidx
                point[win] += abs(ts-us)     # 총 공격력 차이만큼 포인트 획득

                # 진 플레이어 이동 및 총 선택:
                # 총 내려놓기
                if units[lose][3] > init_power[lose]:
                    if arr[nx][ny] == [0]:
                        arr[nx][ny] = [abs(init_power[lose]-units[lose][3])]
                    else:
                        arr[nx][ny].append(abs(init_power[lose]-units[lose][3]))

                units[lose] = [nx, ny, units[lose][2], units[lose][3]]
                lose_x, lose_y, lose_d = lose_move(lose)
                v[lose_x][lose_y] = True
                units[lose] = [lose_x, lose_y, lose_d, init_power[lose]]
                get_gun(lose)

                # 이긴 플레이어 이동 및 총 선택:
                units[win] = [nx, ny, units[win][2], units[win][3]]
                get_gun(win)

        if not flag:        # 싸움 안 함
            units[idx] = [nx, ny, nd, us]
            get_gun(idx)

point.pop(0)
print(*point)