import random
def player1_logic(coins, potions, foods, dungeon_map, self_position, other_agent_position):
    # Directions are mapped to 'W', 'A', 'S', 'D'
    directions = {'W': (0, -1), 'A': (-1, 0), 'S': (0, 1), 'D': (1, 0)}
    
    # Get current position of the agent
    x, y = self_position
    
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
    
    # If there are no valid moves, return 'I' to remain idle
    if not valid_moves:
        return 'I'
    
    for action in valid_moves:
        action_coins, action_potions, action_foods, action_player_score, action_player_stamina, action_player_hunger, action_hugerdec = action_utility(coins, potions, foods, self_position, 0, 50, 50, action, False)
        print("test")
    # Randomly choose from the valid moves
    return random.choice(valid_moves)

    #Implementing minimax
    #Need to do a depth first search
    #First, create a utility function to evaluate the "goodness" of an action 


def action_utility(coins, potions, foods, player_position, player_score, player_stamina, player_hunger, action_position, hunger_dec): #Evaluates a given acition for its "goodness" based on number of coins left, score of each player, etc. 
    # Evaluates the results of a given action and returns appropriate values

    #Decrement stamina for movement
    if(player_position != action_position): #Ensure this is not an idle action
        player_stamina -= 1

    #Decrement stamina for hunger
    if(player_hunger == 0):
        player_stamina -= 1

    #Decrement hunger if hunger was not decremented on previous turn
    if(not hunger_dec): #If hunger was not decremented on previous turn
        hunger_dec = True
        player_hunger -= 1
    else: #Hunger was decremented on previous turn
        hunger_dec = False

    #Check for items 
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
        
    return coins, potions, foods, player_score, player_stamina, player_hunger, hunger_dec
