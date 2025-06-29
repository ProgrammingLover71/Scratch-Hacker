from random import randint
from typing import Any
from math import sin, cos, radians

###### MOTION ######
direction: float = 90.0
x_position: float = 0.0
y_position: float = 0.0 

def move_steps(steps: float) -> None:
    global x_position, y_position
    x_position += steps * cos(radians(direction))
    y_position += steps * sin(radians(direction))

def turn_degrees(degrees: float) -> None:
    global direction
    direction += degrees


###### LOOKS ######
def say(message: Any) -> None:
    print(message)

def say_for_secs(message: Any, seconds: float) -> None:
    print(f"{message} (for {seconds} seconds)")


###### OPERATORS ######
def random_int(min_value: float, max_value: float) -> int:
    return randint(int(min_value), int(max_value))