import numpy as np
import json
from datetime import datetime


def encodeDate(month):
    return '0' if month >= 1 and month <7 else '1'

def updateDate(filename,business_dict,Business2Index):
    with open(filename,'r') as finput:
        for line in finput:
            object = json.loads(line)
            dates = object['date'].split('-')

            date = datetime(int(dates[0]),int(dates[1]),int(dates[2]))
            id = object['business_id']
            if id in Business2Index:
                if id in business_dict:
                    old_date = business_dict[id]
                    if old_date > date:
                        business_dict[id] = date
                else:
                    business_dict[id] = date

def decodeDate(date_key):
    parts = date_key.split('_')
    year = int(parts[0])
    month = '1-6' if parts[1] == '0' else '7-12'
    if year > 2011:
        return '../resources/TestBusiness_'+parts[0]+'_'+month+'.json'
    else:
        return -1

def buildBusinessObj(finput1,finput2,filename,Business2Index):

    business_dict = {}
    updateDate(finput1,business_dict,Business2Index)
    updateDate(finput2,business_dict,Business2Index)

    with open(filename,'r') as finput:
        for line in finput:
            object = json.loads(line)
            id = object['business_id']
            if id in business_dict:
                new_obj = {}
                new_obj['name'] = object['name']
                new_obj['categories'] = object['categories']
                new_obj['date'] = str(business_dict[id])
                new_obj['id'] = id
                business_dict[id] = new_obj

    return business_dict

def divideByDate(business_dict):
    # divide based on date
    business_date_dict = {}

    for id in business_dict:
        business_obj = business_dict[id]
        date = business_obj['date']
        parts = date.split('-')
        date_key = parts[0] +'_'+ encodeDate(int(parts[1]))
        if date_key in business_date_dict:
            business_date_dict[date_key][id] = business_obj
        else:
            business_date_dict[date_key] = {id:business_obj}

    for date_key in business_date_dict:
        foutput = decodeDate(date_key)
        if foutput != -1:
            with open(foutput, 'w') as outfile:
                json.dump(business_date_dict[date_key], outfile,indent=4, separators=(',', ': '))

def main():
    # my code here

    finput1 = '/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_tip.json'
    finput2 = '/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'

    with open('../resources/Business2Index.txt','r') as finput:
        Business2Index = np.loadtxt(finput,dtype='str')

    filename = '/Users/ztx/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
    test_data = buildBusinessObj(finput1,finput2,filename,Business2Index)

    divideByDate(test_data)


if __name__ == "__main__":
    main()