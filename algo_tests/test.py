from typing import List, Optional, Generator, Tuple
import random


class MazeGrid:
    def __init__(self, width: int, height: int):
        self.cells: List[List[int]] = list()
        self.width = width
        self.height = height
        self.pat_coords: List[tuple[int, int]] = []

    def initialize_all_closed(self) -> None:
        self.cells = [[15 for _ in range(self.width)]
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
                 algorithm: str = "prims"):
        self.width = width
        self.height = height
        self.perfect = perfect
        self.choose_algorithm(algorithm)
        self.random = random.Random.seed(seed)
        self.visual = visual
        self.maze_grid: MazeGrid

    # Create grid
    def choose_algorithm(self, algorithm: str) -> None:
        self.algorithm = algorithm.lower().strip()

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

        if self.width < 10 or self.height < 10:
            raise ValueError("No 42 pattern, maze size too small")
        if self.width < 28 or self.height < 20:
            pattern = pat_small
        elif self.width < 45 or self.height < 30:
            pattern = pat_med
        else:
            pattern = pat_big
        self.maze_grid.add_pattern(pattern)
        return self.maze_grid.pat_coords

    def generate(self) -> Generator[List[List[int]], None, None]:
        if self.algorithm == "prims":
            return self.prims()
        elif self.algorithm == "dfs":
            raise NotImplementedError("DFS not implemented yet")

    def prims(self) -> Generator[List[List[int]], None, None]:
        generator = PrimsAlgorithm(self.random, self.perfect)
        return generator.generate_mst(self.maze_grid)


class PrimsAlgorithm:
    def __init__(self):
         # Bitmask values for walls
        self.NORTH = 1
        self.EAST = 2
        self.SOUTH = 4
        self.WEST = 8

    @staticmethod
    def ignore_logo(visited, maze_grid) -> List[List[bool]]:
        for node in maze_grid.pat_coords:
            y, x = node
            visited[y][x] = True
        return visited

    def generate_mst(self, maze_grid: MazeGrid) -> Generator[List[List[int]], None, None]:
        visited: List[List[bool]] = [[False for _ in range(maze_grid.width)]
                                     for _ in range(maze_grid.height)]
        visited_count = 0

        if maze_grid.pat_coords:
            visited = self.ignore_logo(visited, maze_grid)
            visited_count += len(maze_grid.pat_coords)

        start = (0, 0)
        visited[start[0]][start[1]] = True
        visited_count += 1
        total = maze_grid.width * maze_grid.height
        while visited_count < total:
            edges_pool = self.get_available_edges(visited)
            edge = self.random.choice(edges_pool)
            node, next_node = edge
            maze_grid.cells = self.open_walls(maze_grid.cells, node, next_node)
            y, x = next_node
            visited[y][x] = True
            visited_count += 1
            yield maze_grid.cells
        return maze_grid.cells

    def get_available_edges(self, visited) -> List[Tuple[tuple, tuple]]:
        edges_pool = []

        for row in enumerate(visited):
        # get y = row in [index, list] pairs
            for col in enumerate(row[1]):
            #get x = col in [index, bool] pairs
                if col[1]:
                    node = (row[0], col[0])

                    if row[0] > 0 and not visited[row[0] - 1][col[0]]:
                        # all rows except top one have top neighbours
                        top_node = (row[0] - 1, col[0])
                        edges_pool.append((node, top_node))

                    if col[0] > 0 and not visited[row[0]][col[0] - 1]:
                        # all columns except first have left neighbours
                        left_node = (row[0], col[0] - 1)
                        edges_pool.append((node, left_node))

                    if row[0] < len(visited) - 1 and not visited[row[0] + 1][col[0]]:
                        # all rows except last one have bot neighbours
                        bot_node = (row[0] + 1, col[0])
                        edges_pool.append((node, bot_node))

                    if col[0] < len(visited[0]) - 1 and not visited[row[0]][col[0] + 1]:
                        # all columns except last have right neighbours
                        right_node = (row[0], col[0] + 1)
                        edges_pool.append((node, right_node))

        return edges_pool

    def open_walls(self, cells: List[List[int]], node: tuple, next_node: tuple):
        y, x = node
        n_y, n_x = next_node
        if y - 1 == n_y:
            cells[y][x] = cells[y][x] ^ self.NORTH
            cells[n_y][n_x] = cells[n_y][n_x] ^ self.SOUTH
        if x + 1 == n_x:
            cells[y][x] = cells[y][x] ^ self.EAST
            cells[n_y][n_x] = cells[n_y][n_x] ^ self.WEST
        if y + 1 == n_y:
            cells[y][x] = cells[y][x] ^ self.SOUTH
            cells[n_y][n_x] = cells[n_y][n_x] ^ self.NORTH
        if x - 1 == n_x:
            cells[y][x] = cells[y][x] ^ self.WEST
            cells[n_y][n_x] = cells[n_y][n_x] ^ self.EAST
        return cells



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