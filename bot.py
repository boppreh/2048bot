import random

class GameOver(Exception):
    """ Exception raised when the board has no move lefts. """

class Board(object):
    """
    Class for storing, changing and moving the tiles.
    Methods that change the board return a new changed copy instead.

    Invalid positions return -1.
    """
    def __init__(self, base_board=None):
        self.cells = list(base_board.cells) if base_board else [0] * 16

    def __str__(self):
        str_parts = []
        for y in range(4):
            for x in range(4):
                str_parts.append(str(self[x, y]) + ' ')
            str_parts.append('\n')
        return ''.join(str_parts)

    def __getitem__(self, index):
        x, y = index
        if x < 0 or x > 3 or y < 0 or y > 3:
            return -1
        return self.cells[x + 4 * y]

    def __setitem__(self, index, value):
        x, y = index
        self.cells[x + 4 * y] = value

    def move(self, direction):
        """
        Receives a tuple direction (x, y) and moves all pieces in that
        direction as much as possible. Similar pieces that collide are merged.

        Returns the updated board without changing itself.
        """
        dif_x, dif_y = direction

        # Make sure we move the last tiles first, so they don't block the
        # previous ones.
        x_range = range(4) if dif_x < 1 else range(3, -1, -1)
        y_range = range(4) if dif_y < 1 else range(3, -1, -1)

        new = Board(self)

        for x in x_range:
            for y in y_range:
                # Ignore empty tiles.
                if not self[x, y]:
                    continue
                
                new_x, new_y = x, y
                while True:
                    old_x, old_y = new_x, new_y
                    new_x += dif_x
                    new_y += dif_y

                    if new[new_x, new_y] == new[old_x, old_y]:
                        # Same pieces, merge.
                        new[new_x, new_y] *= 2
                        new[old_x, old_y] = 0
                        break
                    elif new[new_x, new_y]:
                        # Hit a different tile (or border, which is -1), stop.
                        break
                    else:
                        # Move piece one tile and leave an empty space behind.
                        new[new_x, new_y] = new[old_x, old_y]
                        new[old_x, old_y] = 0

        return new

    def _rand_empty_position(self):
        """
        Returns a random (x, y) that is guaranteed to be empty, or raise
        GameOver if there isn't one.
        """
        if self.is_full():
            raise GameOver()

        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if not self[x, y]:
                return x, y

    def _rand_piece(self):
        """ Returns a random piece 2 or 4, with different odds. """
        return random.choice([2] * 9 + [4])

    def place_random(self):
        """
        Places a new random piece (2 or 4) in a random empty tile.
        Returns the updated board without changing itself.
        """
        new = Board(self)
        new[self._rand_empty_position()] = self._rand_piece()
        return new

    def is_full(self):
        """ Return true if all cells are occupied. """
        return all(self.cells)

    def __eq__(self, other):
        return self.cells == other.cells


class Game(object):
    """
    Class for programatically playing the game.
    """
    KEYMAP = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

    def __init__(self):
        # Setup board with two random pieces.
        self.board = Board().place_random().place_random()

    def play(self, key):
        """
        Plays a movement, where `key` can be 'up', 'down', 'left' or
        'right'. Illegal movements are ignored and raises GameOver when the
        board fills up.
        """
        new = self.board.move(Game.KEYMAP[key])
        if new == self.board and not new.is_full():
            return

        self.board = new.place_random()

    def __str__(self):
        return '-------\n' + str(self.board) + '-------'

def play_human():
    """
    Allows for a human player to interactively play the game on the console.
    """
    import console
    def player_logic(board):
        console.display(str(board))
        key = console.get_valid_key(['q', 'up', 'down', 'left', 'right'])
        if key == 'q':
            exit()
        return key

    return play_bot(player_logic)

def play_bot(logic):
    """
    Runs a full playthrough of the game with the given logic, where `logic` is
    a function that takes the current board state and returns a directional
    string ('up', 'down', 'left' or 'right').

    Returns the score reached (biggest tile value).
    """
    g = Game()
    try:
        while True:
            g.play(logic(g.board))
    except GameOver:
        return max(g.board.cells)

def get_bot_max_score(logic, repeats=10):
    """
    Runs a bot logic a number of times, yielding the highest score achieved.
    """
    return max(play_bot(logic) for i in range(repeats))

if __name__ == '__main__':
    # Uncomment to play yourself.
    # play_human()
    # exit()

    import itertools
    cycle = itertools.cycle(['left', 'up', 'right', 'up'])
    # Emit a 'down' once in a while to avoid getting stuck.
    cycler = lambda board: next(cycle) if random.random() > 0.01 else 'down'
    print(get_bot_max_score(cycler, 10000))
