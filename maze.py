import random
from re import I
import numpy as np


def _is_inner(maze, pos):
    return (1 <= pos[0] <= 2 * maze.H - 1) and (1 <= pos[1] <= 2 * maze.W - 1)


class Maze:
    START = 0
    END = 1
    WALL = 4
    YELLOW = 5
    BLUE = 6
    ROAD = 7
    DIRECTIONS = np.array([
        (1, 0),  # Down
        (0, 1),  # Right
        (-1, 0),  # Up
        (0, -1)  # Left
    ])
    output_dict = {
        START: '🟧',
        END: '🟩',
        WALL: '⬛',
        YELLOW: '🟨',
        BLUE: '🟦',
        ROAD: '⬜',
    }
    # output_dict = {
    #     START: 'S',
    #     END: 'E',
    #     WALL: '#',
    #     ROAD: '.',
    #     GRAY: '#',
    #     YELLOW: 'Y',
    #     BLUE: 'B',
    #     RED: 'R',
    # }

    def __init__(self, W=16, H=16, start=None, end=None):
        self.W = W
        self.H = H
        if start is None:
            start = (0, 1)
        if end is None:
            end = (2 * self.H, 2 * self.W - 1)
        self.start = start
        self.end = end
        self.map = np.array([[Maze.YELLOW if j % 2 == 1 and i % 2 == 1
                              else Maze.WALL for j in range(2 * W + 1)]
                             for i in range(2 * H + 1)], dtype=np.int8)
        # self.map[start[0]][start[1]] = Maze.START
        # self.map[end[0]][end[1]] = Maze.END
        # self.generate()

    def generate(self):
        self.map[1][1] = Maze.ROAD
        self.map[1][2] = Maze.BLUE
        self.map[2][1] = Maze.BLUE
        blues = []
        blues.append(np.array([(1, 2), (0, 1)]))
        blues.append(np.array([(2, 1), (1, 0)]))
        while blues:
            x = random.randrange(len(blues))
            blue_pos = blues[x][0]
            opp_pos = blue_pos + blues[x][1]
            # f.write('choose' + str(blue_pos))
            # f.write('opp' + str(opp_pos))
            if _is_inner(self, opp_pos):
                if self.map[opp_pos[0], opp_pos[1]] == Maze.YELLOW:
                    self.map[opp_pos[0], opp_pos[1]] = Maze.ROAD
                    self.map[blue_pos[0], blue_pos[1]] = Maze.ROAD
                    for dir in Maze.DIRECTIONS:
                        pos = opp_pos + dir
                        if _is_inner(self, pos):
                            if self.map[pos[0], pos[1]] == Maze.WALL:
                                # f.write('pos' + str(pos))
                                # f.write('dir' + str(dir))
                                self.map[pos[0], pos[1]] = Maze.BLUE
                                blues.append(np.array([pos, dir]))
                else:
                    self.map[blue_pos[0], blue_pos[1]] = Maze.WALL
            del blues[x]
            # self.print()
        self.map[self.start[0], self.start[1]] = Maze.START
        self.map[self.end[0], self.end[1]] = Maze.END

    def print_to_file(self, filename=r"maze.txt", output_dict=None):
        if output_dict is None:
            output_dict = Maze.output_dict
        with open(filename, 'w', encoding='utf-8') as f:
            for i in self.map:
                for j in i:
                    f.write(output_dict[j])
                f.write('\n')

    def export_pic(self, filename, pixels=10, s=0.3):
        from PIL import Image, ImageDraw
        image = Image.new('RGBA', ((2 * self.W + 1) * pixels,
                                   (2 * self.H + 1) * pixels), (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)
        for i in range(2 * self.H + 1):
            for j in range(2 * self.W + 1):
                if self.map[i][j] in (Maze.ROAD, Maze.START, Maze.END):
                    draw.rectangle(
                        ((round((j-s)*pixels), round((i-s)*pixels)), (round((j+1+s)*pixels), round((i+1+s)*pixels))), fill=(255, 255, 255, 255))
        image.save(filename)


if __name__ == '__main__':
    maze = Maze(30, 30)
    maze.generate()
    # maze.print()
    maze.export_pic('maze.png', 10)
    maze.print_to_file()
