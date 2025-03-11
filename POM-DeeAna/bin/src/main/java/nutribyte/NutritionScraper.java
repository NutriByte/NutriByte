package nutribyte;

import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class NutritionScraper {

    public String getIngredients(Document doc) {
        StringBuilder ingredients = new StringBuilder();
        Elements ingredientItems = doc.select(".ingredients-list li");
        for (Element item : ingredientItems) {
            ingredients.append(item.text()).append("\n");
        }
        return ingredients.toString();
    }

    public String getNutritionInfo(Document doc) {
        StringBuilder nutritionInfo = new StringBuilder();
        Elements rows = doc.select(".nutrition-table tr");

        if (rows.isEmpty()) {
            return "No nutrition data found!";
        }

        for (Element row : rows) {
            String nutrient = row.select(".nutrient-name").text();
            String value = row.select(".nutrient-value").text();
            if (!nutrient.isEmpty() && !value.isEmpty()) {
                nutritionInfo.append(nutrient).append(": ").append(value).append("\n");
            }
        }

        return nutritionInfo.length() > 0 ? nutritionInfo.toString() : "No nutrition data found!";
    }
}
