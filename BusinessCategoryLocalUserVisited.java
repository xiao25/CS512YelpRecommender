import java.io.BufferedReader;
import java.io.FileReader;
import java.util.*;

public class BusinessCategoryLocalUserVisited {
	public static HashMap<String, Set<String>> getBusinessCategoriesInUrbana() {
		//Key is the business_id, values are a set of categories this business belong to
		HashMap<String, Set<String>> businessCategories = new HashMap<>();

		String line = "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(
					"/Users/haowang/Desktop/CS512YelpRecommender/business_in_Urbana.txt"));

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

	public static HashMap<String, Double> getAllBusinessVisistedByLocalPeople(int cluster) {
		/**
		 * need to use a hashmap to store the category scores local users visited
		 * Key: the category local people visited, Value : its score
		 */

		HashMap<String, Set<String>> businessCategories = getBusinessCategoriesInUrbana();

		//Key is a business category, values is the overall sum of the ratings of this category visited by local people
		HashMap<String, Double> businessVisited = new HashMap<>();

		String line = "";

		try {
			String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/ReviewOnUser.txt";
			BufferedReader reader = new BufferedReader(new FileReader(fileName));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");
				String businessId = strs[1];
				int rating = Integer.parseInt(strs[2]);

				//this array is a soft clustering of the user in each cluster, use this to compute the normalized rating
				String[] clusters = strs[3].split(",");
				double normRating = rating * Double.parseDouble(clusters[cluster]);

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

	public static HashMap<String, Integer> getLocalBusinessCategory(int cluster) {
		/**
		 * need to use a hashmap to store the category scores in local cluster
		 * Key: the category locally, Value : its score
		 */

		HashMap<String, Integer> localCategory = new HashMap<>();
		HashMap<String, Set<String>> businessCategories = getBusinessCategoriesInUrbana();

		String line = "";

		try {
			String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/ReviewOnBusiness.txt";
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
								localCategory.put(category, 0);
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

	public static void main(String[] args) {
		System.out.println(getAllBusinessListsVisistedByLocalPeople(0));
		System.out.println(getLocalBusinessCategory(0));
	}
}
