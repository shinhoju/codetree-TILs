# 메이즈 러너

N, M, K = map(int, input().split())
maze = []
for _ in range(N):
    maze.append(list(map(int, input().split())))

participants = []
for i in range(M):
    xi, yi = map(int, input().split())
    participants.append((xi-1, yi-1))

esc_x, esc_y = map(int, input().split())
esc_x, esc_y = esc_x-1, esc_y-1

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def in_range(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    else:
        return True


def distance(x, y):
    global esc_x, esc_y
    # 맨하튼 거리 구하기
    dist = abs(x - esc_x) + abs(y - esc_y)
    return dist


move_sum = 0
for _ in range(K):
    # [0] 게임 종료 조건: 모든 참가자 탈출 성공
    # if not len(participants):
    #     break

    # [1-1] 4방향 중 하나로 한 칸 이동 -> 이동 후, 출구와 거리 더 가까워 져야 함
    n_participants = []
    for px, py in participants:
        now_distance = distance(px, py)
        for i in range(4):
            npx, npy = px + dx[i], py + dy[i]
            if not in_range(npx, npy):
                continue
            # 벽이면 이 방향 xxx
            if maze[npx][npy] >= 1:
                continue
            # 움직 경우의 수 : 만약 출구 위치면 바로 탈출
            if distance(npx, npy) < now_distance:
                if (npx, npy) != (esc_x, esc_y):
                    n_participants.append((npx, npy))
                now_distance = distance(npx, npy)
                move_sum += 1
                break
        # 거리 안 변하면 좌표 그대로 넣기
        if now_distance == distance(px, py):
            n_participants.append((px, py))
    participants = n_participants

    if not len(participants):
        break

    # [2] 출구와 참가자 최소 1명을 포함한 가장 작은 정사각형 구하기
    min_sq = []
    min_sq_len = 100
    for i in range(N):
        for j in range(N):
            for mul in range(1, N+1):
                # 범위 생성
                if min_sq_len > mul + 1:
                    sq_x, sq_y = i + mul, j + mul
                    if not in_range(sq_x, sq_y):
                        break
                    # 출구 포함 여부 확인
                    if i <= esc_x <= sq_x and j <= esc_y <= sq_y:
                        # 참가자 포함 여부 확인
                        for px, py in participants:
                            if i <= px <= sq_x and j <= py <= sq_y:
                                # min_sq_x, min_sq_y = sq_x, sq_y
                                min_sq = (i, j, sq_x, sq_y)
                                min_sq_len = mul + 1
                                break
                        # break

    # [3] 시계 방향 90도 회전
    # n_maze = [[0] * N for _ in range(N)]
    n_maze = [m[:] for m in maze]
    n_participants = [p for p in participants]
    n_esc_x, n_esc_y = esc_x, esc_y
    si, sj = min_sq[0], min_sq[1]
    for i in range(min_sq_len):
        for j in range(min_sq_len):
            n_maze[si + i][sj + j] = 0

    for i in range(min_sq_len):
        for j in range(min_sq_len):
            if maze[si+i][sj+j] > 0:
                n_maze[si+j][sj+min_sq_len-1-i] = maze[si+i][sj+j] - 1
            if (si+i, sj+j) in participants:
                for _ in range(participants.count((si+i, sj+j))):
                    n_participants.remove((si + i, sj + j))
                    n_participants.append((si + j, sj + min_sq_len - 1 - i))
            if (si+i, sj+j) == (esc_x, esc_y):
                n_esc_x = si + j
                n_esc_y = sj + min_sq_len - 1 - i
    participants = n_participants
    maze = n_maze
    esc_x, esc_y = n_esc_x, n_esc_y


print(move_sum)
print(esc_x+1, esc_y+1)