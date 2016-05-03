import java.util.*;
import java.io.*;

public class ReviewPlusClusterParser {
	public static void main(String[] args) {
		// reviewOnUser();
		// reviewOnBusiness();
		ReviewWithTwoClusters();
	}

	//Each line of the generated txt file is: "business_id	user_id	  rating   business_cluster  user_cluster"
	public static void ReviewWithTwoClusters() {
		HashMap<String, String> businessCluster = getBusinessCluster();
		HashMap<String, String> userCluster = getUserCluster();
		String line = "";

		try {
			String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/Review_in_Urbana_Business_User.txt";
			BufferedReader reader = new BufferedReader(new FileReader(fileName));

			BufferedWriter bw = new BufferedWriter(new FileWriter("ReviewWithTwoClusters.txt"));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split("\t");
				String business_id = strs[0];
				String user_id = strs[1];
				String rating = strs[2];

				String b_cluster = businessCluster.get(business_id);
				String u_cluster = userCluster.get(user_id);

				bw.write(business_id + "\t" + user_id + "\t" + rating + "\t" + b_cluster + "\t" + u_cluster);
				bw.newLine();
			}

			reader.close();
			bw.close();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// public static void reviewOnUser() {
	// 	HashMap<String, String> map = getUserCluster();
	// 	String line = "";

	// 	try {
	// 		String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/Review_in_Urbana_User_Business.txt";
	// 		BufferedReader reader = new BufferedReader(new FileReader(fileName));

	// 		BufferedWriter bw = new BufferedWriter(new FileWriter("ReviewOnUser.txt"));

	// 		while ((line = reader.readLine()) != null) {
	// 			String[] strs = line.split("\t");
	// 			String user_id = strs[0];
	// 			String cluster = map.get(user_id);

	// 			bw.write(user_id + "\t" + strs[1] + "\t" + strs[2] + "\t" + cluster);
	// 			bw.newLine();
	// 		}

	// 		reader.close();
	// 		bw.close();

	// 	} catch (Exception e) {
	// 		e.printStackTrace();
	// 	}

	// }

	// public static void reviewOnBusiness() {
	// 	HashMap<String, String> map = getBusinessCluster();
	// 	String line = "";

	// 	try {
	// 		String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/Review_in_Urbana_Business_User.txt";
	// 		BufferedReader reader = new BufferedReader(new FileReader(fileName));

	// 		BufferedWriter bw = new BufferedWriter(new FileWriter("ReviewOnBusiness.txt"));

	// 		while ((line = reader.readLine()) != null) {
	// 			String[] strs = line.split("\t");
	// 			String business_id = strs[0];
	// 			String cluster = map.get(business_id);

	// 			bw.write(business_id + "\t" + strs[1] + "\t" + strs[2] + "\t" + cluster);
	// 			bw.newLine();
	// 		}

	// 		reader.close();
	// 		bw.close();

	// 	} catch (Exception e) {
	// 		e.printStackTrace();
	// 	}

	// }

	public static HashMap<String, String> getBusinessCluster() {
		HashMap<String, String> map = new HashMap<>();
		String line = "";

		try {
			String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/business_cluster_hard.txt";
			BufferedReader reader = new BufferedReader(new FileReader(fileName));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split(" ");
				String business_id = strs[0];
				String cluster = strs[1];

				map.put(business_id, cluster);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		return map;

	}

	public static HashMap<String, String> getUserCluster() {
		HashMap<String, String> map = new HashMap<>();
		String line = "";

		try {
			String fileName = "/Users/haowang/Desktop/CS512YelpRecommender/user_cluster_soft.txt";
			BufferedReader reader = new BufferedReader(new FileReader(fileName));

			while ((line = reader.readLine()) != null) {
				String[] strs = line.split(" ");
				String user_id = strs[0];
				String cluster = "";

				for(int i = 1; i <= 10; i++) {
					if(i != 10) {
						cluster += strs[i] + ",";
					} else {
						cluster += strs[i];
					}
				}

				map.put(user_id, cluster);
			}

		} catch (Exception e) {
			e.printStackTrace();
		}

		return map;
	}
}