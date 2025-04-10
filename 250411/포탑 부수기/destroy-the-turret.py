# 포탑 뿌수기

from collections import deque

N, M, K = map(int, input().split())
arr = []
for _ in range(N):
    arr.append(list(map(int, input().split())))

init_dead = 0
for i in range(N):
    init_dead += arr[i].count(0)

dx = [0, 1, 1, 1, 0, -1, -1, -1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

# 몇 번째 턴에 공격했는지 기록
attack = [[0] * M for _ in range(N)]


# razor_path = bfs(ax, ay, ex, ey)
def bfs(sx, sy, ex, ey):
    v = [[False] * M for _ in range(N)]
    v[sx][sy] = True
    q = deque()
    q.append((sx, sy, [(sx, sy)]))

    while q:
        x, y, path = q.popleft()

        if (x, y) == (ex, ey):
            path.pop(0)         # 시작 위치 빼기
            return path

        for i in (0, 2, 4, 6):
            nx, ny = (x + dx[i]) % N, (y + dy[i]) % M
            # 부셔진 포탑 자리는 지나가면 안됨
            if arr[nx][ny] == 0:
                continue
            if v[nx][ny]:
                continue
            q.append((nx, ny, path + [(nx, ny)]))
            v[nx][ny] = True
    return []


result = 0

for kturn in range(K+1):
    visited = [[False] * M for _ in range(N)]

    # [1] 공격자 선정
    mn_power = 5001
    mn_attack = -1
    ax, ay = 11, 11             # 예외 처리
    for i in range(N):
        for j in range(M):
            if arr[i][j] == 0:                   # 부셔진 포탑이면 패스
                continue
            if arr[i][j] < mn_power:             # 공격력 가장 낮은 포탑
                mn_power = arr[i][j]
                mn_attack = attack[i][j]
                ax, ay = i, j
            elif arr[i][j] == mn_power:          # 가장 최근에 공격한 포탑
                if mn_attack < attack[i][j]:
                    mn_attack = attack[i][j]
                    ax, ay = i, j
                elif mn_attack == attack[i][j]:  # 행과 열의 합이 가장 큰 포탑
                    if ax+ay < i+j:
                        ax, ay = i, j
                    elif ax+ay == i+j:           # 열이 가장 큰 포탑
                        if ay < j:
                            ax, ay = i, j
    # [1-1] 공격자 공격력 증가
    arr[ax][ay] += (N+M)
    mn_power = arr[ax][ay]
    visited[ax][ay] = True
    attack[ax][ay] = (kturn+1)

    # [2] 피공격자 정하기
    mx_power = -1
    mx_attack = 1002
    ex, ey = 11, 11
    for i in range(N):
        for j in range(M):
            if arr[i][j] == 0 or (i, j) == (ax, ay):    # 부셔진 포탑이거나 공격자면 패스
                continue
            if arr[i][j] > mx_power:                    # 공격력 가장 높은 포탑
                mx_power = arr[i][j]
                mx_attack = attack[i][j]
                ex, ey = i, j
            elif arr[i][j] == mx_power:                 # 가장 이전에 공격한 포탑 (수가 작을 때)
                if mx_attack > attack[i][j]:
                    mx_attack = attack[i][j]
                    ex, ey = i, j
                elif mx_attack == attack[i][j]:         # 행과 열의 합이 가장 작은 포탑
                    if ex+ey > i+j:
                        ex, ey = i, j
                    elif ex+ey == i+j:                  # 열이 가장 작은 포탑
                        if ey > j:
                            ex, ey = i, j
    visited[ex][ey] = True

    # K+1번째 턴이면 가장 강한 포탑 저장하고 끝
    if kturn == K:
        result = arr[ex][ey]
        break

    # [3] 공격
    # [3-1] 레이저 공격
    razor_path = bfs(ax, ay, ex, ey)
    if razor_path:
        for rx, ry in razor_path:
            visited[rx][ry] = True
            if (rx, ry) == (ex, ey):                # 공격 위치일 때
                if arr[rx][ry] > mn_power:
                    arr[rx][ry] -= mn_power
                else:
                    arr[rx][ry] = 0
                    init_dead += 1
            else:                                   # 이동 경로 상의 포탑일 때
                if arr[rx][ry] > mn_power // 2:
                    arr[rx][ry] -= mn_power // 2
                else:
                    arr[rx][ry] = 0
                    init_dead += 1

    # [3-2] 포탄 공격 => 레이저 공격 안되면
    else:
        for i in range(8):
            # =================================
            # 여기 약간 싸한데

            nx, ny = (ex + dx[i]) % N, (ey + dy[i]) % M
            visited[nx][ny] = True

            if arr[nx][ny] == 0:
                continue

            if (nx, ny) == (ax, ay):
                continue

            if arr[nx][ny] > mn_power // 2:
                arr[nx][ny] -= mn_power // 2
            else:
                arr[nx][ny] = 0
                init_dead += 1

            # =================================
        if arr[ex][ey] > mn_power:
            arr[ex][ey] -= mn_power
        else:
            arr[ex][ey] = 0
            init_dead += 1

    # 종료 조건: 공격력 남은 포탑이 1개면 멈춤
    if init_dead == N*M-1:
        result = max([max(a) for a in arr])
        break

    # [4] 포탑 정비
    # 방문하지 않은 좌표에 대해서 공격력 +1
    for i in range(N):
        for j in range(M):
            if arr[i][j] != 0 and not visited[i][j]:
                arr[i][j] += 1

print(result)
