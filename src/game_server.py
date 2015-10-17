# Tudor Berariu, 2015

from random import choice
from itertools import count, izip, product
from signal import signal, alarm, SIGALRM

def get_move(board, score, move_fnc):
    def handler(signum, frame):
        raise Exception("Timeout!")
    signal(SIGALRM, handler)
    alarm(1)
    try:
        move = move_fnc(board, score)
    finally:
        alarm(0)
    return move

def play_game(player0, player1, height=10, width=10):
  cells_no = height * width
  board = [[0 for col in range(width + row % 2)] for row in range(height * 2 + 1)]
  score = (0,0)
  current = 0
  players = [player0, player1]
  while next((row for row in board if 0 in row), False):
    try:
      (r, c) = get_move(board, (score[current], score[1-current]), players[current].move)
      if board[r][c] != 0:
        # This means your algorithm sucks!
        return (cells_no * current, cells_no * (1-current), "wrong move")
      else:
        board[r][c] = 1
        if r % 2 == 0:
          # Check if cell above is closed now
          if r > 0 and sum([board[x][y] for (x,y) in [(r-2,c), (r-1,c), (r-1,c+1)]]) == 3:
            score = (score[0] + (1-current), score[1] + current)
          # Check if cell below is closed now
          if r < 2 * height and sum([board[x][y] for (x,y) in [(r+2,c), (r+1,c), (r+1,c+1)]]) == 3:
            score = (score[0] + (1-current), score[1] + current)
        else:
          # Check if cell on left is closed now
          if c > 0 and sum([board[x][y] for (x,y) in [(r-1,c-1), (r, c-1), (r+1, c-1)]]) == 3:
            score = (score[0] + (1-current), score[1] + current)
          # Check if cell on right is closed now
          if c < width and sum([board[x][y] for (x,y) in [(r-1,c), (r, c+1), (r+1, c)]]) == 3:
            score = (score[0] + (1-current), score[1] + current)
    except Exception as e:
      return (cells_no * current, cells_no * (1-current), str(e))
    current = 1 -current
  return (score[0], score[1], "ok")

class BetterPlayer:
  def __init__(self):
    pass

  def move(self, board, score):
    cells_height = (len(board) - 1) / 2
    cells_width = len(board[0])
    # Look for a cell with 3 walls
    for r, c in product(range(cells_height), range(cells_width)):
        cells = [(r*2,c), (r*2+2,c), (r*2+1,c), (r*2+1,c+1)]
        if sum(map(lambda (x, y): board[x][y], cells)) == 3:
            return next((x,y) for (x,y) in cells if board[x][y] == 0)
    # If there was no such cell, pick a random one
    good_rows = filter(lambda i: 0 in board[i], range(len(board)))
    row = choice(good_rows)
    col = choice([c for c, val in izip(count(), board[row]) if val == 0])
    return row, col

class RandomPlayer:
  def __init__(self):
    pass

  def move(self, board, score):
    (row_idx, row) = choice([(idx, row) for (idx, row) in zip(count(), board) if 0 in row])
    col_idx = choice([col_idx for col_idx, value in zip(count(), row) if value == 0])
    return (row_idx, col_idx)

class WrongPlayer:
  def __init__(self):
    pass

  def move(self, board, score):
    from random import randint
    from time import sleep
    sleep(0.8)
    row = randint(0, len(board)-1)
    col = randint(0, len(board[row])-1)
    return (row, col)

if __name__ == "__main__":
  p1 = RandomPlayer()
  p2 = BetterPlayer()
  print(play_game(p2, p1))
