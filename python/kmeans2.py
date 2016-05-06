
import random
# Download from https://gist.github.com/iandanforth/5862470
# Copyright @iandanforth

import sys
import math

import subprocess

"""
This is a pure Python implementation of the K-Means Clustering algorithmn. The
original can be found here:
http://pandoricweb.tumblr.com/post/8646701677/python-implementation-of-the-k-means-clustering
I have refactored the code and added comments to aid in readability.
After reading through this code you should understand clearly how K-means works.
If not, feel free to email me with questions and suggestions. (iandanforth at
gmail)
This script specifically avoids using numpy or other more obscure libraries. It
is meant to be *clear* not fast.
I have also added integration with the plot.ly plotting service. If you put in
your (free) plot.ly credentials below, it will automatically plot the discovered
clusters and their centroids.
To use plotly integration you will need to:
1. Get a username/key from www.plot.ly/api and enter them below
2. Install the plotly module: pip install plotly
"""




class Point:
    '''
    An point in n dimensional space
    '''
    def __init__(self, coords):
        '''
        coords - A list of values, one per dimension
        '''

        self.coords = coords
        self.n = len(coords)

    def __repr__(self):
        return str(self.coords)


class KMeans:
    '''
    A set of points and their centroid
    '''

    def __init__(self, points):
        '''
        points - A list of point objects
        '''

        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        # The points that belong to this cluster
        self.points = points

        # The dimensionality of the points in this cluster
        self.n = points[0].n

        # Assert that all points are of the same dimensionality
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: wrong dimensions")

        # Set up the initial centroid (this is usually based off one point)
        self.centroid = self.calculateCentroid()

    def __repr__(self):
        '''
        String representation of this object
        '''
        return str(self.points)

    def update(self, points):
        '''
        Returns the distance between the previous centroid and the new after
        recalculating and storing the new centroid.
        '''
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid)
        return shift

    def calculateCentroid(self):
        '''
        Finds a virtual center point for a group of n-dimensional points
        '''
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]

        return Point(centroid_coords)


def reduce(clusters,threshold_strict,iterations):
    converage_flag1 = False
    loop_iteration = 0
    clusters_new = []
    while (loop_iteration <= iterations) and (not converage_flag1):
        converage_flag2 = False
        for cluster in clusters:
            for another in clusters:
                dist = getDistance(cluster.centroid, another.centroid)
                if cluster != another and  dist < threshold_strict:
                    pts = cluster.points + another.points
                    cluster_new = KMeans(pts)
                    clusters.remove(cluster)
                    clusters.remove(another)
                    clusters.append(cluster_new)
                    converage_flag2 = True
                    break


        if not converage_flag2:
            converage_flag1 = True
        loop_iteration += 1


def kmeans2(points, cutoff,threshold,reduce_threshold):

    k = 1

    # Pick out k random points to use as our initial centroids
    initial = random.sample(points, k)

    # Create k clusters using those centroids
    clusters = [KMeans([p]) for p in initial]

    # Loop through the dataset until the clusters stabilize
    loopCounter = 0
    while True:
        # Create a list of lists to hold the points in each cluster
        lists = [ [] for c in clusters]
        clusterCount = len(clusters)

        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
            # Get the distance between that point and the centroid of the first
            # cluster.
            smallest_distance = getDistance(p, clusters[0].centroid)

            # Set the cluster this point belongs to
            clusterIndex = 0

            # For the remainder of the clusters ...
            for i in range(clusterCount - 1):
                # calculate the distance of that point to each other cluster's
                # centroid.
                distance = getDistance(p, clusters[i+1].centroid)
                # If it's closer to that cluster's centroid update what we
                # think the smallest distance is, and set the point to belong
                # to that cluster
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1

            if smallest_distance > threshold:
                lists.append([p])
                clusters.append(KMeans([p]))
                clusterCount += 1
            else:
                lists[clusterIndex].append(p)

        # Set our biggest_shift to zero for this iteration
        biggest_shift = 0.0

        # As many times as there are clusters ...
        for i in range(clusterCount):
            # Calculate how far the centroid moved in this iteration
            shift = clusters[i].update(lists[i])
            # Keep track of the largest move from all cluster centroid updates
            biggest_shift = max(biggest_shift, shift)

        # If the centroids have stopped moving much, say we're done!
        if biggest_shift < cutoff:
            print "Converged after %s iterations" % loopCounter
            break



    reduce(clusters,reduce_threshold,10)
    print(len(clusters))
    return clusters

def getDistance(a, b):

    lat1 = a.coords[0]
    lon1 = a.coords[1]

    lat2 = b.coords[0]
    lon2 = b.coords[1]

    if lat1 == lat2 and lon1 == lon2:
        return 0

    fa1 = math.radians(lat1)
    fa2 = math.radians(lat2)
    dela = math.radians(lon2-lon1)
    R = 6371000.0
    dist = math.acos(math.sin(fa1)*math.sin(fa2) + math.cos(fa1)*math.cos(fa2) * math.cos(dela) ) * R

    return dist

