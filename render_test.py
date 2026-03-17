# import sys
# import os
import time
# from config import Config
# from mazegen import MazeGenerator, Maze
# from serializer import write_output_file


class AsciiRender:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        maze_pieces = [
            f""
        ]

    # def _draw_maze(self,
    #                maze: Maze,
    #                cfg: Config,
    #                path: list[str],
    #                visited: set[tuple[int, int]] | None = None,
    #                frontier: set[tuple[int, int]] | None = None,
    #                current: tuple[int, int] | None = None) -> None:
    #     self.current = current

    def calc_piece(self, curr_cell, path) -> str:
        cell_base = [0, 0, 0, 0]
        default_piece1 = "    "
        default_piece2 = "   ┼"
        if curr_cell == 4:
            default_piece2 = "───┼"
        elif curr_cell == 8:
            curr_cell

    def animator(self) -> None:
        curr_x, curr_y = self.current
        time.sleep(0.3)

    def builder(self) -> None:
        print("┌" + ("───┬" * (self.width - 1)) + "───┐")
        for i in range(1, self.height):
            print("│   ", end="")
            for _ in range(1, self.width):
                print(("│ ▪ │" * (self.width - 1)) + " ▪ ")
            print("├" + ("───┼" * (self.width - 1)) + "───┤")
        print("│" + (" ▪ │" * (self.width - 1)) + " ▪ │")
        print("└" + ("───┴" * (self.width - 1)) + "───┘")


# if __name__ == "__main__":
    # os.system('clear')
    # print("Hello party people!")

# print("\033[F\033[2K" * n, end="", flush=True) (clears n amount of lines)
# 0  = all open
# 1  = N closed
# 2  = E closed
# 3  = NE closed
# 4  = S closed
# 5  = NS closed
# 6  = ES closed
# 7  = NES closed
# 8  = W closed
# 9  = NW closed
# 10 = EW closed
# 11 = NEW closed
# 12 = SW closed
# 13 = NSW closed
# 14 = ESW closed
# 15 = NESW closed

