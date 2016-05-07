id_cluster = {}
f = open("../resources/KMeans2.txt", "r")
for line in f.readlines():
    info = line.split()
    yelp_id = info[0]
    cluster = int(info[1])
    id_cluster[yelp_id] = cluster
f.close()

id_info = []
f = open("../resources/ID2Point.txt", "r")
for line in f.readlines():
    info = line.split()
    yelp_id = info[0]
    longitude = float(info[1])
    latitude = float(info[2])
    cluster = id_cluster[yelp_id]
    id_info.append((yelp_id, longitude, latitude, cluster))
f.close()

output_filename = "../resources/clustered_businesses.txt"

f = open(output_filename, "w")
for (yelp_id, longitude, latitude, cluster) in id_info:
    f.write(yelp_id + "," + str(latitude) + "," + str(longitude) + "," + str(cluster) + "\n")
f.close()