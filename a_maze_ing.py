# import sys
import time
import os
import random
# from config import load_config
from maze_generator import MazeGenerator
from render_test import AsciiRender, Animator


# def main(argv: list[str]) -> int:
#     try:
#         with open(argv[1]) as cfg:
#         gen = MazeGenerator()
#         while True:
#             if gen.visual is True:
#                 iter = gen.Generate()
#                 animate_gen(iter)
#                 time.sleep(anim_speed)
#             if gen.Complete is True:
#                 break
#     except FileNotFoundError:
#         print("Usage: python3 a_maze_ing.py <config file path>",
#               file=sys.stderr)
#         return 2


class Error(Exception):
    def __init__(self, *args):
        super().__init__(*args)


# def parse_config():
#     try:
#         with open("config.txt", "r") as config:
#             if


if __name__ == "__main__":

    command = ""
    color = False
    show_path = False
    gen_maze = None
    gen_path = None
    comm_error = ""
    anim_speed = ""
    anim_error = False
    animator = False
    seed = True
    seed_val = 238576
    maze_gen = MazeGenerator(11, 11, (0, 0), (10, 10), 238576)
    maze_grid = maze_gen.initialize()
    gen_grid = maze_grid.cells
    logo = maze_gen.logo
    maze = AsciiRender(maze_gen.width, maze_gen.height,
                       maze_gen.entry, maze_gen.exit)
    speed_types = {"slow": 0.3, "normal": 0.1, "fast": 0.03}
    test_grid = [[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                 [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 12]]
    grid = [[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [2, 0, 4, 0, 4, 0, 4, 4, 4, 0, 8],
            [2, 8, 15, 10, 15, 10, 15, 15, 15, 2, 8],
            [2, 8, 15, 14, 15, 2, 5, 13, 15, 2, 8],
            [2, 8, 15, 15, 15, 10, 15, 15, 15, 2, 8],
            [2, 0, 1, 9, 15, 10, 15, 7, 5, 0, 8],
            [2, 0, 0, 8, 15, 10, 15, 15, 15, 2, 8],
            [2, 0, 0, 0, 1, 0, 1, 1, 1, 0, 8],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 12]]
    path = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    is_42 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
             [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
             [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    os.system('clear')
    print("Welcome to this a_MAZE_ing maze tester!")
    try:
        while True:
            if command == "q" or command == "quit":
                gen_maze = None
                raise Error
            elif command == "t" or command == "test":
                gen_maze = grid
                color_grid = is_42
                path_grid = path
                maze = AsciiRender(11, 13, (10, 2), (1, 9))
            elif command == "g" or command == "generate":
                if seed is True:
                    maze_gen = MazeGenerator(11, 11, (0, 0), (10, 10),
                                             random.seed())
                else:
                    maze_gen = MazeGenerator(11, 11,
                                             (0, 0), (10, 10), seed_val)
                maze_generated = maze_gen.generator_method
                maze = AsciiRender(maze_gen.width, maze_gen.height,
                                   maze_gen.entry, maze_gen.exit)
                animate = Animator(maze)
                color_grid = maze.set_colors(logo)
                path_grid = None
                for _ in maze_generated:
                    gen_maze = next(maze_generated)
                    if animator is True:
                        animate.print_frame(gen_maze,
                                            path_grid,
                                            color_grid,
                                            color)
                        time.sleep(speed_types[anim_speed])
                    os.system('clear')

            elif command == "p" or command == "path":
                if show_path is False:
                    show_path = True
                else:
                    show_path = False
            elif command == "c" or command == "color":
                if color is False:
                    color = True
                else:
                    color = False
            elif command == "a" or command == "animate":
                if animator is False:
                    animator = True
                else:
                    animator = False
            elif command == "s" or command == "seed":
                if seed is False:
                    seed = True
                else:
                    seed = False
            elif command:
                comm_error = "Error - Invalid command"
            if gen_maze is not None:
                if show_path is False:
                    maze.draw_maze(gen_maze, None)
                    maze.builder(color_grid, color)
                else:
                    maze.draw_maze(gen_maze, path_grid)
                    maze.builder(color_grid, color)
            print()
            if comm_error != "":
                print("\x1b[0m" + comm_error)
                print()
            print("\x1b[0m" + "Available commands:")
            print(" 'g' or 'generate' - Generates a new maze")
            print(" 'p' or 'path' - Displays the shortest path")
            print(" 'c' or 'color' - Changes to the alt maze color")
            print(" 't' or 'test' - Generates an unsolvable test maze")
            print(" 'a' or 'animate' - Animates the next generation")
            print(" 's' or 'seed' - Toggles generation using the seed "
                  "in config.txt")
            print(" 'q' or 'quit' - Quits the program")
            print()
            if seed is True:
                print("# The maze will generate from the config seed")
            if show_path is True:
                print("# Animator will show the pathing process...")
            if anim_speed != "":
                print(f"# Animator speed is set to {anim_speed}")
            command = str.casefold(input("Choose a command: "))
            if command == "a" or command == "animate":
                if anim_speed == "":
                    while anim_speed not in speed_types.keys():
                        print()
                        print("Please select the speed of the animation:")
                        print(" 1 - Slow speed")
                        print(" 2 - Normal speed")
                        print(" 3 - Fast speed")
                        print()
                        anim_speed = str.casefold(input("Animation speed = "))
                        if anim_speed == "1":
                            anim_speed = "slow"
                        elif anim_speed == "2":
                            anim_speed = "normal"
                        elif anim_speed == "3":
                            anim_speed = "fast"
                        else:
                            if anim_error is False:
                                print("\033[F\033[2K" * 7, end="", flush=True)
                                anim_error = True
                            else:
                                print("\033[F\033[2K" * 9, end="", flush=True)
                            print()
                            print("Error - Invalid command")
                            anim_speed = ""
                else:
                    anim_speed = ""
                anim_error = False
            if comm_error != "":
                comm_error = ""
            os.system('clear')
    except (KeyboardInterrupt, Error) as e:
        if type(e) is KeyboardInterrupt:
            print("\x1b[0m" + "\n\nForcibly exiting program...\n")


# print("\033[F\033[2K" * n, end="", flush=True) (clears n amount of lines)
# 0  = all open
# 1  = N closed
# 2  = E closed
# 3  = NE closed
# 4  = S closed
# 5  = NS closed
# 6  = ES closed
# 7  = NES closed
# 8  = W closed
# 9  = NW closed
# 10 = EW closed
# 11 = NEW closed
# 12 = SW closed
# 13 = NSW closed
# 14 = ESW closed
# 15 = NESW closed
