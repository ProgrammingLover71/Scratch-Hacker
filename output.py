from scratch_hacker import *

def main():
    my_var = (1 + 1)
    my_var += my_var
    move_steps((my_var - (6 + 2)))
    turn_degrees(random_int((my_var / 4), ((my_var + 1) * (7 / 3))))
    say(direction)
    say_for_secs(my_var, 2)

if __name__ == '__main__':
	main()
	exit(0)
