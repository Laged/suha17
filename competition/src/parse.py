import numpy as np
import sys
import operator


class Cache(object):
    def __init__(self, id, size):
        print 'Cache ' + str(id) + ' ' + str(size)
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
        if self.weights.contains(video.id):
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



#List of Cache objects
cacheList = []

class Video(object):
    def __init__(self, id, size):
        print 'Video ' + str(id) + ' ' + str(size)
        self.id = id
        self.size = size

#class VideoList(object):
#    def __init__(self, videoSizes):
#        self.list = [] # TODO List of the Video objects

#List of Video objects
videoList = []

class Endpoint(object):
    def __init__(self, id, dcLatency):
        print 'Endpoint ' + str(id) + ' ' + str(dcLatency)
        self.latencies = {}
        self.id = id
        self.requests = {} # {Video.id, requestCount}
        self.caches = self.latencies.keys()
        self.dc_latency = dcLatency
    def setLatencyToCache(self, cacheId, latency):
        self.latencies[cacheId] = latency

#List of Endpoint objects
endpointList = []

def loadData(path):
    # Parse and print metadata
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

    # Initialize actual classes
    # Initalize caches 
    for cacheId in range(cacheCount):
        cacheList.append(Cache(len(cacheList), cacheSize))

    # Initialize VideoList
    videoSizes = map(int, file.readline().split(' '))
    # TODO INITIALIZE VIDEOS
    for videoId in range(len(videoSizes)):
        videoList.append(Video(videoId, videoSizes[videoId]))
    print 'len videoList ' + str(len(videoList))
    # Initialize endpoints
    states = ["cacheDescription", "cacheData", "request"]
    state = "cacheDescription"
    dataLeft = 0
    for line in file:
        lineData = line.split(' ')
        if len(lineData) == 3:
            state = "request"
        if state == "cacheDescription":
            dcDelay = int(lineData[0])
            endpointList.append(Endpoint(len(endpointList), dcDelay))
            dataLeft = int(lineData[1])
            state = "cacheData"
        elif state == "cacheData":
            #TODO
            cacheId = int(lineData[0])
            latency = int(lineData[1])
            endpointList[len(endpointList) - 1].setLatencyToCache(cacheId, latency)
            dataLeft -= 1
            if dataLeft == 0:
                state = "cacheDescription"
        elif state == "request":
            #TODO
            print "requestData"
            print lineData

if __name__ == "__main__":
    dataPath = '../data/' + sys.argv[1] + '.in'
    print 'dataPath ' + dataPath
    loadData(dataPath)
    print cacheList
    print endpointList
    print videoList
