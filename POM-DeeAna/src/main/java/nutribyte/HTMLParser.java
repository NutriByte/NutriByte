package nutribyte;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class HTMLParser {
    public static void parseWebPage() {
        try {
            // Change the URL to the one you want to scrape
            Document doc = Jsoup.connect("https://www.nutritionvalue.org/search.php?food_query=banana")
                                .userAgent("Mozilla/5.0")
                                .get();
            
            // Get page title
            String title = doc.title();
            System.out.println("Page Title: " + title);
            
            // Example: Find all links in the page
            Elements links = doc.select("a[href]"); // Find all links
            for (Element link : links) {
                System.out.println("Link: " + link.attr("href"));
                System.out.println("Text: " + link.text());
            }
            
            // You can also select other elements like nutrition facts if present
            // Example: Print all nutrition information if available
            Elements nutritionInfo = doc.select(".nutritionalInfo"); // Adjust this selector according to actual website structure
            for (Element info : nutritionInfo) {
                System.out.println("Nutrient: " + info.text());
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
