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
        if (video.id in self.weights):
            self.weights[video.id].append(weight)
        else:
            self.weights[video.id] = [weight]

    def sortFunction(self, tupl):
        totalWeight = 0
        weights = tupl[1]
        for w in weights:
            totalWeight += w.calculate()
        return totalWeight

    def pickBest(self, videosByIndex):
        x = self.weights
        sortedValues = sorted(x.items(), key=self.sortFunction)
        space = self.size
        for item in sortedValues:
            video = videosByIndex[item[0]]
            space -= video.size
            if (space > 0):
                self.finalVideos.append(video)
                weights = item[1]
                for w in weights:
                    for pVal in w.probs:
                        pVal.recalculate(video.id, w.endpointId)
            else:
                break



#List of Cache objects
cacheList = []

class Video(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size

#class VideoList(object):
#    def __init__(self, videoSizes):
#        self.list = [] # TODO List of the Video objects

#List of Video objects
videoList = []

class Endpoint(object):
    def __init__(self, id, dcLatency):
        self.latencies = {}
        self.id = id
        self.requests = {} # {Video.id, requestCount}
        self.dc_latency = dcLatency
        self.caches = []
        self.videos = []

    def setLatencyToCache(self, cacheId, latency):
        self.latencies[cacheId] = latency
        self.caches.append(cacheList[cacheId])

    def setRequestCount(self, videoId, count):
        self.requests[videoId] = count
        self.videos.append(videoList[videoId])

#List of Endpoint objects
endpointList = []

def score(caches, endpoints):
    n_requests = 0
    score = 0

    kissa = [[] for i in range(len(videoList))]
    for c_id in len(caches):
        for v_id in caches[c_id].finalVideos:
            kissa[v_id].append(c_id)

    for ep in endpoints:
        for v_id, v_n in ep.requests:
            L_D = v_n * ep.d_latency
            saved = 0

            for c_id in kissa[v_id]:
                if c_id in ep.caches:
                    saved_ = L_D - ep.latencies[c_id] * v_n
                    if saved_ > saved:
                        saved = saved_
            
            score += saved           
            n_requests += v_n
    
    return float(score) / n_requests

def loadData(path):
    # Parse and print metadata
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
            videoId = int(lineData[0])
            endpointId = int(lineData[1])
            requestCount = int(lineData[2])
            endpointList[endpointId].setRequestCount(videoId, requestCount)

if __name__ == "__main__":
    dataPath = '../data/' + sys.argv[1] + '.in'
    loadData(dataPath)
