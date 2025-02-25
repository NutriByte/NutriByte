package nutribyte;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import org.jsoup.nodes.Element;

public class NutritionScraper {
    public static void scrapeNutritionData(String url) {
        try {
            Document doc = Jsoup.connect(url)
                              .userAgent("Mozilla/5.0")
                              .timeout(5000)
                              .get();
            
            // Example selectors: Adjust based on the actual website structure
            // For illustration, assuming ".nutrition-facts" contains the data
            Elements nutritionFacts = doc.select(".nutrition-table");  // Adjust this based on actual website structure


            // If the nutrition facts are not found
            if (nutritionFacts.isEmpty()) {
                System.out.println("No nutrition data found on the page.");
            }

            // Loop through the nutrition facts and print each one
            for (Element fact : nutritionFacts) {
                String nutrientName = fact.select(".nutrient-name").text();
                String nutrientValue = fact.select(".nutrient-value").text();
                String nutrientUnit = fact.select(".nutrient-unit").text();
                
                System.out.printf("%s: %s %s%n", nutrientName, nutrientValue, nutrientUnit);
            }
            
        } catch (Exception e) {
            System.out.println("Error scraping nutrition data: " + e.getMessage());
        }
    }
}
