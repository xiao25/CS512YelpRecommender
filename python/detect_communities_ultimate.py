class Detector:
    def __init__(self, business_business_rbfs, user_business_rcs, user_user_fs,
        num_clusters, initial_business_cluster_hards):
        self.business_business_rbfs = business_business_rbfs
        self.user_business_rcs = user_business_rcs
        self.user_user_fs = user_user_fs
        
        self.num_businesses = len(self.business_business_rbfs)
        self.num_users = len(self.user_business_rcs)
        self.num_clusters = num_clusters
        
        self.business_cluster_hards = self.get_initial_business_cluster_hards(initial_business_cluster_hards)
        
        self.business_cluster_ranks = create_matrix(self.num_businesses, self.num_clusters, 0.0)
        self.business_cluster_softs = create_matrix(self.num_businesses, self.num_clusters, 0.0)
        
        self.user_cluster_ranks = create_matrix(self.num_users, self.num_clusters, 0.0)
        self.user_cluster_softs = create_matrix(self.num_users, self.num_clusters, 0.0)
        
        self.cluster_weights = create_vector(self.num_clusters, 1.0 / self.num_clusters)
        
    def get_initial_business_cluster_hards(self, initial_business_cluster_hards):
        if initial_business_cluster_hards != None:
            return initial_business_cluster_hards
        else:
            return [business % self.num_clusters for business in xrange(self.num_businesses)]
            
    def detect(self, num_assignment_iterations, num_ranking_iterations, 
        combine_effects_user, combine_effects_business, 
        use_uniform_cluster_weights, use_soft_directly):
        print("Detecting communities...")
        for assignment_iteration in xrange(num_assignment_iterations):
            print("Running assignment iteration " + str(assignment_iteration) + "...")
            self.compute_ranks(num_ranking_iterations, combine_effects_user, combine_effects_business)
            self.compute_business_cluster_hards(use_uniform_cluster_weights, use_soft_directly)
            self.compute_user_cluster_softs()
            
    def compute_ranks(self, num_iterations, combine_effects_user, combine_effects_business):
        self.initialize_ranks()
        for iteration in xrange(num_iterations):
            self.compute_user_ranks(combine_effects_user)
            self.compute_business_ranks(iteration != num_iterations - 1, combine_effects_business)
    
    def initialize_ranks(self):
        for business in xrange(self.num_businesses):
            for cluster in xrange(self.num_clusters):
                if self.business_cluster_hards[business] == cluster:
                    self.business_cluster_ranks[business][cluster] = 1.0
                else:
                    self.business_cluster_ranks[business][cluster] = 0.0
                    
        for user in xrange(self.num_users):
            for cluster in xrange(self.num_clusters):
                self.user_cluster_ranks[user][cluster] = 0.0
                    
    def compute_user_ranks(self, combine_effects):
        temp_user_cluster_ranks_business = create_matrix(self.num_users, self.num_clusters, 0.0)
        for user in xrange(self.num_users):
            for business in self.user_business_rcs[user]:
                cluster = self.business_cluster_hards[business]
                temp_user_cluster_ranks_business[user][cluster] += self.business_cluster_ranks[business][cluster] * \
                    self.user_business_rcs[user][business]

        temp_user_cluster_ranks_user = create_matrix(self.num_users, self.num_clusters, 0.0)
        for user in xrange(self.num_users):
            for another_user in self.user_user_fs[user]:
                for cluster in xrange(self.num_clusters):
                    if temp_user_cluster_ranks_business[user][cluster] > 0.0:
                        temp_user_cluster_ranks_user[user][cluster] += self.user_cluster_ranks[another_user][cluster]
        
        cluster_sums = create_vector(self.num_clusters, 0.0)
        for user in xrange(self.num_users):
            for cluster in xrange(self.num_clusters):
                self.user_cluster_ranks[user][cluster] = combine_effects(
                    temp_user_cluster_ranks_user[user][cluster],
                    temp_user_cluster_ranks_business[user][cluster])
                cluster_sums[cluster] += self.user_cluster_ranks[user][cluster]
        for user in xrange(self.num_users):
            for cluster in xrange(self.num_clusters):
                if cluster_sums[cluster] > 0.0:
                    self.user_cluster_ranks[user][cluster] /= cluster_sums[cluster]
                
    def compute_business_ranks(self, limited_to_subgraph, combine_effects):
        temp_business_cluster_ranks_user = create_matrix(self.num_businesses, self.num_clusters, 0.0)
        for user in xrange(self.num_users):
            for business in self.user_business_rcs[user]:
                if limited_to_subgraph:
                    cluster = self.business_cluster_hards[business]
                    temp_business_cluster_ranks_user[business][cluster] += self.user_cluster_ranks[user][cluster] * \
                        self.user_business_rcs[user][business]
                else:
                    for cluster in xrange(self.num_clusters):
                        temp_business_cluster_ranks_user[business][cluster] += self.user_cluster_ranks[user][cluster] * \
                            self.user_business_rcs[user][business]

        temp_business_cluster_ranks_business = create_matrix(self.num_businesses, self.num_clusters, 0.0)
        for business in xrange(self.num_businesses):
            cluster = self.business_cluster_hards[business]
            for another_business in self.business_business_rbfs[business]:
                if self.business_cluster_hards[another_business] == cluster or not limited_to_subgraph:
                    temp_business_cluster_ranks_business[another_business][cluster] += self.business_cluster_ranks[business][cluster] * \
                        self.business_business_rbfs[business][another_business]
        
        cluster_sums = create_vector(self.num_clusters, 0.0)
        for business in xrange(self.num_businesses):
            for cluster in xrange(self.num_clusters):
                self.business_cluster_ranks[business][cluster] = combine_effects(
                    temp_business_cluster_ranks_user[business][cluster],
                    temp_business_cluster_ranks_business[business][cluster])
                cluster_sums[cluster] += self.business_cluster_ranks[business][cluster]
        for business in xrange(self.num_businesses):
            for cluster in xrange(self.num_clusters):
                if cluster_sums[cluster] > 0.0:
                    self.business_cluster_ranks[business][cluster] /= cluster_sums[cluster]
        
    def compute_business_cluster_hards(self, use_uniform_cluster_weights, use_soft_directly):
        for business in xrange(self.num_businesses):
            sum = 0.0
            for cluster in xrange(self.num_clusters):
                if use_uniform_cluster_weights:
                    self.business_cluster_softs[business][cluster] = self.business_cluster_ranks[business][cluster]
                else:
                    self.business_cluster_softs[business][cluster] = self.business_cluster_ranks[business][cluster] * self.cluster_weights[cluster]
                sum += self.business_cluster_softs[business][cluster]
            for cluster in xrange(self.num_clusters):
                if sum > 0.0:
                    self.business_cluster_softs[business][cluster] /= sum
             
        for cluster in xrange(self.num_clusters):
            cluster_weight = 0.0
            for business in xrange(self.num_businesses):
                cluster_weight += self.business_cluster_softs[business][cluster]
            self.cluster_weights[cluster] = cluster_weight / self.num_businesses
        
        if use_soft_directly:
            for business in xrange(self.num_businesses):
                max_cluster = -1
                max_soft = 0.0
                for cluster in xrange(self.num_clusters):
                    soft = business_cluster_softs[business][cluster]
                    if soft > max_soft:
                        max_soft = soft
                        max_cluster = cluster
                self.business_cluster_hards[business] = max_cluster
        else:
            cluster_centers = create_matrix(self.num_clusters, self.num_clusters, 0.0)
            for business in xrange(self.num_businesses):
                cluster = self.business_cluster_hards[business]
                for attribute in xrange(self.num_clusters):
                    cluster_centers[cluster][attribute] += self.business_cluster_softs[business][attribute]

            cluster_center_lengths = create_vector(self.num_clusters, 0.0)
            for cluster in xrange(self.num_clusters):
                for attribute in xrange(self.num_clusters):
                    cluster_center_lengths[cluster] += cluster_centers[cluster][attribute] * cluster_centers[cluster][attribute]
                cluster_center_lengths[cluster] **= 0.5

            for business in xrange(self.num_businesses):
                max_cosine = 0.0
                max_cluster = -1
                for cluster in xrange(self.num_clusters):
                    inner_product = 0.0
                    for attribute in xrange(self.num_clusters):
                        inner_product += self.business_cluster_softs[business][attribute] * cluster_centers[cluster][attribute]
                    cosine = 0.0
                    if cluster_center_lengths[cluster] > 0.0:
                        cosine = inner_product / cluster_center_lengths[cluster]
                    if cosine > max_cosine:
                        max_cluster = cluster
                        max_cosine = cosine
                self.business_cluster_hards[business] = max_cluster
                
    def compute_user_cluster_softs(self):
        user_business_counts = create_vector(self.num_users, 0)
        for user in xrange(self.num_users):
            for cluster in xrange(self.num_clusters):
                self.user_cluster_softs[user][cluster] = 0.0
            for business in self.user_business_rcs[user]:
                user_business_counts[user] += self.user_business_rcs[user][business]
                for cluster in xrange(self.num_clusters):
                    self.user_cluster_softs[user][cluster] += self.business_cluster_softs[business][cluster] * \
                        self.user_business_rcs[user][business]
            for cluster in xrange(self.num_clusters):
                self.user_cluster_softs[user][cluster] /= user_business_counts[user]

