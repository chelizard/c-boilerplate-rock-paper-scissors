# Bot methods
# Quincy: follows R, R, P, P, S repeating
# Kris: plays the move that beats the player's last move
# Mrugesh: plays the move that beats our most frequent out of the last 10 moves
# Abbey: predicts the player's next move based on the last two moves (markov chain)

# Strategy:
# Random choices at the start to throw off opponents
# Counter repeating moves with the move that beats the last move
# When moves change, break patterns

import random

win = {
  "R": "P",
  "P": "S",
  "S": "R"
}

def player(prev_play, opponent_moves=[]):
  # Initialize the next move
  next_move = ""

  # First move or reset condition
  if not prev_play:
    # Clear history when starting a new game
    opponent_moves.clear()
    # Start with a random move for unpredictability
    next_move = random.choice(["R", "P", "S"])
  # Early game strategy - play randomly until data is collected
  elif len(opponent_moves) < 3:
    # Record opponent's move
    opponent_moves.append(prev_play)
    # Use randomness in early game
    next_move = random.choice(["R", "P", "S"])
  # Pattern detection – opponent repeating the same move
  elif opponent_moves[-1] == opponent_moves[-2]:
    opponent_moves.append(prev_play)
    # Counter the opponent's last move directly
    next_move = win[prev_play]
  # Pattern detection – opponent alternating moves
  elif opponent_moves[-1] != opponent_moves[-2]:
    opponent_moves.append(prev_play)
    # Double counter – anticipate opponent's counter to our counter
    next_move = win[win[prev_play]]
  else:
    opponent_moves.append(prev_play)
    # Default to random when no pattern is detected
    next_move = random.choice(["R", "P", "S"])

  return next_move