from cube_2x2x2 import Cube
import numpy as np


def get_state(cube):
    state = ""
    for id, face in cube.faces.items():
        for color in face:
            state += color
    return state


def state_to_cube(s):
    F = np.array(list(s[0:4]))
    B = np.array(list(s[4:8]))
    R = np.array(list(s[8:12]))
    L = np.array(list(s[12:16]))
    U = np.array(list(s[16:20]))
    D = np.array(list(s[20:24]))
    return Cube(F, B, R, L, U, D)


class Node:
    def __init__(self, string, depth, move):
        self.s = string
        self.g = depth
        self.m = move


def bfs():
    init = "GGGGBBBBRRRROOOOWWWWYYYY"
    frontier = [Node(init, 0, "START")]
    visited = []
    table = {}
    while(len(table) < 100000):  # 3674160):
        print(len(table))
        node = frontier.pop(0)
        if not node in visited:
            visited.append(node)
            moves = state_to_cube(node.s).apply_all_moves()
            old_move = node.m
            for move, cube in moves.items():
                # fix corner "DBL"
                if move[0] not in ["D", "B", "L"]:
                    # prune same face moves
                    if move[0] != old_move[0]:
                        string = get_state(cube)
                        frontier.append(Node(string, node.g+1, move))
                        if string not in table.keys():
                            table[string] = node.g+1
    return table


if __name__ == "__main__":

    db = BFS()
    print(db.values())
