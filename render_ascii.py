import os
import time
import random
from typing import Optional, Any

Coord = tuple[int, int]
PathGrid = list[list[str]]
CellGrid = list[list[int]]


class AsciiRender:
    """Render a maze grid as styled ASCII/Unicode art.

    This class converts the internal maze bitmask representation into a
    multi-line textual view suitable for terminal output. It can also overlay
    a path and apply colors for the entry, exit, and optional blocked logo.
    """
    def __init__(self, width: int, height: int,
                 maze_entry: Coord, maze_exit: Coord) -> None:
        """Initialize the renderer for a maze of a given size.

        Args:
            width: Number of maze columns.
            height: Number of maze rows.
            maze_entry: Entry coordinate as `(row, column)`.
            maze_exit: Exit coordinate as `(row, column)`.
        """
        self.width = width
        self.height = height
        self.maze_entry = maze_entry
        self.maze_exit = maze_exit

    def set_proportions(self, width: int, height: int) -> None:
        """Update the renderer dimensions.

        Args:
            width: New number of maze columns.
            height: New number of maze rows.
        """
        self.width = width
        self.height = height

    def blank_grid(self, type: str = "int") -> list[list[Any]]:
        """Create an empty grid matching the renderer dimensions.

        Args:
            grid_type: Type of blank grid to produce:
                - `"int"` for an integer grid filled with `0`
                - `"str"` for a string grid filled with `""`

        Returns:
            A 2D grid of the requested type.

        Raises:
            ValueError: If `grid_type` is not `"int"` or `"str"`.
        """
        grid: list[list[Any]] = []
        for i in range(self.height):
            grid.append([])
            for _ in range(self.width):
                if type == "int":
                    grid[i].append(0)
                elif type == "str":
                    grid[i].append("")
        return grid

    def draw_maze(self,
                  grid: CellGrid,
                  path: Optional[PathGrid] = None) -> None:
        """Convert a maze grid into renderable character pieces.

        This method populates `self.maze_pieces`, where each maze cell becomes
        a five-line Unicode representation. If a path grid is provided, the
        corresponding path glyph is drawn in each cell.

        Args:
            grid: Maze cell grid encoded as wall bitmasks.
            path: Optional grid of path markers aligned with the maze grid.
        """
        self.maze_pieces: list[list[list[str]]] = []
        self.maze_color: CellGrid = []
        x = 0
        y = 0
        path_grid: list[list[Any]] = []
        if isinstance(path, list) and len(path) > 0:
            path_grid = path
        else:
            path_grid = self.blank_grid("str")
        for row in grid:
            r = []
            for _ in row:
                r.append(self.calc_piece(grid[y][x],
                                         path_grid[y][x],
                                         x,
                                         y))
                x += 1
            self.maze_pieces.append(r)
            x = 0
            y += 1

    def draw_path(self,
                  empty_grid: PathGrid,
                  f_path: tuple[list[Coord], str]) -> PathGrid:
        """Overlay a solution path onto a blank string grid.

        Each coordinate in the solution path is annotated with the direction
        letter that should be displayed at that position. The final coordinate
        may remain empty if the path string is shorter than the coordinate
        list.

        Args:
            empty_grid: Preallocated empty string grid.
            f_path: Tuple containing:
                - an ordered list of coordinates
                - a direction string using `N`, `E`, `S`, `W`, and optionally
                `C` for current.

        Returns:
            The same grid object with path markers written into it.
        """
        i = 0
        coords, string = f_path
        for coord in coords:
            y, x = coord
            if i < len(string):
                empty_grid[y][x] = string[i]
            i += 1
        return empty_grid

    def calc_piece(self, curr_cell: int,
                   path: Optional[str] = None,
                   x: int = 0, y: int = 0) -> list[str]:
        """Convert one maze cell into a 5-line Unicode drawing.

        The input cell uses bitmask walls:

        - 1 = NORTH wall
        - 2 = EAST wall
        - 4 = SOUTH wall
        - 8 = WEST wall

        A cleared bit means an opening exists in that direction.

        Args:
            curr_cell: Integer wall bitmask for the current cell.
            path: Optional path marker to draw in the cell center.
            x: Column index of the cell.
            y: Row index of the cell.

        Returns:
            A list of five strings representing the rendered cell.
        """
        directions = {
            "N": "🮧",
            "E": "🮥",
            "S": "🮦",
            "W": "🮤",
            "C": "🯅"
        }
        cell_base = [0, 0, 0, 0]
        i = [0, 8]
        for n in cell_base:
            if curr_cell > 0 and i[1] <= curr_cell:
                curr_cell -= i[1]
                n += 1
                i[1] = i[1] // 2
            else:
                i[1] = i[1] // 2
            cell_base[i[0]] = n
            i[0] += 1
        connect = [[" │", " │", " │"],
                   ["─────"],
                   ["│ ", "│ ", "│ "],
                   ["─────"]]
        if cell_base[0] == 0:
            connect[0] = ["─┘", "  ", "─┐"]
        if cell_base[1] == 0:
            connect[1] = ["┐   ┌"]
        if cell_base[2] == 0:
            connect[2] = ["└─", "  ", "┌─"]
        if cell_base[3] == 0:
            connect[3] = ["┘   └"]
        center = " "
        if isinstance(path, str) and path != "":
            center = directions[path]
        if (y, x) == self.maze_entry:
            center = "🮮"
        elif (y, x) == self.maze_exit:
            center = "╳"

        cell_top1 = (" ┌" + connect[3][0] + "┐ ")
        cell_top2 = (connect[0][0] + "     " + connect[2][0])
        cell_mid1 = (connect[0][1] + "  " + center + "  " + connect[2][1])
        cell_bot2 = (connect[0][2] + "     " + connect[2][2])
        cell_bot1 = (" └" + connect[1][0] + "┘ ")

        return [cell_top1, cell_top2, cell_mid1, cell_bot2, cell_bot1]

    def set_colors(self, logo_coords: set[Coord] | None) -> CellGrid:
        """Build a color-code grid for rendering.

        Color codes:
            - 0: normal maze cell
            - 1: blocked logo cell
            - 2: maze entry
            - 3: maze exit

        Args:
            logo_coords: Optional set of coordinates reserved for the logo.

        Returns:
            A grid of integer color codes aligned with the maze dimensions.
        """
        color_grid = self.blank_grid()
        if logo_coords is not None:
            for cell in logo_coords:
                y, x = cell
                color_grid[y][x] = 1
        y, x = self.maze_entry
        color_grid[y][x] = 2
        y, x = self.maze_exit
        color_grid[y][x] = 3
        return color_grid

    def color_picker(self, code: int, alt_color: bool) -> str:
        """Return the ANSI escape sequence for a given render code.

        Args:
            code: Integer color code for the current cell.
            alt_color: Whether to use the alternate maze color theme.

        Returns:
            ANSI escape sequence string for terminal coloring.
        """
        color = "\x1b[0m"
        color_42 = "\x1b[95m"
        maze_entry = "\x1b[92m"
        maze_exit = "\x1b[93m"
        off_color = "\x1b[30m"
        if alt_color is True:
            color = "\x1b[36m"
            color_42 = "\x1b[31m"
        if code == 1:
            color = color_42
        elif code == 2:
            color = maze_entry
        elif code == 3:
            color = maze_exit
        elif code == 4:
            color = off_color
        return color

    def builder(self, colors: CellGrid,
                alt_color: bool = False) -> None:
        """Print the fully rendered maze to the terminal.

        This method assumes `draw_maze()` has already populated
        `self.maze_pieces`.

        Args:
            colors: Grid of color codes aligned with the maze cells.
            alt_color: Whether to use the alternate maze frame/cell theme.
        """
        x = 0
        y = 0
        z = 0
        if alt_color is True:
            frame_color = "\x1b[31m"
        else:
            frame_color = "\x1b[95m"
        print(frame_color + "┌" + ("─────────" * (self.width)) + "┐")
        for y in range(0, self.height):
            for z in range(0, len(self.maze_pieces[y][x])):
                print(frame_color + "│", end="")
                for x in range(0, self.width):
                    color = self.color_picker(colors[y][x], alt_color)
                    print(color + self.maze_pieces[y][x][z], end="")
                print(frame_color + "│")
                x = 0
            z = 0
        print(frame_color + "└" + ("─────────" * (self.width)) + "┘")


