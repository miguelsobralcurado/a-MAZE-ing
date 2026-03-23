import sys
import time
import os
import random
# from config import load_config
from typing import Dict, Any, Tuple
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


def validate_keys(config: Dict[str, str]) -> None:
    try:
        required = ["WIDTH", "HEIGHT",
                    "ENTRY", "EXIT",
                    "OUTPUT_FILE", "PERFECT", "ALGORITHM"]
        for k in required:
            if k not in config:
                raise ValueError
    except ValueError:
        print(f"Error: Config file is missing required input: {k}",
              file=sys.stderr)
        sys.exit(1)


def validate_values(config: Dict[str, str]) -> None:
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        if config["ENTRY"] == config["EXIT"]:
            raise ValueError("Error: Entry and Exit cannot be in "
                             "the same position")
        y1, x1 = format_coords(config["ENTRY"])
        y2, x2 = format_coords(config["EXIT"])
        rows = [x1, x2]
        columns = [y1, y2]
        for r in rows:
            if r < 0 or r >= width:
                raise ValueError(f"Error: {r} not within maze bounds")
        for c in columns:
            if c < 0 or c >= height:
                raise ValueError(f"Error: {c} not within maze bounds")
        if config["ALGORITHM"] not in ["prim", "dfs"]:
            raise ValueError("Error: Invalid algorithm. Use prim or dfs")
        if (str.capitalize(config["PERFECT"]) != "True" and
            str.capitalize(config["PERFECT"]) != "False"):
            raise ValueError("Error: Invalid boolean value "
                             f"'{config["PERFECT"]}'. Expected True/False")
    except ValueError as e:
        print(e)
        sys.exit(1)


