package nutribyte;

public class Main {
    public static void main(String[] args) {
        System.out.println("Testing HTML Parser:");
        HTMLParser.parseWebPage();
        
        System.out.println("\nTesting HTML String Parser:");
        HTMLStringParser.parseHTMLString();
        
        System.out.println("\nTesting Nutrition Scraper:");
        // Replace with an actual nutrition website URL
        NutritionScraper.scrapeNutritionData("https://www.nutritionvalue.org/");

    }
}
