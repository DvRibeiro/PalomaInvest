package com.example.palomagem;

import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class IaThesisActivity extends AppCompatActivity {

    private Toolbar toolbar;
    private TextView textViewThesisTitle;
    private TextView textViewIaThesisContent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ia_thesis);

        toolbar = findViewById(R.id.toolbar_ia_thesis);
        setSupportActionBar(toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setTitle("Tese da IA");
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        }

        textViewThesisTitle = findViewById(R.id.textViewThesisTitle);
        textViewIaThesisContent = findViewById(R.id.textViewIaThesisContent);

        String stockTicker = getIntent().getStringExtra("STOCK_TICKER");
        if (stockTicker != null) {
            textViewThesisTitle.setText("Tese de Investimento para " + stockTicker);

            fetchIaThesis(stockTicker);
        } else {
            textViewThesisTitle.setText("Ticker não encontrado");
            textViewIaThesisContent.setText("Não foi possível carregar a tese, pois o ticker da ação não foi fornecido.");
        }
    }

    private void fetchIaThesis(String ticker) {
        textViewIaThesisContent.setText("Gerando tese da IA...");

        double lpaExemplo = 2.5;
        double vpaExemplo = 15.8;

        TeseRequest requestBody = new TeseRequest(lpaExemplo, vpaExemplo);

        ApiService apiService = RetroFitClient.getClient().create(ApiService.class);

        Call<Thesis> call = apiService.getIaThesis(ticker, requestBody);

        call.enqueue(new Callback<Thesis>() {
            @Override
            public void onResponse(Call<Thesis> call, Response<Thesis> response) {
                if (response.isSuccessful() && response.body() != null) {
                    String thesisText = response.body().getThesisText();
                    textViewIaThesisContent.setText(thesisText);
                } else {
                    textViewIaThesisContent.setText("Não foi possível gerar a tese para esta ação. Código: " + response.code());
                }
            }

            @Override
            public void onFailure(Call<Thesis> call, Throwable t) {
                textViewIaThesisContent.setText("Erro de conexão ao gerar a tese: " + t.getMessage());
            }
        });
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}