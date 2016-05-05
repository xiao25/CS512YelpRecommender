import math

def detect_communities(business_business_rbf, user_business_rc, initial_business_cluster_hard,
    num_clusters, num_assignment_iterations, num_ranking_iterations):
    print("Detecting communities...")
    
    num_businesses = len(business_business_rbf)
    num_users = len(user_business_rc)
    
    business_cluster_rank = [[0.0 for cluster in xrange(num_clusters)] for business in xrange(num_businesses)]
    business_cluster_soft = [[0.0 for cluster in xrange(num_clusters)] for business in xrange(num_businesses)]
    business_cluster_hard = initial_business_cluster_hard #[business % num_clusters for business in xrange(num_businesses)]
        
    user_cluster_rank = [[0.0 for cluster in xrange(num_clusters)] for user in xrange(num_users)]
    user_cluster_soft = [[0 for cluster in xrange(num_clusters)] for user in xrange(num_users)]
    
    cluster_weights = [1.0 / num_clusters for cluster in xrange(num_clusters)]
    
    for assignment_iteration in xrange(num_assignment_iterations):
        print("Running assignment iteration " + str(assignment_iteration) + "...")
        compute_ranks(business_cluster_rank, business_cluster_hard, user_cluster_rank, 
            business_business_rbf, user_business_rc, num_ranking_iterations)
        compute_assignment(business_cluster_rank, cluster_weights, business_cluster_soft, business_cluster_hard)
        compute_user_cluster_soft(business_cluster_soft, user_business_rc, user_cluster_soft)
        
    return (business_cluster_hard, user_cluster_soft)
    
def compute_ranks(business_cluster_rank, business_cluster_hard, user_cluster_rank, 
    business_business_rbf, user_business_rc, num_iterations):
    num_businesses = len(business_business_rbf)
    num_users = len(user_business_rc)
    num_clusters = len(business_cluster_rank[0])
    
    for business in xrange(num_businesses):
        for cluster in xrange(num_clusters):
            if business_cluster_hard[business] == cluster:
                business_cluster_rank[business][cluster] = 1.0
            else:
                business_cluster_rank[business][cluster] = 0.0
    
    for iteration in xrange(num_iterations):
        cluster_sums = [0.0 for cluster in xrange(num_clusters)]
        
        for user in xrange(num_users):
            for cluster in xrange(num_clusters):
                user_cluster_rank[user][cluster] = 0.0
            for business in user_business_rc[user]:
                cluster = business_cluster_hard[business]
                contribution = business_cluster_rank[business][cluster] * user_business_rc[user][business]
                user_cluster_rank[user][cluster] += contribution
                cluster_sums[cluster] += contribution

        for user in xrange(num_users):
            for cluster in xrange(num_clusters):
                user_cluster_rank[user][cluster] /= cluster_sums[cluster]
                
        temp_business_cluster_rank_user = [[0.0 for cluster in xrange(num_clusters)] for business in xrange(num_businesses)]
        for user in xrange(num_users):
            for business in user_business_rc[user]:
                if iteration == num_iterations - 1:
                    for cluster in xrange(num_clusters):
                        contribution = user_cluster_rank[user][cluster] * user_business_rc[user][business]
                        temp_business_cluster_rank_user[business][cluster] += contribution
                else:
                    cluster = business_cluster_hard[business]
                    contribution = user_cluster_rank[user][cluster] * user_business_rc[user][business]
                    temp_business_cluster_rank_user[business][cluster] += contribution

        
        temp_business_cluster_rank_business = [[0.0 for cluster in xrange(num_clusters)] for business in xrange(num_businesses)]
        for business in xrange(num_businesses):
            cluster = business_cluster_hard[business]
            for another_business in business_business_rbf[business]:
                if business_cluster_hard[another_business] == cluster or iteration == num_iterations - 1:
                    contribution = business_cluster_rank[business][cluster] * business_business_rbf[business][another_business]
                    temp_business_cluster_rank_business[another_business][cluster] += contribution
        
        temp_business_cluster_rank = [[0.0 for cluster in xrange(num_clusters)] for business in xrange(num_businesses)]
        cluster_sums = [0.0 for cluster in xrange(num_clusters)]
        for business in xrange(num_businesses):
            for cluster in xrange(num_clusters):
                temp_business_cluster_rank[business][cluster] += temp_business_cluster_rank_user[business][cluster] * \
                    temp_business_cluster_rank_business[business][cluster]
                cluster_sums[cluster] += temp_business_cluster_rank[business][cluster]
        
        for business in xrange(num_businesses):
            for cluster in xrange(num_clusters):
                business_cluster_rank[business][cluster] = temp_business_cluster_rank[business][cluster] / cluster_sums[cluster]
    
