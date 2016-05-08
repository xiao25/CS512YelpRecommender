import java.util.*;
import java.io.*;

public class Recommendation2_Helper {
	private static final int TARGET_CLUSTERS = 10;
	private static final int IDEAL_CLUSTERS = 10;
	private static final int CATEGORIES = 292;

	public static HashMap<String, Set<String>> getBusinessCategoriesInUrbana() {
		//Key is the business_id, values are a set of categories this business belong to
		HashMap<String, Set<String>> businessCategories = new HashMap<>();

		HashSet<String> set = getTestingBusiness();

		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512_Project/Business_in_Urbana.txt"));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");
				String businessId = strs[0];
				String[] categories = strs[1].split(",");

				if(set.contains(businessId)) continue; //remove those testing business from the dataset

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

	public static HashMap<Integer, Set<String>> getBusinessCluster(String type) {
		//Key is the cluster #, values is a set of all the business in the cluster
		HashMap<Integer, Set<String>> businessCluster = new HashMap<>();

		HashSet<String> set = getTestingBusiness();

		String line = "";

		String targetCluster = "/Users/haowang/Desktop/CS512_Project/KMeans.txt";
		String idealCluster = "/Users/haowang/Desktop/CS512_Project/business_cluster_hard_mixed.txt";
		BufferedReader reader = null;

		try {
			if(type.equals("targetCluster")) {
				reader = new BufferedReader(new FileReader(targetCluster));
			} else if(type.equals("idealCluster")){
				reader = new BufferedReader(new FileReader(idealCluster));
			}

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split(" ");
				String businessId = strs[0];
				int cluster = Integer.parseInt(strs[1]);

				if(set.contains(businessId)) continue; //remove those testing business from the dataset

				if(cluster >= 0) {
					if(!businessCluster.containsKey(cluster)) {
						businessCluster.put(cluster, new HashSet<String>());
					}

					businessCluster.get(cluster).add(businessId);
				}
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
		/**
		 * The key is the two clusters with the format like 1_2 (cluster 1 and 2), 2_1(cluster 2 and 1)
		 * The value is their cosine similarity
		 */
		HashMap<String, Double> similarity = new HashMap<>();

		for(int i = 0; i < TARGET_CLUSTERS; i++) {
			for(int j = 0; j < IDEAL_CLUSTERS; j++) {
				similarity.put(i + "," + j, cosineSimilarity(i, j));
			}
		}

		return similarity;
	}

	//compute the cosine similarity of two clusters based on their vector representations
	public static double cosineSimilarity(int cluster1, int cluster2) {
		int[] c1_cluster = getClusterVector(cluster1, "targetCluster");
		int[] c2_cluster = getClusterVector(cluster2, "idealCluster");

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
	public static int[] getClusterVector(int cluster, String type) {
		int[] vector = new int[CATEGORIES];

		HashMap<String, Set<String>> businessCategories = getBusinessCategoriesInUrbana();
		HashMap<String, Integer> categoryIndex = mappingCategory2Index();

		HashMap<Integer, Set<String>> businessCluster = getBusinessCluster(type);

		for(String businessId : businessCluster.get(cluster)) {
			for(String category : businessCategories.get(businessId)) {
				vector[categoryIndex.get(category)]++;
			}
		}

		return vector;
	}

	public static HashMap<String, Integer> checkInNums() {
		HashMap<String, Integer> result = new HashMap<>();

		HashSet<String> set = getTestingBusiness();

		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512_Project/BusinessCheckIns.txt"));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");

				if(set.contains(strs[0])) continue; //remove those testing business from the dataset

				result.put(strs[0], Integer.parseInt(strs[1]));
			}

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return result;
	}

	// public static HashMap<String, Integer> Review2CheckIns() {
	// 	HashMap<String, Integer> result = new HashMap<>();

	// 	HashSet<String> set = getTestingBusiness();

	// 	String line = "";

