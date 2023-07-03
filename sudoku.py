from random import sample

BASE = 3
SIDE = BASE * BASE


def pattern(r, c):
    return (BASE * (r % BASE) + r // BASE + c) % SIDE


def shuffle(s):
    return sample(s, len(s))


class Sudoku:
    def __init__(self, open_cells):
        self.open_cells = open_cells
        rBASE = range(BASE)

        rows = []
        for g in shuffle(rBASE):
            for r in shuffle(rBASE):
                rows.append(g * BASE + r)

        cols = []
        for g in shuffle(rBASE):
            for c in shuffle(rBASE):
                cols.append(g * BASE + c)

        nums = shuffle(range(1, BASE * BASE + 1))

        self.field = []
        for r in rows:
            self.field.append([nums[pattern(r, c)] for c in cols])

        # remove some cells
        squares = SIDE * SIDE
        for p in sample(range(squares), squares - self.open_cells):
            self.field[p // SIDE][p % SIDE] = 0

    def solve(self):
        for y in range(9):
            for x in range(9):
                if self.field[y][x] == 0:
                    for i in range(1, 10):
                        if self.possible(x, y, i):
                            print(x, y, i)
                            self.print()
                            self.solve()
                            self.field[y][x] = 0

    def possible(self, x, y, num):
        for right in range(x, 9):
            if self.field[y][right] == num:
                return False

        for down in range(y, 9):
            if self.field[down][x] == num:
                return False

        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.field[y0 + i][x0 + j] == num:
                    return False

        self.field[y][x] = num
        self.open_cells += 1
        return True

    def print(self):
        numSize = len(str(SIDE))
        for line in self.field: print("[" + "  ".join(f"{n or '.':{numSize}}" for n in line) + "]")


if __name__ == '__main__':
    open_cells = int(input('input number of open cells\n'))
    mode = int(input('input mode (1 or 2)\n'))

    game = Sudoku(open_cells)
    game.print()

    if mode == 1:
        while game.open_cells != 81:
            x, y, num = input().split()
            game.possible(int(x) - 1, int(y) - 1, int(num))
            game.print()

        print('You won!')
    else:
        while game.open_cells != 81:
            game.solve()
            game.print()