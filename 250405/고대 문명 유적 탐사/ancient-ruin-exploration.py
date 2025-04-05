# 고대 문명 유적 탐사

from collections import deque

K, M = map(int, input().split())
ruins = []
for _ in range(5):
    ruins.append(list(map(int, input().split())))
ruin_numbers = list(map(int, input().split()))

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def in_range(x, y):
    if x < 0 or x >= 5 or y < 0 or y >= 5:
        return False
    else:
        return True


def rotate(x, y, n, u_r):
    n_r = [r[:] for r in u_r]
    ux, uy = x-1, y-1

    # 회전할 부분 0으로 만들기
    for x_i in range(x-1, x+2):
        for y_i in range(y-1, y+2):
            n_r[x_i][y_i] = 0

    # 회전
    for xx in range(3):
        for yy in range(3):
            n_r[ux+yy][uy+2-xx] = u_r[ux+xx][uy+yy]

    if n > 1:
        return rotate(x, y, n-1, n_r)

    return n_r


def bfs(x, y):
    global n_ruins, visited
    queue = deque()
    queue.append((x, y))
    visited[x][y] = True
    acquired_ruins = [(x, y)]
    now_ruin_num = n_ruins[x][y]

    while queue:
        x, y = queue.popleft()
        for d in range(4):
            nx, ny = x + dx[d], y + dy[d]
            if not in_range(nx, ny):
                continue
            if visited[nx][ny]:
                continue
            if now_ruin_num == n_ruins[nx][ny]:
                acquired_ruins.append((nx, ny))
                visited[nx][ny] = True
                queue.append((nx, ny))

    if len(acquired_ruins) < 3:
        return []
    else:
        return acquired_ruins

results = []
for _ in range(K):
    # [1] 탐사 진행
    # [1-1] 유물 1차 획득 가치 최대화 / 회전 각도 가장 작은 / 열이 가장 작은 / 행이 가장 작은
    cx, cy = 0, 0       # 회전 중심 좌표
    rotate_num = 10
    acq_ruins = 0
    result = 0
    for i in range(1, 4):
        for j in range(1, 4):
            for n in range(1, 4):
                # 3번 돌려 보면서 획득 가치 최대화
                n_ruins = rotate(i, j, n, ruins)
                visited = [[False] * 5 for _ in range(5)]
                exp_ruins = 0
                for ii in range(5):
                    for jj in range(5):
                        if not visited[ii][jj]:
                            temp = bfs(ii, jj)
                            exp_ruins += len(temp)
                # 획득 가치가 가장 클 때
                if exp_ruins > acq_ruins:
                    cx, cy = i, j
                    rotate_num = n
                    acq_ruins = exp_ruins
                # 획득 가치가 똑같을 때 ) 회전 각도가 가장 작은
                elif exp_ruins == acq_ruins:
                    if rotate_num > n:
                        cx, cy = i, j
                        rotate_num = n
                    # 회전 각도가 똑같을 때 ) 열이 가장 작은
                    elif rotate_num == n:
                        if cy > j:
                            cx, cy = i, j
                        # 열이 똑같을 때 ) 행이 가장 작은
                        elif cy == j:
                            if cx > i:
                                cx, cy = i, j
    result += acq_ruins
    # 만약 아무리 돌려도 유물을 획득할 수 없으면 멈춤
    if not acq_ruins:
        break

    # [2] 유물 조각 없애기
    n_ruins = rotate(cx, cy, rotate_num, ruins)
    visited = [[False] * 5 for _ in range(5)]
    empty_ruins = []
    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                temp = bfs(i, j)
                for tx, ty in temp:
                    empty_ruins.append((tx, ty))

    # [3] 빈 칸에 유물 채우기
    # [3-1] 열이 작고 / 행이 큰 순
    empty_ruins.sort(key=lambda e: e[0], reverse=True)
    empty_ruins.sort(key=lambda e: e[1])
    for ex, ey in empty_ruins:
        n_ruins[ex][ey] = ruin_numbers.pop(0)

    # [4] 연쇄 유물 획득: 3개 이상 연결된 유물 조각 찾기 / 없으면 다음 턴으로
    while True:
        visited = [[False] * 5 for _ in range(5)]
        empty_ruins = []
        for i in range(5):
            for j in range(5):
                if not visited[i][j]:
                    temp = bfs(i, j)
                    for tx, ty in temp:
                        empty_ruins.append((tx, ty))

        if not len(empty_ruins):
            break

        result += len(empty_ruins)

        # [3] 빈 칸에 유물 채우기
        # [3-1] 열이 작고 / 행이 큰 순
        empty_ruins.sort(key=lambda e: e[0], reverse=True)
        empty_ruins.sort(key=lambda e: e[1])
        for ex, ey in empty_ruins:
            n_ruins[ex][ey] = ruin_numbers.pop(0)

    ruins = n_ruins
    results.append(result)

print(*results)