from scratch_hacker import *

def main():
    my_var = (1.0 + 1.0)
    my_var += my_var
    while True:
        move_steps((my_var - (6.0 + 2.0)))
        turn_degrees(random_int((my_var / 4.0), ((my_var + 1.0) * (7.0 / 3.0))))
        say_for_secs(my_var, 0.0)
        say(direction)
        if (direction > 50.0):
            my_var += (my_var / (1.34 * 5.323))
            say("A")


if __name__ == '__main__':
	main()
	exit(0)
