from math import pow
from parse import *

class HasSpace(object):
    def __init__(self, val, videoId, endpointId):
        self.p = val
        self.videoId = videoId
        self.endpointId = endpointId

    def setProbability(self):
        self.p = val

    def recalculate(self, videoId, endpointId):
        if (videoId == self.videoId and endpointId == self.endpointId):
            self.p = 0

class Weight(object):
    def __init__(self, probs, latencies, endpointId):
        self.probs = probs
        self.latencies = latencies
        self.endpointId = endpointId

    def calculate(self):
        weight = 0
        for p in self.probs:
            for l in self.latencies:
                weight += p.p*l
        return weight


def main(endpoints, caches, videos):
    # Add candidates to all caches
    print "Start main"
    preparse(endpoints)
    # Add weights
    length = len(caches)
    i=0
    j=0
    videoL = len(videos)
    for cache in caches:
        for video in cache.candidates:
            for endpoint in endpoints:
                if (video in endpoint.videos and cache in endpoint.caches):
                    weight = composeWeight(cache, video, endpoint)
                    cache.requestAddition(video, weight)
            j+=1
            print "video ready", j, "of", videoL
        i += 1
        print i, "out of", length

    #pick best weights
    for cache in caches:
        cache.pickBest(videos)
    return caches


def baseline(cache, video, endpoint):
    l = endpoint.latencies[cache.id]
    return ( l - endpoint.dc_latency)*endpoint.requests[video.id]

def composeWeight(cache, video, endpoint):
    # Initial savings is the baseline for current
    savings = baseline(cache, video, endpoint)
    # Because we have to chain probabilities always keep tap of previous probabilities
    allP = [HasSpace(probability(cache, video), video.id, endpoint.id)]
    allBaselines = [savings]
    # TODO: Is first probability already with precondition NOT this server ?
    iterVals = endpoint.caches[0]
    for altCache in iterVals:
        p = HasSpace(probability(altCache, video), video.id, endpoint.id)
        trueP = chainedProbability(allP) * p.p
        savings -= trueP * baseline(altCache, video, endpoint)
        allP.append(p)
        allBaselines.append(baseline(altCache, video, endpoint))
    returnObject = Weight(allP, allBaselines, endpoint.id)
    return returnObject

def chainedProbability(ps):
    p = 1
    for val in ps:
        p = p * (1-val.p)
    return p

def probability(cache, video):
    totalVideos = 0
    # TODO: Cache total size of candidates
    for video in cache.candidates:
        totalVideos += video.size
    averageSize = totalVideos/len(cache.candidates)
    averageVideosCount = cache.size/averageSize
    nTimesAverage = video.size/averageSize
    probability = pow(1/averageVideosCount, nTimesAverage)
    return probability

def preparse(endpoints):
    for endpoint in endpoints:
        for cache in endpoint.caches:
            #print "Here are", len(endpoint.videos), "videos"
            for video in endpoint.videos:
                if video.size < cache.size:
                    cache.addCandidate(video)

loadData('../data/3.in')

results = main(endpointList, cacheList, videoList)
for cache in results:
    print cache.finalVideos
