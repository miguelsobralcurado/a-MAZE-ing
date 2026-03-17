import random
from typing import List, Optional, Generator


class MazeGrid:
    def __init__(self, width: int, height: int):
        self.cells: List[List[int]] = list()
        self.width = width
        self.height = height
        self.pat_coords: List[tuple[int, int]] = []

    def initialize_all_closed(self) -> None:
        self.cells = [15 for _ in range(self.width)
                      for _ in range(self.height)]
        
    def add_pattern(self, pattern: List[str]) -> list:
        y_offset = self.height // 2 - len(pattern) // 2
        x_offset = self.width // 2 - len(pattern[0]) // 2
        self.pat_coords: List[tuple[int, int]] = [
            (r + y_offset, c + x_offset)
            for r, row in enumerate(pattern)
            for c, col in enumerate(row)
            if col == "#"]
        return self.pat_coords

class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Optional[int],
                 perfect: bool, visual: bool,
                 algorithm: str = "dfs", density: float = 0.06):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.choose_algorithm(algorithm)
        self.random = random.Random(seed)
        self.density = density
        self.visual = visual
        self._42 = False
        self.maze_grid: MazeGrid

    # Create grid
    def choose_algorithm(self, algorithm: str) -> None:
        self.algorithm = algorithm.lower().strip() if algorithm else "dfs"

    def initialize(self, entry: tuple[int, int],
                 exit: tuple[int, int]) -> MazeGrid:
        self.validate_params(entry, exit)
        self.maze_grid = MazeGrid(self.width, self.height)
        self.maze_grid.initialize_all_closed()
        return self.maze_grid

    def set_42(self) -> List[tuple[int, int]]:
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

        if self._42 is False:
            return self.maze_grid
        elif maze.width < 10 or maze.height < 10:
            raise ValueError("No 42 pattern, maze size too small")
        if maze.width < 28 or maze.height < 20:
            pattern = pat_small
        elif maze.width < 45 or maze.height < 30:
            pattern = pat_med
        else:
            pattern = pat_big
        self.maze_grid.add_pattern(pattern)
        return self.maze_grid.pat_coords

    def generate(self) -> Generator:
        if self.algorithm == "prim":
            return self.prim
        elif self.algorithm == "dfs":
            return

    def prim(self) -> Generator:
        not_included = self.maze_grid.cells
        included = []
        logo = self.maze_grid.pat_coords

        start = random.random()


maze: List[List[int]] = {
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15],
    [15, 14, 15, 15, 15],
    [15, 14, 15, 15, 15],
    [15, 15, 15, 15, 15],
}

algorithm = gen.algorithm()

for _ in algorithm:











"""
A-Maze-ing — reusable maze generator module

Standalone, reusable module:
- Maze data model (walls bitmask)
- Generation algorithms + constraints
- Solver (shortest path)

Rules:
- No printing
- No file I/O
- No user interaction

Short documentation
------------------------------
1) Instantiate and use the generator (basic example):
    from mazegen import MazeGenerator
    gen = MazeGenerator(width=31, height=21, seed=42,
                              perfect=True, algorithm="dfs")
    entry = (1, 1)
    exit_ = (29, 19)
    maze = gen.generate(entry=entry, exit=exit_)
    path = gen.solve(maze=maze, entry=entry, exit=exit_)

2) Pass custom parameters (size, seed, etc.):
    - width, height: maze dimensions (int)
    - seed: int or None (None => random)
    - perfect: bool (True => perfect maze; False => may create loops)
    - algorithm: "dfs" or "prim"
    - density: float (used when perfect=False)

3) Access the generated structure and a solution:
    - maze.width, maze.height
    - maze.cells[y][x]: int bitmask in 0..15
      Bits: N=1, E=2, S=4, W=8 (bit set => wall is CLOSED)
    - "42" stamp: maze.omitted_42 and maze.stamp42 (if present)
    - path: list of moves like ["N", "E", ...] from solve(...)

Packaging note
--------------
This file must be packagable as mazegen-* (.whl or .tar.gz) and installable
via pip.
"""