	// 	try {
	// 		BufferedReader reader = new BufferedReader(new FileReader(
	// 				"/Users/haowang/Desktop/CS512_Project/BusinessReviews.txt"));

	// 		while ((line = reader.readLine()) != null) {
	// 			String[] strs = line.split("\t");

	// 			if(set.contains(strs[0])) continue; //remove those testing business from the dataset

	// 			result.put(strs[0], Integer.parseInt(strs[1]));
	// 		}

	// 		reader.close();
	// 	} catch (Exception e) {
	// 		e.printStackTrace();
	// 	}

	// 	return result;
	// }

	public static HashMap<String, Double> businessScoreInCluster(int cluster, String type) {
		//p(b|c'), the score of the business category in the cluster
		HashMap<String, Double> categoryScores = new HashMap<>();

		HashMap<String, Set<String>> businessCategories = getBusinessCategoriesInUrbana();
		HashMap<Integer, Set<String>> businessCluster = getBusinessCluster(type);

		HashMap<String, Integer> checkInCounts = checkInNums();
		// HashMap<String, Integer> reviews = Review2CheckIns();

		Set<String> business_in_cluster = businessCluster.get(cluster);

		for(String businessId : business_in_cluster) {
			//use checkin numbers + review scores to represent p(b|c')
			double score = 0.0;

			if(checkInCounts.containsKey(businessId)) {
				score += checkInCounts.get(businessId);
			}

			// if(reviews.containsKey(businessId)) {
			// 	score += reviews.get(businessId) / 2.5;
			// }

			for(String category : businessCategories.get(businessId)) {
				if(!categoryScores.containsKey(category)){
					categoryScores.put(category, 0.0);
				}

				categoryScores.put(category, categoryScores.get(category) + score);
			}
		}

		return categoryScores;
	}

	public static HashMap<String, Double> getAllBusinessScore(int targetCluster) {
		//key: the the business category (overall 292 categories)
		//value: the category score computed from the similarity bewteen this target cluster and all other ideal clusters
		HashMap<String, Double> allBusinessScores = new HashMap<>();

		HashMap<String, Double> similarity = clusterSimilarity();

		//all 292 categories
		HashMap<String, Integer> allCategories = mappingCategory2Index();

		for(String category : allCategories.keySet()) {
			double score = 0.0;

			//p(b|c) = sum(similarity(c, c') * P(b|c'))
			for(int idealCluster = 0; idealCluster < IDEAL_CLUSTERS; idealCluster++) {
				HashMap<String, Double> categoryScore = businessScoreInCluster(idealCluster, "idealCluster");

				if(categoryScore.containsKey(category)) {
					score += similarity.get(targetCluster + "," + idealCluster) * categoryScore.get(category);
				}
			}

			allBusinessScores.put(category, score);
		}

		//normalize the values to be within 0 and 1
		HashMap<String, Double> normalizedScores = normalize(allBusinessScores);

		return normalizedScores;
	}

	public static List<BusinessRatings> getAllBusinessLists(int cluster) {
		HashMap<String, Double> businessScores = getAllBusinessScore(cluster);

		/**
		 * the sorted business categories based on overall scores computed from the similarity
		 * between target cluster and ideal cluster
		 */
		List<BusinessRatings> businessLists = new ArrayList<>();

		for(Map.Entry<String, Double> entry : businessScores.entrySet()) {
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

	public static HashMap<String, Double> normalize(HashMap<String, Double> map) {
		double sum = 0.0;

		for(double score : map.values()) {
			sum += score;
		}

		HashMap<String, Double> result = new HashMap<>();

		for(String category : map.keySet()) {
			result.put(category, map.get(category) / sum);
		}

		return result;
	}

	public static HashSet<String> getTestingBusiness() {
		//get the testing set business_id
		HashSet<String> result = new HashSet<>();
		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512_Project/TestBusiness10.txt"));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");
				result.add(strs[0]);
			}

			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return result;
	}


	public static void main(String[] args) {
		System.out.println(getAllBusinessLists(1));
	}
}