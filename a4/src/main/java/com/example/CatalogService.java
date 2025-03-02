package com.example;

import retrofit2.*;
import retrofit2.converter.gson.GsonConverterFactory;

public class CatalogService {
    private static final String BASE_URL = "https://api.example.com/"; //Replace with actual API URL

    public static Retrofit getRetrofitInstance(){
        return new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create()) //Converts JSON to Java objects
            .build();
    }
}
