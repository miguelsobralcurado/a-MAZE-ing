"""
    Maze generator supporting multiple algorithms.

    Example:
        >>> gen = MazeGenerator(10, 10, seed=42)
        >>> for _ in gen.generate():
        ...     pass
        >>> coords, path = gen.solve((0,0), (9,9))
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Generator, Set, Optional, Protocol
from collections import deque
import random


# === Constants ===

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRS = [(-1, 0, NORTH, SOUTH), (0, 1, EAST, WEST),
        (1, 0, SOUTH, NORTH), (0, -1, WEST, EAST)]


# === Maze Grid ===

class MazeGrid:
    def __init__(self, width: int, height: int):
        self.cells: List[List[int]] = [[15 for _ in range(width)]
                                       for _ in range(height)]
        self.width = width
        self.height = height
        self.pat_coords = None

    def add_pattern(self, pattern: List[str]) -> set:
        y_offset = self.height // 2 - len(pattern) // 2
        x_offset = self.width // 2 - len(pattern[0]) // 2
        self.pat_coords: Set[tuple[int, int]] = {
            (r + y_offset, c + x_offset)
            for r, row in enumerate(pattern)
            for c, col in enumerate(row)
            if col == "#"
        }
        return self.pat_coords

    def in_bounds(self, y: int, x: int) -> bool:
        if 0 <= y < self.height and 0 <= x < self.width:
            if self.pat_coords:
                return (y, x) not in self.pat_coords
        return 0 <= y < self.height and 0 <= x < self.width

    def neighbors(self, y: int, x: int):
        for dy, dx, wall, opposite in DIRS:
            ny, nx = y + dy, x + dx
            if self.in_bounds(ny, nx):
                yield ny, nx, wall, opposite

    def remove_wall(self, y: int, x: int, ny: int, nx: int,
                    wall: int, opposite: int) -> None:
        self.cells[y][x] &= ~wall
        self.cells[ny][nx] &= ~opposite


# === Algorithms ===

class PrimGenerator:
    def __init__(self, perfect: bool = False, seed: int = 0):
        self.random = random.Random(seed)
        self.perfect = perfect

    def generate(self, maze: MazeGrid) -> Generator[List[list[int]],
                                                    None, None]:
        visited: Set[Tuple[int, int]] = set()
        walls: List[Tuple[int, int, int, int, int, int]] = []

        start = (0, 0)
        visited.add(start)

        for ny, nx, wall, opposite in maze.neighbors(*start):
            walls.append((start[0], start[1], ny, nx, wall, opposite))

        while walls:
            y, x, ny, nx, wall, opposite = self.random.choice(walls)
            walls.remove((y, x, ny, nx, wall, opposite))

            if (ny, nx) not in visited:
                maze.remove_wall(y, x, ny, nx, wall, opposite)
                visited.add((ny, nx))

                for nny, nnx, w, opp in maze.neighbors(ny, nx):
                    if (nny, nnx) not in visited:
                        walls.append((ny, nx, nny, nnx, w, opp))

                yield maze.cells

        if self.perfect is False:
            extras = round((maze.height * maze.width) * 0.2)
            while extras:
                y = self.random.randint(0, maze.height - 1)
                x = self.random.randint(0, maze.width - 1)
                while (y, x) not in visited:
                    y = self.random.randint(0, maze.height - 1)
                    x = self.random.randint(0, maze.width - 1)
                neighbors = [option for option in maze.neighbors(y, x)]
                if neighbors:
                    ny, nx, wall, opposite = self.random.choice(neighbors)
                    maze.remove_wall(y, x, ny, nx, wall, opposite)
                    extras -= 1
                    yield maze.cells


class DFSGenerator:
    def __init__(self, perfect: bool = False, seed: int = 0):
        self.random = random.Random(seed)
        self.perfect = perfect

    def generate(self, maze: MazeGrid) -> Generator[List[list[int]],
                                                    None, None]:
        stack: List[Tuple[int, int]] = [(0, 0)]
        visited: Set[Tuple[int, int]] = {(0, 0)}

        while stack:
            y, x = stack[-1]
            neighbors = [
                (ny, nx, wall, opposite)
                for ny, nx, wall, opposite in maze.neighbors(y, x)
                if (ny, nx) not in visited
            ]

            if neighbors:
                ny, nx, wall, opposite = self.random.choice(neighbors)
                maze.remove_wall(y, x, ny, nx, wall, opposite)
                visited.add((ny, nx))
                stack.append((ny, nx))
                yield maze.cells
            else:
                stack.pop()

        if self.perfect is False:
            extras = round((maze.height * maze.width) * 0.2)
            while extras:
                y = self.random.randint(0, maze.height - 1)
                x = self.random.randint(0, maze.width - 1)
                while (y, x) not in visited:
                    y = self.random.randint(0, maze.height - 1)
                    x = self.random.randint(0, maze.width - 1)
                neighbors = [n for n in maze.neighbors(y, x)]
                if neighbors:
                    ny, nx, wall, opposite = self.random.choice(neighbors)
                    maze.remove_wall(y, x, ny, nx, wall, opposite)
                    extras -= 1
                    yield maze.cells


# === Generator API ===

class MazeGenerator:
    def __init__(self, width: int, height: int, entry, exit, seed: int = 0,
                 perfect: bool = True, algorithm: str = "prim"):
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.maze_grid = MazeGrid(self.width, self.height)
        self.algorithm = algorithm.lower().strip()
        self.logo = self.set_42()

    def set_42(self) -> Optional[Set[tuple[int, int]]]:
        pat_small = [
            "#.#.###",
            "#.#...#",
            "###.###",
            "..#.#..",
            "..#.###"
        ]  # 7x5

        pat_med = [
            "#..#.####",
            "#..#....#",
            "#..#....#",
            "####.####",
            "...#.#...",
            "...#.#...",
            "...#.####"
        ]  # 9x7

        pat_big = [
            "#...#.#####",
            "#...#.....#",
            "#...#.....#",
            "#...#.....#",
            "#####.#####",
            "....#.#....",
            "....#.#....",
            "....#.#....",
            "....#.#####"
        ]  # 11x9

        if self.width < 10 or self.height < 10:
            print("Error: maze size too small to place 42 pattern")
            return
        if self.width < 25 or self.height < 25:
            pattern = pat_small
        elif self.width < 31 or self.height < 31:
            pattern = pat_med
        else:
            pattern = pat_big
        self.maze_grid.add_pattern(pattern)
        return self.maze_grid.pat_coords

    def validate_entry_exit(self) -> bool:
        if not self.maze_grid.in_bounds(*self.entry):
            print("Entry out of bounds")
            return False
        if not self.maze_grid.in_bounds(*self.exit):
            print("Exit out of bounds")
            return False
        if self.entry == self.exit:
            print("Entry and exit have the same cell")
            return False
        return True

    def generate_maze(self) -> Generator[List[List[int]], None, None]:
        gen = {"prim": PrimGenerator, "dfs": DFSGenerator}
        if self.algorithm not in gen:
            raise ValueError("Unkwnown algorithm")
        return gen[self.algorithm](self.perfect, self.seed).generate(
            self.maze_grid)

    @staticmethod
    def solve(cells: List[list[int]], entry: tuple[int, int],
              exit: tuple[int, int]) -> Tuple[list[tuple[int, int]], str]:
        queue = deque([entry])
        visited = {entry}
        prev_cell: Dict[Tuple[int, int], Tuple[tuple[int, int], int]] = dict()

        while queue:
            y, x = queue.popleft()

            if (y, x) == exit:
                break

            for i, (dy, dx, wall, _) in enumerate(DIRS):
                if cells[y][x] & wall == 0:
                    ny, nx = y + dy, x + dx
                    if (ny, nx) not in visited:
                        prev_cell[(ny, nx)] = ((y, x), i)
                        visited.add((ny, nx))
                        queue.append((ny, nx))

        path = ""
        coords: List[tuple[int, int]] = [exit]
        current = exit
        dir_str = "NESW"

        while current != entry:
            (py, px), i = prev_cell[current]
            path = dir_str[i] + path
            coords.insert(0, (py, px))
            current = (py, px)
        return coords, path


def main():
    entry = (0, 0)
    exit = (9, 8)
    maze_gen = MazeGenerator(10, 10, entry, exit, 0, False, "prim")

    maze_grid = maze_gen.maze_grid

    logo = maze_gen.logo
    # Lista tuples y, x para aplicar directamente na grid

    try:
        maze_gen.validate_entry_exit()
    except ValueError as e:
        print(e)
    else:
        print("Entry and exit values validated")

    maze_generator = maze_gen.generate_maze()
    # Generator passo a passo do algoritmo
    next_grid = []
    i = 0
    for step in maze_generator:
        next_grid = step
        print(next_grid)
        print()
        i += 1
#    for row in next_grid:
#        print(row)
#        print()
    print(i)
    print()
    coords, path = maze_gen.solve(next_grid, entry, exit)
    print(path)
    for line in coords:
        print(line)
    print()


if __name__ == "__main__":
    main()
