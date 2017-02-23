import numpy as np
import sys

class Pizza(object):
    def __init__(self, filename):
        f = open(filename)
        metadata = f.readline().split(' ')
        self.rows = int(metadata[0])
        self.columns = int(metadata[1])
        self.minIngredients = metadata[2]
        self.maxCells = metadata[3]
        self.pizza = np.empty([self.rows, self.columns])
        self.pizza.astype(int)
        self.slices = np.empty([self.rows, self.columns], dtype=int)
        self.slices.fill(0)
        self.sliceCounter = 1
        self.readPizza(f)

    def readPizza(self, f):
        y = 0
        for line in f:
            x = 0
            for char in line:
                if (char == 'T' or char == 'M'):
                    self.pizza[y][x] = self.charToEnum(char)
                    x += 1
            y += 1
        self.pizza.astype(int)

    def printPizza(self):
        for row in self.pizza:
            for column in row:
                sys.stdout.write(self.enumToChar(column))
            sys.stdout.write('\n')

    def charToEnum(self, c):
        return {
            'T': 0,
            'M': 1,
        }[c]

    def enumToChar(self, e):
        return {
            0: 'T',
            1: 'M',
        }[e]

    def addSlice(r1, r2, c1, c2):
        error = False
        hasTomato = False
        hasMushroom = False

        #Check input validity
        if (r2 > self.rows || c2 > self.columns):
            return False

        if (r1 > r2 || c1 > c2):
            return False

        #Check that the area is empty and has both stuffings
        for row in range(r1, r2):
            for column in range(c1, c2):
                if (self.slices[row][column] != 0):
                    error = True
                if (self.pizza[row][column] == 0):
                    hasTomato = True
                if (self.pizza[row][column] == 1):
                    hasMushroom = True
        if (error):
            return False
        if (!hasTomato || !hasMushroom):
            return False

        #If everything is ok add the slice
        for row in range(r1, r2):
            for column in range(c1, c2):
                self.slices[row][column] = self.sliceCounter
        self.sliceCounter += 1
        return True

    def result():
        pizzaUsage = 0
        for row in range(r1, r2):
            for column in range(c1, c2):
                if (self.slices[row][column] != 0):
                    pizzaUsage += 1
        return pizzaUsage


pitsu = Pizza('../data/small.in')
print pitsu.printPizza()
