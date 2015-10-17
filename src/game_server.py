# Tudor Berariu, 2015

from itertools import product
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

def get_players():
  from os import listdir
  from os.path import isfile, join
  from imp import load_source
  import inspect

  dir_path = "./players/"
  loader = lambda f: (f.strip(".py"), load_source(f.strip(".py"), join(dir_path, f)))
  modules = [loader(f) for f in listdir(dir_path) if isfile(join(dir_path,f)) and f.endswith(".py")]

  players = []
  for name, module in modules:
    cls = next(obj[1] for obj in inspect.getmembers(module) if obj[0] == name)
    assert(inspect.isclass(cls))
    players.append(cls)

  return players

if __name__ == "__main__":
  players = get_players()
  scores = {name: 0 for name in map(lambda P: P().name, players)}
  stats = {name: {"W": 0, "L": 0, "W_reasons": {}, "L_reasons": {}} for name in scores.keys()}
  for (P1, P2) in product(players, players):
    if P1 == P2:
      continue
    for size in [7, 11, 15]:
      p1 = P1()
      p2 = P2()
      (p1_score, p2_score, msg) = play_game(p1, p2, size, size)
      scores[p1.name] = scores[p1.name] + p1_score
      scores[p2.name] = scores[p2.name] + p2_score
      if p1_score > p2_score:
        winner = p1.name
        loser = p2.name
      else:
        winner = p2.name
        loser = p1.name
      stats[winner]["W"] = stats[winner]["W"] + 1
      stats[winner]["W_reasons"][msg] = stats[winner]["W_reasons"].get(msg, 0) + 1
      stats[loser]["L"] = stats[loser]["L"] + 1
      stats[loser]["L_reasons"][msg] = stats[loser]["L_reasons"].get(msg, 0) + 1
  print(scores)
  print(stats)