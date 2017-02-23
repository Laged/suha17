import numpy as np
import sys
from datetime import datetime
from random import randint, seed

seed(1203)


class Pizza(object):
    def __init__(self, filename):
        f = open(filename)
        metadata = f.readline().split(' ')
        self.rows = int(metadata[0])
        self.columns = int(metadata[1])
        self.minIngredients = int(metadata[2])
        self.maxCells = int(metadata[3])
        self.pizza = np.empty([self.rows, self.columns], dtype=int)
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

    def printSlices(self):
        for row in self.slices:
            for column in row:
                sys.stdout.write("%02x|" % column)
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

    def addSlice(self, r1, r2, c1, c2):
        #Index 0 is for tomatos, index 1 for mushroom
        counts = [0, 0]

        #Check input validity
        if (r2 >= self.rows or c2 >= self.columns or r1 < 0 or c1 < 0):
            return False

        if (r1 > r2 or c1 > c2):
            return False

        #Check size validity
        size = (r2-r1+1)*(c2-c1+1)
        if (size > self.maxCells):
            return False

        #Check that the area is empty and has both stuffings
        for row in xrange(r1, r2 + 1):
            for column in xrange(c1, c2 + 1):
                if (self.slices[row][column] != 0):
                    return True #Slice conflict
                counts[self.pizza[row][column]] += 1
        tomatoCount = counts[0]
        mushroomCount = counts[1]
        if (tomatoCount < self.minIngredients or mushroomCount < self.minIngredients):
            return False

        #If everything is ok add the slice
        for row in xrange(r1, r2 + 1):
            for column in xrange(c1, c2 + 1):
                self.slices[row][column] = self.sliceCounter
        self.sliceCounter += 1
        return True

    def result(self):
        pizzaUsage = 0
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                if (self.slices[row][column] != 0):
                    pizzaUsage += 1
        return pizzaUsage

    def sliceCount(self):
        return self.sliceCounter

def perfTest():
    pitsu = Pizza('../data/big.in')
    start=datetime.now()
    for i in range(10000):
        xStart = randint(100, 900)
        yStart = randint(100, 900)
        pitsu.addSlice(randint(0, 2) + xStart, randint(2,6) + xStart, randint(0, 2) + yStart, randint(2, 6) + yStart)
    print "Addslice runtime", datetime.now()-start
    print pitsu.result()

if __name__ == "__main__":
    perfTest()
"""=======
    dataset = sys.argv[1]
    pitsu = Pizza('../data/' + dataset + '.in')
    print pitsu.printPizza()
    pitsu.addSlice(0, 1, 0, 1)
    print pitsu.printSlices()
>>>>>>> 3df6a5604da35e8fef6f5798ff3ad806633caa91"""
