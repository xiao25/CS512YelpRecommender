import java.util.*;
import java.io.*;

public class RecommendBusinessCategory_2 {
	// private static final int MAX_RECOMMENDED_BUSINESS = 10;
	private static final int TARGET_CLUSTERS = 10;
	private static final double THRESHOLD = 0.75;

	public static void main(String[] args) {
		//This is the lists of TOP 10 new business categories recommended for each cluster
		for(int i = 0; i < TARGET_CLUSTERS; i++) {
			List<String> recommendedBusiness = recommendBusiness(i);
			System.out.println("Top 10 recommended business for cluster " + i + " are:\n" + recommendedBusiness);
			System.out.println();
		}
	}

	//THE CORE ALGORITHM TO RECOMMEND BUSINESS
	public static List<String> recommendBusiness(int cluster) {
		/**
		 * For the target cluster for the recommendation: P(b|c) = sum(similarity(c, c') * P(b|c'))
		 * So we compute the similarity between this target cluster and each ideal cluster
		 * and then multiply the similarity and the popularity of the business category in the ideal cluster
		 * and sum up to get the total probability of a business category in the target cluster
		 */

		List<String> results = new ArrayList<>();

		//GET the ranked list of the business categories computed from the similarity between target cluster and all other ideal clusters
		List<BusinessRatings> listsBasedSimilarity = Recommendation2_Helper.getAllBusinessLists(cluster);
		// System.out.println(listsBasedSimilarity);

		//GET the scores of the business categories already existed in the current geo cluster
		HashMap<String, Double> listsBasedGeo = Recommendation2_Helper.businessScoreInCluster(cluster, "targetCluster");
		HashMap<String, Double> normalizedGeoLists = Recommendation2_Helper.normalize(listsBasedGeo);
		// System.out.println(normalizedGeoLists.get("Food"));

		/**
		 * To make the recommendations:
		 * Logic 1: Recommend the category which does not exist locally
		 * Logic 2: Recommend those categories with
		 * p(b|c)(computed from the geo cluster) / p(b|c)(computed from similarities) < threshold
		 */
		int count = 0;

		for(BusinessRatings business : listsBasedSimilarity) {
			String category = business.category;
			if(!normalizedGeoLists.containsKey(category) || (normalizedGeoLists.get(category)) / business.rating < THRESHOLD) {
				results.add(category);
				// count++;
				// if(count >= MAX_RECOMMENDED_BUSINESS) {
				// 	break;
				// }
			}
		}

		return results;
	}
}
