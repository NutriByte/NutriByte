package com.example;

import retrofit2.*;
import retrofit2.converter.gson.GsonConverterFactory;
import java.io.IOException;
import java.util.List;

public class CatalogService {
    private static final String BASE_URL = "https://api.example.com/"; //Replace with actual API URL

    private final CatalogApi api;

    public CatalogService(CatalogApi api){
        this.api = api;
    }

    //Synchronous method (for simple use cases)
    public List<Product> fetchProductsSync() throws IOException{
        Call<List<Product>> call = api.getProducts();
        Response<List<Product>> response = call.execute();
        if(response.isSuccessful() && response.body() != null){
            return response.body();
        } else{
            throw new IOException("Failed to fetch products: " + response.errorBody());
        }
    }

    //Asynchronous method using Retrofit's enqueue()
    public void fetchProductsAsync(ProductCallback callback){
        api.getProducts().enqueue(new Callback<List<Product>>() {
            @Override
            public void onResponse(Call<List<Product>> call, Response<List<Product>> response){
                if(response.isSuccessful() && response.body() != null){
                    callback.onSuccess(response.body());
                } else{
                    callback.onFailure(new IOException("Failed to fetch products"));
                }
            }

            @Override
            public void onFailure(Call<List<Product>> call, Throwable t){
                callback.onFailure(t);
            }
        });
    }

    // Callback interface for async calls
    public interface ProductCallback{
        void onSuccess(List<Product> products);
        void onFailure(Throwable t);
    }

    public static Retrofit getRetrofitInstance(){
        return new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create()) //Converts JSON to Java objects
            .build();
    }
}
