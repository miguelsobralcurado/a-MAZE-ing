# mazegen

Reusable maze generator module.

## Installation

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
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


https://github.com/foundersandcoders/git-workflow-workshop-for-two


https://www.youtube.com/watch?v=V1oZQm1HtVw
https://github.com/JTexpo/Maze_Solver_BFS/blob/main/maze_solver_bfs/maze_solver.py
https://www.geeksforgeeks.org/dsa/count-number-of-ways-to-reach-destination-in-a-maze-using-bfs/
