# Game Rules and Bot Framework

## Introduction
This project is a two-player strategy game where players compete to dominate the map by controlling cities and defeating their opponent's capital. The game is turn-based, with both players executing their strategies simultaneously. Bots are used to automate gameplay, and developers can create custom bots to participate.

## Table of Contents
- [Game Rules](#game-rules)
- [Classes and API](#classes-and-api)
  - [Game](#game)
  - [City](#city)
  - [Capital](#capital)
  - [Group](#group)
  - [Player](#player)
  - [Bot](#bot)
- [Bot Implementation Guidelines](#bot-implementation-guidelines)
- [Example Code](#example-code)

## Game Rules
1. **Map Setup**: 
   - The map includes neutral cities and two starting capitals, one for each player.
   - All other cities start as neutral.

2. **Gameplay**:
   - Each player takes turns simultaneously.
   - During a turn, each city can either:
     1. Send soldiers to another city.
     2. Upgrade itself.

3. **Victory Conditions**:
   - The game ends if:
     1. A player captures the opponent's capital.
     2. 300 turns pass.
     3. A player crashes or fails to act within allowed limits.
   - If 300 turns elapse, the player with more cities wins. If the number is equal, the game ends in a draw.

## Classes and API

### Game
Represents the game's state and provides information to bots.

#### Properties
- **`turn`**: The current turn number (1-300).

#### Methods
- **`get_enemy_cities()`**: Returns a list of the opponent's cities (excluding their capital).
- **`get_enemy_city_capital()`**: Returns the opponent's capital.
- **`get_enemy_groups()`**: Returns a list of the opponent's groups.
- **`get_my_cities()`**: Returns a list of the player’s cities (excluding their capital).
- **`get_my_city_capital()`**: Returns the player’s capital.
- **`get_my_groups()`**: Returns a list of the player’s groups.
- **`get_neutral_cities()`**: Returns a list of neutral cities.

---

### City
Represents a city in the game.

#### Properties
- **`level`**: The city's level.
- **`people_amount`**: Number of people in the city.
- **`position`**: The city's coordinates (for reference only).

#### Methods
- **`get_turns_till_arrival(destination)`**: Returns the number of turns to reach the destination city.
- **`send_group(destination, people_amount)`**: Sends a group of people to a destination.
- **`upgrade()`**: Upgrades the city.
- **`can_upgrade()`**: Returns whether the city can be upgraded.
- **`can_send_group(people_amount)`**: Checks if the city can send the specified number of people.
- **`get_distance_to(destination)`**: Returns the distance to another city.

---

### Capital
Currently behaves like a regular city but may be expanded with unique features in future updates. 

For now, it inherits all properties and methods from the **City** class.

---


### Group
Represents a group of people traveling between cities.

#### Properties
- **`people_amount`**: Number of people in the group.
- **`source`**: The city the group departed from.
- **`destination`**: The city the group is heading to.
- **`turns_till_arrival`**: Turns left until arrival.
- **`position`**: The group's current position.
- **`speed`**: Speed of the group.

---

### Player
The **Player** class is not currently part of the API but may be added in future updates. Once implemented, it is expected to manage player-specific data such as their cities, groups, and overall strategy.

---

### Bot
Represents the bot controlling a player's actions.

#### Implementation Notes
- The bot must implement the `do_turn()` method.
- Bots must inherit from the `Bot` class.
- Place the bot implementation in a file named `main.py`.
- The bot class must be named `MyBot`.

---

## Bot Implementation Guidelines
1. **Forbidden Imports**: The following modules/functions are prohibited:
   - `"os"`, `"Engine"`, `"open"`, `"pathlib"`, `"sys"`, `"eval"`, `"TimeoutError"`, `"input"`, `"socket"`, `"json"`, `"yaml"`
2. **Runtime Limitations**: Bots have a maximum runtime of 2 seconds per turn.
3. **Exceptions**: Using except Exception, in this too broad of an expression is forbidden.
4. **Efficiency**: Write efficient code to avoid timeouts or crashes.

---

## Example Code
The document includes a sample bot implementation and demonstrates the structure of the `do_turn()` function. Refer to the provided example for details.

---

