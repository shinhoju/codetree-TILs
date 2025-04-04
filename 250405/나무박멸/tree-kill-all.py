# 2022 상반기 오후 2번. 나무 박멸
# 깊은 복사: [arr[:] for arr in a]

N, M, K, C = map(int, input().split())
trees = []
for _ in range(N):
    trees.append(list(map(int, input().split())))

# 짝수: 정방향, 홀수: 대각선
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]


def in_range(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    else:
        return True


def delete(x, y):
    global trees
    del_list = [(x, y)]
    del_sum = trees[x][y]

    for d in range(1, 8, 2):
        xx, yy = x, y
        for _ in range(K):
            nx, ny = xx + dx[d], yy + dy[d]
            if not in_range(nx, ny):
                break
            # 벽이 있거나 나무가 없는 칸 만나면 끝
            if trees[nx][ny] == -1:
                break
            if trees[nx][ny] == 0:
                del_list.append((nx, ny))
                break

            # 제초제 칸이면 무시
            if not trees[nx][ny] < -1:
                del_sum += trees[nx][ny]
            del_list.append((nx, ny))
            xx, yy = nx, ny
    return del_list, del_sum


result = 0
for _ in range(M):
    # [1] 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 성장
    n_trees = [t[:] for t in trees]
    for i in range(N):
        for j in range(N):
            if trees[i][j] > 0:
                growth = 0
                for d in range(0, 8, 2):
                    ni, nj = i + dx[d], j + dy[d]
                    if in_range(ni, nj):
                        # 나무가 있는 경우
                        if trees[ni][nj] > 0:
                            growth += 1
                n_trees[i][j] += growth
    trees = n_trees

    # [2] 4 방향 번식
    n_trees = [t[:] for t in trees]
    for i in range(N):
        for j in range(N):
            if trees[i][j] > 0:
                spread = []
                for d in range(0, 8, 2):
                    ni, nj = i + dx[d], j + dy[d]
                    if in_range(ni, nj):
                        # 벽, 나무, 제초제 없음
                        if trees[ni][nj] == -1 or trees[ni][nj] >= 1 or trees[ni][nj] <= -2:
                            continue
                        spread.append(d)
                # spread 방향 씨 뿌리기
                for s in spread:
                    si, sj = i + dx[s], j + dy[s]
                    n_trees[si][sj] += trees[i][j] // len(spread)
    trees = n_trees

    # [3-1] 제초제 뿌릴 곳 찾기
    del_trees = []
    del_trees_sum = 0
    for i in range(N):
        for j in range(N):
            if trees[i][j] > 0:
                # 박멸 나무의 수 구하기
                t_del_trees, t_del_trees_sum = delete(i, j)
                if del_trees_sum < t_del_trees_sum:
                    del_trees = t_del_trees
                    del_trees_sum = t_del_trees_sum

    # [3-2] 이전에 뿌린 제초제 수명 줄이기
    for i in range(N):
        for j in range(N):
            if trees[i][j] < -1:
                trees[i][j] += 2

    # [3-3] 제초제 뿌리기
    for di, dj in del_trees:
        trees[di][dj] = -2 * C

    # [4] 박멸한 나무 수
    result += del_trees_sum

print(result)