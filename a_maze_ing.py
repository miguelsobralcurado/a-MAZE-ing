import sys
import time
import os
import random
from typing import Dict, Any
from mazegen import MazeGenerator
from render_ascii import AsciiRender, Animator

Coord = tuple[int, int]
PathGrid = list[list[str]]
CellGrid = list[list[int]]


class Error(Exception):
    """Custom exception for maze validation and runtime errors."""
    def __init__(self, message: str) -> None:
        """Initialize the exception with a human-readable message.

        Args:
            message: Error message describing the failure.
        """
        super().__init__(message)


def validate_keys(config: Dict[str, str]) -> None:
    """Validate that all required configuration keys are present.

    Args:
        config: Parsed configuration mapping from key to raw string value.

    Raises:
        SystemExit: If any required key is missing.
    """
    try:
        required = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "ALGORITHM"
        ]
        for k in required:
            if k not in config:
                raise ValueError
    except ValueError:
        print(f"Error: Config file is missing required input: {k}",
              file=sys.stderr)
        sys.exit(1)


def validate_values(config: Dict[str, str]) -> None:
    """Validate configuration values after parsing.

    This function checks maze dimensions, entry/exit positions, and the
    selected generation algorithm.

    Args:
        config: Parsed configuration mapping from key to raw string value.

    Raises:
        SystemExit: If any configuration value is invalid.
    """
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
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def validate_logo(logo_coords: set[Coord] | None,
                  entry: Coord,
                  exit: Coord) -> None:
    """Ensure entry and exit do not overlap blocked logo coordinates.

    Args:
        logo_coords: Set of blocked coordinates occupied by the embedded logo,
            or `None` if no logo was generated.
        entry: Maze entry coordinate as `(row, column)`.
        exit: Maze exit coordinate as `(row, column)`.

    Raises:
        SystemExit: If the entry or exit overlaps a logo coordinate.
    """
    try:
        if logo_coords is not None:
            for coord in logo_coords:
                if coord == entry:
                    raise Error("Error: Entry cannot be on top of the 42 logo")
                if coord == exit:
                    raise Error("Error: Exit cannot be on top of the 42 logo")
    except Error as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def parse_config(filepath: str) -> Dict[str, Any]:
    """Parse a key-value configuration file.

    Blank lines and comment lines beginning with `#` are ignored.
    Keys are normalized to uppercase.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A dictionary of configuration keys to raw string values.

    Raises:
        SystemExit: If the file cannot be read, contains invalid syntax, or
            fails semantic validation.
    """
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
    return {}


def format_coords(to_format: str) -> Coord:
    """Parse a coordinate string in `x,y` format into internal `(row, column)`.

    The input uses `x,y`, but the internal maze representation uses `(y, x)`.

    Args:
        to_format: Coordinate string formatted as `x,y`.

    Returns:
        A coordinate tuple as `(row, column)`.

    Raises:
        SystemExit: If the coordinate format is invalid.
    """
    try:
        x, y = map(int, to_format.split(","))
        return (y, x)
    except ValueError:
        print(f"Error: Invalid coordinate format '{to_format}'. "
              "Expected format: 'x,y'", file=sys.stderr)
        sys.exit(1)


def format_maze(maze_grid: CellGrid) -> PathGrid:
    """Convert an integer maze grid into an uppercase hexadecimal string grid.

    Each integer cell is transformed into its hexadecimal representation
    without the `0x` prefix.

    Args:
        maze_grid: Maze grid encoded as integer wall bitmasks.

    Returns:
        A new grid where each cell is represented as an uppercase hexadecimal
        string.
    """
    f_maze: list[list[Any]] = maze_grid
    for row in f_maze:
        for cell in row:
            cell = hex(cell)
    print(f_maze)
    return f_maze


def create_output(maze_grid: CellGrid,
                  output_fname: str,
                  maze: AsciiRender,
                  path_str: str = "") -> None:
    """Write the generated maze and optional solution path to an output file.

    The file format is:

    1. Maze rows encoded as uppercase hexadecimal digits.
    2. A blank line.
    3. Entry coordinate as `row,column`.
    4. Exit coordinate as `row,column`.
    5. Optional path string using directional letters.

    Args:
        maze_grid: Final generated maze grid.
        output_fname: Destination output file path.
        maze: ASCII renderer instance providing entry and exit coordinates.
        path_str: Optional solution string using directional characters.

    Raises:
        None explicitly. Errors are reported to standard error.
    """
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
        print(f"Error: Unexpected error writing to file {e}", file=sys.stderr)


