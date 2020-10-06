# We are not alone

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Overview
_We are not alone_ is a shooter game made in Python using PyGame and LiveWires libraries. Action takes place in the space and concerns fight between player (_rocket_) and aliens (their _spaceships_).  All the graphics has been created by author in PaintNet.

## Requirements

[![Generic badge](https://img.shields.io/badge/Python-3.x-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/PyGame-1.9.5-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/LiveWires-2.0-<COLOR>.svg)](https://shields.io/)

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

 ## Sample graphics
 
![graphic1](https://github.com/Stardust87/We-are-not-alone/blob/main/assets/screen4.png)
