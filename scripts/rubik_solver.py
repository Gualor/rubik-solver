from visual3D import VisualCube
from cube_2x2x2 import Cube
import numpy as np
import time
import copy
import os


class Node:
    def __init__(self, cube, g, seq):
        self.cube = cube  # state
        self.g = g  # path cost from root
        self.sequence = seq  # sequence of moves
        self.h = self.heuristic(cube)  # compute heuristic value

    def heuristic(self, cube):
        h = 0
        for id, face in cube.faces.items():
            if id == "F":
                h += (4 - list(face).count("G"))
            if id == "B":
                h += (4 - list(face).count("B"))
            if id == "R":
                h += (4 - list(face).count("R"))
            if id == "L":
                h += (4 - list(face).count("O"))
            if id == "U":
                h += (4 - list(face).count("W"))
            if id == "D":
                h += (4 - list(face).count("Y"))
        return h/4


def cube_solver(cube):
    frontier = [Node(cube, 0, ["START"])]
    visited = []
    opposite = {"B": "F", "L": "R", "D": "U"}
    while(frontier):
        min_f = 100000
        index = None
        for i in range(len(frontier)):
            # select best node in frontier
            f = frontier[i].g + frontier[i].h
            if f < min_f:
                min_f = f
                index = i
        # remove and return node from frontier
        node = frontier.pop(index)
        if node.g <= 11:
            #print(min_f, node.g, min_f - node.g)
            if node not in visited:
                visited.append(node)
                # goal test
                if node.cube.solved:
                    return node.sequence
                # expand node and update frontier
                moves = node.cube.apply_all_moves()
                old_move = node.sequence[-1]
                for move, cube in moves.items():
                    # prune moves on same face twice in a row
                    if move[0] != old_move[0]:
                        # prune moves on opposite face
                        if old_move[0] in opposite.keys():
                            if opposite[old_move[0]] != move[0]:
                                frontier.append(Node(cube, node.g + 1, node.sequence + [move]))
                        else:
                            frontier.append(Node(cube, node.g + 1, node.sequence + [move]))


if __name__ == "__main__":

    F = np.array(["G"]*4)
    B = np.array(["B"]*4)
    R = np.array(["R"]*4)
    L = np.array(["O"]*4)
    U = np.array(["W"]*4)
    D = np.array(["Y"]*4)

    # cube definition
    cube = Cube(F, B, R, L, U, D)

    # Rubik's cube 3D render
    cube_render = VisualCube(cube)
    os.system("cls")

    # main loop
    exit_loop = False
    while not (exit_loop):

        # scramble cube
        while(True):
            cube.print_cube()
            print("Use the following symbols separated by spaces to scramble the cube:")
            print("F  F' F2  B  B' B2  R  R' R2  L  L' L2  U  U' U2  D  D' D2\n")
            print("Enter sequence:", end=" ")

            # read user move sequence
            seq = str(input()).split(" ")

            # apply sequence
            print("Scrambling...\n")
            cube = cube.apply_sequence(seq)
            cube_render.animate(seq)
            cube.print_cube()
            print("Solving...\n")
            break

        # returns the shortest sequence to solve the cube
        solution = cube_solver(cube)

        # print out moves sequence
        string = ""
        for i in solution[1:]:
            string += (" " + i)
        print("Sequence to solve the cube: {}\n".format(string))

        # cube Solving
        for move in solution[1:]:
            # apply move
            print("Applying move:", move)
            time.sleep(1)
            cube = cube.apply_sequence([move])
            cube_render.animate([move])
            cube.print_cube()
        print("The cube is now solved.\n")

        # Continue
        ans = None
        while(ans not in ["Yes", "Y", "y", "No", "N", "n"]):
            print("Continue? [Yes/No]:", end=" ")
            ans = str(input())
            if ans in ["No", "N", "n"]:
                exit_loop = True
            elif ans in ["Yes", "Y", "y"]:
                os.system("cls")
