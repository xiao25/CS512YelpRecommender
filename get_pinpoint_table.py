id_cluster = {}
f = open("business_cluster_hard.txt", "r")
for line in f.readlines():
    info = line.split()
    yelp_id = info[0]
    cluster = int(info[1])
    id_cluster[yelp_id] = cluster
f.close()

id_info = []
f = open("ID2Point.txt", "r")
for line in f.readlines():
    info = line.split()
    yelp_id = info[0]
    longitude = float(info[1])
    latitude = float(info[2])
    cluster = id_cluster[yelp_id]
    id_info.append((yelp_id, longitude, latitude, cluster))
f.close()

f = open("pinpoint_table.csv", "w")
f.write("Name,Cluster,Latitude,Longitude\n")
for (yelp_id, longitude, latitude, cluster) in id_info:
    if cluster >= 0 and cluster < 7: # it seems that the found website can only display 7 colors...
        f.write(yelp_id + "," + str(cluster) + "," + str(latitude) + "," + str(longitude) + "\n")
f.close()