import os
import time
import random
from typing import Optional, Any


class AsciiRender:
    def __init__(self, width: int, height: int,
                 maze_entry: list[int], maze_exit: list[int]) -> None:
        self.width = width
        self.height = height
        self.maze_entry = maze_entry
        self.maze_exit = maze_exit

    def set_proportions(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def blank_grid(self, type: str = "int") -> list[list[Any]]:
        grid = []
        for i in range(self.height):
            grid.append([])
            for j in range(self.width):
                if type == "int":
                    grid[i].append(0)
                elif type == "str":
                    grid[i].append("")
        return grid

    def draw_maze(self,
                  grid: list[list[int]],
                  path: Optional[tuple[list[tuple], str]] = None) -> None:
        self.maze_pieces = []
        self.maze_color = []
        x = 0
        y = 0
        if path is None:
            path_grid = self.blank_grid()
        elif isinstance(path, list):
            path_grid = path
        else:
            path_grid = self.draw_path(self.blank_grid("str"), path)
        for row in grid:
            r = []
            for col in row:
                r.append(self.calc_piece(grid[y][x],
                                         path_grid[y][x],
                                         x,
                                         y))
                x += 1
            self.maze_pieces.append(r)
            x = 0
            y += 1

    def draw_path(self,
                  empty_grid: list[list[str]],
                  f_path: tuple[list[tuple], str]) -> list[list[str]]:
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
                   x: int = 0, y: int = 0) -> set[str]:
        directions = {"N": "^", "E": ">", "S": "v", "W": "<", "C": "O"}
        if curr_cell == 42:
            return
        cell_base = [0, 0, 0, 0]
        i = [0, 8]
        for n in cell_base:
            if curr_cell > 0 and i[1] <= curr_cell:
                curr_cell -= i[1]
                n += 1
                i[1] = i[1] / 2
            else:
                i[1] = i[1] / 2
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
        if isinstance(path, str):
            if path != "":
                center = directions[path]
        if (y, x) == self.maze_entry and path != "C":
            center = "H"
        elif (y, x) == self.maze_exit and path != "C":
            center = "╳"

        cell_top1 = (" ┌" + connect[3][0] + "┐ ")
        cell_top2 = (connect[0][0] + "     " + connect[2][0])
        cell_mid1 = (connect[0][1] + "  " + center + "  " + connect[2][1])
        cell_bot2 = (connect[0][2] + "     " + connect[2][2])
        cell_bot1 = (" └" + connect[1][0] + "┘ ")

        return [cell_top1, cell_top2, cell_mid1, cell_bot2, cell_bot1]

    def set_colors(self, logo_coords: set[tuple[int, int]]) -> list[list[int]]:
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
        color = "\x1b[0m"
        color_42 = "\x1b[95m"
        maze_entry = "\x1b[92m"
        maze_exit = "\x1b[93m"
        off_color = "\x1b[31m"
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
            color == off_color
        return color

    def builder(self, colors: list[list[int]],
                alt_color: bool = False) -> None:
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
    def __init__(self, to_animate: AsciiRender) -> None:
        self.to_animate = to_animate
        self.curr_load = 0
        self.max_load = 50
        self.dots = 1

    def loading(self, type: str) -> str:
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
        print(f"    ----- {load_message}{"." * self.dots}"
              f"{" " * (3 - self.dots)} -----")
        print(("█" * self.curr_load) +
              ("─" * (self.max_load - self.curr_load)))

    def load_maze(self,
                  color: bool, anim_speed: float) -> None:
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
                start_grid[y][x] = 1
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
            os.system('cls')
            y += 1
            x = 0
        self.curr_load = 0

    def print_frame(self, grid: list[list[int]],
                    path: list[list[str]],
                    color_grid: list[list[int]],
                    color: bool,) -> None:
        self.to_animate.draw_maze(grid, path)
        self.to_animate.builder(color_grid, color)
        self.loading("gen")
        self.last_frame = [grid, path, color_grid]

    def anim_path(self, solution: tuple[list[tuple], str],
                  color: bool, anim_speed: float) -> None:
        i = 0
        coords, path = solution
        if anim_speed < 0.5:
            anim_speed = anim_speed * 2
        for coord in coords:
            if i < len(path):
                curr_frame = (coords[:(i + 1)], (path[:i] + "C"))
            else:
                curr_frame = solution
            i += 1
            self.to_animate.draw_maze(self.last_frame[0], curr_frame)
            self.to_animate.builder(self.last_frame[2], color)
            self.loading("path")
            time.sleep(anim_speed)
            os.system('cls')


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