def create_matrix(num_rows, num_cols, initial_value):
    return [[initial_value for col in xrange(num_cols)] for row in xrange(num_rows)]
    
def create_vector(num_entries, initial_value):
    return [initial_value for entry in xrange(num_entries)]
    
def load_ids(filename):
    ids = []
    ids_file = open(filename, "r")
    for line in ids_file.readlines():
        ids.append(line[:-1])
    ids_file.close()
    return ids
    
def load_relationships(filename, convert_value, exclusive_min_value, inclusive_max_value):
    relationships = []
    relationship_file = open(filename, "r")
    src = 0
    for line in relationship_file.readlines():
        dest_values = {}
        dest = 0
        for raw_value_str in line.split():
            value = convert_value(float(raw_value_str))
            if src != dest and value > exclusive_min_value:
                if inclusive_max_value == None or value <= inclusive_max_value:
                    dest_values[dest] = value
                else:
                    dest_values[dest] = inclusive_max_value
            dest += 1
        src += 1
        relationships.append(dest_values)
    relationship_file.close()
    return relationships
    
def output_matrix(filename, matrix, convert_index):
    output_file = open(filename, "w")
    for index in xrange(len(matrix)):
        converted_index = convert_index(index)
        output_file.write(str(converted_index))
        for item in matrix[index]:
            output_file.write(" " + str(item))
        output_file.write("\n")
    output_file.close()
    
