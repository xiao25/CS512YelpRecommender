colors = ["black", "blue", "brown", "burgundy", "cloud", 
    "forest", "fuscia", "green", "grey", "lavender", "light blue", 
    "light green", "light purple", "light yellow", "maize", "mold", 
    "olive", "orange", "purple", "red", "red dust", "sky", "spring", 
    "sunset", "teal", "tree", "white", "yellow"]
    
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
f.write("Name,Color,Latitude,Longitude\n")
for (yelp_id, longitude, latitude, cluster) in id_info:
    color = colors[cluster]
    f.write(yelp_id + "," + str(longitude) + "," + str(latitude) + "," + color + "\n")
f.close()