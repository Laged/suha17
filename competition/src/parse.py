import numpy as np
import sys

class Cache(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size

class CacheList(object):
    def __init__(self, cacheCount, cacheSize):
        self.list = [] # TODO initialize this with Cache objects with real ids

class Videos(object):
    def __init__(self, videoSizes):
        self.list = videoSizes # List of the video sizes [100, 100, 100]

def loadData(path):
    print 'Parsing: ' + path
    file = open(path)
    metadata = file.readline().split(' ')
    videoCount = int(metadata[0])
    endpointCount = int(metadata[1])
    requestCount = int(metadata[2])
    cacheCount = int(metadata[3])
    cacheSize = int(metadata[4])
    print 'videoCount ' + str(videoCount)
    print 'endpointCount ' + str(endpointCount)
    print 'requestCount ' + str(requestCount)
    print 'cacheCount ' + str(cacheCount)
    print 'cacheSize ' + str(cacheSize)

if __name__ == "__main__":
    dataPath = '../data/' + sys.argv[1] + '.in'
    print 'dataPath ' + dataPath
    loadData(dataPath)