def output_vector(filename, vector, convert_index):
    output_file = open(filename, "w")
    for index in xrange(len(vector)):
        converted_index = convert_index(index)
        item = vector[index]
        output_file.write(str(converted_index) + " " + str(item) + "\n")
    output_file.close()
        
def load_initial_business_cluster_hards(filename, business_ids):
    business_cluster_hards_map = {}
    business_cluster_hards_file = open(filename, "r")
    for line in business_cluster_hards_file.readlines():
        info = line.split()
        yelp_id = info[0]
        cluster = int(info[1])
        business_cluster_hards_map[yelp_id] = cluster
    business_cluster_hards_file.close()
    return [business_cluster_hards_map[business_ids[business]] for business in xrange(len(business_ids))]
    
resources_folder = "../resources/"

rbf = lambda distance: 200.0 / (distance + 1.0)
business_business_rbfs = load_relationships(resources_folder + "BB.txt", rbf, 0.4, 200.0)

identity_function = lambda x: x
user_business_rcs = load_relationships(resources_folder + "UB.txt", identity_function, 0.0, None)
user_user_fs = load_relationships(resources_folder + "UU.txt", identity_function, 0.0, None)

business_ids = load_ids(resources_folder + "Business2Index.txt")
user_ids = load_ids(resources_folder + "User2Index.txt")

num_clusters = 20

# initial_business_cluster_hards = load_initial_business_cluster_hards(resources_folder + "KMeans2.txt", business_ids)

detector = Detector(business_business_rbfs, user_business_rcs, user_user_fs, 
    num_clusters, None)
    
num_assignment_iterations = 30
num_ranking_iterations = 20
combine_effects_user = lambda effect_user, effect_business: 0.2 * effect_user + 0.8 * effect_business
combine_effects_business = lambda effect_user, effect_business: effect_user
use_uniform_cluster_weights = False
use_soft_directly = False

detector.detect(num_assignment_iterations, num_ranking_iterations, 
    combine_effects_user, combine_effects_business, 
    use_uniform_cluster_weights, use_soft_directly)
    
output_vector(resources_folder + "clusters/business_cluster_hards_pure.txt", detector.business_cluster_hards, lambda index: business_ids[index])
output_matrix(resources_folder + "clusters/user_cluster_softs_pure.txt", detector.user_cluster_softs, lambda index: user_ids[index])
    