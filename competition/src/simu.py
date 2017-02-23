from math import pow
from parse import *

class HasSpace(object):
    __init__(self, val, videoId, endPointId):
        self.p = val
        self.videoId = videoId
        self.endPointId = endPointId

    def setProbability(self):
        self.p = val

    def recalculate(self, videoId, endpointId):
        if (videoId == self.videoId && endpointId == self.endpointId):
            self.p = 0

class Weight(object):
    __init__(self, probs, latencies, endpointId):
        self.probs = probs
        self.latencies = latencies
        self.endpointId = endpointId

    def calculate():
        weight = 0
        for p in self.probs:
            for l in self.latencies:
                w += p*l
        return weight


def main(endpoints, caches, videos):
    #Add candidates to all caches
    preparse(endpoints)
    # Add weights
    for cache in caches:
        for video in caches.candidates:
            for endpoint in endpoints:
                if (endpoint.vidoes.contains(video)):
                    weight = composeWeight(cache, video, endpoint)
                    cache.requestAddition(video, weight)

    #pick best weights
    for cache in caches:
        cache.pickBest(videos)


def baseline(cache, video, endpoint):
    return (endpoint.delay(cache) - endpoint.delay(datacenter))*endpoint.requests[video.id]

def composeWeight(cache, video, endpoint):
    # Initial savings is the baseline for current
    savings = baseline(cache, video, endpoint)
    # Because we have to chain probabilities always keep tap of previous probabilities
    allP = [HasSpace(probability(cache, video), video.id, endpoint.id)]
    allBaselines = [savings]
    # TODO: Is first probability already with precondition NOT this server ?
    for altCache in endpoint.caches:
        p = HasSpace(probability(altCache, video), video.id, endpoint.id)
        trueP = chainedProbability(allP) * p
        savings -= trueP * baseline(altCache, video)
        allP.append(p)
        allBaselines.append(baseline(altCache, video))
    returnObject = Weight(allP, allBaselines, endpoint.id)

def chainedProbability(ps):
    p = 1
    for val in ps:
        p = p * (1-val.p)

def probability(cache, video):
    totalVideos = 0
    # TODO: Cache total size of candidates
    for video in cache.candidates:
        totalVidoes += video.size
    averageSize = totalVidoes/cache.preparsedVideos.length()
    averageVideosCount = cache.size/averageSize
    nTimesAverage = video.size/averageSize
    probability = pow(1/averageVideosCount, nTimesAverage)

def preparse(endpoints):
    for cache in endpoints.caches:
        for video in endpoints.videos:
            if video.size < cache.size:
                cache.addCandidate(video)
