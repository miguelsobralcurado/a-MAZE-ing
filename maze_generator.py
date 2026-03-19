from typing import List, Optional, Generator, Tuple, Set
import random


class MazeGrid:
    def __init__(self, width: int, height: int):
        self.cells: List[List[int]] = list()
        self.width = width
        self.height = height
        self.pat_coords: Set[tuple[int, int]] = set()

    def initialize_all_closed(self) -> None:
        self.cells = [[15 for _ in range(self.width)]
                      for _ in range(self.height)]

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


class MazeGenerator:
    def __init__(self, width: int, height: int, entry, exit, seed: int = 0,
                 perfect: bool = True, algorithm: str = "prims"):
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.maze_grid: MazeGrid = self.initialize()
        self.choose_algorithm(algorithm)
        self.generator_method = self.choose_generator_method()
        self.logo = self.set_42()

    # Create grid
    def choose_algorithm(self, algorithm: str) -> None:
        self.algorithm = algorithm.lower().strip()

    def initialize(self) -> MazeGrid:
        self.maze_grid = MazeGrid(self.width, self.height)
        self.maze_grid.initialize_all_closed()
        return self.maze_grid

    def validate_entry_exit(self):
        if self.entry in self.maze_grid.pat_coords:
            raise ValueError("Entry coordinates on top of 42 logo")
        if self.exit in self.maze_grid.pat_coords:
            raise ValueError("Exit coordinates on top of 42 logo")
        return True

    def set_42(self) -> Set[tuple[int, int]]:
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
        if self.width < 25 or self.height < 25:
            pattern = pat_small
        elif self.width < 31 or self.height < 31:
            pattern = pat_med
        else:
            pattern = pat_big
        self.maze_grid.add_pattern(pattern)
        return self.maze_grid.pat_coords

    def choose_generator_method(self):
        if self.algorithm == "prims":
            return self.prims()
        elif self.algorithm == "dfs":
            raise NotImplementedError("DFS not implemented yet")

    def prims(self) -> Generator[List[List[int]], None, None]:
        generator = PrimsAlgorithm(self.perfect, self.seed)
        return generator.generate_mst(self.maze_grid)


class PrimsAlgorithm:
    def __init__(self, perfect, seed: int = 0):
        # Bitmask values for walls
        self.NORTH = 1
        self.EAST = 2
        self.SOUTH = 4
        self.WEST = 8
        self.perfect = perfect
        self.seed = seed
        self.random = random.Random(seed)

    def generate_mst(self, maze_grid: MazeGrid) -> Generator[List[List[int]], None, None]:
        # Minimum Spanning Tree is a list of (y, x, wall_vallue) tuples
        mst = maze_grid.cells
        total_nodes = (maze_grid.width ** 2)
        unvisited = [n for n in range(total_nodes)]
        current_node = unvisited[int(self.random.random())]
        visited = [current_node]
        unvisited.remove(current_node)

        while len(unvisited) > len(maze_grid.pat_coords):
            edges_pool = self.get_available_edges(visited, maze_grid)
            edge = self.random.choice(edges_pool)
            current_node, next_node = edge
            mst = self.open_walls(mst, current_node, next_node, maze_grid)
            visited.append(next_node)
            unvisited.remove(next_node)
            yield mst
        if self.perfect:
            return mst

    def get_available_edges(self, visited, maze_grid) -> List[Tuple[tuple, tuple]]:
        edges_pool = []

        for node in visited:

            row = node // maze_grid.width
            col = node % maze_grid.width

            if (row, col) not in maze_grid.pat_coords:
                if row > 0:
                    # all rows except top one have top neighbours
                    top_node = node - maze_grid.width
                    if top_node not in visited:
                        if (top_node // maze_grid.width, top_node % maze_grid.width) not in maze_grid.pat_coords:
                            edges_pool.append((node, top_node))

                if col > 0:
                    # all columns except first have left neighbours
                    left_node = node - 1
                    if left_node not in visited:
                        if (left_node // maze_grid.width, left_node % maze_grid.width) not in maze_grid.pat_coords:
                            edges_pool.append((node, left_node))

                if row < maze_grid.width - 1:
                    # all rows except last one have bot neighbours
                    bot_node = node + maze_grid.width
                    if bot_node not in visited:
                        if (bot_node // maze_grid.width, bot_node % maze_grid.width) not in maze_grid.pat_coords:
                            edges_pool.append((node, bot_node))

                if col < maze_grid.width - 1:
                    # all columns except last have right neighbours
                    right_node = node + 1
                    if right_node not in visited:
                        if (right_node // maze_grid.width, right_node % maze_grid.width) not in maze_grid.pat_coords:
                            edges_pool.append((node, right_node))

        return edges_pool

    def open_walls(self, mst: List[List[int]], node: int, next_node: int, maze_grid):
        y = node // maze_grid.width
        x = node % maze_grid.width
        n_y = next_node // maze_grid.width
        n_x = next_node % maze_grid.width
        if node - maze_grid.width == next_node:
            mst[y][x] ^= self.NORTH
            mst[n_y][n_x] ^= self.SOUTH
        if node - 1 == next_node:
            mst[y][x] ^= self.EAST
            mst[n_y][n_x] ^= self.WEST
        if node + maze_grid.width == next_node:
            mst[y][x] ^= self.SOUTH
            mst[n_y][n_x] ^= self.NORTH
        if node + 1 == next_node:
            mst[y][x] ^= self.WEST
            mst[n_y][n_x] ^= self.EAST
        return mst


def main():
    entry = (0, 0)
    exit = (19, 14)
    maze_gen = MazeGenerator(21, 21, entry, exit, 0)

#    ascii_rend = AsciiRenderer(bla bla)

    maze_grid = maze_gen.initialize()
    test_grid = maze_grid.cells

#    ascii_rend.draw_maze(maze_grid.cells)
    # List 2D com tudo a 15

    logo = maze_gen.logo
    # Lista tuples y, x para aplicar directamente na grid?

    try:
        maze_gen.validate_entry_exit()
    except ValueError as e:
        print(e)
    else:
        print("Entry and exit values validated")

#    ascii_rend.paint(logo)

    for cell in logo:
        y, x = cell
#        ascii_rend.maze_colors[y][x] = 42
        test_grid[y][x] = 42
    y, x = entry
#    ascii_rend.maze_colors[y][x] = 2
    test_grid[y][x] = 20
    y, x = exit
#    ascii_rend.maze_colors[y][x] = 3
    test_grid[y][x] = 50
    # Adicionar entry e exit ao maze_grid

#    for row in test_grid:
#        print(row)
#    print()

    maze_generator = maze_gen.generator_method
    # Generator passo a passo do algoritmo
    # Um tuple por passo (y, x, valor paredes) para aplicar directamente na grid?
    # Lista completa no fim

    for _ in maze_generator:
        next_grid = next(maze_generator)
    for row in next_grid:
        print(row)
#        print()
    print()


if __name__ == "__main__":
    main()
