


# Architectural Design

## Game
The Battleship game is run by a main game function that controls the GUI and game data.

![AD Diagram](https://github.com/mpzinke/Battleship/blob/master/Documentation/Images/ArchitecturalDesign.png)

[DESCRIPTION]

1. The GUI will send user input to the Game module.
2. The Game module will tell the GUI what displays to update.
3. The Game module will process input information from the GUI and from the player to control the player data
4. The player data will send updates and information on move results to the Game module


## Classes

### Game Data
- Game
- Player
- Ship
### GUI
- Window
- Board
- Field
- Ocean
- Status
