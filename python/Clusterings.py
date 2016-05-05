import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from kmeans import kmeans
from PreprocessData import readBusinessata
from kmeans import Point


finput = open('Business2Index.txt','r')
Business2Index = np.loadtxt(finput,dtype='str')

def buildLabels(est,X):
    cluster_dict = {}
    id = 0
    for cluster in est:
        for point in cluster.points:
            cluster_dict[point] = id
        id += 1

    labels = []
    id2point = []
    for i in xrange(len(X)):
        point = X[i]
        point_id = Business2Index[i]
        labels.append(point_id+' '+str(cluster_dict[point]))
        id2point.append((point_id,point.coords[1],point.coords[0]))


    return (labels,id2point)


def buildLabels2(lables,X):
    result = []
    for i in xrange(len(X)):
        point_id = Business2Index[i]
        result.append(point_id+' '+str(lables[i]))
    return result

def prepareX():
    X = []
    business_dict = readBusinessata('/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json')
    finput.close()
    for id in Business2Index:
        point =  Point(business_dict[id])
        X.append(point)
    return np.array(X)




def main():
    finput = open('BB.txt','r')
    mat = np.loadtxt(finput,delimiter=' ',)
    finput.close()


    X = prepareX()
    k = 10
    min_samples = 4
    opt_cutoff = 0.5



    est = kmeans(X,k,opt_cutoff)

    (cluster_label0,id2point) = buildLabels(est,X)
    cluster_label1 = SpectralClustering(k).fit_predict(mat)
    cluster_label1 = buildLabels2(cluster_label1,X)
    cluster_label2 = DBSCAN(min_samples=min_samples).fit_predict(mat)
    cluster_label2 = buildLabels2(cluster_label2,X)

    np.savetxt('KMeans.txt', cluster_label0, fmt='%s', newline='\n', header='', footer='', comments='# ')
    np.savetxt('SpectralClustering.txt', cluster_label1, fmt='%s', newline='\n', header='', footer='', comments='# ')
    np.savetxt('DBSCAN.txt', cluster_label2, fmt='%s', newline='\n', header='', footer='', comments='# ')

    np.savetxt('ID2Point.txt', id2point, fmt=["%s",]*3, newline='\n')

if __name__ == "__main__":
    main()