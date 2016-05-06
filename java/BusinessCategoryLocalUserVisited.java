import java.io.BufferedReader;
import java.io.FileReader;
import java.util.*;

public class BusinessCategoryLocalUserVisited {
	private static final int CLUSTERS = 10;

	public static HashMap<String, Set<String>> getBusinessCategoriesInUrbana() {
		//Key is the business_id, values are a set of categories this business belong to
		HashMap<String, Set<String>> businessCategories = new HashMap<>();

		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512_Project/business_in_Urbana.txt"));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");
				String businessId = strs[0];
				String[] categories = strs[1].split(",");

				if(!businessCategories.containsKey(businessId)) {
					businessCategories.put(businessId, new HashSet<String>());
				}

				for(String category : categories) {
					if(!category.equals("")) {
						businessCategories.get(businessId).add(category);
					}
				}

			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return businessCategories;
	}

	public static HashMap<String, Integer> getBusinessCluster() {
		HashMap<String, Integer> businessCluster = new HashMap<>();

		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512_Project/business_cluster_hard.txt"));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split(" ");
				String businessId = strs[0];
				int cluster = Integer.parseInt(strs[1]);

				businessCluster.put(businessId, cluster);
			}

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return businessCluster;
	}

	public static HashMap<String, Integer> mappingCategory2Index () {
		//Key is the category name, value is its corresponding index in the vector
		HashMap<String, Integer> categoryIndex = new HashMap<>();

		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512_Project/Categories_in_Urbana.txt"));

			int index = 0;

			while ((line = reader.readLine()) != null) {
				categoryIndex.put(line, index++);
			}

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}


		return categoryIndex;
	}

	public static HashMap<String, Double> clusterSimilarity() {
		//The key is the two clusters with the format like 1_2 (cluster 1 and 2), 2_1(cluster 2 and 1)
		HashMap<String, Double> similarity = new HashMap<>();

		for(int i = 0; i < CLUSTERS; i++) {
			for(int j = 0; j < CLUSTERS; j++) {
				similarity.put(i + "," + j, cosineSimilarity(i, j));
			}
		}

		return similarity;
	}

	public static HashMap<String, Double> getAllBusinessVisistedByLocalPeople(int cluster) {
		/**
		 * need to use a hashmap to store the category scores local users visited
		 * Key: the category local people visited, Value : its score
		 */

		HashMap<String, Set<String>> businessCategories = getBusinessCategoriesInUrbana();
		HashMap<String, Integer> businessCluster = getBusinessCluster();
		HashMap<String, Double> clusterSimilarity = clusterSimilarity();

		//Key is a business category, values is the overall sum of the ratings of this category visited by local people
		HashMap<String, Double> businessVisited = new HashMap<>();

		String line = "";

		try {
			String fileName = "/Users/haowang/Desktop/CS512_Project/ReviewOnUser.txt";
			BufferedReader reader = new BufferedReader(new FileReader(fileName));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");
				String businessId = strs[1];
				int rating = Integer.parseInt(strs[2]);

				int clusterOfReviewedBusiness = businessCluster.get(businessId);
				double similarity = clusterSimilarity.get(cluster + "," + clusterOfReviewedBusiness);

				//this array is a soft clustering of the user in each cluster, use this to compute the normalized rating
				String[] clusters = strs[3].split(",");
				double normRating = rating * Double.parseDouble(clusters[cluster]) * similarity;

				Set<String> categories = businessCategories.get(businessId);

				if(!categories.isEmpty()){
					for(String category: categories) {
						if(!businessVisited.containsKey(category)) {
							businessVisited.put(category, 0.0);
						} else {
							businessVisited.put(category, businessVisited.get(category) + normRating);
						}
					}
				}
			}

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return businessVisited;
	}

	public static HashMap<String, Double> getLocalBusinessCategory(int cluster) {
		/**
		 * need to use a hashmap to store the category scores in local cluster
		 * Key: the category locally, Value : its score
		 */

		HashMap<String, Double> localCategory = new HashMap<>();
		HashMap<String, Set<String>> businessCategories = getBusinessCategoriesInUrbana();

		String line = "";

		try {
			String fileName = "/Users/haowang/Desktop/CS512_Project/ReviewOnBusiness.txt";
			// String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/ReviewWithTwoClusters.txt";

			BufferedReader reader = new BufferedReader(new FileReader(fileName));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");
				String businessId = strs[0];
				int rating = Integer.parseInt(strs[2]);

				Set<String> categories = businessCategories.get(businessId);

				if(Integer.parseInt(strs[3]) == cluster) {
					if(!categories.isEmpty()){
						for(String category: categories) {
							if(!localCategory.containsKey(category)) {
								localCategory.put(category, 0.0);
							} else {
								localCategory.put(category, localCategory.get(category) + rating);
							}
						}
					}
				}

			}

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return localCategory;

	}

	public static List<BusinessRatings> getAllBusinessListsVisistedByLocalPeople(int cluster) {
		HashMap<String, Double> businessRatings = getAllBusinessVisistedByLocalPeople(cluster);

		//the sorted business categories based on overall ratings visited by local people
		List<BusinessRatings> businessLists = new ArrayList<>();

		for(Map.Entry<String, Double> entry : businessRatings.entrySet()) {
			businessLists.add(new BusinessRatings(entry.getKey(), entry.getValue()));
		}

		Collections.sort(businessLists, new Comparator<BusinessRatings>(){
			@Override
			public int compare(BusinessRatings r1, BusinessRatings r2) {
				if(r1.rating == r2.rating) return 0;
				return r1.rating < r2.rating? 1 : -1;
			}
		});

		return businessLists;
	}

	//compute the cosine similarity of two clusters based on their vector representations
	public static double cosineSimilarity(int cluster1, int cluster2) {
		int[] c1_cluster = getClusterVector(cluster1);
		int[] c2_cluster = getClusterVector(cluster2);

		int numerator = 0;
        int A_Square = 0;
        int B_Square = 0;

        for(int i = 0; i < c1_cluster.length; i++) {
            numerator += c1_cluster[i] * c2_cluster[i];
            A_Square += c1_cluster[i] * c1_cluster[i];
            B_Square += c2_cluster[i] * c2_cluster[i];
        }

        double denominator = Math.sqrt(A_Square) * Math.sqrt(B_Square);

        return numerator / denominator;
	}

	/**
	 *	For each cluster, use a vector to represent it, each entry in the vector is the # of that category in the cluster
	 * 	There are 292 business categories in Urbana, so it is a vector of length 292
	 */
	public static int[] getClusterVector(int cluster) {
		int[] vector = new int[292];

		HashMap<String, Set<String>> businessCategories = getBusinessCategoriesInUrbana();
		HashMap<String, Integer> categoryIndex = mappingCategory2Index();

		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512_Project/business_cluster_hard.txt"));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split(" ");
				String businessId = strs[0];
				int cur_cluster = Integer.parseInt(strs[1]);

				if(cur_cluster == cluster) {
					Set<String> categories = businessCategories.get(businessId);

					for(String category : categories) {
						if(!category.equals("")) {
							vector[categoryIndex.get(category)]++;
						}
					}
				}
			}

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return vector;
	}

	public static void main(String[] args) {
		System.out.println(getAllBusinessListsVisistedByLocalPeople(1));
		System.out.println(getLocalBusinessCategory(1));

		// for(int i = 0; i < getClusterVector(0).length; i++) {
		// 	if(getClusterVector(0)[i] != 0) {
		// 		System.out.println(i + ":" + getClusterVector(0)[i]);
		// 	}
		// }
	}
}
