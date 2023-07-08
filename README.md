# Tetris
Fundamentals of Programming Project: "Create a game using tkinter python library and OOP".

### Gameplay Notes: 
- Ensure capslock is off.
- Every 300 points the game gets faster, and every 500 points the grid gets smaller by adding an indestructible row at the bottom.
- Various cheats to overcome obstacles provided in the Details menu.
- You can get a hidden easter egg by mashing the "w" key while playing (a bug found during development made into a feature).

### Functionality Overview
As the usage of tkinter was enforced, the grid logic consts of a 2D-Array which uses numbers to represent colors in order to generate borders and blocks. The turtle pen uses the colors and coordinate system to draw over the screen every gameloop. Similar to the grid, the blocks use the 2D-Array system for compatibilty in logic and manipulation. The game functions just like traditional tetris aside from a few additional challenges.

### Known Bugs
- Details menu does not dynamically resize according to screen size.
- Rotating shapes at the exact moment they land causes an error in the grid logic causing shapes to dissapear (or crash the game if it's the bottom of the grid).
- Bosskey functionality is bugged.
- Restart game causes two music instances to play.
