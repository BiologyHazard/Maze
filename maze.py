import random

import numpy as np

DIRECTIONS = [
    (1, 0),  # Down
    (0, 1),  # Right
    (-1, 0),  # Up
    (0, -1)  # Left
]


def _is_inner(maze, pos):
    return (1 <= pos[0] <= 2 * maze.H - 1) and (1 <= pos[1] <= 2 * maze.W - 1)


class Maze_grid:
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
        self.map = np.array([[Maze_grid.YELLOW if j % 2 == 1 and i % 2 == 1
                              else Maze_grid.WALL for j in range(2 * W + 1)]
                             for i in range(2 * H + 1)], dtype=np.int8)
        # self.map[start[0]][start[1]] = Maze.START
        # self.map[end[0]][end[1]] = Maze.END
        # self.generate()

    def generate(self):
        self.map[1][1] = Maze_grid.ROAD
        self.map[1][2] = Maze_grid.BLUE
        self.map[2][1] = Maze_grid.BLUE
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
                if self.map[opp_pos[0], opp_pos[1]] == Maze_grid.YELLOW:
                    self.map[opp_pos[0], opp_pos[1]] = Maze_grid.ROAD
                    self.map[blue_pos[0], blue_pos[1]] = Maze_grid.ROAD
                    for dir in Maze_grid.DIRECTIONS:
                        pos = opp_pos + dir
                        if _is_inner(self, pos):
                            if self.map[pos[0], pos[1]] == Maze_grid.WALL:
                                # f.write('pos' + str(pos))
                                # f.write('dir' + str(dir))
                                self.map[pos[0], pos[1]] = Maze_grid.BLUE
                                blues.append(np.array([pos, dir]))
                else:
                    self.map[blue_pos[0], blue_pos[1]] = Maze_grid.WALL
            del blues[x]
            # self.print()
        self.map[self.start[0], self.start[1]] = Maze_grid.START
        self.map[self.end[0], self.end[1]] = Maze_grid.END

    def print_to_file(self, filename=r"maze.txt", output_dict=None):
        if output_dict is None:
            output_dict = Maze_grid.output_dict
        with open(filename, 'w', encoding='utf-8') as f:
            for i in self.map:
                for j in i:
                    f.write(output_dict[j])
                f.write('\n')

    def export_pic(self, filename=r"maze.png", pixels=10, s=0.3):
        from PIL import Image, ImageDraw
        image = Image.new('RGBA', ((2 * self.W + 1) * pixels,
                                   (2 * self.H + 1) * pixels), (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)
        for i in range(2 * self.H + 1):
            for j in range(2 * self.W + 1):
                if self.map[i][j] in (Maze_grid.ROAD, Maze_grid.START, Maze_grid.END):
                    draw.rectangle(((round((j-s)*pixels), round((i-s)*pixels)),
                                    (round((j+1+s)*pixels), round((i+1+s)*pixels))), fill=(255, 255, 255, 255))
        image.save(filename)


class Maze:
    KRUSKAL = 0
    PRIM = 1
    RECURSIVE_BACKTRACKING = 2

    def __init__(self, w: int = 16, h: int = 16, start=None, end=None) -> None:
        self.w = w
        self.h = h
        self.start = start
        self.end = end

    def generate(self, method: int = KRUSKAL) -> None:
        self.map = np.zeros((self.h, self.w, 2), dtype=np.bool_)
        if method == Maze.KRUSKAL:
            self._generate_kruskal()
        elif method == Maze.PRIM:
            self._generate_prim()
        elif method == Maze.RECURSIVE_BACKTRACKING:
            self._generate_recursive_backtracking()
        else:
            raise ValueError

    def _generate_kruskal(self) -> None:
        def find(x: int, y: int) -> int:
            if parents[x][y] != (x, y):
                parents[x][y] = find(*parents[x][y])
            return parents[x][y]

        def union(x1: int, y1: int, x2: int, y2: int) -> None:
            x1, y1 = find(x1, y1)
            x2, y2 = find(x2, y2)
            parents[x2][y2] = (x1, y1)

        parents = [[(i, j) for j in range(self.w)] for i in range(self.h)]
        edges = []
        for i in range(self.h):
            for j in range(self.w):
                if i < self.h - 1:
                    edges.append(((i, j), (i+1, j), 0))
                if j < self.w - 1:
                    edges.append(((i, j), (i, j+1), 1))

        random.shuffle(edges)
        for edge in edges:
            (x1, y1), (x2, y2), direction = edge
            if find(x1, y1) != find(x2, y2):
                self.map[x1][y1][direction] = True
                union(x1, y1, x2, y2)

    def _generate_prim(self) -> None:
        pass

    def _generate_recursive_backtracking(self) -> None:
        '递归解法会爆栈'
        # def recur(x: int, y: int) -> None:
        #     visited[x][y] = True

        #     psb_dirs = []
        #     for dx, dy in DIRECTIONS:
        #         xx, yy = x+dx, y+dy
        #         if 0 <= xx < self.h and 0 <= yy < self.w:
        #             if not visited[xx][yy]:
        #                 psb_dirs.append((dx, dy))

        #     if not psb_dirs:
        #         return

        #     random.shuffle(psb_dirs)
        #     for dx, dy in psb_dirs:
        #         xx, yy = x+dx, y+dy
        #         if not visited[xx][yy]:
        #             if (dx, dy) == (1, 0):
        #                 self.map[x][y][0] = True
        #             elif (dx, dy) == (0, 1):
        #                 self.map[x][y][1] = True
        #             elif (dx, dy) == (-1, 0):
        #                 self.map[x-1][y][0] = True
        #             else:
        #                 self.map[x][y-1][1] = True
        #             recur(xx, yy)

        # visited = np.zeros((self.h, self.w), dtype=np.bool_)
        # recur(random.randrange(self.h), random.randrange(self.w))

        visited = np.zeros((self.h, self.w), dtype=np.bool_)
        stack = []
        stack.append((random.randrange(self.h), random.randrange(self.w)))
        while stack:
            # print(stack)
            x, y = stack[-1]
            visited[x][y] = True

            psb_dirs = []
            for dx, dy in DIRECTIONS:
                xx, yy = x+dx, y+dy
                if 0 <= xx < self.h and 0 <= yy < self.w:
                    if not visited[xx][yy]:
                        psb_dirs.append((dx, dy))

            if not psb_dirs:
                stack.pop()

            else:
                dx, dy = random.choice(psb_dirs)
                xx, yy = x+dx, y+dy
                if not visited[xx][yy]:
                    if (dx, dy) == (1, 0):
                        self.map[x][y][0] = True
                    elif (dx, dy) == (0, 1):
                        self.map[x][y][1] = True
                    elif (dx, dy) == (-1, 0):
                        self.map[x-1][y][0] = True
                    else:
                        self.map[x][y-1][1] = True
                    stack.append((xx, yy))

    def print_to_file(self, filename=r"maze.txt", output_dict=None):
        # if output_dict is None:
        #     output_dict = Maze_grid.output_dict
        # with open(filename, 'w', encoding='utf-8') as f:
        #     for i in self.map:
        #         for j in i:
        #             f.write(output_dict[j])
        #         f.write('\n')
        m = np.empty((self.h * 2 + 1, self.w * 2 + 1), dtype=np.str_)
        m.fill('#')
        for i in range(self.h):
            for j in range(self.w):
                m[2*i+1][2*j+1] = ' '
                if self.map[i][j][0]:
                    m[2*i+2][2*j+1] = ' '
                if self.map[i][j][1]:
                    m[2*i+1][2*j+2] = ' '
        for line in m:
            print(*line)

    def export_pic(self, filename=r"maze.png", pixels=10, s=0.3):

        from PIL import Image, ImageDraw
        image = Image.new('RGBA',
                          (self.w * pixels, self.h * pixels),
                          (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)
        for i in range(self.h):
            for j in range(self.w):
                draw.rectangle(((round((j+s)*pixels), round((i+s)*pixels)),
                                (round((j+1-s)*pixels), round((i+1-s)*pixels))),
                               fill=(255, 255, 255, 255))
                if self.map[i][j][0]:
                    draw.rectangle(((round((j+s)*pixels), round((i+1/2+s)*pixels)),
                                    (round((j+1-s)*pixels), round((i+1+1/2-s)*pixels))),
                                   fill=(255, 255, 255, 255))
                if self.map[i][j][1]:
                    draw.rectangle(((round((j+1/2+s)*pixels), round((i+s)*pixels)),
                                    (round((j+1+1/2-s)*pixels), round((i+1-s)*pixels))),
                                   fill=(255, 255, 255, 255))

        image.save(filename)


if __name__ == '__main__':
    import time
    maze = Maze(16, 16)
    t0 = time.time()
    maze.generate(method=Maze.RECURSIVE_BACKTRACKING)
    # maze.generate(method=Maze.KRUSKAL)
    print(f'time used {time.time() - t0:.3f}s')

    # maze.export_pic('maze.png', 5, 0.125)
    maze.export_pic('maze.png', 4, 0.25)
    # maze.print_to_file()
