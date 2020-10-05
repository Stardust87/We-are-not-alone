# We are not alone
## Overview
_We are not alone_ is a shooter game made in Python using PyGame and LiveWires libraries. Action takes place in the space and concerns fight between player (_rocket_) and aliens (their _spaceships_).  All the graphics has been created by author in PaintNet.

## Installation
 Below a few console commands to run a game  
  ``` 
  git clone https://github.com/Stardust87/We-are-not-alone.git 
 cd We-are-not-alone/
pip install livewires/
pip install pygame
python main.py
```

## Rules and controls

After running `main.py` file user will see on the splash screen instruction refering to game control. 
 A few general informations:
 * pressing _enter_ start new game.
 * player character is a rocket
 * rocket shoot with laser projectiles after pressing _space_
* rocket moves with an arrows ← → ↑ ↓
* maximum health value displayed on rocket life bar is 100%
* alien spaceships shoot with ball missiles in two sizes (small and big)
* both alien missiles and collisions with aliens decrease rocket health
* taking a repair kit increase rocket health
* game can end in two scenarios 
	* rocket destroys all alien spaceships and win
	* rocket loses all health and lose 
* after game ending player see splash screen again and can start new game
