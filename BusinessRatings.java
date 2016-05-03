public class BusinessRatings {
	String category;
	double rating;

	public BusinessRatings(String category, double rating) {
		this.category = category;
		this.rating = rating;
	}

	@Override
	public String toString() {
		return this.category + ":" + this.rating;
	}
}
