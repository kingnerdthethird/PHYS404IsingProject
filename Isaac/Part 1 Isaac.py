import numpy as np

def GenerateMatrix(m, n):
    matrix = []
    pretty_matrix = []
    magnetization = 0
    N = m*n
    for row in range(0, m):
        column = []
        pretty_column = []
        for col in range(0, n):
            if np.random.random() >= 0.5:
                spin = +1
                pretty_spin = "+"
            else:
                spin = -1
                pretty_spin = "-"
            column.append(spin)
            magnetization += spin
            pretty_column.append(pretty_spin)
        matrix.append(column)
        pretty_matrix.append(pretty_column)
    magnetization /= N
    return (matrix, pretty_matrix, magnetization)

test, pretty_test, magnet = GenerateMatrix(10, 10)
test2, pretty_test2, magnet2 = GenerateMatrix(64, 64)
output = open("spin matrix.txt", "w+")

for row in pretty_test:
    print(*row, sep = ' ')
    for col in row:
        output.write(col)
        output.write(' ')
    output.write('\n')
for row in pretty_test2:
    print(*row, sep = ' ')
    for col in row:
        output.write(col)
        output.write(' ')
    output.write('\n')

print(magnet)
print(magnet2)