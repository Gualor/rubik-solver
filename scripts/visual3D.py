from cube_2x2x2 import Cube
import vpython as v
import numpy as np
import math
import time
import copy
import os

# color vector definition
RED = v.vector(1, 0, 0)
GREEN = v.vector(0, 1, 0)
BLUE = v.vector(0, 0, 1)
WHITE = v.vector(1, 1, 1)
ORANGE = v.vector(0.75, 0.45, 0)
YELLOW = v.vector(1, 1, 0)
BLACK = v.vector(0, 0, 0)
GRAY = v.vector(0.7, 0.7, 0.7)

# color coding
color_dict = {"W": WHITE, "R": RED, "Y": YELLOW, "B": BLUE, "G": GREEN, "O": ORANGE}


class Corner:
    # Corner piece class
    def __init__(self, scene, id, col1, col2, col3):
        if id == "0":  # FLU
            center = v.vector(-0.25, 0.25, 0.25)
            pos1 = v.vector(-0.25, 0.25, 0.5)  # F
            pos2 = v.vector(-0.5, 0.25, 0.25)  # L
            pos3 = v.vector(-0.25, 0.5, 0.25)  # U
        elif id == "1":  # BLU
            center = v.vector(-0.25, 0.25, -0.25)
            pos1 = v.vector(-0.25, 0.25, -0.5)  # B
            pos2 = v.vector(-0.5, 0.25, -0.25)  # L
            pos3 = v.vector(-0.25, 0.5, -0.25)  # U
        elif id == "2":  # BRU
            center = v.vector(0.25, 0.25, -0.25)
            pos1 = v.vector(0.25, 0.25, -0.5)  # B
            pos2 = v.vector(0.5, 0.25, -0.25)  # R
            pos3 = v.vector(0.25, 0.5, -0.25)  # U
        elif id == "3":  # FRU
            center = v.vector(0.25, 0.25, 0.25)
            pos1 = v.vector(0.25, 0.25, 0.5)  # F
            pos2 = v.vector(0.5, 0.25, 0.25)  # R
            pos3 = v.vector(0.25, 0.5, 0.25)  # U
        elif id == "4":  # FLD
            center = v.vector(-0.25, -0.25, 0.25)
            pos1 = v.vector(-0.25, -0.25, 0.5)  # F
            pos2 = v.vector(-0.5, -0.25, 0.25)  # L
            pos3 = v.vector(-0.25, -0.5, 0.25)  # D
        elif id == "5":  # BLD
            center = v.vector(-0.25, -0.25, -0.25)
            pos1 = v.vector(-0.25, -0.25, -0.5)  # B
            pos2 = v.vector(-0.5, -0.25, -0.25)  # L
            pos3 = v.vector(-0.25, -0.5, -0.25)  # D
        elif id == "6":  # BRD
            center = v.vector(0.25, -0.25, -0.25)
            pos1 = v.vector(0.25, -0.25, -0.5)  # B
            pos2 = v.vector(0.5, -0.25, -0.25)  # R
            pos3 = v.vector(0.25, -0.5, -0.25)  # D
        elif id == "7":  # FRD
            center = v.vector(0.25, -0.25, 0.25)
            pos1 = v.vector(0.25, -0.25, 0.5)  # F
            pos2 = v.vector(0.5, -0.25, 0.25)  # R
            pos3 = v.vector(0.25, -0.5, 0.25)  # D
        # single element definitions
        self.base = v.box(canvas=scene, pos=center,
                          length=0.5, height=0.5, width=0.5, color=BLACK)
        self.face1 = v.box(canvas=scene, pos=pos1,
                           length=0.45, height=0.45, width=0.001, color=color_dict[col1])
        self.face2 = v.box(canvas=scene, pos=pos2,
                           length=0.001, height=0.45, width=0.45, color=color_dict[col2])
        self.face3 = v.box(canvas=scene, pos=pos3,
                           length=0.45, height=0.001, width=0.45, color=color_dict[col3])
        # compound object definition
        self.compound = v.compound([self.base, self.face1, self.face2, self.face3])


