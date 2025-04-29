def counter_move(move):
    # Returns the move that beats the input move
    return {'R': 'P', 'P': 'S', 'S': 'R'}[move]

def player(prev_play, opponent_history=[], my_history=[], round_num=[0], detected_bot=[""]):
    # Track the round number
    round_num[0] += 1

    # Add the previous plays to my and my opponent's history
    if prev_play:
        opponent_history.append(prev_play)
    if len(my_history) < round_num[0] - 1:
        my_history.append("R")  # Default to "R" for the first round

    # Bot detection phase (first 20 rounds)
    if round_num[0] <= 20:
        # Use a probing sequence that helps identify each bot
        probing_moves = ["R", "R", "P", "P", "S", "R", "R", "P", "P", "S", 
                        "R", "R", "P", "P", "S", "R", "R", "P", "P", "S"]
        guess = probing_moves[round_num[0] - 1]
        my_history.append(guess)
        return guess

    # Bot identification
    if detected_bot[0] == "":
        # Check for Quincy (repeats R, R, P, P, S)
        pattern = ["R", "R", "P", "P", "S"]
        is_quincy = False
        if len(opponent_history) >= 5:
            for i in range(16):  # Check starting positions 0 through 15
                if all(opponent_history[i+j] == pattern[j] for j in range(5)):
                    is_quincy = True
                    break
        
        if is_quincy:
            detected_bot[0] = "quincy"
        # Check for Kris (always counters our last move)
        elif len(opponent_history) >= 20 and all(
            len(my_history) > i and opponent_history[i] == counter_move(my_history[i-1])
            for i in range(1, 20)
        ):
            detected_bot[0] = "kris"
        # Check for Mrugesh (counts our last 10 moves and plays what beats our most common move)
        elif len(my_history) >= 10:
            last_ten = my_history[-10:]
            most_common = max(set(last_ten), key=last_ten.count)
            expected_move = counter_move(most_common)
            if opponent_history[-1] == expected_move:
                detected_bot[0] = "mrugesh"
        # Otherwise, assume Abbey
        else:
            detected_bot[0] = "abbey"

    # Counter strategies for each bot
    if detected_bot[0] == "quincy":
        # Quincy's exact pattern from RPS_game.py: ["R", "R", "P", "P", "S"]
        # We can predict exactly what Quincy will play next
        pattern = ["R", "R", "P", "P", "S"]
        position = (round_num[0] - 1) % 5  # -1 because round_num starts at 1
        quincy_move = pattern[position]
        # Play what beats Quincy's move
        guess = counter_move(quincy_move)
        
    elif detected_bot[0] == "kris":
        # From RPS_game.py: Kris always plays what beats our last move
        # To beat Kris, we need to play what would lose to our last move
        # Because Kris will counter our last move, and we want to counter that
        if my_history:
            last_move = my_history[-1]
            # What would lose to our last move? That's what Kris will play
            lose_to = {'R': 'S', 'P': 'R', 'S': 'P'}
            kris_move = lose_to[last_move]
            # Play what beats Kris's move
            guess = counter_move(kris_move)
        else:
            guess = "R"
            
    elif detected_bot[0] == "mrugesh":
        # From RPS_game.py: Mrugesh looks at our last 10 moves and plays what beats our most common move
        if len(my_history) >= 10:
            last_ten = my_history[-10:]
            most_common = max(set(last_ten), key=last_ten.count)
            # Mrugesh will play what beats our most common move
            mrugesh_move = counter_move(most_common)
            # We play what beats Mrugesh's move
            guess = counter_move(mrugesh_move)
        else:
            guess = "R"
            
    elif detected_bot[0] == "abbey":
        # From RPS_game.py: Abbey looks at our last two moves and predicts what we'll play next
        # She then counters that predicted move
        if len(my_history) >= 2:
            last_two = "".join(my_history[-2:])
            
            # Count what moves we've played after this sequence
            next_moves = {"R": 0, "P": 0, "S": 0}
            for i in range(len(my_history) - 2):
                if "".join(my_history[i:i+2]) == last_two and i + 2 < len(my_history):
                    next_moves[my_history[i + 2]] += 1
            
            # Abbey would predict our most common move after this sequence
            predicted_move = max(next_moves, key=next_moves.get)
            abbey_move = counter_move(predicted_move)
            
            # We play what beats Abbey's move
            guess = counter_move(abbey_move)
        else:
            guess = "R"
    else:
        guess = "R"

    my_history.append(guess)
    return guess 