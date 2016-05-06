import numpy as np
import json
from datetime import datetime
from operator import itemgetter


def updateDate(filename,business_dict):
    with open(filename,'r') as finput:
        for line in finput:
            object = json.loads(line)
            dates = object['date'].split('-')
            date = datetime(int(dates[0]),int(dates[1]),int(dates[2]))
            id = object['business_id']
            if id in business_dict:
                old_date = business_dict[id]
                if old_date > date:
                    business_dict[id] = date
            else:
                business_dict[id] = date



def findNewestBusiness(finput1,finput2,Business2Index):
    # {business_id : oldest date}
    business_dict = {}
    updateDate(finput1,business_dict)
    updateDate(finput2,business_dict)

    # sorted by date
    business_lst = []
    for (id,date) in business_dict.items():
        if (id in Business2Index):
            business_lst.append((id,date))



    business_lst = sorted(business_lst, key = itemgetter(1),reverse=True)

    return business_lst[:20]



def main():
    # my code here

    finput1 = '/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_tip.json'
    finput2 = '/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'


    with open('../resources/Business2Index.txt','r') as finput:
        Business2Index = np.loadtxt(finput,dtype='str')



    test_data = findNewestBusiness(finput1,finput2,Business2Index)
    np.savetxt('../resources/TestBusiness.txt', test_data, fmt='%s', newline='\n')


if __name__ == "__main__":
    main()