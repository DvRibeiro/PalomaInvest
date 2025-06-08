package com.example.palomagem;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import java.util.ArrayList;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class StocksFragment extends Fragment {

    private ArrayList<Stock> stockList = new ArrayList<>();
    private StockAdapter stockAdapter;
    private RecyclerView recyclerViewStocks;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_stocks, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        Log.d("StocksFragmentDebug", "onViewCreated foi chamado. Preparando para buscar API.");

        recyclerViewStocks = view.findViewById(R.id.recyclerViewStocks);
        recyclerViewStocks.setLayoutManager(new LinearLayoutManager(getContext()));
        stockAdapter = new StockAdapter(getContext(), stockList);
        recyclerViewStocks.setAdapter(stockAdapter);

        fetchStocksFromApi();
    }
    private void fetchStocksFromApi() {
        // Pega o nosso cliente Retrofit e cria a implementação da interface ApiService.
        ApiService apiService = RetroFitClient.getClient().create(ApiService.class);
        Call<List<Stock>> call = apiService.getStocks();

        // Executa a chamada de forma assíncrona (em uma thread de fundo).
        call.enqueue(new Callback<List<Stock>>() {
            @Override
            public void onResponse(Call<List<Stock>> call, Response<List<Stock>> response) {
                // 'onResponse' é chamado quando o servidor responde, seja com sucesso ou erro.

                // Verificamos se a resposta foi bem-sucedida (código 2xx) e se o corpo não é nulo.
                if (response.isSuccessful() && response.body() != null) {
                    // Se deu certo, limpamos a lista antiga para não duplicar dados.
                    stockList.clear();
                    // Adicionamos todos os dados recebidos da API na nossa lista.
                    stockList.addAll(response.body());
                    // ESSENCIAL: Avisamos o adapter que os dados mudaram para que ele atualize a tela.
                    stockAdapter.notifyDataSetChanged();
                } else {
                    // Caso o servidor responda com um erro (ex: 404, 500).
                    Toast.makeText(getContext(), "Erro ao carregar a lista de ações.", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Stock>> call, Throwable t) {
                Toast.makeText(getContext(), "Falha na conexão: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

}