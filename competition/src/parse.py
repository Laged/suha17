import numpy as np
import sys


class Cache(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.candidates = []
        self.videoSavings = { }
        self.avgVideoSize = 0.0

    #Add a video that might be added on this server
    def addCandidate(self, video):
        self.candidates.append(video)

    def requestAddition(self, video, weight):
        if self.videoSavings.contains(video.index)
            self.videoSavings[video.id] += weight
        else:
            self.videoSavings[video.id] = weight


class CacheList(object):
    def __init__(self, cacheCount, cacheSize):
        self.list = [] # TODO initialize this with Cache objects with real ids

class Video(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size

class VideoList(object):
    def __init__(self, videoSizes):
        self.list = [] # TODO List of the Video objects

class Endpoint(object):
    def __init__(self, latencyList, requestList):
        self.latencies = {}
        self.requests = {} # {Video.id, requestCount}
        self.caches = self.latencies.keys()

class EndpointList(object):
    def __init__(self, latencyList):
        self.list = [] # TODO List of Endpoint objects

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
