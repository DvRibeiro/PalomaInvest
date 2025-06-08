package com.example.palomagem;

import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import io.noties.markwon.Markwon;

public class IaThesisActivity extends AppCompatActivity {

    private Toolbar toolbar;
    private TextView textViewThesisTitle;
    private TextView textViewIaThesisContent;
    private TextView textViewIntrinsicValue;

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
        textViewIntrinsicValue = findViewById(R.id.textViewIntrinsicValue);

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

        double lpa = getIntent().getDoubleExtra("LPA", 0);
        double vpa = getIntent().getDoubleExtra("VPA", 0);

        TeseRequest requestBody = new TeseRequest(lpa, vpa);

        ApiService apiService = RetroFitClient.getClient().create(ApiService.class);

        Call<Thesis> call = apiService.getIaThesis(ticker, requestBody);

        call.enqueue(new Callback<Thesis>() {
            @Override
            public void onResponse(Call<Thesis> call, Response<Thesis> response) {
                if (response.isSuccessful() && response.body() != null) {
                    String thesisText = response.body().getThesisText();
                    String valorIntrinseco = response.body().getVi();

                    if (valorIntrinseco != null && !valorIntrinseco.isEmpty()) {
                        textViewIntrinsicValue.setText("Valor Intrínseco: " + valorIntrinseco);
                    } else {
                        textViewIntrinsicValue.setText("Valor Intrínseco: Não foi possível calcular.");
                    }


                    // Renderizando markdown
                    Markwon markwon = Markwon.create(IaThesisActivity.this);
                    markwon.setMarkdown(textViewIaThesisContent, thesisText != null ? thesisText : "Nenhum conteúdo gerado.");


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