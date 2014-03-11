import random

class GameOver(Exception):
    pass

class Board(object):
    def __init__(self):
        self.cells = [0] * 16

    def __str__(self):
        c = list(map(str, self.cells))
        return (c[0] + ' ' + c[1] + ' ' + c[2] + ' ' + c[3] + '\n' +
                c[4] + ' ' + c[5] + ' ' + c[6] + ' ' + c[7] + '\n' +
                c[8] + ' ' + c[9] + ' ' + c[10] + ' ' + c[11] + '\n' +
                c[12] + ' ' + c[13] + ' ' + c[14] + ' ' + c[15] + '\n')

    def __getitem__(self, index):
        x, y = index
        if x < 0 or x > 3 or y < 0 or y > 3:
            return -1
        return self.cells[x + 4 * y]

    def __setitem__(self, index, value):
        x, y = index
        self.cells[x + 4 * y] = value

    def move(self, direction):
        dif_x, dif_y = direction
        # Make sure we move the last tiles first, so they don't block the
        # previous ones.
        x_range = range(4) if dif_x < 1 else range(3, -1, -1)
        y_range = range(4) if dif_y < 1 else range(3, -1, -1)

        for x in x_range:
            for y in y_range:
                if not self[x, y]:
                    continue
                
                new_x, new_y = x, y
                while True:
                    old_x, old_y = new_x, new_y
                    new_x += dif_x
                    new_y += dif_y
                    if self[new_x, new_y] == self[old_x, old_y]:
                        self[new_x, new_y] *= 2
                        break
                    elif self[new_x, new_y]:
                        break
                    else:
                        self[new_x, new_y] = self[old_x, old_y]
                        self[old_x, old_y] = 0


    def _rand_empty_position(self):
        if all(self.cells):
            raise GameOver()

        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if not self[x, y]:
                return x, y

    def _rand_piece(self):
        return random.choice([2] * 9 + [4])

    def place_random(self):
        self[self._rand_empty_position()] = self._rand_piece()


class Game(object):
    def __init__(self):
        self.board = Board()
        self.board.place_random()
        self.board.place_random()

    def play(self, direction):
        self.board.move(direction)
        self.board.place_random()

    def __str__(self):
        return '-------\n' + str(self.board) + '-------'

if __name__ == '__main__':
    import console
    g = Game()

    keymap = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

    while True:
        console.display(str(g))
        key = console.get_valid_key(list(keymap.keys()) + ['q'])
        if key == 'q':
            break
        g.play(keymap[key])
