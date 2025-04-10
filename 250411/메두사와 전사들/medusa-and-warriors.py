from collections import deque

N, M = map(int, input().split())
sr, sc, er, ec = map(int, input().split())
temp = list(map(int, input().split()))
men = []
for i in range(0, len(temp)-1, 2):
    men.append((temp[i], temp[i+1]))
arr = []
for _ in range(N):
    arr.append(list(map(int, input().split())))

dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 1, 1, 1, 0, -1, -1, -1]


def in_range(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    else:
        return True


def bfs(si, sj, ei, ej):
    v = [[0] * N for _ in range(N)]
    q = deque()
    v[si][sj] = 1
    q.append((si, sj, [(si, sj)]))

    while q:
        ci, cj, path = q.popleft()

        if (ci, cj) == (ei, ej):
            path.pop(0)
            return path

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci + di, cj + dj
            # 범위 체크
            if not in_range(ni, nj):
                continue
            if v[ni][nj]:
                continue
            # 조건: 도로만 지나갈 수 있음
            if arr[ni][nj] == 0:
                q.append((ni, nj, path + [(ni, nj)]))
                v[ni][nj] = 1
    return -1           # 예외 처리


def down(v, si, sj, sd):
    # sd 방향으로 계속 아래로 내리면서 표시하면 됨
    # 전사 만나면 2로 표시 / 그 다음 칸부터 가지 xxx
    rock = []
    # for mul in range(1, N+1):
    for mul in range(N):

        ni, nj = si + dr[sd] * mul, sj + dc[sd] * mul
        if in_range(ni, nj) and in_range(ni-dr[sd], nj-dc[sd]):
            if v[ni-dr[sd]][nj-dc[sd]] == 2 or v[ni-dr[sd]][nj-dc[sd]] == 3:
                v[ni][nj] = 3

            elif (ni, nj) in men and v[ni][nj] == 0:     # 전사 만난 경우 => 2 표시, break
                v[ni][nj] = 2
                rock.append((ni, nj))

            elif v[ni][nj] == 0:                   # 전사 없음 => 1 표시
                v[ni][nj] = 1
    return v, rock

# ===========================================
def sight(si, sj, sd):
    v = [[0] * N for _ in range(N)]
    sum_rock = 0

    # 직선 => sd 방향으로 쭉 내려가면 됨
    v, temp_rock = down(v, si, sj, sd)
    if temp_rock:
        sum_rock += men.count((temp_rock[0][0], temp_rock[0][1]))

    # 진행 방향 기준 왼쪽 이동 => 기준 위치 바꾸고 down
    di, dj = dr[sd-1], dc[sd-1]
    for mul in range(1, N+1):
        ni, nj = si + di * mul, sj + dj * mul
        # 범위 체크
        if not in_range(ni, nj):
            break

        v, temp_rock = down(v, ni, nj, sd)
        # 돌이 되는 위치 있는 경우 ) safe 표시
        if temp_rock:
            ti, tj = temp_rock[0][0], temp_rock[0][1]
            for mmul in range(1, N + 1):
                ni, nj = ti + di * mmul, tj + dj * mmul
                # 범위 체크
                if not in_range(ni, nj):
                    break
                v[ni][nj] = 3
                v, _ = down(v, ni, nj, sd)
        if temp_rock:
            sum_rock += men.count((temp_rock[0][0], temp_rock[0][1]))

    # 진행 방향 기준 오른쪽 이동 => 기준 위치 바꾸고 down
    di, dj = dr[sd+1], dc[sd+1]
    for mul in range(1, N+1):
        ni, nj = si + di * mul, sj + dj * mul
        # 범위 체크
        if not in_range(ni, nj):
            break

        v, temp_rock = down(v, ni, nj, sd)
        # 돌이 되는 위치 있는 경우 ) safe 표시
        if temp_rock:
            ti, tj = temp_rock[0][0], temp_rock[0][1]
            for mmul in range(1, N + 1):
                ni, nj = ti + di * mmul, tj + dj * mmul
                # 범위 체크
                if not in_range(ni, nj):
                    break
                v[ni][nj] = 3
                v, _ = down(v, ni, nj, sd)
        if temp_rock:
            sum_rock += men.count((temp_rock[0][0], temp_rock[0][1]))
    v[si][sj] = 0
    return sum_rock, v
# =================================================



def manhattan(si, sj, ei, ej):
    return abs(si-ei) + abs(sj-ej)


# 메두사의 이동 경로 구해두기 (맵이 변하지 않기 때문에 한 번만 구하면 됨)
mpath = bfs(sr, sc, er, ec)


while True:
    # 출력: 모든 전사가 이동한 거리의 합 / 돌이 된 전사의 수 / 공격한 전사의 수
    men_dist, men_rock, men_attack = 0, 0, 0

    # [0] 메두사가 공원으로 이동 불가능 => -1
    if mpath == -1:
        print(-1)
        break

    # [1] 메두사 한 칸 이동 / 전사 있을 경우 => 전사 없어짐
    sr, sc = mpath.pop(0)
    for i in range(len(men)-1, -1, -1):
        if men[i] == (sr, sc):
            men.pop(i)

    # 종료 조건: 메두사가 공원에 도착
    if (sr, sc) == (er, ec):
        print(0)
        break

    # [2] 메두사의 시선
    mx_rock = -1        # 예외 처리 필요
    marr = []

    # [2-1] 상 하 좌 우 우선순위로 / 돌이 되는 전사의 수 & v 출력
    for md in (0, 4, 6, 2):
        t_rock, tarr = sight(sr, sc, md)
        if t_rock > mx_rock:
            mx_rock = t_rock
            marr = tarr
    men_rock = mx_rock

    # [3] 전사 이동
    if men:
        # [3-1] 첫번째 이동 : 메두사와 거리 감소 / 상하좌우 우선순위 / 1 이 아닌 곳 o
        for idx in range(len(men)):
            move = 0
            mi, mj = men[idx]
            if marr[mi][mj] == 2:
                continue
            cur_dist = manhattan(mi, mj, sr, sc)
            for md in (0, 4, 6, 2):
                nmi, nmj = mi + dr[md], mj + dc[md]
                if in_range(nmi, nmj):
                    if marr[nmi][nmj] != 1 and marr[nmi][nmj] != 2:
                        nxt_dist = manhattan(nmi, nmj, sr, sc)
                        if cur_dist > nxt_dist:
                            # cur_dist = nxt_dist
                            men[idx] = (nmi, nmj)
                            break
            if (mi, mj) != (men[idx]):
                mi, mj = men[idx]
                move += 1

            # [3-2] 두번째 이동
            if move:
                cur_dist = manhattan(mi, mj, sr, sc)
                for md in (6, 2, 0, 4):
                    nmi, nmj = mi + dr[md], mj + dc[md]
                    if in_range(nmi, nmj):
                        if marr[nmi][nmj] != 1 and marr[nmi][nmj] != 2:
                            nxt_dist = manhattan(nmi, nmj, sr, sc)
                            if cur_dist > nxt_dist:
                                # cur_dist = nxt_dist
                                men[idx] = (nmi, nmj)
                                break
                if (mi, mj) != (men[idx]):
                    mi, mj = men[idx]
                    move += 1
            men_dist += move


    # [4] 전사의 공격
    if men:
        # 메두사 위치 == 전사 위치 ) 없앰
        for idx in range(len(men)-1, -1, -1):
            if men[idx] == (sr, sc):
                men.pop(idx)
                men_attack += 1

    print(men_dist, men_rock, men_attack)
