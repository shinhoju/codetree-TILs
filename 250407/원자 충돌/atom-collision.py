# 원자 충돌

N, M, K = map(int, input().split())

atoms = {}
for _ in range(M):
    x, y, m, s, d = map(int, input().split())
    atoms[(x-1, y-1)] = [[m, s, d]]

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

for _ in range(K):
    # [1] 모든 원자 이동
    n_atoms = {}
    for sx, sy in atoms:
        for m, s, d in atoms[(sx, sy)]:
            nx, ny = (sx + dx[d] * s) % N, (sy + dy[d] * s) % N
            if (nx, ny) in n_atoms.keys():
                n_atoms[(nx, ny)].append([m, s, d])
            else:
                n_atoms[(nx, ny)] = [[m, s, d]]
    atoms = n_atoms

    n_atoms = {}
    # [2] 하나의 칸에 2개 이상의 원자 있는 경우 ) 합성 과정
    for sx, sy in atoms:
        if len(atoms[(sx, sy)]) > 1:
            # [2-1] 질량 & 속력 하나의 원자로 합침
            sum_s = 0
            sum_m = 0
            directions = []
            for m, s, d in atoms[(sx, sy)]:
                sum_s += s
                sum_m += m
                directions.append(d % 2)
            # [2-3] 4개의 원자로 나눔
            divided_s = sum_s // len(atoms[(sx, sy)])
            divided_m = sum_m // 5
            if divided_m:
                # 질량 0이 아니면 추가
                if all(d == 0 for d in directions) or all(d == 1 for d in directions):
                    temp = []
                    for dd in [0, 2, 4, 6]:
                        temp.append([divided_m, divided_s, dd])
                    n_atoms[(sx, sy)] = temp
                else:
                    temp = []
                    for dd in [1, 3, 5, 7]:
                        temp.append([divided_m, divided_s, dd])
                    n_atoms[(sx, sy)] = temp
        else:
            # 1개면 그냥 추가
            n_atoms[(sx, sy)] = [[atoms[(sx, sy)][0][0], atoms[(sx, sy)][0][1], atoms[(sx, sy)][0][2]]]
    atoms = n_atoms

# 남아있는 질량의 합 구하기
result = 0
for atom in atoms.values():
    for m, _, _ in atom:
        result += m

print(result)