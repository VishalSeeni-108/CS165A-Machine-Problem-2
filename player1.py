import random

# Directions are mapped to 'W', 'A', 'S', 'D'
directions = {'W': (0, -1), 'A': (-1, 0), 'S': (0, 1), 'D': (1, 0)}
RECURSION_LIMIT = 3
#TODO: Implement alpha-beta pruning so recursion limit can be increased - already very slow for just 10

def player1_logic(coins, potions, foods, dungeon_map, self_position, other_agent_position):
    results = recursive_minimax(dungeon_map, coins, potions, foods, self_position, 0, 50, 50, other_agent_position, 0, 50, 50, True, True, 'W', True, 0)

    return results[0]


def action_utility(coins, potions, foods, player_position, player_score, player_stamina, player_hunger, opponent_position, opponent_score, opponent_stamina, opponent_hunger, action, hunger_dec_player, hunger_dec_opponent, turn): #Evaluates a given action and specifices the changed values - that is, calculate the resulting state  
    if(turn): #Player's turn
        # Evaluates the results of a given action and returns appropriate values
        #Calculate action_position
        xi, yi = player_position
        dx, dy = directions[action]
        action_position = xi+dx, yi+dy

        #Decrement stamina for movement
        if(player_position != action_position): #Ensure this is not an idle action
            player_stamina -= 1

        #Decrement stamina for hunger
        if(player_hunger == 0):
            player_stamina -= 1

        #Decrement hunger if hunger was not decremented on previous turn
        if(not hunger_dec_player): #If hunger was not decremented on previous turn
            hunger_dec_player = True
            player_hunger -= 1
        else: #Hunger was decremented on previous turn
            hunger_dec_player = False

        #Check for items 
        print("Action position: " + str(action_position))
        if action_position in coins: #Check if there is a coin at that position - if there is, increment score and collect coin
            player_score += 1
            coins.remove(action_position) 
        elif action_position in foods:  #Check if there is a food at that position - if there is, increment hunger appropriately 
            player_hunger += 30
            if(player_hunger > 50): 
                player_hunger = 50
            foods.remove(action_position)
        elif action_position in potions: #Check if there is a potion at that position 0 if there is increment stamina appropriately
            player_stamina += 20
            if(player_stamina > 50):
                player_stamina = 50
            potions.remove(action_position)
    else: #Opponent's turn
        # Evaluates the results of a given action and returns appropriate values
        #Calculate action_position
        xi, yi = opponent_position
        dx, dy = directions[action]
        action_position = xi+dx, yi+dy

        #Decrement stamina for movement
        if(opponent_position != action_position): #Ensure this is not an idle action
            opponent_stamina -= 1

        #Decrement stamina for hunger
        if(opponent_hunger == 0):
            opponent_stamina -= 1

        #Decrement hunger if hunger was not decremented on previous turn
        if(not hunger_dec_opponent): #If hunger was not decremented on previous turn
            hunger_dec_opponent = True
            opponent_hunger -= 1
        else: #Hunger was decremented on previous turn
            hunger_dec_opponent = False

        #Check for items 
        if action_position in coins: #Check if there is a coin at that position - if there is, increment score and collect coin
            opponent_score += 1
            coins.remove(action_position) 
        elif action_position in foods:  #Check if there is a food at that position - if there is, increment hunger appropriately 
            opponent_hunger += 30
            if(opponent_hunger > 50): 
                opponent_hunger = 50
            foods.remove(action_position) 
        elif action_position in potions: #Check if there is a potion at that position 0 if there is increment stamina appropriately
            opponent_stamina += 20
            if(opponent_stamina > 50):
                opponent_stamina = 50
            potions.remove(action_position) 
        
    return coins, potions, foods, player_score, player_stamina, player_hunger, hunger_dec_player, opponent_score, opponent_stamina, opponent_hunger, hunger_dec_opponent, action_position

def utility(player_score, player_stamina, player_hunger, opponent_score, opponent_stamina, opponent_hunger): #for a given state, calculate a score based on player score, stamina, hunger and opponent score, stamina, hunger
    ##return ((10*player_score) + (1*player_stamina) + (1*player_hunger) - (10*opponent_score) - (10*opponent_stamina) - (10*opponent_hunger))/6 #Returns weighted average
    return player_score - opponent_score
def recursive_minimax(dungeon_map, coins, potions, foods, player_position, player_score, player_stamina, player_hunger, opponent_position, opponent_score, opponent_stamina, opponent_hunger, hunger_dec_player, hunger_dec_opponent, curr_action, turn, recursion_depth): #Recursive function for minimax
    #Calculate next moves for the either the player or the opponent taking their turn
    # Get current position of the agent
    if(turn): #Player's turn
        x, y = player_position
    else: #Opponent's turn
        x, y = opponent_position
    
    # List to hold possible moves
    valid_moves = []
    
    # Check each possible direction
    for move in directions:
        dx, dy = directions[move]
        nx, ny = x + dx, y + dy
        
        # Ensure the new position is within the bounds of the map and is not a wall
        # Notice that you have to access position (x, y) via dungeon_map[y][x]
        # Because the dungeon_map is a list of lists
        if dungeon_map[ny][nx] == 'floor':
            valid_moves.append(move)
    
    # If there are no valid move, break
    if((recursion_depth == RECURSION_LIMIT) or (len(valid_moves) == 0)):
        return utility(player_score, player_stamina, player_hunger, opponent_score, opponent_stamina, opponent_hunger)

    #For each possible move, calculate potential results and store recursive call
    move_scores = {}

    for action in valid_moves:
        utility_coins = coins.copy()
        utility_foods = foods.copy()
        utility_potions = potions.copy()
        action_coins, action_potions, action_foods, action_player_score, action_player_stamina, action_player_hunger, action_hunger_dec_player, action_opponent_score, action_opponent_stamina, action_opponent_hunger, action_hunger_dec_opponent, action_position = action_utility(utility_coins, utility_potions, utility_foods, player_position, player_score, player_stamina, player_hunger, opponent_position, opponent_score, opponent_stamina, opponent_hunger, action, hunger_dec_player, hunger_dec_opponent, not turn)
        if(turn): #Player's turn
            move_scores[action] = recursive_minimax(dungeon_map, action_coins, action_potions, action_foods, action_position, action_player_score, action_player_stamina, action_player_hunger, opponent_position, action_opponent_score, action_opponent_stamina, action_opponent_hunger, action_hunger_dec_player, action_hunger_dec_opponent, action, not turn, recursion_depth + 1)
        else: #Opponent's turn
            move_scores[action] = recursive_minimax(dungeon_map, action_coins, action_potions, action_foods, player_position, action_player_score, action_player_stamina, action_player_hunger, action_position, action_opponent_score, action_opponent_stamina, action_opponent_hunger, action_hunger_dec_player, action_hunger_dec_opponent, action, not turn, recursion_depth + 1)

    print(move_scores)

    if(turn): #Player's turn, want to MAXIMIZE heuristic
        print("Max is " + str(max(move_scores)))
        return max(move_scores), max(move_scores, key=move_scores.get)
    else: #Opponent's turn, want to MINIMIZE heuristic
        print("Min is " + str(min(move_scores)))
        return min(move_scores), min(move_scores, key=move_scores.get)
