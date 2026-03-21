from collections import deque
from typing import List, Dict


maze_grid = [
    [3, 13, 11, 11],
    [10, 3, 4, 8],
    [2, 4, 9, 10],
    [6, 13, 14, 14]
]


def bfs(cells: List[list[int]], entry: tuple[int, int],
        exit: tuple[int, int]) -> list[list[tuple[int, int]], str]:
    # Visited is a set for complexity.
    # 'n not in visited' below is O(1) instead of O(n).
    visited = set()
    # Queue is a deque for complexity too.
    # Popping the first element is O(1) instead of O(n).
    queue = deque()

    prev_cell: Dict[tuple[int, int], tuple[int, int], int] = dict()
    dir_str = "NESW"

    visited.add(entry)
    queue.append(entry)

    while queue:
        y, x = queue.popleft()

        if (y, x) == exit:
            break

        for i in range(4):
            if cells[y][x] & (1 << i) == 0:
                ny = y
                nx = x
                if i == 0:
                    ny -= 1
                elif i == 1:
                    nx += 1
                elif i == 2:
                    ny += 1
                elif i == 3:
                    nx -= 1
                next = (ny, nx)
                if next not in visited:
                    prev_cell[next] = ((y, x), i)
                    visited.add(next)
                    queue.append(next)
    path: str = ''
    coords: List[tuple[int, int]] = []
    current = exit
    coords.append(exit)
    while current != entry:
        (py, px), i = prev_cell[current]
        path = dir_str[i] + path
        coords.insert(0, (py, px))
        current = (py, px)

    return [coords, path]


def main():
    output = bfs(maze_grid, (0, 0), (2, 3))
    print(output[1])
    print()
    for line in output[0]:
        print(line)


main()
