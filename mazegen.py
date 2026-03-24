"""
Reusable maze generation module.

Basic usage:
    >>> from mazegen import MazeGenerator
    >>> gen = MazeGenerator(10, 10, seed=42)
    >>> for _ in gen.generate_maze():
    ...     pass
    >>> cells = gen.maze_grid.cells
    >>> coords, path = gen.solve(cells, gen.entry, gen.exit)

Custom parameters:
    - width, height
    - entry, exit
    - seed
    - perfect
    - algorithm ("prim" or "dfs")

Access:
    - Maze structure: gen.maze_grid.cells
    - Blocked pattern coordinates: gen.logo
    - Solution path: MazeGenerator.solve(...)
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Generator, Set, Optional, Iterator, Union
from collections import deque
import random


# === Constants ===

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRS = [(-1, 0, NORTH, SOUTH), (0, 1, EAST, WEST),
        (1, 0, SOUTH, NORTH), (0, -1, WEST, EAST)]

Coord = tuple[int, int]
CellGrid = list[list[int]]
Neighbor = tuple[int, int, int, int]
WallEdge = tuple[int, int, int, int, int, int]


# === Maze Grid ===

class MazeGrid:
    """Represent a maze as a grid of cells with bitmask-encoded walls.

    Each cell stores four wall bits:

    - `NORTH`
    - `EAST`
    - `SOUTH`
    - `WEST`

    A set bit means the wall is present; a cleared bit means the wall
    has been removed and passage is possible in that direction.

    Attributes:
        cells: Two-dimensional grid of wall bitmasks.
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        pat_coords: Optional set of coordinates reserved by a pattern that
            must be excluded from traversal and generation.
    """
    def __init__(self, width: int, height: int):
        """Initialize a grid with all walls present in every cell.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
        """
        self.cells: CellGrid = [[15 for _ in range(width)]
                                for _ in range(height)]
        self.width = width
        self.height = height
        self.pat_coords: Union[Set[Coord], None] = None

    def add_pattern(self, pattern: List[str]) -> set[Coord]:
        """Place a `#`-based pattern centered in the grid.

        Cells marked with `#` are treated as blocked cells and excluded from
        maze generation and navigation.

        Args:
            pattern: Sequence of strings representing the pattern, where `#`
                marks blocked cells and any other character is ignored.

        Returns:
            Set of blocked `(row, column)` coordinates corresponding to the
            centered pattern.
        """
        y_offset = self.height // 2 - len(pattern) // 2
        x_offset = self.width // 2 - len(pattern[0]) // 2
        self.pat_coords = {
            (r + y_offset, c + x_offset)
            for r, row in enumerate(pattern)
            for c, col in enumerate(row)
            if col == "#"
        }
        return self.pat_coords

    def in_bounds(self, y: int, x: int) -> bool:
        """Return whether a coordinate is valid and not blocked by a pattern.

        Args:
            y: Row index.
            x: Column index.

        Returns:
            `True` if the coordinate is inside the grid and, when a pattern is
            present, not part of the blocked pattern area.
        """
        if 0 <= y < self.height and 0 <= x < self.width and self.pat_coords:
            return (y, x) not in self.pat_coords
        return 0 <= y < self.height and 0 <= x < self.width

    def neighbors(self, y: int, x: int) -> Iterator[Neighbor]:
        """Yield valid neighboring cells and the corresponding wall metadata.

        For each adjacent in-bounds cell, this method returns:

        - neighbor row
        - neighbor column
        - wall bit from the current cell toward the neighbor
        - opposite wall bit from the neighbor back to the current cell

        Args:
            y: Row index of the current cell.
            x: Column index of the current cell.

        Yields:
            Tuples of the form `(ny, nx, wall, opposite)`.
        """
        for dy, dx, wall, opposite in DIRS:
            ny, nx = y + dy, x + dx
            if self.in_bounds(ny, nx):
                yield ny, nx, wall, opposite

    def remove_wall(self, y: int, x: int, ny: int, nx: int,
                    wall: int, opposite: int) -> None:
        """Open the passage between two adjacent cells."""
        self.cells[y][x] &= ~wall
        self.cells[ny][nx] &= ~opposite

    def _is_edge_open(self, y1: int, x1: int, y2: int, x2: int,
                      pending: Optional[tuple[int, int, int, int]]
                      = None) -> bool:
        """Return whether the shared edge between two adjacent cells is open.

        Args:
            y1: Row index of the first cell.
            x1: Column index of the first cell.
            y2: Row index of the second cell.
            x2: Column index of the second cell.
            pending: Optional simulated wall removal as `(y, x, ny, nx)`.
                When provided, that edge is treated as already open without
                mutating the grid.

        Returns:
            `True` if the two cells are adjacent, in bounds, and connected by
            an open passage; otherwise `False`.
        """
        if not (self.in_bounds(y1, x1) and self.in_bounds(y2, x2)):
            return False
        if pending is not None:
            py, px, pny, pnx = pending
            if ((y1, x1, y2, x2) in [(py, px, pny, pnx), (pny, pnx, py, px)]):
                return True

        if y2 == y1 - 1 and x2 == x1:
            return (self.cells[y1][x1] & NORTH) == 0
        if y2 == y1 + 1 and x2 == x1:
            return (self.cells[y1][x1] & SOUTH) == 0
        if y2 == y1 and x2 == x1 + 1:
            return (self.cells[y1][x1] & EAST) == 0
        if y2 == y1 and x2 == x1 - 1:
            return (self.cells[y1][x1] & WEST) == 0

        return False

    def creates_open_3x3(self, y: int, x: int, ny: int, nx: int) -> bool:
        """Check whether opening an edge would create a fully open 3x3 region.

        This is used to avoid introducing large open rooms by rejecting wall
        removals that would make every internal edge in any 3x3 block open.

        Args:
            y: Row index of the first cell.
            x: Column index of the first cell.
            ny: Row index of the adjacent second cell.
            nx: Column index of the adjacent second cell.

        Returns:
            `True` if removing the wall between the two cells would create at
            least one fully open 3x3 area; otherwise `False`.
        """
        pending = (y, x, ny, nx)

        min_y = max(0, min(y, ny) - 2)
        max_y = min(self.height - 3, max(y, ny))
        min_x = max(0, min(x, nx) - 2)
        max_x = min(self.width - 3, max(x, nx))

        for top in range(min_y, max_y + 1):
            for left in range(min_x, max_x + 1):
                cells_ok = all(
                    self.in_bounds(top + dy, left + dx)
                    for dy in range(3)
                    for dx in range(3)
                )
                if not cells_ok:
                    continue

                # All horizontal shared edges inside the 3x3 must be open
                horizontal_open = all(
                    self._is_edge_open(top + dy, left + dx,
                                       top + dy, left + dx + 1, pending)
                    for dy in range(3)
                    for dx in range(2)
                )

                if not horizontal_open:
                    continue

                # All vertical shared edges inside the 3x3 must be open
                vertical_open = all(
                    self._is_edge_open(top + dy, left + dx,
                                       top + dy + 1, left + dx, pending)
                    for dy in range(2)
                    for dx in range(3)
                )

                if horizontal_open and vertical_open:
                    return True

        return False


# === Algorithms ===

class PrimGenerator:
    """Generate a maze using a randomized Prim-style algorithm."""
    def __init__(self, seed: int = 0, perfect: bool = False):
        """Initialize the generator.

        Args:
            seed: Seed used to initialize the internal random number generator.
            perfect: Whether to keep the maze perfect, meaning acyclic with a
                unique path between any two reachable cells. When `False`,
                extra passages may be carved after generation.
        """
        self.random = random.Random(seed)
        self.perfect = perfect

    def generate(self, maze: MazeGrid, entry: Coord
                 ) -> Generator[CellGrid, None, None]:
        """Generate a maze incrementally.

        The generator yields the maze grid after each wall removal, making it
        suitable for step-by-step visualization.

        Args:
            maze: Maze grid to mutate in place.

        Yields:
            The current maze cell grid after each generation step.
        """
        walls: List[WallEdge] = []
        start = entry
        visited: Set[Coord] = {(start)}

        walls.extend(
            (start[0], start[1], ny, nx, wall, opposite)
            for ny, nx, wall, opposite in maze.neighbors(*start)
        )
        while walls:
            y, x, ny, nx, wall, opposite = self.random.choice(walls)
            walls.remove((y, x, ny, nx, wall, opposite))

            if (ny, nx) not in visited:
                maze.remove_wall(y, x, ny, nx, wall, opposite)
                visited.add((ny, nx))

                walls.extend(
                    (ny, nx, nny, nnx, w, opp)
                    for nny, nnx, w, opp in maze.neighbors(ny, nx)
                    if (nny, nnx) not in visited
                )

                yield maze.cells

        if self.perfect is False:
            yield from self.open_extras(maze, visited)

    def open_extras(self, maze: MazeGrid, visited: Set[Coord]
                    ) -> Generator[CellGrid, None, None]:
        """Generate extra 20% wall openings to make an unperfect maze.

        The generator yields the maze grid after each wall removal, making it
        suitable for implementing with the generate().

        Args:
            maze: Maze grid to mutate in place.

        Yields:
            The current maze cell grid after each generation step.
        """
        extras = round((maze.height * maze.width) * 0.2)
        while extras:
            y = self.random.randint(0, maze.height - 1)
            x = self.random.randint(0, maze.width - 1)
            while (y, x) not in visited:
                y = self.random.randint(0, maze.height - 1)
                x = self.random.randint(0, maze.width - 1)
            if neighbors := list(maze.neighbors(y, x)):
                ny, nx, wall, opposite = self.random.choice(neighbors)
                if not maze.creates_open_3x3(y, x, ny, nx):
                    maze.remove_wall(y, x, ny, nx, wall, opposite)
                    extras -= 1
                    yield maze.cells


class DFSGenerator:
    """Generate a maze using randomized depth-first search backtracking."""
    def __init__(self, seed: int = 0, perfect: bool = False) -> None:
        """Initialize the generator.

        Args:
            seed: Seed used to initialize the internal random number generator.
            perfect: Whether to keep the maze perfect. When `False`, extra
                passages may be carved after the main DFS pass.
        """
        self.random = random.Random(seed)
        self.perfect = perfect

    def generate(self, maze: MazeGrid, entry: Coord
                 ) -> Generator[CellGrid, None, None]:
        """Generate a maze incrementally using DFS backtracking.

        Args:
            maze: Maze grid to mutate in place.

        Yields:
            The current maze cell grid after each wall removal.
        """
        stack: List[Coord] = [entry]
        visited: Set[Coord] = {entry}

        while stack:
            y, x = stack[-1]
            if neighbors := [
                (ny, nx, wall, opposite)
                for ny, nx, wall, opposite in maze.neighbors(y, x)
                if (ny, nx) not in visited
            ]:
                ny, nx, wall, opposite = self.random.choice(neighbors)
                maze.remove_wall(y, x, ny, nx, wall, opposite)
                visited.add((ny, nx))
                stack.append((ny, nx))
                yield maze.cells
            else:
                stack.pop()

        if self.perfect is False:
            yield from self.open_extras(maze, visited)

    def open_extras(self, maze: MazeGrid, visited: Set[Coord]
                    ) -> Generator[CellGrid, None, None]:
        """Generate extra 20% wall openings to make an unperfect maze.

        The generator yields the maze grid after each wall removal, making it
        suitable for implementing with the generate().

        Args:
            maze: Maze grid to mutate in place.

        Yields:
            The current maze cell grid after each generation step.
        """
        extras = round((maze.height * maze.width) * 0.2)
        while extras:
            y = self.random.randint(0, maze.height - 1)
            x = self.random.randint(0, maze.width - 1)
            while (y, x) not in visited:
                y = self.random.randint(0, maze.height - 1)
                x = self.random.randint(0, maze.width - 1)
            if neighbors := list(maze.neighbors(y, x)):
                ny, nx, wall, opposite = self.random.choice(neighbors)
                if not maze.creates_open_3x3(y, x, ny, nx):
                    maze.remove_wall(y, x, ny, nx, wall, opposite)
                    extras -= 1
                    yield maze.cells


# === Generator API ===

class MazeGenerator:
    """High-level API for maze creation, validation, and solving.

    This class owns the maze grid, configures the requested generation
    algorithm, optionally embeds the `42` pattern as blocked cells, and
    provides a breadth-first solver for generated mazes.
    """
    def __init__(
            self,
            width: int,
            height: int,
            entry: Coord = (0, 0),
            exit: Coord | None = None,
            seed: int = 0,
            perfect: bool = True,
            algorithm: str = "prim"
    ) -> None:
        """Initialize a maze generation session.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            entry: Starting cell coordinate as `(row, column)`.
            exit: Target cell coordinate as `(row, column)`.
            seed: Seed for deterministic generation.
            perfect: Whether to generate a perfect maze.
            algorithm: Generation algorithm name. Supported values are
                `"prim"` and `"dfs"`.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.exit = exit if exit is not None else (height - 1, width - 1)
        self.perfect = perfect
        self.maze_grid = MazeGrid(self.width, self.height)
        self.algorithm = algorithm.lower().strip()
        self.logo = self.set_42()

    def set_42(self) -> Optional[Set[Coord]]:
        """Embed a centered `42` pattern as blocked cells in the maze.

        The pattern size is selected according to maze dimensions.

        Returns:
            The set of blocked coordinates if a pattern was added, or `None`
            when the maze is too small to place the pattern.
        """
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
            return None
        if self.width < 15 or self.height < 15:
            pattern = pat_small
        elif self.width < 20 or self.height < 20:
            pattern = pat_med
        else:
            pattern = pat_big
        self.maze_grid.add_pattern(pattern)
        return self.maze_grid.pat_coords

    def validate_entry_exit(self) -> None:
        """Validate entry and exit positions.

        Returns:
            `True` if both coordinates are valid, distinct, and not blocked by
            the reserved pattern; otherwise `False`.
        """
        if not self.maze_grid.in_bounds(*self.entry):
            raise ValueError("Entry out of bounds")
        if not self.maze_grid.in_bounds(*self.exit):
            raise ValueError("Exit out of bounds")
        if self.entry == self.exit:
            raise ValueError("Entry and exit have the same cell")

    def generate_maze(self) -> Generator[CellGrid, None, None]:
        """Create and return the configured maze-generation iterator.

        Returns:
            A generator that mutates the internal maze grid and yields the cell
            matrix after each generation step.

        Raises:
            ValueError: If the configured algorithm name is not supported.
        """
        gen: dict[str, type[PrimGenerator] | type[DFSGenerator]] = {
            "prim": PrimGenerator,
            "dfs": DFSGenerator
        }
        if self.algorithm not in gen:
            raise ValueError("Unkwnown algorithm")
        return gen[self.algorithm](self.seed, self.perfect).generate(
            self.maze_grid, self.entry
        )

    @staticmethod
    def solve(cells: CellGrid, entry: Coord,
              exit: Coord) -> Tuple[list[Coord], str]:
        """Solve a maze using breadth-first search.

        The returned path is guaranteed to be one of the shortest paths in
        terms of number of steps, assuming the maze is connected between
        `entry` and `exit`.

        Args:
            cells: Maze cell grid using the wall-bitmask representation.
            entry: Starting coordinate as `(row, column)`.
            exit: Destination coordinate as `(row, column)`.

        Returns:
            A tuple containing:

            - the ordered list of coordinates from entry to exit
            - a compact direction string using `N`, `E`, `S`, `W`

        Raises:
            KeyError: If no path exists from `entry` to `exit`.
        """
        queue: deque[Coord] = deque([entry])
        visited: Set[Coord] = {entry}
        prev_cell: Dict[Coord, Tuple[Coord, int]] = {}

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
        coords: List[Coord] = [exit]
        current = exit
        dir_str = "NESW"

        while current != entry:
            (py, px), i = prev_cell[current]
            path = dir_str[i] + path
            coords.insert(0, (py, px))
            current = (py, px)

        return coords, path


def main() -> None:
    """Run a small demo that generates and solves a maze."""
    entry = (0, 0)
    exit = (9, 8)
    maze_gen = MazeGenerator(10, 10, entry, exit, 0, False, "prim")

#    logo = maze_gen.logo
    try:
        maze_gen.validate_entry_exit()
        print("Entry and exit values validated")
    except Exception:
        pass

    maze_generator = maze_gen.generate_maze()
    # Generator passo a passo do algoritmo
    next_grid = []
    i = 0
    for step in maze_generator:
        next_grid = step
        print(next_grid)
        print()
        i += 1
    print(i)
    print()
    coords, path = maze_gen.solve(next_grid, entry, exit)
    print(path)
    for line in coords:
        print(line)
    print()


if __name__ == "__main__":
    main()
