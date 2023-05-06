# Overiew
Simple Python implementation of cellular automata using Tkinter for GUI

Interface to upload/create automata is not implemented yet, but you can directly pass automata in a form of JSON file. Example can be found in "automata" directory.

**Left click on the cell** — changes state of a cell.

**Save** —  saves current state of a board as .txt file.  

**Load** — loads .txt file into a state of a board. 

Repository comes with a few pre-saved interesting patterns which you can run.

**Next step** — creates and renders next iteration of a board.

**Randomize** — creates and renders board randomly filled with dead and alive cells.

**Simulate** — creates next iteration of a board every 100 ms, if simulation is already running, then pressing button again will stop it. 

**Clear** — clears the board.




![image](https://user-images.githubusercontent.com/117105291/236638453-03b0b8bc-5e47-4a0f-aed3-c74695d11ebf.png)



# Installation 
To run you need to simply clone repo, and run in a directory using terminal:
```
python3 main.py
```
