package com.example;

import static org.mockito.Mockito.*;
import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import retrofit2.Call;
import retrofit2.Response;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class CatalogServiceTest {
    private CatalogApi mockApi;
    private CatalogService service;

    @Before
    public void setUp() {
        // Create a mock instance of CatalogApi
        mockApi = Mockito.mock(CatalogApi.class);
        service = new CatalogService(mockApi);
    }

    @Test
    public void testFetchProducts_Success() throws IOException {
        // Fake product list
        List<Product> fakeProducts = Arrays.asList(
            new Product("Apple", 2.99),
            new Product("Banana", 1.49)
        );

        // Mock API response
        Call<List<Product>> mockCall = mock(Call.class);
        when(mockCall.execute()).thenReturn(Response.success(fakeProducts));
        when(mockApi.getProducts()).thenReturn(mockCall);

        // Call the method
        List<Product> products = service.fetchProducts();
        
        // Assertions
        assertNotNull(products);
        assertEquals(2, products.size());
        assertEquals("Apple", products.get(0).getName());
        assertEquals(2.99, products.get(0).getPrice(), 0.01);

        // Verify API interaction
        verify(mockApi, times(1)).getProducts();
    }

    @Test
    public void testFetchProducts_EmptyList() throws IOException {
        // Mock API returning an empty list
        Call<List<Product>> mockCall = mock(Call.class);
        when(mockCall.execute()).thenReturn(Response.success(Collections.emptyList()));
        when(mockApi.getProducts()).thenReturn(mockCall);

        // Call the method
        List<Product> products = service.fetchProducts();
        
        // Assertions
        assertNotNull(products);
        assertEquals(0, products.size());

        // Verify API interaction
        verify(mockApi, times(1)).getProducts();
    }

    @Test
    public void testFetchProducts_ApiFailure() throws IOException {
        // Mock API returning a 500 error
        Call<List<Product>> mockCall = mock(Call.class);
        when(mockCall.execute()).thenReturn(Response.error(500, okhttp3.ResponseBody.create(null, "")));
        when(mockApi.getProducts()).thenReturn(mockCall);

        // Call the method
        List<Product> products = service.fetchProducts();
        
        // Assertions
        assertNull(products);  // Expecting null due to API failure

        // Verify API interaction
        verify(mockApi, times(1)).getProducts();
    }

    @Test
    public void testFetchProducts_NetworkException() throws IOException {
        // Mock API throwing an IOException
        Call<List<Product>> mockCall = mock(Call.class);
        when(mockCall.execute()).thenThrow(new IOException("Network error"));
        when(mockApi.getProducts()).thenReturn(mockCall);

        // Call the method
        List<Product> products = null;
        try {
            products = service.fetchProducts();
        } catch (IOException e) {
            assertEquals("Network error", e.getMessage());
        }

        // Assertions
        assertNull(products);  // Expecting null because of IOException

        // Verify API interaction
        verify(mockApi, times(1)).getProducts();
    }

    @Test
    public void testFetchProducts_NullResponse() throws IOException {
        // Mock API returning a response with a null body
        Call<List<Product>> mockCall = mock(Call.class);
        when(mockCall.execute()).thenReturn(Response.success(null));
        when(mockApi.getProducts()).thenReturn(mockCall);

        // Call the method
        List<Product> products = service.fetchProducts();
        
        // Assertions
        assertNull(products);  // Expecting null because response body is null

        // Verify API interaction
        verify(mockApi, times(1)).getProducts();
    }
}
