from random import randint
from typing import Any
from math import sin, cos

direction: float = 90.0
x_position: float = 0.0
y_position: float = 0.0

def move_steps(steps: float) -> None:
    global x_position, y_position
    x_position += steps * cos(direction * (3.141592653589793 / 180))
    y_position += steps * sin(direction * (3.141592653589793 / 180))

def turn_degrees(degrees: float) -> None:
    global direction
    direction += degrees

def say(message: Any) -> None:
    print(message)

def say_for_secs(message: Any, seconds: float) -> None:
    print(f"{message} (for {seconds} seconds)")

def random_int(min_value: float, max_value: float) -> int:
    return randint(int(min_value), int(max_value))