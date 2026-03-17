# import sys
# import time
# from config import load_config
# from mazegen import MazeGenerator
from render_test import AsciiRender


# def main(argv: list[str]) -> int:
#     try:
#         with open(argv[1]) as cfg:
#         gen = MazeGenerator()
#         while True:
#             if gen.visual is True:
#                 iter = gen.Generate()
#                 animate_gen(iter)
#                 time.sleep(anim_speed)
#             if gen.Complete is True:
#                 break
#     except FileNotFoundError:
#         print("Usage: python3 a_maze_ing.py <config file path>",
#               file=sys.stderr)
#         return 2


if __name__ == "__main__":
    maze = AsciiRender(25, 25)
    maze.builder()
