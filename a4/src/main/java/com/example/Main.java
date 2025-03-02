package com.example;

import retrofit2.*;
import java.io.IOException;
import java.util.List;

//This should call the /products endpoint, 
//convert the JSON response to a List<Product>,
// and print out the product name and price
// and if possible will try to add nutritional values/info

// I chose Retrofit since it was easier to use and supports asynch requests
// However, it only works with REST APIs(mainly JSON-based)
// Though it's not as flexible as the other option I was considering (HttpClient)

//HttpClient is more flexible working with any HTTP requests
// it supports all data formats and better for handling file uploads, streaming, and raw HTTP calls
// Its downsides include: manually parsing JSON/XML responses and harder to manage asynch requests

//Both of these can fetch catalog data from an online store

public class Main 
{
    public static void main( String[] args )
    {
        CatalogApi api = CatalogService.getRetrofitInstance().create(CatalogApi.class);

        //Make the API request
        Call<List<Product>> call = api.getProducts();

        try{
            Response<List<Product>> response = call.execute(); //Synchronous call
            if (response.isSuccessful()) {
                List<Product> products = response.body();
                assert products != null;
                for(Product product : products){
                    System.out.println(product);
                }
            } else{
                System.out.println("API Error: " + response.code());
            }
        } catch (IOException e){
            e.printStackTrace();
        }

    }
}
