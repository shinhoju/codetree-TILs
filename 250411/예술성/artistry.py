"""

bfs 돌면서 그룹 번호로 arr 채움
딕셔너리에 그룹 번호 : 실제 숫자 값 저장
그룹 별 조합에 대한 예술성 계산

"""

from collections import deque

N = int(input())
arr = []
for _ in range(N):
    arr.append(list(map(int, input().split())))


def bfs(i, j, v, num):
    q = deque()
    q.append((i, j))
    cur = arr[i][j]
    v[i][j] = num
    count = 1

    while q:
        i, j = q.popleft()
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= N or nj < 0 or nj >= N:
                continue
            if v[ni][nj]:
                continue
            if arr[ni][nj] == cur:
                count += 1
                q.append((ni, nj))
                v[ni][nj] = num
    return v, count


def art():
    # 예술 점수 구하기
    # [1] 그룹 나누기
    gdict = {}          # 그룹 번호 : [숫자 값, 칸 수]
    v = [[0] * N for _ in range(N)]
    num = 1
    for i in range(N):
        for j in range(N):
            if not v[i][j]:
                v, count = bfs(i, j, v, num)
                gdict[num] = [arr[i][j], count]
                num += 1

    # [2] 조합 별로 예술성 점수 구하기
    near_group = [[0] * (num+1) for _ in range(num+1)]
    for i in range(N):
        for j in range(N):
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ni, nj = i + di, j + dj
                # 범위 제한
                if ni < 0 or ni >= N or nj < 0 or nj >= N:
                    continue
                cur_idx, nxt_idx = v[i][j], v[ni][nj]
                # 현재 칸과 다음 칸의 그룹이 다르면, 맞닿은 면 추가 => (맞닿은 면 * 2)
                if cur_idx != nxt_idx:
                    near_group[cur_idx][nxt_idx] += 1
                    near_group[nxt_idx][cur_idx] += 1

    # [3] 맞닿은 면의 수가 0이 아닌 조합의 조화로움 계산
    # (칸의 수 합) * (그룹 1 숫자) * (그룹 2 숫자) * (맞닿은 변의 수)
    harmony = 0
    for r in range(1, num):
        for c in range(r+1, num):
            if near_group[r][c]:
                x1 = gdict[r][1] + gdict[c][1]
                x2, x3 = gdict[r][0], gdict[c][0]
                x4 = near_group[r][c] // 2
                harmony += x1 * x2 * x3 * x4
    return harmony


def rotate():
    global arr
    # [1] 십자 부분 회전
    # [1-1] 전체 반시계 회전
    narr = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            narr[i][j] = arr[j][N-1-i]

    # [2] 십자 제외 4개의 정사각형 => 각각 시계 방향 90도 회전
    for si, sj in ((0, 0), (0, N//2+1), (N//2+1, 0), (N//2+1, N//2+1)):
        for i in range(N//2):
            for j in range(N//2):
                narr[si+j][sj+(N//2)-1-i] = arr[si+i][sj+j]

    arr = narr


result = 0
# [1] 초기 예술 점수 구하기
result += art()

# [2] 1회전 후 점수
rotate()
result += art()

# [2] 2회전 후 점수
rotate()
result += art()

# [3] 3회전 후 점수
rotate()
result += art()

print(result)