class VisualCube:
    # class for pocket cube 3D render
    def __init__(self, cube):
        faces = cube.faces
        # scene and lights definition
        self.scene = v.canvas(background=GRAY, width=500, height=500)
        self.scene.range = 2
        self.scene.ambient = WHITE
        lights = []
        lights.append(v.distant_light(direction=v.vector(0.22, 0.44, -0.88), color=WHITE))
        lights.append(v.distant_light(direction=v.vector(-0.22, -0.44, 0.88), color=WHITE))
        self.scene.lights + lights
        # corner pieces definition
        self.corners = {}
        self.corners["0"] = Corner(self.scene, "0", faces["F"][0], faces["L"][1], faces["U"][2])
        self.corners["1"] = Corner(self.scene, "1", faces["B"][1], faces["L"][0], faces["U"][0])
        self.corners["2"] = Corner(self.scene, "2", faces["B"][0], faces["R"][1], faces["U"][1])
        self.corners["3"] = Corner(self.scene, "3", faces["F"][1], faces["R"][0], faces["U"][3])
        self.corners["4"] = Corner(self.scene, "4", faces["F"][2], faces["L"][3], faces["D"][0])
        self.corners["5"] = Corner(self.scene, "5", faces["B"][3], faces["L"][2], faces["D"][2])
        self.corners["6"] = Corner(self.scene, "6", faces["B"][2], faces["R"][3], faces["D"][3])
        self.corners["7"] = Corner(self.scene, "7", faces["F"][3], faces["R"][2], faces["D"][1])
        # initialize positios
        self.pos = {}
        self.pos["0"] = "0"
        self.pos["1"] = "1"
        self.pos["2"] = "2"
        self.pos["3"] = "3"
        self.pos["4"] = "4"
        self.pos["5"] = "5"
        self.pos["6"] = "6"
        self.pos["7"] = "7"

    def animate(self, seq):
        # animation of cube rotations
        for move in seq:
            if move == "F":
                self.f_cw()
            elif move == "F'":
                self.f_ccw()
            elif move == "F2":
                self.f_cw()
                self.f_cw()
            elif move == "B":
                self.b_cw()
            elif move == "B'":
                self.b_ccw()
            elif move == "B2":
                self.b_cw()
                self.b_cw()
            elif move == "R":
                self.r_cw()
            elif move == "R'":
                self.r_ccw()
            elif move == "R2":
                self.r_cw()
                self.r_cw()
            elif move == "L":
                self.l_cw()
            elif move == "L'":
                self.l_ccw()
            elif move == "L2":
                self.l_cw()
                self.l_cw()
            elif move == "U":
                self.u_cw()
            elif move == "U'":
                self.u_ccw()
            elif move == "U2":
                self.u_cw()
                self.u_cw()
            elif move == "D":
                self.d_cw()
            elif move == "D'":
                self.d_ccw()
            elif move == "D2":
                self.d_cw()
                self.d_cw()

    def f_cw(self):
        # front face clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["0"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["3"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["4"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["7"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["0"] = c_pos["4"]
        self.pos["4"] = c_pos["7"]
        self.pos["7"] = c_pos["3"]
        self.pos["3"] = c_pos["0"]

    def f_ccw(self):
        # front face counter clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["0"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["3"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["4"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["7"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["4"] = c_pos["0"]
        self.pos["7"] = c_pos["4"]
        self.pos["3"] = c_pos["7"]
        self.pos["0"] = c_pos["3"]

    def b_cw(self):
        # back face clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["1"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["2"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["5"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["6"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["1"] = c_pos["2"]
        self.pos["2"] = c_pos["6"]
        self.pos["6"] = c_pos["5"]
        self.pos["5"] = c_pos["1"]

    def b_ccw(self):
        # back face counter clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["1"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["2"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["5"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
            self.corners[self.pos["6"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 0, 1), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["2"] = c_pos["1"]
        self.pos["6"] = c_pos["2"]
        self.pos["5"] = c_pos["6"]
        self.pos["1"] = c_pos["5"]

    def r_cw(self):
        # right face clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["2"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["3"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["6"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["7"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["3"] = c_pos["7"]
        self.pos["7"] = c_pos["6"]
        self.pos["6"] = c_pos["2"]
        self.pos["2"] = c_pos["3"]

    def r_ccw(self):
        # right face counter clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["2"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["3"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["6"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["7"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["7"] = c_pos["3"]
        self.pos["6"] = c_pos["7"]
        self.pos["2"] = c_pos["6"]
        self.pos["3"] = c_pos["2"]

    def l_cw(self):
        # left face clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["0"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["1"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["4"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["5"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["0"] = c_pos["1"]
        self.pos["1"] = c_pos["5"]
        self.pos["5"] = c_pos["4"]
        self.pos["4"] = c_pos["0"]

    def l_ccw(self):
        # left face counter clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["0"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["1"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["4"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["5"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(1, 0, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["1"] = c_pos["0"]
        self.pos["5"] = c_pos["1"]
        self.pos["4"] = c_pos["5"]
        self.pos["0"] = c_pos["4"]

    def u_cw(self):
        # up face clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["0"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["1"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["2"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["3"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["1"] = c_pos["0"]
        self.pos["0"] = c_pos["3"]
        self.pos["3"] = c_pos["2"]
        self.pos["2"] = c_pos["1"]

    def u_ccw(self):
        # up face counter clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["0"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["1"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["2"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["3"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["0"] = c_pos["1"]
        self.pos["3"] = c_pos["0"]
        self.pos["2"] = c_pos["3"]
        self.pos["1"] = c_pos["2"]

    def d_cw(self):
        # down face clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["4"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["5"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["6"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["7"]].compound.rotate(
                angle=(math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["7"] = c_pos["4"]
        self.pos["6"] = c_pos["7"]
        self.pos["5"] = c_pos["6"]
        self.pos["4"] = c_pos["5"]

    def d_ccw(self):
        # down face counter clockwise
        for i in range(10):
            time.sleep(0.05)
            self.corners[self.pos["4"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["5"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["6"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
            self.corners[self.pos["7"]].compound.rotate(
                angle=(-math.pi/20), axis=v.vector(0, 1, 0), origin=v.vector(0, 0, 0))
        # update corner position
        c_pos = copy.deepcopy(self.pos)
        self.pos["4"] = c_pos["7"]
        self.pos["7"] = c_pos["6"]
        self.pos["6"] = c_pos["5"]
        self.pos["5"] = c_pos["4"]


if __name__ == "__main__":

    F = np.array(["G"]*4)
    B = np.array(["B"]*4)
    R = np.array(["R"]*4)
    L = np.array(["O"]*4)
    U = np.array(["W"]*4)
    D = np.array(["Y"]*4)

    # cube definition
    cube = Cube(F, B, R, L, U, D)
    cube_render = VisualCube(cube)

    # cleanup console
    os.system("cls")

    # scramble cube
    while(True):
        print("Use the following symbols separated by spaces to scramble the cube:")
        print("F  F' F2  B  B' B2  R  R' R2  L  L' L2  U  U' U2  D  D' D2\n")
        print("Enter sequence:", end=" ")

        # read user move sequence
        seq = str(input()).split(" ")

        # apply sequence
        cube = cube.apply_sequence(seq)

        # animate cube render
        cube_render.animate(seq)