def parse_config(filepath: str) -> Dict[str, Any]:
    parsed = {}
    try:
        with open(filepath, "r") as config:
            for line_num, line in enumerate(config, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if "=" not in line:
                    raise ValueError
                k, v = line.split("=", 1)
                parsed[k.strip().upper()] = v.strip()
        validate_keys(parsed)
        validate_values(parsed)
        return parsed
    except (ValueError, FileNotFoundError, Exception) as e:
        if type(e) is ValueError:
            print("Error: Invalid syntax on line "
                  f"{line_num}: '{line}'.", file=sys.stderr)
            sys.exit(1)
        elif type(e) is FileNotFoundError:
            print(f"Error: Configuration file '{filepath}' not found.",
                  file=sys.stderr)
            sys.exit(1)
        elif type(e) is Exception:
            print(f"Error: An unexpected error has occurred: {e}",
                  file=sys.stderr)
            sys.exit(1)


def format_coords(to_format: str) -> Tuple[int, int]:
    try:
        x, y = map(int, to_format.split(","))
        return (y, x)
    except ValueError:
        print(f"Error: Invalid coordinate format '{to_format}'. "
              "Expected format: 'x,y'")
        sys.exit(1)


def format_bool(to_format: str) -> bool:
    value = True
    try:
        if to_format == "False":
            value = False
        return value
    except ValueError:
        print("Error: An unexpected error has occurred")


def format_maze(maze_grid: list[list[int]]) -> list[list[str]]:
    f_maze = maze_grid
    for row in f_maze:
        for cell in row:
            cell = hex(cell)
    print(f_maze)
    return f_maze


def create_output(maze_grid: list[list[int]],
                  output_fname: str,
                  maze: AsciiRender,
                  path_str: str = "") -> None:
    # f_maze = format_maze(maze_grid)
    try:
        with open(output_fname, "w") as file:
            for row in maze_grid:
                file.write("".join(f"{hex(cell)[2:].upper()}" for cell in row)
                           + "\n")
            file.write("\n")
            file.write(f"{maze.maze_entry[0]},{maze.maze_entry[1]}\n")
            file.write(f"{maze.maze_exit[0]},{maze.maze_exit[1]}\n")
            file.write(path_str + "\n")
    except IOError as e:
        print(f"Error: Unexpected error writing to file {e}")


if __name__ == "__main__":
    config = parse_config("config.txt")
    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    output_file = config["OUTPUT_FILE"]
    perfect = format_bool(str.capitalize(config["PERFECT"]))
    entry = format_coords(config["ENTRY"])
    exit = format_coords(config["EXIT"])
    seed_val = config["SEED"] if "SEED" in config else None
    algorithm = config["ALGORITHM"]
    command = ""
    color = False
    show_path = False
    generated = None
    gen_path = None
    comm_error = ""
    anim_speed = "off"
    anim_error = False
    animator = False
    seed = True
    debug = False
    maze_gen = MazeGenerator(width, height, entry, exit, seed_val,
                             perfect, algorithm)
#    gen_grid = maze_gen.maze_grid.cells
    logo = maze_gen.logo
    maze = AsciiRender(maze_gen.width, maze_gen.height,
                       maze_gen.entry, maze_gen.exit)
    speed_types = {"off": "", "slow": 0.3, "normal": 0.1, "fast": 0.03}
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
    grid = [[9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
            [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [8, 0, 4, 0, 4, 0, 4, 4, 4, 0, 2],
            [8, 2, 15, 10, 15, 10, 15, 15, 15, 8, 2],
            [8, 2, 15, 14, 15, 8, 5, 7, 15, 8, 2],
            [8, 2, 15, 15, 15, 10, 15, 15, 15, 8, 2],
            [8, 0, 1, 3, 15, 10, 15, 13, 5, 0, 2],
            [8, 0, 0, 2, 15, 10, 15, 15, 15, 8, 2],
            [8, 0, 0, 0, 1, 0, 1, 1, 1, 0, 2],
            [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [12, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6]]
    path = [["", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "C", "", "C", "", "C", "C", "C", "", ""],
            ["", "", "C", "", "C", "", "", "", "C", "", ""],
            ["", "", "C", "C", "C", "", "C", "C", "C", "", ""],
            ["", "", "", "", "C", "", "C", "", "", "", ""],
            ["", "", "", "", "C", "", "C", "C", "C", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", ""]]
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
    os.system('cls')
    print("Welcome to this a_MAZE_ing maze tester!")
    try:
        while True:
            if command == "q" or command == "quit":
                generated = None
                raise Error
            elif command == "t" or command == "test":
                generated = grid
                color_grid = is_42
                path_grid = path
                maze = AsciiRender(11, 13, (10, 2), (1, 9))
            elif command == "g" or command == "generate":
                if seed is True:
                    maze_gen = MazeGenerator(width, height, entry, exit,
                                             random.seed(), perfect, algorithm)
                else:
                    maze_gen = MazeGenerator(width, height,
                                             entry, exit, seed_val,
                                             perfect, algorithm)
                maze_generator = maze_gen.generate_maze()
                maze = AsciiRender(maze_gen.width, maze_gen.height,
                                   maze_gen.entry, maze_gen.exit)
                animate = Animator(maze)
                color_grid = maze.set_colors(logo)
                path_grid = None
                if animator is True:
                    animate.load_maze(color, speed_types[anim_speed])
                for next in maze_generator:
                    generated = next
                    if animator is True:
                        animate.print_frame(generated,
                                            path_grid,
                                            color_grid,
                                            color)
                        time.sleep(speed_types[anim_speed])
                    os.system('cls')
                if animate.curr_load < animate.max_load:
                    animate.curr_load = animate.max_load
                path_output = maze_gen.solve(generated,
                                             maze_gen.entry,
                                             maze_gen.exit)
                if show_path is True:
                    animate.curr_load = 0
                    animate.anim_path(path_output, color,
                                      speed_types[anim_speed])
                create_output(generated, output_file, maze, path_output[1])
            elif command == "p" or command == "path":
                if show_path is False:
                    show_path = True
                else:
                    show_path = False
            elif command == "perf" or command == "perfect":
                if perfect is False:
                    perfect = True
                else:
                    perfect = False
            elif command == "algo" or command == "algorithm":
                if algorithm == "dfs":
                    algorithm = "prim"
                elif algorithm == "prim":
                    algorithm = "dfs"
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
            elif command == "debug":
                if debug is False:
                    debug = True
                else:
                    debug = False
            elif command:
                comm_error = "Error - Invalid command"
            if generated is not None:
                if show_path is False:
                    maze.draw_maze(generated, None)
                    maze.builder(color_grid, color)
                else:
                    if path_grid == path:
                        maze.draw_maze(generated, path_grid)
                        maze.builder(color_grid, color)
                    else:
                        maze.draw_maze(generated, path_output)
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
            print(" 'perf' or 'perfect' - Toggles perfect maze generation")
            print(" 'algo' or 'algorithm' - Toggles algorithm used")
            print(" 'debug' - Toggles detailed flag settings")
            print(" 'q' or 'quit' - Quits the program")
            print()
            if debug is True:
                if perfect is True:
                    print("# The maze will generate a perfect path")
                else:
                    print("# The maze will generate an imperfect path")
                if seed is False:
                    print("# The maze will generate from the config seed")
                if show_path is True:
                    print("# Animator will show the pathing process")
                if anim_speed != "off":
                    print(f"# Animator speed is set to {anim_speed}")
                print(f"# Current algorithm being used: {algorithm}")
                print(f"# Current seed generated: {maze_gen.seed}")
                print()
                print("# Debug is showing current setting toggles")
            command = str.casefold(input("Choose a command: "))
            if command == "a" or command == "animate":
                while anim_speed in speed_types.keys():
                    print()
                    print("Please select the speed of the animation:")
                    print(" 0 - Stop animator")
                    print(" 1 - Slow speed")
                    print(" 2 - Normal speed")
                    print(" 3 - Fast speed")
                    print()
                    anim_speed = str.casefold(input("Animation speed = "))
                    if anim_speed == "1":
                        anim_speed = "slow"
                        break
                    elif anim_speed == "2":
                        anim_speed = "normal"
                        break
                    elif anim_speed == "3":
                        anim_speed = "fast"
                        break
                    elif anim_speed == "0":
                        anim_speed = "off"
                        break
                    else:
                        if anim_error is False:
                            print("\033[F\033[2K" * 8, end="", flush=True)
                            anim_error = True
                        else:
                            print("\033[F\033[2K" * 10, end="", flush=True)
                        print()
                        print("Error - Invalid command")
                        anim_speed = "off"
                anim_error = False
            if comm_error != "":
                comm_error = ""
            os.system('cls')
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
