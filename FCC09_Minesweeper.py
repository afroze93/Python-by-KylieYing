import random
import re

# lets create a board object to represent the minesweeper game
# this is so that we can just say "create a new board object", or
# "dig here", or "render the game for this object"


class Board:
    def __init__(self, dim_size, num_bombs):
        # let's keep track of these parameters.
        # they'll be helpful later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # let's create the board
        # helper function!!
        self.board = self.make_new_board()  # Also plant bombs
        self.assign_values_to_board()

        # Initialize a set to keep track of which locations we've uncovered
        # we'll save (row,col) tuples into this set
        self.dug() = set()  # if we dig at (0, 0) then self.dug = {(0, 0)}

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we should construct the list of lists here...
        # ... (or what ever rep. you prefer but since we ...
        # have a 2-D board, list of lists is most natural)

        # generate a new board
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]
        # this creates an array like this:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...                  ],
        #  [None, None, ..., None],]
        # we can see how this represents a board!!

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            # return a random integer N such that a <= N <= b
            loc = random.randint(0, self.dim_size**2 - 1)
            # we want the number of times dim_size...
            # ... goes into loc to tell us
            row = loc // self.dim_size
            # we want the remainder to tell us...
            # what index in that tow to look...
            col = loc % self.dim_size

            if board[row][col] == '*':
                # this means we've actually planted a bomb...
                # ... there already so keep going
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8...
        # for all the empty spaces, which represents how many neighboring
        # bombs there are. we can precompute these and it'll save us some
        # effort checking what's around the board later on :)
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                # if this is already a bomb, do nothing he he!!
                continue
            self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions...
        # and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # make sure to not to go out of bonds!

        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location!!
        # return True if successful dig, False if Bomb!!

        # a few scenarios:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig
        # dig at location with no neighboring bombs -> recursively dig neighbors!!

        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue  # don't dig where you've already dug
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we *shouldn't* hot a bomb here
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # putting this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # Playing the game!!!

    # Step 1: Create the board and plant bombs
    board = Board(dim_size, num_bombs)

    # Step 2: Show the user the board and ask for where they want to dig
    # Step 3a: If location = bomb, Game Over!!
    # Step 3b: If location != bomb, dig recursively...
    # ... until each square is at least next to bomb
    # Step 4: Repeat step 2 and 3a/b until...
    # ... no more places to dig --> Victory!!

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(
            ',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if it's valid we dig
        safe = board.dig(row, col)
        if not safe:
            # we've dug a BOMB!! Oh No!!!
            break  # game over RIP!!

    # 2 ways to end loop, lets check which one
    if safe:
        print("Congratulations!!! You are Victorious!!!")
    else:
        print("Sorry, Game Over!!! :(")
        # let's reveal the whole board!
        board.dug = [(r, c) for r in range(board.dim_size)
                     for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':  # good practice :)
    play()