def main() -> None:
    """Run the interactive maze generation and visualization program.

    The program:

    - parses the configuration file passed on the command line,
    - creates a maze generator and ASCII renderer,
    - allows interactive generation and visualization,
    - optionally animates the generation and path solving,
    - writes the latest generated maze to the configured output file.

    Raises:
        None explicitly. Fatal errors terminate the process with `sys.exit`.
    """
    if len(sys.argv) != 2:
        print("Error: Incorrect number of arguments called. Expected 1",
              file=sys.stderr)
        sys.exit(1)

    config = parse_config(sys.argv[1])

    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    output_file = config["OUTPUT_FILE"]
    perfect = config["PERFECT"] == "True"
    entry = format_coords(config["ENTRY"])
    exit = format_coords(config["EXIT"])
    seed_val = int(config["SEED"]) if "SEED" in config else 0
    algorithm = config["ALGORITHM"]

    command = ""
    color = False
    show_path = False
    generated: CellGrid = []
    comm_error = ""
    anim_speed = "off"
    anim_error = False
    animator = False
    seed = True
    debug = False
    maze_seed = 0

    maze_gen = MazeGenerator(width, height, entry, exit, seed_val,
                             perfect, algorithm)
    logo = maze_gen.logo

    validate_logo(logo, entry, exit)

    maze = AsciiRender(maze_gen.width, maze_gen.height,
                       maze_gen.entry, maze_gen.exit)

    speed_types: dict[str, float] = {
        "off": 0,
        "slow": 0.3,
        "normal": 0.1,
        "fast": 0.03
    }
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
    os.system('clear')
    print("Welcome to this a_MAZE_ing maze tester!")
    try:
        while True:
            if command == "q" or command == "quit":
                generated = []
                sys.exit(1)
            elif command == "t" or command == "test":
                generated = grid
                color_grid = is_42
                path_grid = path
                maze = AsciiRender(11, 13, (10, 2), (1, 9))
            elif command == "g" or command == "generate":
                if seed is True:
                    maze_seed = random.randint(0, 99999999)
                    maze_gen = MazeGenerator(width, height, entry, exit,
                                             maze_seed, perfect,
                                             algorithm)
                else:
                    maze_seed = seed_val
                    maze_gen = MazeGenerator(width, height,
                                             entry, exit, seed_val,
                                             perfect, algorithm)
                maze_generator = maze_gen.generate_maze()
                maze = AsciiRender(maze_gen.width, maze_gen.height,
                                   maze_gen.entry, maze_gen.exit)
                animate = Animator(maze)
                color_grid = maze.set_colors(logo)
                path_grid = []
                if animator is True:
                    animate.load_maze(color)
                for next in maze_generator:
                    generated = next
                    if animator is True:
                        animate.print_frame(generated,
                                            path_grid,
                                            color_grid,
                                            color)
                        time.sleep(speed_types[anim_speed])
                    os.system('clear')
                if animate.curr_load < animate.max_load:
                    animate.curr_load = animate.max_load
                path_output = maze_gen.solve(generated,
                                             maze_gen.entry,
                                             maze_gen.exit)
                if show_path is True and animator is True:
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
            if len(generated) > 0:
                if show_path is False:
                    maze.draw_maze(generated, None)
                    maze.builder(color_grid, color)
                else:
                    if path_grid == path:
                        maze.draw_maze(generated, path_grid)
                        maze.builder(color_grid, color)
                    else:
                        path_grid = maze.draw_path(maze.blank_grid("str"),
                                                   path_output)
                        maze.draw_maze(generated, path_grid)
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
                print(f"# Current seed generated: {maze_seed}")
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
                    anim_input = str.casefold(input("Animation speed = "))
                    if anim_input == "1":
                        anim_speed = "slow"
                        break
                    elif anim_input == "2":
                        anim_speed = "normal"
                        break
                    elif anim_input == "3":
                        anim_speed = "fast"
                        break
                    elif anim_input == "0":
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
            os.system('clear')
    except (KeyboardInterrupt, Error) as e:
        if type(e) is KeyboardInterrupt:
            print("\x1b[0m" + "\n\nForcibly exiting program...\n")


if __name__ == "__main__":
    main()
