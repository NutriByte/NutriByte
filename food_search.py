import requests
import json

def search_food(query):
    """
    Queries the Open Food Facts search API with the given query.
    Returns a list of relevant products (or an empty list if none found).
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': query,
        'json': 1,         # Fetch results in JSON format
        'page_size': 5     # Limit results so we don't get overloaded
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    data = response.json()
    # The 'products' key in the returned JSON typically contains the product list
    products = data.get("products", [])
    return products

def print_product_info(products):
    """
    Prints basic product info like product name, brand, and nutrients (if available).
    """
    if not products:
        print("No products found.")
        return

    for i, product in enumerate(products, start=1):
        product_name = product.get("product_name", "N/A")
        brands = product.get("brands", "N/A")
        nutriments = product.get("nutriments", {})

        # Examples of potential fields (always handle carefully, some might be missing)
        calories = nutriments.get("energy-kcal_100g", "N/A")
        fat = nutriments.get("fat_100g", "N/A")
        carbs = nutriments.get("carbohydrates_100g", "N/A")
        protein = nutriments.get("proteins_100g", "N/A")
        sodium = nutriments.get("sodium_100g", "N/A")

        print(f"\nProduct #{i}")
        print(f"Name: {product_name}")
        print(f"Brand(s): {brands}")
        print(f"Calories per 100g: {calories}")
        print(f"Fat per 100g: {fat}")
        print(f"Carbs per 100g: {carbs}")
        print(f"Protein per 100g: {protein}")
        print(f"Sodium per 100g: {sodium}")

def main():
    print("Welcome to the Open Food Facts search test!")
    user_query = input("Type a food name or keyword to search for: ")
    if not user_query.strip():
        print("Please enter a valid food name.")
        return

    products = search_food(user_query.strip())
    print_product_info(products)

if __name__ == "__main__":
    main()
