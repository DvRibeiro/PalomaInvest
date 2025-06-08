package com.example.palomagem;

import java.util.List;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface ApiService {

    @GET("detalhes/")
    Call<List<Stock>> getStocks();

    @POST("api/gerarTese/{ticker}")
    Call<Thesis> getIaThesis(@Path("ticker") String ticker, @Body TeseRequest body);
}