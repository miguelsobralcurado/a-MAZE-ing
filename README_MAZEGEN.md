# mazegen

Reusable maze generator module.

## Installation

```bash
pip install dist/mazegen-1.0.0.tar.gz
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
