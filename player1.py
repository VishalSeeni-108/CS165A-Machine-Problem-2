import math

# Directions are mapped to 'W', 'A', 'S', 'D'
directions = {'W': (0, -1), 'A': (-1, 0), 'S': (0, 1), 'D': (1, 0)}
DEPTH_LIMIT = 2

def player1_logic(coins, potions, foods, dungeon_map, self_position, other_agent_position):
  
    initial_state = {
        "player_position": self_position,
        "player_score": 0,
        "player_stamina": 50, 
        "player_hunger": 50, 
        "player_hunger_dec": True,
        "opponent_position": other_agent_position, 
        "opponent_score": 0, 
        "opponent_stamina": 50, 
        "opponent_hunger": 50,
        "opponent_hunger_dec": True,
        "coins": coins.copy(),
        "potions": potions.copy(),
        "foods": foods.copy(),
        "valid": True
    }

    potential_moves = {}
    for move in directions:
            #Get player position
            x, y = self_position
            dx, dy = directions[move]
            nx, ny = x + dx, y + dy
            # Ensure the new position is within the bounds of the map and is not a wall
            # Notice that you have to access position (x, y) via dungeon_map[y][x]
            # Because the dungeon_map is a list of lists
            if dungeon_map[ny][nx] == 'floor':
                move_state = state_gen(initial_state, move, True, 1, dungeon_map)
                potential_moves[move] = recursive_minimax(move_state, False, 1, -math.inf, math.inf, dungeon_map)
    # print("Taking move " + max(potential_moves, key=potential_moves.get))
    # print(potential_moves)
    return max(potential_moves, key=potential_moves.get)

def utility(state): #for a given state, calculate a score based on player score, stamina, hunger and opponent score, stamina, hunger
    #TODO - need to find a good utility function
    return (100*state["player_score"]) + state["player_stamina"] + state["player_hunger"] + (1/player_dist_to_coin(state))


def recursive_minimax(state, turn, depth, alpha, beta, dungeon_map): #Recursive function for minimax
    
    if(depth == DEPTH_LIMIT):
        return utility(state)
    
    if(turn): #Player's turn
        new_states = []
        for move in directions:
            new_states.append(state_gen(state, move, True, depth, dungeon_map))

        curr_max = -math.inf
        for new_state in new_states:
            new_score = recursive_minimax(new_state, False, depth+1, alpha, beta, dungeon_map)
            curr_max = max(curr_max, new_score)
            alpha = max(alpha, curr_max)
            if(beta <= alpha):
                break
        return curr_max
    else: #Opponent's turn
        new_states = []
        for move in directions:
            new_states.append(state_gen(state, move, False, depth, dungeon_map))

        curr_min = math.inf
        for new_state in new_states:
            new_score = recursive_minimax(new_state, True, depth+1, alpha, beta, dungeon_map)
            curr_min = min(curr_min, new_score)
            beta = min(beta, curr_min)
            if(beta <= alpha):
                break
        return curr_min



def state_gen(state, action, player, depth, dungeon_map):
    new_state = state.copy()

    if(player):
        #Get player position
        x, y = new_state["player_position"]
        dx, dy = directions[action]
        nx, ny = x + dx, y + dy
        # Ensure the new position is within the bounds of the map and is not a wall
            # Notice that you have to access position (x, y) via dungeon_map[y][x]
            # Because the dungeon_map is a list of lists
        if dungeon_map[ny][nx] != 'floor':
            new_state["valid"] = False
            return new_state
        
        new_state["player_position"] = nx, ny
        
        #Check for items
        if(new_state["player_position"] in new_state["coins"]):
            new_state["player_score"] += 1
            new_state["coins"].remove(new_state["player_position"])
        elif(new_state["player_position"] in new_state["potions"]):
            new_state["player_stamina"] += 20
            if(new_state["player_stamina"] > 50):
                new_state["player_stamina"] = 50
            new_state["potions"].remove(new_state["player_position"])
        elif(new_state["player_position"] in new_state["foods"]):
            new_state["player_hunger"] += 30
            if(new_state["player_hunger"] > 50):
                new_state["player_hunger"] = 50
            new_state["foods"].remove(new_state["player_position"])

        #Decrement hunger and stamina
        if(new_state["player_hunger"] == 0):
            new_state["player_stamina"] -= 2
        else:
            new_state["player_stamina"] -= 1
        if(new_state["player_hunger_dec"]): #Decremented hunger on previous turn
            new_state["player_hunger_dec"] = False
        else: 
            new_state["player_hunger_dec"] = True
            new_state["player_hunger"] -= 1
            new_state["player_stamina"] += 1
    else: 
        #Get opponent position
        x, y = new_state["opponent_position"]
        dx, dy = directions[action]
        nx, ny = x + dx, y + dy
        # Ensure the new position is within the bounds of the map and is not a wall
            # Notice that you have to access position (x, y) via dungeon_map[y][x]
            # Because the dungeon_map is a list of lists
        if dungeon_map[ny][nx] != 'floor':
            new_state["valid"] = False
            return new_state
        
        new_state["opponent_position"] = nx, ny
        
        #Check for items
        if(new_state["opponent_position"] in new_state["coins"]):
            new_state["opponent_score"] += 1
            new_state["coins"].remove(new_state["opponent_position"])
        elif(new_state["opponent_position"] in new_state["potions"]):
            new_state["opponent_stamina"] += 20
            if(new_state["opponent_stamina"] > 50):
                new_state["opponent_stamina"] = 50
            new_state["potions"].remove(new_state["opponent_position"])
        elif(new_state["opponent_position"] in new_state["foods"]):
            new_state["opponent_hunger"] += 30
            if(new_state["opponent_hunger"] > 50):
                new_state["opponent_hunger"] = 50
            new_state["foods"].remove(new_state["opponent_position"])

        #Decrement hunger and stamina
        if(new_state["opponent_hunger"] == 0):
            new_state["opponent_stamina"] -= 2
        else:
            new_state["opponent_stamina"] -= 1
        if(new_state["opponent_hunger_dec"]): #Decremented hunger on previous turn
            new_state["opponent_hunger_dec"] = False
        else: 
            new_state["opponent_hunger_dec"] = True
            new_state["opponent_hunger"] -= 1
            new_state["opponent_stamina"] += 1

    return new_state

def player_dist_to_coin(state):
    player_x, player_y = state["player_position"]
    min_dist = math.inf
    for coin in state["coins"]:
        coin_x, coin_y = coin
        dist = math.sqrt(pow(coin_x - player_x, 2) + pow(coin_y - player_y, 2))
        if(dist < min_dist):
            min_dist = dist
    return min_dist