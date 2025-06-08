package com.example.palomagem;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import java.text.NumberFormat;
import java.util.Locale;

public class StockDetailActivity extends AppCompatActivity {

    private Toolbar toolbar;
    private TextView textViewDetailStockName, textViewDetailStockTicker, textViewDetailPrice;
    private TextView textViewDetailSetor, textViewDetailPL, textViewDetailROE; // Novos TextViews
    private ImageView imageViewStockChart;
    private TextView textViewDetailDescription;
    private Button buttonGoToThesis;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_stock_detail);

        toolbar = findViewById(R.id.toolbar_stock_detail);
        setSupportActionBar(toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("DETALHES DA AÇÃO");
        }
        textViewDetailStockName = findViewById(R.id.textViewDetailStockName);
        textViewDetailStockTicker = findViewById(R.id.textViewDetailStockTicker);
        textViewDetailPrice = findViewById(R.id.textViewDetailPrice);
        textViewDetailSetor = findViewById(R.id.textViewDetailSetor);
        textViewDetailPL = findViewById(R.id.textViewDetailPL);
        textViewDetailROE = findViewById(R.id.textViewDetailROE);
        textViewDetailDescription = findViewById(R.id.textViewDetailDescription);
        buttonGoToThesis = findViewById(R.id.buttonGoToThesis);

        // 1. Recebe o OBJETO Stock inteiro da Intent
        Stock stock = (Stock) getIntent().getSerializableExtra("STOCK_OBJECT");

        // 2. Verifica se o objeto não é nulo antes de usar
        if (stock != null) {
            // --- Popula todos os campos com os dados do objeto ---
            textViewDetailStockName.setText(stock.getName());
            textViewDetailStockTicker.setText("TICKER: " + stock.getTicker());

            // Formata o preço
            double precoCorrigido = stock.getPreco() / 100.0;
            NumberFormat formatadorMoeda = NumberFormat.getCurrencyInstance(new Locale("pt", "BR"));
            textViewDetailPrice.setText("Preço: " + formatadorMoeda.format(precoCorrigido));

            // Popula os novos campos
            textViewDetailSetor.setText("Setor: " + stock.getSetor());

            // Loop para encontrar e exibir indicadores específicos da lista
            if (stock.getIndicadores() != null) {
                for (Indicador indicador : stock.getIndicadores()) {
                    if ("PL".equalsIgnoreCase(indicador.nome)) {
                        textViewDetailPL.setText("P/L: " + indicador.valor);
                    }
                    if ("ROE".equalsIgnoreCase(indicador.nome)) {
                        textViewDetailROE.setText(String.format(Locale.forLanguageTag("pt-BR"), "ROE: %.1f%%", indicador.valor / 10.0));
                    }
                }
            }

            buttonGoToThesis.setOnClickListener(view -> {
                Intent intent = new Intent(StockDetailActivity.this, IaThesisActivity.class);
                intent.putExtra("STOCK_TICKER", stock.getTicker());
                intent.putExtra("STOCK_PRICE", precoCorrigido);
                startActivity(intent);
            });
        }
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}