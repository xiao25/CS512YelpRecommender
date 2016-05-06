import java.util.*;
import java.io.*;

public class RecommendBusinessCategory_1 {
	private static final int MAX_RECOMMENDED_BUSINESS = 10;
	private static final double THRESHOLD = 0.4;
	private static final int CLUSTERS = 10;

	public static void main(String[] args) {
		//This is the lists of TOP 10 new business categories recommended for each cluster
		for(int i = 0; i < CLUSTERS; i++) {
			List<String> recommendedBusiness = recommendBusiness(i);
			System.out.println("Top 10 recommended business for cluster " + i + " are:\n" + recommendedBusiness);
			System.out.println();
		}
	}

	//THE CORE ALGORITHM TO RECOMMEND BUSINESS
	public static List<String> recommendBusiness(int cluster) {
		/**
		 * Each cluster has a set of user_ids and business_ids
		 * 1.	Use user_ids to compute all the categories visited by local users and their scores
		 * 2.	Use business_ids to compute all the categories existed locally and their scores
		 */

		//this is the list of all the business categories local users visited ranked by their overall ratings
		List<BusinessRatings> visitedLists = BusinessCategoryLocalUserVisited.getAllBusinessListsVisistedByLocalPeople(cluster);
		//System.out.println(visitedLists);

		//this is the list of all the local business categories ranked by their overall ratings
		HashMap<String, Double> localCategory = BusinessCategoryLocalUserVisited.getLocalBusinessCategory(cluster);
		//System.out.println(localCategory);

		List<String> results = new ArrayList<>();

		/**
		 * To make the recommendations:
		 * Logic 1: Recommend the category which does not exist locally
		 * Logic 2: Recommend those categories with sum(scores)_locally / sum(scores)_overall < threshold
		 */
		int count = 0;
		for(BusinessRatings business : visitedLists) {
			String category = business.category;
			if(!localCategory.containsKey(category) || (localCategory.get(category) + 0.0) / business.rating < THRESHOLD) {
				results.add(category);
				count++;
				if(count >= MAX_RECOMMENDED_BUSINESS) {
					break;
				}
			}
		}

		return results;
	}
}