def compute_assignment(business_cluster_rank, cluster_weights, business_cluster_soft, business_cluster_hard):
    num_businesses = len(business_cluster_soft)
    num_clusters = len(business_cluster_soft[0])
    
    for business in xrange(num_businesses):
        sum = 0.0
        for cluster in xrange(num_clusters):
            business_cluster_soft[business][cluster] = business_cluster_rank[business][cluster] # * cluster_weights[cluster]
            sum += business_cluster_soft[business][cluster]
        for cluster in xrange(num_clusters):
            business_cluster_soft[business][cluster] /= sum
                
    for cluster in xrange(num_clusters):
        cluster_weight = 0.0
        for business in xrange(num_businesses):
            cluster_weight += business_cluster_soft[business][cluster]
        cluster_weights[cluster] = cluster_weight / num_businesses
            
    for business in xrange(num_businesses):
        max_cluster = -1
        max_soft = 0.0
        for cluster in xrange(num_clusters):
            soft = business_cluster_soft[business][cluster]
            if soft > max_soft:
                max_soft = soft
                max_cluster = cluster
        business_cluster_hard[business] = max_cluster
            
    # cluster_centers = [[0.0 for attribute in xrange(num_clusters)] for cluster in xrange(num_clusters)]
    # cluster_center_lengths = [0.0 for cluster in xrange(num_clusters)]
    
    # for business in xrange(num_businesses):
    #     cluster = business_cluster_hard[business]
    #     for attribute in xrange(num_clusters):
    #         cluster_centers[cluster][attribute] += business_cluster_soft[business][attribute]
    #
    # for cluster in xrange(num_clusters):
    #     for attribute in xrange(num_clusters):
    #         cluster_center_lengths[cluster] += cluster_centers[cluster][attribute] * cluster_centers[cluster][attribute]
    #     cluster_center_lengths[cluster] **= 0.5
    #
    # for business in xrange(num_businesses):
    #     max_cosine = 0.0
    #     max_cluster = -1
    #     for cluster in xrange(num_clusters):
    #         inner_product = 0.0
    #         for attribute in xrange(num_clusters):
    #             inner_product += business_cluster_soft[business][attribute] * cluster_centers[cluster][attribute]
    #         cosine = inner_product / cluster_center_lengths[cluster]
    #         if cosine > max_cosine:
    #             max_cluster = cluster
    #             max_cosine = cosine
    #     business_cluster_hard[business] = max_cluster
    
def compute_user_cluster_soft(business_cluster_soft, user_business_rc, user_cluster_soft):
    num_businesses = len(business_cluster_soft)
    num_users = len(user_business_rc)
    num_clusters = len(business_cluster_soft[0])

    user_business_counts = [0.0 for user in xrange(num_users)]
    
    for user in xrange(num_users):
        for cluster in xrange(num_clusters):
            user_cluster_soft[user][cluster] = 0.0
        for business in user_business_rc[user]:
            user_business_counts[user] += user_business_rc[user][business]
            for cluster in xrange(num_clusters):
                user_cluster_soft[user][cluster] += business_cluster_soft[business][cluster] * user_business_rc[user][business]
        for cluster in xrange(num_clusters):
            user_cluster_soft[user][cluster] /= user_business_counts[user]

def load_business_business_rbf(max_threshold, min_threshold, rbf):
    business_business_rbf = []
    f = open("BB.txt", "r")
    business = 0
    for line in f.readlines():
        business_rbf = {}
        another_business = 0
        for distance_str in line.split():
            distance = float(distance_str)
            if business != another_business and distance < max_threshold:
                if distance > min_threshold:
                    business_rbf[another_business] = rbf(distance)
                else:
                    business_rbf[another_business] = rbf(0.0)
            another_business += 1
        business += 1
        business_business_rbf.append(business_rbf)
    f.close()
    return business_business_rbf
    
def load_user_business_rc():
    user_business_rc = []
    f = open("UB.txt", "r")
    for line in f.readlines():
        business_rc = {}
        business = 0
        for rc_str in line.split():
            rc = int(rc_str)
            if rc != 0:
                business_rc[business] = rc
            business += 1
        user_business_rc.append(business_rc)
    f.close()
    return user_business_rc
    
def load_business_id():
    business_id = []
    f = open("Business2Index.txt", "r")
    for line in f.readlines():
        business_id.append(line[:-1])
    f.close()
    return business_id
    
def load_user_id():
    user_id = []
    f = open("User2Index.txt", "r")
    for line in f.readlines():
        user_id.append(line[:-1])
    f.close()
    return user_id
    
def load_initial_business_cluster_hard(business_id, num_businesses):
    business_cluster_hard_map = {}
    f = open("Keans.txt", "r")
    for line in f.readlines():
        info = line.split()
        yelp_id = info[0]
        cluster = int(info[1])
        business_cluster_hard_map[yelp_id] = cluster
    f.close()
    return [business_cluster_hard_map[business_id[business]] for business in xrange(num_businesses)]
    
def write_business_cluster_hard(business_cluster_hard, business_id):
    f = open("business_cluster_hard.txt", "w")
    for business in xrange(len(business_cluster_hard)):
        yelp_id = business_id[business]
        cluster = business_cluster_hard[business]
        f.write(yelp_id + " " + str(cluster) + "\n")
    f.close()
    
def write_user_cluster_soft(user_cluster_soft, user_id):
    f = open("user_cluster_soft.txt", "w")
    for user in xrange(len(user_cluster_soft)):
        yelp_id = user_id[user]
        f.write(yelp_id)
        for weight in user_cluster_soft[user]:
            f.write(" " + str(weight))
        f.write("\n")
    f.close()
    
def write_matrix(matrix):
    f = open("temp.txt", "w")
    f.write("\n".join([" ".join([str(item) for item in row]) for row in matrix]))
    f.close()
    
if __name__ == "__main__":
    business_business_rbf = load_business_business_rbf(1000000.0, 20.0, lambda distance: (200.0 / (distance + 1.0)) ** 2.0) # + 1.0 to deal with 0.0 input
    user_business_rc = load_user_business_rc()
    
    num_clusters = 10
    
    business_id = load_business_id()
    initial_business_cluster_hard = load_initial_business_cluster_hard(business_id, len(business_business_rbf))
    
    (business_cluster_hard, user_cluster_soft) = detect_communities(business_business_rbf, user_business_rc, initial_business_cluster_hard, num_clusters, 0, 20)
    
    write_business_cluster_hard(business_cluster_hard, business_id)
    user_id = load_user_id()
    write_user_cluster_soft(user_cluster_soft, user_id)
    