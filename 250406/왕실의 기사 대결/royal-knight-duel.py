# 왕실의 기사 대결

L, N, Q = map(int, input().split())
chessboard = [[2] * (L+2)]
for _ in range(L):
    chessboard.append([2] + list(map(int, input().split())) + [2])
chessboard.append([2] * (L+2))

knights = dict()
init_k = [0] * (N+1)
for n in range(1, N+1):
    r, c, h, w, k = map(int, input().split())
    init_k[n] = k
    knights[n] = ([r, c, h, w, k])

order = []
for _ in range(Q):
    order.append(tuple(map(int, input().split())))

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def push_knights(start, d):
    queue = []              # bfs 위한 큐 / 기사 번호 넣기
    p_knight = set()        # push 할 기사 번호
    damages = [0] * (N+1)

    queue.append(start)
    p_knight.add(start)

    while queue:
        c_idx = queue.pop(0)
        ci, cj, h, w, k = knights[c_idx]

        # 현재 기사가 벽과 만나는 지 체크
        ni, nj = ci + dx[d], cj + dy[d]
        for i in range(ni, ni+h):
            for j in range(nj, nj+w):
                if chessboard[i][j] == 2:
                    return
                if chessboard[i][j] == 1:
                    damages[c_idx] += 1

        # 다른 모든 유닛과 비교
        for idx in knights:
            if idx in p_knight:
                continue
            ti, tj, th, tw, tk = knights[idx]
            # 겹치는 경우
            if ni <= ti + th - 1 and ni + h - 1 >= ti and nj <= tj + tw - 1 and nj + w - 1 >= tj:
                p_knight.add(idx)
                queue.append(idx)

    # 명령 받은 기사는 데미지 안 입음
    damages[start] = 0

    # 대결 데미지 : 움직일 기사들 위치에 있는 함정의 갯수 만큼 데미지 입음
    # 체력 보다 큰 데미지 입을 경우, 기사 삭제
    for knight in p_knight:
        si, sj, h, w, k = knights[knight]
        if damages[knight] >= knights[knight][4]:
            knights.pop(knight)
        else:
            # 데미지 입히고, 위치 변경
            ni, nj = si + dx[d], sj + dy[d]
            knights[knight] = [ni, nj, h, w, k-damages[knight]]


for i, d in order:
    if i in knights:
        push_knights(i, d)

result = 0
for k in knights:
    result += (init_k[k] - knights[k][4])

print(result)