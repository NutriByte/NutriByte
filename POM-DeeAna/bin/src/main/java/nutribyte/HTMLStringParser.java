package nutribyte;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class HTMLStringParser {
    public static void parseHTMLString() {
        String html = "<html><body><p>Banana</p></body></html>";
        Document doc = Jsoup.parse(html);
        
        // Example of extracting text from the HTML string
        System.out.println("Parsed HTML: " + doc.body().text());
    }
}
