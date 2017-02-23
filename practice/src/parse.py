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
        self.sliceCoordinates = []

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
        self.sliceCoordinates.append('%d %d %d %d' % (r1, r2, c1, c2))
        return True

    def result(self):
        pizzaUsage = 0
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                if (self.slices[row][column] != 0):
                    pizzaUsage += 1
        return pizzaUsage

    def printResult(self):
        sys.stdout.write(str(self.sliceCounter))
        sys.stdout.write('\n')
        for coords in self.sliceCoordinates:
            sys.stdout.write(coords)
            sys.stdout.write('\n')

    def sliceCount(self):
        return self.sliceCounter

def perfTest(file = '../data/big.in'):
    pitsu = Pizza(file)
    start=datetime.now()
    xMax = pitsu.rows-1
    yMax = pitsu.columns-1
    for i in range(100000000):
        xStart = randint(0, pitsu.rows-1)
        yStart = randint(0, pitsu.columns-1)
        pitsu.addSlice(xStart, min(xMax, xStart + randint(0,7)), yStart, min(yStart + randint(0,7), yMax))
    #print "Addslice runtime", datetime.now()-start
    print "Estimated result", pitsu.result()
    pitsu.printResult()
    #print "Estimated score", pitsu.result()

def shotgun(logfile):
    pitsu = Pizza(logfile)
    maxResult = pitsu.result()
    if (pitsu.rows > 300 or pitsu.columns > 300):
        perfTest(logfile)
    attempts = 100
    for a in range(attempts):
        pitsu = Pizza(logfile)
        xMax = pitsu.rows-1
        yMax = pitsu.columns-1
        for i in range(10000):
            xStart = randint(0, xMax)
            yStart = randint(0, yMax)
            pitsu.addSlice(xStart, min(xMax, xStart + randint(0,7)), yStart, min(yStart + randint(0,7), yMax))

        if (pitsu.result() > maxResult):
            maxResult = pitsu.result()
            bestResult = pitsu
    print "Estimated result", pitsu.result()
    bestResult.printResult()

if __name__ == "__main__":
    dataset = sys.argv[1]
    shotgun('../data/' + dataset + '.in')