class Animator:
    """Animate maze generation and path rendering in the terminal."""
    def __init__(self, to_animate: AsciiRender) -> None:
        """Initialize the animator.

        Args:
            to_animate: Renderer used to draw each animation frame.
        """
        self.to_animate = to_animate
        self.curr_load = 0
        self.max_load = 50
        self.dots = 1
        self.last_frame: list[Any] = []

    def loading(self, type: str) -> None:
        """Render a progress bar and status message.

        Args:
            animation_type: Animation phase identifier. Supported values are:
                - `"start"`
                - `"gen"`
                - `"path"`
        """
        if type == "start":
            if self.curr_load < 20:
                load_message = "LOADING MAZE"
            else:
                load_message = "INJECTING 42"
        elif type == "gen":
            if self.curr_load < 10:
                load_message = "GENERATING MAZE"
            elif self.curr_load >= 10 and self.curr_load < 25:
                load_message = "LOOKING FOR EXIT"
            else:
                load_message = "OPENING NEW PATHWAYS"
        elif type == "path":
            load_message = "CHARTING SHORTEST PATH"
        if random.randint(0, 10) > 3:
            self.curr_load += random.randint(1, 3)
            if self.curr_load > self.max_load:
                self.curr_load = self.max_load
        if self.dots < 3:
            self.dots += 1
        else:
            self.dots = 1
        print()
        print(f"    ----- {load_message}{'.' * self.dots}"
              f"{' ' * (3 - self.dots)} -----")
        print(("█" * self.curr_load) +
              ("─" * (self.max_load - self.curr_load)))

    def load_maze(self,
                  color: bool) -> None:
        """Animate an initial maze-loading sequence.

        Args:
            color: Whether to use the alternate color scheme.
            anim_speed: Requested animation speed in seconds.

        Notes:
            The current implementation uses fixed sleep values for the loading
            sequence and does not directly apply `anim_speed`.
        """
        x = 0
        y = 0
        blank_grid = self.to_animate.blank_grid()
        for row in blank_grid:
            for col in row:
                blank_grid[y][x] = 15
                x += 1
            y += 1
            x = 0
        y = 0
        start_grid = self.to_animate.blank_grid()
        for row in start_grid:
            for col in row:
                start_grid[y][x] = 4
                x += 1
            y += 1
            x = 0
        y = 0
        for row in start_grid:
            for col in row:
                start_grid[y][x] = 0
                x += 1
            self.to_animate.draw_maze(blank_grid, None)
            self.to_animate.builder(start_grid, color)
            if y == len(start_grid) - 1:
                while self.curr_load != self.max_load:
                    self.loading("start")
                    time.sleep(0.1)
                    print("\033[F\033[2K" * 3, end="", flush=True)
            else:
                self.loading("start")
            time.sleep(0.1)
            os.system('clear')
            y += 1
            x = 0
        self.curr_load = 0

    def print_frame(self, grid: list[list[int]],
                    path: list[list[str]],
                    color_grid: list[list[int]],
                    color: bool,) -> None:
        """Render one animation frame for the current maze state.

        Args:
            grid: Maze cell grid to render.
            path: Current path overlay grid.
            color_grid: Grid of render color codes.
            color: Whether to use the alternate color theme.
        """
        self.to_animate.draw_maze(grid, path)
        self.to_animate.builder(color_grid, color)
        self.loading("gen")
        self.last_frame = [grid, path, color_grid]

    def anim_path(self, solution: tuple[list[Coord], str],
                  color: bool, anim_speed: float) -> None:
        """Animate the progressive reveal of the solution path.

        Args:
            solution: Tuple containing path coordinates and direction string.
            color: Whether to use the alternate color theme.
            anim_speed: Delay between frames in seconds.
        """
        i = 0
        coords, path = solution
        if anim_speed < 0.5:
            anim_speed = anim_speed * 2
        for _ in coords:
            if i < len(path):
                curr_frame = (coords[:(i + 1)], (path[:i] + "C"))
            else:
                curr_frame = solution
            i += 1
            curr_path = self.to_animate.draw_path(self.to_animate.
                                                  blank_grid("str"),
                                                  curr_frame)
            self.to_animate.draw_maze(self.last_frame[0], curr_path)
            self.to_animate.builder(self.last_frame[2], color)
            self.loading("path")
            time.sleep(anim_speed)
            os.system('clear')
