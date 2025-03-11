package nutribyte;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        String recipeUrl = "https://www.myplate.gov/recipes/2-step-chicken";  // Update with actual recipe URL
        
        try {
            NutritionScraper scraper = new NutritionScraper();
            // Update the method name to the correct one, e.g., getNutritionInfo
            Document doc = Jsoup.connect(recipeUrl).get();
            String nutritionData = scraper.getNutritionInfo(doc);  // Calling the correct method
            
            System.out.println("Nutrition Data: \n" + nutritionData);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
