# mazegen

Reusable maze generator module.

## ⚙️ Installation

```bash
pip install ./mazegen-*.tar.gz
```

## Basic usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(10, 10, seed=42)

for _ in gen.generate_maze():
    pass

cells = gen.maze_grid.cells
coords, path = gen.solve(cells, gen.entry, gen.exit)

print("Path:", path)
print("Coordinates:", coords)
```

## Custom parameters

```python
gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(14, 19),
    seed=123,
    perfect=False,
    algorithm="dfs",
)
```

## Access the generated structure

```python
cells = gen.maze_grid.cells
print(cells)
```

## Access a solution

```python
coords, path = gen.solve(gen.maze_grid.cells, gen.entry, gen.exit)
print(path)
```

## Algorithms

| Algorithm | Usage | Description|
|-------------|-------------|---------------|
| Randomized Prim's Algorithm | Maze Generation | Prim is a maze generation specific algorithm that searches keeps track of all the walls available to open and applies a random opening on one of them until all cells are connected. |
|Recursive DFS (Depth-First Search) | Maze Generation | DFS is a standard graph algorithm that traverses or searches tree and graph data structures by exploring a branch as deeply as possible before backtracking implementing stack data operations. |
| BFS (Breadth-First Search) | Path Finding | BFS is also a standard graph algorithm. It's a graph traversal technique that explores a graph or tree data structure level by level. BFS gives us the smallest path between graph nodes. For that reason it's used for the path solution. |
