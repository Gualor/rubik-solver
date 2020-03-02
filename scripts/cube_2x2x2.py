from text_color import text_color as tc
import numpy as np
import copy


# Rubik's cube 2x2x2 class definition
class Cube:
    def __init__(self, f, b, r, l, u, d):
        # defines cube state and stores useful info
        self.faces = {'F': f, 'B': b, 'R': r, 'L': l, 'U': u, 'D': d}
        self.solved = self.check_solved()  # True: solved, False: unsolved
        self.coord = self.get_coordinates()  # get spatial coordinates of the cubies
        self.pos = self.get_positions()  # get color orientation of the cubies

    def check_solved(self):
        # checks if the cube is solved
        for face in self.faces.values():
            if not len(set(face)) == 1:
                return False
        return True

    def get_coordinates(self):
        # links spatial coordinates with corner id number
        coord = {}
        coord["0"] = (0, 0, 0)
        coord["1"] = (0, 0, 1)
        coord["2"] = (1, 0, 1)
        coord["3"] = (1, 0, 0)
        coord["4"] = (0, 1, 0)
        coord["5"] = (0, 1, 1)
        coord["6"] = (1, 1, 1)
        coord["7"] = (1, 1, 0)
        return coord

    def get_positions(self):
        # links color orientations with corner id number
        d = dict()
        d["0"] = (self.faces["F"][0], self.faces["L"][1], self.faces["U"][2])
        d["1"] = (self.faces["B"][1], self.faces["L"][0], self.faces["U"][0])
        d["2"] = (self.faces["B"][0], self.faces["R"][1], self.faces["U"][1])
        d["3"] = (self.faces["F"][1], self.faces["R"][0], self.faces["U"][3])
        d["4"] = (self.faces["F"][2], self.faces["L"][3], self.faces["D"][0])
        d["5"] = (self.faces["B"][3], self.faces["L"][2], self.faces["D"][2])
        d["6"] = (self.faces["B"][2], self.faces["R"][3], self.faces["D"][3])
        d["7"] = (self.faces["F"][3], self.faces["R"][2], self.faces["D"][1])
        return d

    def get_id(self, colors):
        # get corner number id based on faces coloring
        if set([colors[0], colors[1], colors[2]]) == set(["G", "O", "W"]):
            return 0
        elif set([colors[0], colors[1], colors[2]]) == set(["B", "O", "W"]):
            return 1
        elif set([colors[0], colors[1], colors[2]]) == set(["B", "R", "W"]):
            return 2
        elif set([colors[0], colors[1], colors[2]]) == set(["G", "R", "W"]):
            return 3
        elif set([colors[0], colors[1], colors[2]]) == set(["G", "O", "Y"]):
            return 4
        elif set([colors[0], colors[1], colors[2]]) == set(["B", "O", "Y"]):
            return 5
        elif set([colors[0], colors[1], colors[2]]) == set(["B", "R", "Y"]):
            return 6
        elif set([colors[0], colors[1], colors[2]]) == set(["G", "R", "Y"]):
            return 7

    def apply_sequence(self, seq):
        # applies sequence of valid moves and returns resulting cube
        cube = self
        for s in seq:
            if s == "F":
                cube = cube.f_cw()
            elif s == "F'":
                cube = cube.f_ccw()
            elif s == "F2":
                cube = cube.f_2()
            elif s == "B":
                cube = cube.b_cw()
            elif s == "B'":
                cube = cube.b_ccw()
            elif s == "B2":
                cube = cube.b_2()
            elif s == "R":
                cube = cube.r_cw()
            elif s == "R'":
                cube = cube.r_ccw()
            elif s == "R2":
                cube = cube.r_2()
            elif s == "L":
                cube = cube.l_cw()
            elif s == "L'":
                cube = cube.l_ccw()
            elif s == "L2":
                cube = cube.l_2()
            elif s == "U":
                cube = cube.u_cw()
            elif s == "U'":
                cube = cube.u_ccw()
            elif s == "U2":
                cube = cube.u_2()
            elif s == "D":
                cube = cube.d_cw()
            elif s == "D'":
                cube = cube.d_ccw()
            elif s == "D2":
                cube = cube.d_2()
            else:
                print("Invalid sequence\n")
        return cube

    def apply_all_moves(self):
        # returns dict of cubes obtained applying all moves to current cube
        moves = {}
        moves["F"] = self.f_cw()
        moves["F'"] = self.f_ccw()
        moves["F2"] = self.f_2()
        moves["B"] = self.b_cw()
        moves["B'"] = self.b_ccw()
        moves["B2"] = self.b_2()
        moves["R"] = self.r_cw()
        moves["R'"] = self.r_ccw()
        moves["R2"] = self.r_2()
        moves["L"] = self.l_cw()
        moves["L'"] = self.l_ccw()
        moves["L2"] = self.l_2()
        moves["U"] = self.u_cw()
        moves["U'"] = self.u_ccw()
        moves["U2"] = self.u_2()
        moves["D"] = self.d_cw()
        moves["D'"] = self.d_ccw()
        moves["D2"] = self.d_2()
        return moves

    def f_cw(self):
        # applies F move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['F'] = tempf['F'].reshape(2, 2)
        tempf['F'] = np.rot90(tempf['F'], 3)
        tempf['F'] = tempf['F'].flatten()
        # reassign values
        for i in range(2):
            tempf['R'][0+i*2] = self.faces['U'][2+i]
            tempf['D'][1-i] = self.faces['R'][0+i*2]
            tempf['L'][3-i*2] = self.faces['D'][1-i]
            tempf['U'][2+i] = self.faces['L'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def f_ccw(self):
        # applies F' move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['F'] = tempf['F'].reshape(2, 2)
        tempf['F'] = np.rot90(tempf['F'], 1)
        tempf['F'] = tempf['F'].flatten()
        # reassign values
        for i in range(2):
            tempf['U'][2+i] = self.faces['R'][0+i*2]
            tempf['R'][0+i*2] = self.faces['D'][1-i]
            tempf['D'][1-i] = self.faces['L'][3-i*2]
            tempf['L'][3-i*2] = self.faces['U'][2+i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def f_2(self):
        # applies F2 move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['F'] = tempf['F'].reshape(2, 2)
        tempf['F'] = np.rot90(tempf['F'], 2)
        tempf['F'] = tempf['F'].flatten()
        # reassign values
        for i in range(2):
            tempf['D'][1-i] = self.faces['U'][2+i]
            tempf['L'][3-i*2] = self.faces['R'][0+i*2]
            tempf['U'][2+i] = self.faces['D'][1-i]
            tempf['R'][0+i*2] = self.faces['L'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def b_cw(self):
        # applies B move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['B'] = tempf['B'].reshape(2, 2)
        tempf['B'] = np.rot90(tempf['B'], 3)
        tempf['B'] = tempf['B'].flatten()
        # reassign values
        for i in range(2):
            tempf['L'][0+i*2] = self.faces['U'][1-i]
            tempf['D'][2+i] = self.faces['L'][0+i*2]
            tempf['R'][3-i*2] = self.faces['D'][2+i]
            tempf['U'][1-i] = self.faces['R'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def b_ccw(self):
        # applies B' move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['B'] = tempf['B'].reshape(2, 2)
        tempf['B'] = np.rot90(tempf['B'], 1)
        tempf['B'] = tempf['B'].flatten()
        # reassign values
        for i in range(2):
            tempf['U'][1-i] = self.faces['L'][0+i*2]
            tempf['L'][0+i*2] = self.faces['D'][2+i]
            tempf['D'][2+i] = self.faces['R'][3-i*2]
            tempf['R'][3-i*2] = self.faces['U'][1-i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def b_2(self):
        # applies B2 move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['B'] = tempf['B'].reshape(2, 2)
        tempf['B'] = np.rot90(tempf['B'], 2)
        tempf['B'] = tempf['B'].flatten()
        # reassign values
        for i in range(2):
            tempf['D'][2+i] = self.faces['U'][1-i]
            tempf['R'][3-i*2] = self.faces['L'][0+i*2]
            tempf['U'][1-i] = self.faces['D'][2+i]
            tempf['L'][0+i*2] = self.faces['R'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def r_cw(self):
        # applies R move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['R'] = tempf['R'].reshape(2, 2)
        tempf['R'] = np.rot90(tempf['R'], 3)
        tempf['R'] = tempf['R'].flatten()
        # reassign values
        for i in range(2):
            tempf['B'][0+i*2] = self.faces['U'][3-i*2]
            tempf['D'][3-i*2] = self.faces['B'][0+i*2]
            tempf['F'][3-i*2] = self.faces['D'][3-i*2]
            tempf['U'][3-i*2] = self.faces['F'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def r_ccw(self):
        # applies R' move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['R'] = tempf['R'].reshape(2, 2)
        tempf['R'] = np.rot90(tempf['R'], 1)
        tempf['R'] = tempf['R'].flatten()
        # reassign values
        for i in range(2):
            tempf['U'][3-i*2] = self.faces['B'][0+i*2]
            tempf['B'][0+i*2] = self.faces['D'][3-i*2]
            tempf['D'][3-i*2] = self.faces['F'][3-i*2]
            tempf['F'][3-i*2] = self.faces['U'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def r_2(self):
        # applies R2 move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['R'] = tempf['R'].reshape(2, 2)
        tempf['R'] = np.rot90(tempf['R'], 2)
        tempf['R'] = tempf['R'].flatten()
        # reassign values
        for i in range(2):
            tempf['D'][3-i*2] = self.faces['U'][3-i*2]
            tempf['F'][3-i*2] = self.faces['B'][0+i*2]
            tempf['U'][3-i*2] = self.faces['D'][3-i*2]
            tempf['B'][0+i*2] = self.faces['F'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def l_cw(self):
        # applies L move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['L'] = tempf['L'].reshape(2, 2)
        tempf['L'] = np.rot90(tempf['L'], 3)
        tempf['L'] = tempf['L'].flatten()
        # reassign values
        for i in range(2):
            tempf['F'][0+i*2] = self.faces['U'][0+i*2]
            tempf['D'][0+i*2] = self.faces['F'][0+i*2]
            tempf['B'][3-i*2] = self.faces['D'][0+i*2]
            tempf['U'][0+i*2] = self.faces['B'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def l_ccw(self):
        # applies L' move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['L'] = tempf['L'].reshape(2, 2)
        tempf['L'] = np.rot90(tempf['L'], 1)
        tempf['L'] = tempf['L'].flatten()
        # reassign values
        for i in range(2):
            tempf['U'][0+i*2] = self.faces['F'][0+i*2]
            tempf['F'][0+i*2] = self.faces['D'][0+i*2]
            tempf['D'][0+i*2] = self.faces['B'][3-i*2]
            tempf['B'][3-i*2] = self.faces['U'][0+i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def l_2(self):
        # applies L2 move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['L'] = tempf['L'].reshape(2, 2)
        tempf['L'] = np.rot90(tempf['L'], 2)
        tempf['L'] = tempf['L'].flatten()
        # reassign values
        for i in range(2):
            tempf['D'][0+i*2] = self.faces['U'][0+i*2]
            tempf['B'][3-i*2] = self.faces['F'][0+i*2]
            tempf['U'][0+i*2] = self.faces['D'][0+i*2]
            tempf['F'][0+i*2] = self.faces['B'][3-i*2]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def u_cw(self):
        # applies U move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['U'] = tempf['U'].reshape(2, 2)
        tempf['U'] = np.rot90(tempf['U'], 3)
        tempf['U'] = tempf['U'].flatten()
        # reassign values
        for i in range(2):
            tempf['R'][1-i] = self.faces['B'][1-i]
            tempf['F'][1-i] = self.faces['R'][1-i]
            tempf['L'][1-i] = self.faces['F'][1-i]
            tempf['B'][1-i] = self.faces['L'][1-i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def u_ccw(self):
        # applies U' move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['U'] = tempf['U'].reshape(2, 2)
        tempf['U'] = np.rot90(tempf['U'], 1)
        tempf['U'] = tempf['U'].flatten()
        # reassign values
        for i in range(2):
            tempf['B'][1-i] = self.faces['R'][1-i]
            tempf['R'][1-i] = self.faces['F'][1-i]
            tempf['F'][1-i] = self.faces['L'][1-i]
            tempf['L'][1-i] = self.faces['B'][1-i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def u_2(self):
        # applies U2 move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['U'] = tempf['U'].reshape(2, 2)
        tempf['U'] = np.rot90(tempf['U'], 2)
        tempf['U'] = tempf['U'].flatten()
        # reassign values
        for i in range(2):
            tempf['F'][1-i] = self.faces['B'][1-i]
            tempf['L'][1-i] = self.faces['R'][1-i]
            tempf['B'][1-i] = self.faces['F'][1-i]
            tempf['R'][1-i] = self.faces['L'][1-i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def d_cw(self):
        # applies D move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['D'] = tempf['D'].reshape(2, 2)
        tempf['D'] = np.rot90(tempf['D'], 3)
        tempf['D'] = tempf['D'].flatten()
        # reassign values
        for i in range(2):
            tempf['R'][2+i] = self.faces['F'][2+i]
            tempf['B'][2+i] = self.faces['R'][2+i]
            tempf['L'][2+i] = self.faces['B'][2+i]
            tempf['F'][2+i] = self.faces['L'][2+i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def d_ccw(self):
        # applies D' move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['D'] = tempf['D'].reshape(2, 2)
        tempf['D'] = np.rot90(tempf['D'], 1)
        tempf['D'] = tempf['D'].flatten()
        # reassign values
        for i in range(2):
            tempf['F'][2+i] = self.faces['R'][2+i]
            tempf['R'][2+i] = self.faces['B'][2+i]
            tempf['B'][2+i] = self.faces['L'][2+i]
            tempf['L'][2+i] = self.faces['F'][2+i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def d_2(self):
        # applies D2 move and returns corresponding cube
        tempf = copy.deepcopy(self.faces)
        # rotate front face
        tempf['D'] = tempf['D'].reshape(2, 2)
        tempf['D'] = np.rot90(tempf['D'], 2)
        tempf['D'] = tempf['D'].flatten()
        # reassign values
        for i in range(2):
            tempf['B'][2+i] = self.faces['F'][2+i]
            tempf['L'][2+i] = self.faces['R'][2+i]
            tempf['F'][2+i] = self.faces['B'][2+i]
            tempf['R'][2+i] = self.faces['L'][2+i]
        # return new Cube
        return Cube(tempf['F'], tempf['B'], tempf['R'], tempf['L'], tempf['U'], tempf['D'])

    def print_cube(self):
        # prints out cube state with ascii characters in console
        term = {"W": tc.w, "R": tc.r, "O": tc.o, "B": tc.b, "G": tc.g, "Y": tc.y}
        print(tc.d + "\n      +-----+")
        for row in self.faces["U"].reshape(2, 2):
            print("      |", end=" ")
            for col in row:
                print(term[col] + col + tc.d, end=" ")
            print("|")
        print("+-----+-----+-----+-----+")
        mat = []
        for row in range(2):
            for id in ["L", "F", "R", "B"]:
                mat.append(self.faces[id].reshape(2, 2)[row])
        mat = np.array(mat).reshape(2, 8)
        for row in mat:
            for i in range(len(row)):
                if i % 2 == 0:
                    print("|", end=" ")
                print(term[row[i]] + row[i] + tc.d, end=" ")
            print("|")
        print("+-----+-----+-----+-----+")
        for row in self.faces["D"].reshape(2, 2):
            print("      |", end=" ")
            for col in row:
                print(term[col] + col + tc.d, end=" ")
            print("|")
        print("      +-----+" + tc.w, end="\n\n")


if __name__ == "__main__":

    F = np.array(["G"]*4)
    B = np.array(["B"]*4)
    R = np.array(["R"]*4)
    L = np.array(["O"]*4)
    U = np.array(["W"]*4)
    D = np.array(["Y"]*4)

    # cube definition
    cube = Cube(F, B, R, L, U, D)
    cube.print_cube()

    # scramble cube
    while(True):
        print("Use the following symbols separated by spaces to scramble the cube:")
        print("F  F' F2  B  B' B2  R  R' R2  L  L' L2  U  U' U2  D  D' D2\n")
        print("Enter sequence:", end=" ")

        # read user move sequence
        seq = str(input()).split(" ")

        # apply sequence
        cube = cube.apply_sequence(seq)
        cube.print_cube()
