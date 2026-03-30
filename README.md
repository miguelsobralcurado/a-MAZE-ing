*This project has been created as part of the 42 curriculum by <msobral-@student.42lisboa.com>, <lyokoiga@student.42lisboa.com>.*
<br/><br/>
<h1 align="center">🧩 a-MAZE-ing</h1>

<p align="center">
    <img src="https://github.com/miguelsobralcurado/a-MAZE-ing/blob/main/media/a-maze-ing.png" width="630px" alt="Screenshot of the terminal" />
</p>
<p align="center">
  Procedurally generating mazes one cell at a time! Something something Daedalus.
</p>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/miguelsobralcurado/a-MAZE-ing?style=for-the-badge" />
    <img src="https://img.shields.io/github/last-commit/miguelsobralcurado/a-MAZE-ing?style=for-the-badge" />
    <img src="https://img.shields.io/github/contributors/miguelsobralcurado/a-MAZE-ing?style=for-the-badge" />
</p>
<table align="center">
    <tbody>
        <tr>
            <td align="center" valign="top" width="16%"><a href="https://github.com/miguelsobralcurado"><img src="https://avatars.githubusercontent.com/u/174656941?v=4" width="100px;" alt="Miguel Sobral Curado"/><br /><sub><b>Miguel Sobral Curado</b></sub></a><br /><a href="#question-miguelsobralcurado" title="Answering Questions">💬</a></td>
            <td align="center" valign="top" width="14%"><a href="https://github.com/Lyokoigawa"><img src="https://avatars.githubusercontent.com/u/78232506?v=4" width="100px;" alt="Lyokoigawa"/><br /><sub><b>Lyokoigawa</b></sub></a><br /><a href="#question-lyokoigawa" title="Answering Questions">💬</a>
        </tr>
    </tbody>
</table>



## 📌 Description

**`A-Maze-ing`** is a configurable maze generation program written in Python that produces a solvable, fully connected maze, that can be perfect or imperfect (Meaning it has only one possible solution between entry and exit).

The project demonstrates applications of:

- Graph theory (Spanning trees)
- Randomized algorithms
- File parsing and validation
- Data encoding (bitwise hexadecimal representation)
- Visualization techniques using ASCII

The programs reads and parses the contents of a configuration file (config.txt) and runs a UI, that can be used to generate mazes based on the parameters provided and provides a visual representation, then outputting the result in an encoded format in an output file (output_file.txt)

## 📁 Project Structure

```text
.
├── a_maze_ing.py
├── config.txt
├── Makefile
├── mazegen-*.tar.gz
├── mazegen.py
├── pyproject.toml
├── README_MAZEGENERATOR.md
├── README.md
└── render_ascii.py
```

## 🧠 MazeGenerator and Algorithms

Reusable maze generator module.

### - ⚙️ Installation

```bash
pip install ./mazegen-*.tar.gz
```

### - Basic usage

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

### - Custom parameters

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

### - Access the generated structure

```python
cells = gen.maze_grid.cells
print(cells)
```

### - Access a solution

```python
coords, path = gen.solve(gen.maze_grid.cells, gen.entry, gen.exit)
print(path)
```

### - Algorithms

| Algorithm | Usage | Description|
|-------------|-------------|---------------|
| Randomized Prim's Algorithm | Maze Generation | Prim is a maze generation specific algorithm that searches keeps track of all the walls available to open and applies a random opening on one of them until all cells are connected. |
|Recursive DFS (Depth-First Search) | Maze Generation | DFS is a standard graph algorithm that traverses or searches tree and graph data structures by exploring a branch as deeply as possible before backtracking implementing stack data operations. |
| BFS (Breadth-First Search) | Path Finding | BFS is also a standard graph algorithm. It's a graph traversal technique that explores a graph or tree data structure level by level. BFS gives us the smallest path between graph nodes. For that reason it's used for the path solution. |


## 🚀 Instructions

### 🛠️ Requirements

- Python 3.10+
- pip

### Setup

```bash
make
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip build wheel setuptools
python -m build

pip install mazegen-1.0.0.tar.gz
```

### Usage

```bash
python3 a_maze_ing.py config.txt
```

**Example**

```bash
python3 a_maze_ing.py configs/funny_maze.txt
```

### Configuration File Format

The config file uses `KEY=VALUE` pairs:

Example:
```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=False
```

Optional settings:
```text
SEED=2112
ALGORITHM=dfs
```
| key | Value |
|--------|-----------|
|`Width`| Sets the width of the maze|
|`Height`| Sets the height of the maze|
|`Entry`| The maze's entry (coordinates start from 0)|
|`Exit`| The maze's exit (Coordinates start from 0)|
|`Output_File`| Will contain the resulting maze using hexadecimal encoding for each cell, the entry and exit coordinates, and the fastest solution|
|`Perfect`| Toggle to allow the creation of a perfect maze (Meaning it will only have one valid path)|
|`Seed`| The seed with which the program will generate based on|
|`Algorithm`| The algorithm used to create the maze (Supports only 'prim' and 'dfs')|

⚠️ If an incorrect value is found, the program will handled gracefully


## 🌈 Team & Project Management

### Roles

- Team Leader: miguelsobralcurado (msobral-)
- Core algorithm & Data structures: miguelsobralcurado (msobral-)
- Parsing, Validation & Error handling: Lyokoigawa (lyokoiga)
- Visualization & UX: Lyokoigawa (lyokoiga)

### Planning

- Start phase: Prototyping visuals & Algorithm selection
- Middle phase: UI development & Generator implementation
- Final phase: Animator & Packaging

### What worked well

- Early testing strategy
- Generator to Animator logic
- Separation of tasks

### What could be improved

- ¯\\\_(ツ)\_/¯
- Our workflow ran very smoothly and the objectives we had in the begining were met. There were no bumps or misfortunes at any of the stages of the project.

### Tools Used

- Git / Github
- `flake8`, `mypy`
- VSCode
- Live Share

## Resources
- https://github.com/foundersandcoders/git-workflow-workshop-for-two


- https://www.youtube.com/watch?v=V1oZQm1HtVw
- https://www.youtube.com/watch?v=ioUl1M77hww&pp=ygUWcHl0aG9uIG1hemUgZ2VuZXJhdGlvbg%3D%3D
- https://github.com/JTexpo/Maze_Solver_BFS/blob/main/maze_solver_bfs/maze_solver.py
- https://www.geeksforgeeks.org/dsa/count-number-of-ways-to-reach-destination-in-a-maze-using-bfs/

- https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
- https://en.wikipedia.org/wiki/Box-drawing_characters

## Bonuses (Optional)

- Multiple algorithms support
- Animated maze generation

## 🤖 AI Contributions

- Help in prototyping this README
- Help in optimizing the code structure
- Debugging

---

## 🛎️ License

This project is part of the [42 Network](https://www.42network.org/) curriculum.
