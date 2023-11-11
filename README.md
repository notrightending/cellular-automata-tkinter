
# Cellular Automata Tkinter

This project is a cellular automata simulator built with Python and Tkinter. It allows users to create, visualize, and interact with cellular automata in a grid-based environment. 

![image](https://github.com/NightPuppet/cellular-automata-tkinter/assets/117105291/450ab211-6aed-4b4a-a2b5-0481324fdd5d)

## Features

The application provides a simple and intuitive graphical user interface (GUI) for users to interact with cellular automata.

### Toolbar Buttons

The toolbar provides the following buttons to control the simulation:

- **Next step**: Advances the simulation by one generation. This button is useful for observing the evolution of the cellular automata step-by-step.
- **Randomize**: Fills the grid with random cell states, providing a starting point for exploring different patterns and behaviors.
- **Simulate**: Starts the simulation and updates the grid according to the defined rules. If simulation is already running, pressing the button will stop it.
- **Clear**: Clears the grid.

### Menu options
Menu provides following buttons:
- #### Board
  - **Save board**: Saves current state of a board as .txt file
  - **Load board**: Loads choosen .txt file as current state of a board   
- #### Automata
  - **Create automata**: Opens text box which allows to create custom automata.
  - **Edit automata**: Opens text box allowing to edit existing automata
  - **Load automata**: Loads .json as automata to use for simulation.


### Automata creation

To create automata you need to press **Create Automata**, after this textbox will appear, textbox will already have filled template inside it:
1. States and their transition conditions should be located as a value of "transition" key. Also, its advised to add "default" key inside of every state, so you can define as little conditions as possible.   
2. When defining conditions remember, that main principle is that every cell always has 8 neighbours. Keys inside of state are indicating how much neighbours current state should have to transition for specific state.
  Example: 
  ```
  {
        "transition": [{"53": 1, "default": 0}, {"53": 1, "62": 1, "default": 0}],
        "state_color": ["white", "black"]
  }
  ```
  Inside ["transition"][0] we have following line: "53": 1, "default": 0  
  This can be translated as: if current state of a cell is "0", and it has 5 cells with state "0" and 3 states with state "1", then it will transition to state "1", else it will transition to state "0"  
  
 3. If your automata has more than two states, you might need to iterate conditions inside of the state, example:
```
{
        "transition": [
            {
                "026": 1,
                "125": 1,
                "224": 1,
                "323": 1,
                "422": 1,
                "521": 1,
                "620": 1,
                "default": 0
            },
            {
                "default": 2
            },
            {
                "default": 0
            }
        ],
        "state_color": ["white", "black", "blue"]
}
```
4. Colors of the states are matched with corresponding state. For example cell with state "2" will be automatically matched with a ["state_color"][2]



### Grid Interaction

Users can interact with the grid by clicking. Clicking on a cell toggles its state and fills cell with a choosen color.

## Installation and Running the Application

To install and run the cellular automata simulator, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/NightPuppet/cellular-automata-tkinter.git
   ```

2. Change to the project directory:

   ```
   cd cellular-automata-tkinter
   ```

3. Run the application:

   ```
   python main.py
   ```
4. Press "Automata" and "Load automata", choose one of the existing automatas. 



