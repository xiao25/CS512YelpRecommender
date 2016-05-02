import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from kmeans import kmeans
from PreprocessData import readBusinessata
from kmeans import Point

def buildLabels(est,X):
    cluster_dict = {}
    id = 0
    for cluster in est:
        for point in cluster.points:
            cluster_dict[point] = id
        id += 1

    labels = []
    for point in X:
        labels.append(cluster_dict[point])
    return np.array(labels)




def prepareX():
    X = []
    business_dict = readBusinessata('/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json')
    finput = open('Business2Index.txt','r')
    Business2Index = np.loadtxt(finput,dtype='str')
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

    cluster_label0 = buildLabels(est,X)
    cluster_label1 = SpectralClustering(k).fit_predict(mat)
    cluster_label2 = DBSCAN(min_samples=min_samples).fit_predict(mat)


    np.savetxt('Keans.txt', cluster_label0, fmt='%d', newline='\n', header='', footer='', comments='# ')
    np.savetxt('SpectralClustering.txt', cluster_label1, fmt='%d', newline='\n', header='', footer='', comments='# ')
    np.savetxt('DBSCAN.txt', cluster_label2, fmt='%d', newline='\n', header='', footer='', comments='# ')

if __name__ == "__main__":
    main()