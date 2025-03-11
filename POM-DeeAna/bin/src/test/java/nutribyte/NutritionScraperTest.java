package nutribyte;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class NutritionScraperTest {

    @Test
    public void testGetIngredients() {
        // Sample HTML content (replace with a realistic mock of the page)
        String html = "<html><body><ul class='ingredients-list'>" +
                "<li>1 tablespoon vegetable oil</li>" +
                "<li>2 chicken breasts</li>" +
                "<li>1 can cream of chicken soup</li>" +
                "</ul></body></html>";

        Document doc = Jsoup.parse(html);
        NutritionScraper scraper = new NutritionScraper();  // Create an instance of NutritionScraper
        String ingredients = scraper.getIngredients(doc);  // Call the method on the instance

        // Verify the ingredients list
        assertEquals("1 tablespoon vegetable oil\n2 chicken breasts\n1 can cream of chicken soup\n", ingredients);
    }

    @Test
    public void testGetNutritionInfo() {
        // Sample HTML content (replace with a realistic mock of the page)
        String html = "<html><body><table class='nutrition-table'>" +
                "<tr><td class='nutrient-name'>Total Calories</td><td class='nutrient-value'>154</td></tr>" +
                "<tr><td class='nutrient-name'>Total Fat</td><td class='nutrient-value'>7 g</td></tr>" +
                "</table></body></html>";

        Document doc = Jsoup.parse(html);
        NutritionScraper scraper = new NutritionScraper();  // Create an instance of NutritionScraper
        String nutritionInfo = scraper.getNutritionInfo(doc);  // Call the method on the instance

        // Verify the nutrition information
        assertEquals("Total Calories: 154\nTotal Fat: 7 g\n", nutritionInfo);
    }

    @Test
    public void testGetNutritionInfo_NoData() {
        // HTML with no nutrition data
        String html = "<html><body><table class='nutrition-table'></table></body></html>";

        Document doc = Jsoup.parse(html);
        NutritionScraper scraper = new NutritionScraper();  // Create an instance of NutritionScraper
        String nutritionInfo = scraper.getNutritionInfo(doc);  // Call the method on the instance

        // Verify that no nutrition data is found
        assertEquals("No nutrition data found!", nutritionInfo);
    }

    @Test
    public void testGetNutritionInfo_InvalidHTML() {
        // HTML with an invalid structure for nutrition info
        String html = "<html><body><div class='nutrition-data'>" +
                "<p>Some invalid nutrition data</p>" +
                "</div></body></html>";

        Document doc = Jsoup.parse(html);
        NutritionScraper scraper = new NutritionScraper();  // Create an instance of NutritionScraper
        String nutritionInfo = scraper.getNutritionInfo(doc);  // Call the method on the instance

        // Verify that no nutrition data is found
        assertEquals("No nutrition data found!", nutritionInfo);
    }
}
