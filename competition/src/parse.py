import numpy as np
import sys
import operator


class Cache(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.candidates = []
        self.finalVideos = []
        self.weights = { }
        self.videoSavings = { }
        self.avgVideoSize = 0.0

    #Add a video that might be added on this server
    def addCandidate(self, video):
        self.candidates.append(video)

    def requestAddition(self, video, weight):
        if self.weights.contains(video.id)
            self.weights[video.id].append(weight)
        else:
            self.weights[video.id] = [weight]

    def sortFunction(self, tupl):
        totalWeight = 0
        weights = tupl[1]
        for w in weights:
            totalWeight += w.calculate()
        return totalWeight

    def pickBest(self, videosByIndex, solutions):
        x = self.weights
        sortedValues = sorted(x.items(), key=self.sortFunction)
        space = self.size
        for item in sortedValues:
            video = videosByIndex[item[0]]
            space -= space
            if (space > 0):
                self.finalVideos.append(video)
                weights = item[1]
                for w in weights:
                    for pVal in w:
                        pVals.recalculate(video.id, w.endpointId)
            else:
                break




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
        self.dc_latency = 0

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
