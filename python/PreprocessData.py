# Build 2 matrices UB and BB within Urbana-Champaign area
import json
import numpy as np
import math

def readBusinessata(filename):
    finput = open(filename,'r')
    obj_dict = {}
    for line in finput:
        object = json.loads(line)
        city = object['city']
        id = object['business_id']
        if city == 'Urbana' or city == 'Champaign' :
            obj_dict[id] = (object['latitude'],object['longitude'])
    return obj_dict


def writeMatrix2File(matrix,fname,fmt):
    np.savetxt(fname, matrix, fmt=fmt, newline='\n', header='', footer='', comments='# ')


def buildUBMatrix(filename,business_dict):
    finput = open(filename,'r')
    UB_dict = {}
    for line in finput:
        review = json.loads(line)
        user_id = review['user_id']
        business_id = review['business_id']
        if business_id in business_dict:
            if user_id in UB_dict:
                if business_id in UB_dict[user_id]:
                    UB_dict[user_id][business_id] +=1
                else:
                    UB_dict[user_id][business_id] = 1
            else:
                UB_dict[user_id] = {}
                UB_dict[user_id][business_id] = 1


    user_lst = UB_dict.keys()
    business_lst = business_dict.keys()
    M = len(user_lst)
    N = len(business_lst)

    UB_Matrix = np.zeros((M,N),dtype='int32')
    for row in xrange(M):
        for col in xrange(N):
            userid = user_lst[row]
            businessid = business_lst[col]
            if userid in UB_dict and businessid in UB_dict[userid]:
                UB_Matrix[row][col] = UB_dict[userid][businessid]

    return (user_lst,business_lst,UB_Matrix)


def buildBBMatrix(business_dict,business_lst):
    '''
    To compute the geo-distance between two gps coordinates, there are many options according to http://www.movable-type.co.uk/scripts/latlong.html
    Consider performance, I choose Equirectangular approximation formula here; Unit is km
    '''

    N = len(business_lst)
    BB_Matrix = np.zeros((N,N),dtype='float16')

    for row in xrange(N):
        for col in xrange(N):
            if row != col:
                business1 = business_dict[business_lst[row]]
                business2 = business_dict[business_lst[col]]
                lat1 = float(business1[0])
                lon1 = float(business1[1])
                lat2 = float(business2[0])
                lon2 = float(business2[1])
                fa1 = math.radians(lat1)
                fa2 = math.radians(lat2)
                dela = math.radians(lon2-lon1)
                R = 6371000.0
                dist = math.acos( math.sin(fa1)*math.sin(fa2) + math.cos(fa1)*math.cos(fa2) * math.cos(dela) ) * R
                BB_Matrix[row][col] = dist

    return BB_Matrix


def main():
    # my code here
    business_dict = readBusinessata('/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json')
    (user_lst,business_lst,UB) = buildUBMatrix('/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json',business_dict)
    BB = buildBBMatrix(business_dict,business_lst)
    writeMatrix2File(UB,'UB.txt','%d')
    writeMatrix2File(BB,'BB.txt','%.4f')
    writeMatrix2File(user_lst,'User2Index.txt','%s')
    writeMatrix2File(business_lst,'Business2Index.txt','%s')




if __name__ == "__main__":
    main()