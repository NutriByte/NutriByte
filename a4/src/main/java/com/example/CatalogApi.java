package com.example;

import retrofit2.*;
import retrofit2.http.GET;

import java.util.List;

public interface CatalogApi {
    @GET("products") //Replace with actual API path
    Call<List<Product>> getProducts();
}
