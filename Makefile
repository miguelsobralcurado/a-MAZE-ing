PY = python3
PIP = pip

NAME = a_maze_ing.py
REND = render_ascii.py
FILE = config.txt

install:
	$(PIP) install flake8
	$(PIP) install mypy

run:
	$(PY) $(NAME) $(FILE)

debug:
	$(PY) -m pdb $(NAME) $(FILE)

clean:
	rm -rf __pycache__/ .mypy_cache/  build/ dist/ *.egg-info

lint:
	flake8 .
	mypy $(NAME) $(REND) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy $(NAME) $(REND) --strict

.PHONY: install run debug clean lint lint-strict