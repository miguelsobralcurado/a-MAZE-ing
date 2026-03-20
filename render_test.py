# import sys
# import os
# import time
from typing import Optional
# from config import Config
# from mazegen import MazeGenerator, Maze
# from serializer import write_output_file


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

    def blank_grid(self) -> list[list[int]]:
        grid = []
        for i in range(self.height):
            grid.append([])
            for j in range(self.width):
                grid[i].append(0)
        return grid

    def draw_maze(self,
                  grid: list[list[int]],
                  path: Optional[list[int]] = None) -> None:
        self.maze_pieces = []
        self.maze_color = []
        x = 0
        y = 0
        if path is None:
            path = self.blank_grid()
        for row in grid:
            r = []
            for col in row:
                r.append(self.calc_piece(grid[y][x],
                                         path[y][x],
                                         x,
                                         y))
                x += 1
            self.maze_pieces.append(r)
            x = 0
            y += 1

    def calc_piece(self, curr_cell: int,
                   path: Optional[int] = None,
                   x: int = 0, y: int = 0) -> set[str]:
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
        connect = [["│ ", "│ ", "│ "],
                   ["─────"],
                   [" │", " │", " │"],
                   ["─────"]]
        if cell_base[0] == 0:
            connect[0] = ["└─", "  ", "┌─"]
        if cell_base[1] == 0:
            connect[1] = ["┐   ┌"]
        if cell_base[2] == 0:
            connect[2] = ["─┘", "  ", "─┐"]
        if cell_base[3] == 0:
            connect[3] = ["┘   └"]
        center = " "
        if isinstance(path, int):
            if path == 1:
                center = "￭"
            elif (y, x) == self.maze_entry:
                center = "🮮"
            elif (y, x) == self.maze_exit:
                center = "╳"

        cell_top1 = (" ┌" + connect[3][0] + "┐ ")
        cell_top2 = (connect[2][0] + "     " + connect[0][0])
        cell_mid1 = (connect[2][1] + "  " + center + "  " + connect[0][1])
        cell_bot2 = (connect[2][2] + "     " + connect[0][2])
        cell_bot1 = (" └" + connect[1][0] + "┘ ")

        return [cell_top1, cell_top2, cell_mid1, cell_bot2, cell_bot1]

    def set_colors(self, logo_coords: set[tuple[int, int]]) -> list[list[int]]:
        color_grid = self.blank_grid()
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
        if alt_color is True:
            color = "\x1b[36m"
            color_42 = "\x1b[31m"
        if code == 1:
            color = color_42
        elif code == 2:
            color = maze_entry
        elif code == 3:
            color = maze_exit
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

    def print_frame(self, grid: list[list[int]],
                    path: list[list[int]],
                    color_grid: list[list[int]],
                    color: bool,) -> None:
        self.to_animate.draw_maze(grid, path)
        self.to_animate.builder(color_grid, color)

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
