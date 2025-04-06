#놀이기구 탑승

N = int(input())
units = dict()
for _ in range(N**2):
    f0, f1, f2, f3, f4 = map(int, input().split())
    units[f0] = [f1, f2, f3, f4]

arr = [[0] * N for _ in range(N)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def in_range(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    else:
        return True


def find_friends(x, y, idx):
    num_f = 0
    num_empty = 0
    for d in range(4):
        nx, ny = x + dx[d], y + dy[d]
        if not in_range(nx, ny):
            continue
        if arr[nx][ny] in units[idx]:
            # 옆 자리가 좋아하는 친구일 때
            num_f += 1
        if arr[nx][ny] == 0:
            num_empty += 1

    return num_f, num_empty


for f_i, cur in enumerate(units):
    if f_i == N**2 - 1:
        # 마지막 학생이면 그냥 빈자리에 앉아야함
        for i in range(N):
            for j in range(N):
                if arr[i][j] == 0:
                    arr[i][j] = cur
        break

    # [1] 좋아하는 친구의 수가 가장 많은 위치
    max_friends = 0
    max_empty = 0
    max_x, max_y = 30, 30
    for i in range(N):
        for j in range(N):
            if arr[i][j] > 0:
                continue
            temp_friends, temp_empty = find_friends(i, j, cur)
            if max_friends < temp_friends:
                # 좋아하는 친구의 수 최대값 갱신되는 경우 )
                max_friends = temp_friends
                max_empty = temp_empty
                max_x, max_y = i, j
            elif max_friends == temp_friends:
                # 좋아하는 친구 수 최대 값과 동일할 경우 ) 비어있는 칸이 많은 자리
                if max_empty < temp_empty:
                    max_empty = temp_empty
                    max_x, max_y = i, j
                elif max_empty == temp_empty:
                    # 행 번호가 가장 작은 위치
                    if max_y > j:
                        max_x, max_y = i, j
                    elif max_y == j:
                        if max_x > i:
                            max_x, max_y = i, j
    # arr 업데이트
    arr[max_x][max_y] = cur

# 점수 구하기
result = 0
for i in range(N):
    for j in range(N):
        score, _ = find_friends(i, j, arr[i][j])
        if score > 0:
            result += 10 ** (score - 1)

print(result)