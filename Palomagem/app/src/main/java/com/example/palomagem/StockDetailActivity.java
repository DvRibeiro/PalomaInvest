package com.example.palomagem;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout; // Importe o LinearLayout
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import java.text.NumberFormat;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class StockDetailActivity extends AppCompatActivity {

    public static final String EXTRA_TICKER = "STOCK_TICKER";

    private Toolbar toolbar;
    private TextView textViewDetailStockName, textViewDetailStockTicker, textViewDetailPrice;
    private Button buttonGoToThesis;
    private LinearLayout containerIndicadores; // O nosso container para os indicadores

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_stock_detail);

        initializeViews();
        setupToolbar();

        String ticker = getIntent().getStringExtra(StockDetailActivity.EXTRA_TICKER);

        if (ticker != null && !ticker.isEmpty()) {
            fetchStockDetails(ticker);
        } else {
            Toast.makeText(this, "Erro: Ticker da ação não recebido.", Toast.LENGTH_LONG).show();
            finish();
        }
    }

    private void initializeViews() {
        toolbar = findViewById(R.id.toolbar_stock_detail);
        textViewDetailStockName = findViewById(R.id.textViewDetailStockName);
        textViewDetailStockTicker = findViewById(R.id.textViewDetailStockTicker);
        textViewDetailPrice = findViewById(R.id.textViewDetailPrice);
        buttonGoToThesis = findViewById(R.id.buttonGoToThesis);
        // Pegamos a referência do nosso container
        containerIndicadores = findViewById(R.id.containerIndicadores);
    }

    private void setupToolbar() {
        setSupportActionBar(toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("DETALHES DA AÇÃO");
        }
    }

    private void fetchStockDetails(String ticker) {
        textViewDetailStockName.setText("Carregando dados para " + ticker + "...");

        ApiService apiService = RetroFitClient.getClient().create(ApiService.class);
        Call<Stock> call = apiService.getStockByTicker(ticker);

        call.enqueue(new Callback<Stock>() {
            @Override
            public void onResponse(Call<Stock> call, Response<Stock> response) {
                if (response.isSuccessful() && response.body() != null) {
                    populateUI(response.body());
                } else {
                    Toast.makeText(StockDetailActivity.this, "Falha ao carregar detalhes da ação.", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Stock> call, Throwable t) {
                Toast.makeText(StockDetailActivity.this, "Erro de conexão: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void populateUI(Stock stock) {
        LinearLayout containerIndicadores = findViewById(R.id.containerIndicadores);

        // Nome da Ação e Ticker já estão definidos no XML
        TextView textViewDetailStockName = findViewById(R.id.textViewDetailStockName);
        textViewDetailStockName.setText(stock.getName());

        TextView textViewDetailStockTicker = findViewById(R.id.textViewDetailStockTicker);
        textViewDetailStockTicker.setText("TICKER: " + stock.getTicker());

        TextView textViewDetailPrice = findViewById(R.id.textViewDetailPrice);
        textViewDetailPrice.setText("Preço: R$ " + stock.getPreco());

        // Setor e Período
        TextView setorPeriodoView = new TextView(this);
        setorPeriodoView.setText("Empresa: " + stock.getName() +
                "\nSetor: " + stock.getSetor() +
                "\nPeríodo: " + stock.getPeriodo());
        setorPeriodoView.setTextColor(0xFFFFFFFF);
        setorPeriodoView.setTextSize(18);
        setorPeriodoView.setPadding(0, 24, 0, 24);
        containerIndicadores.addView(setorPeriodoView);
        adicionarDivisor(containerIndicadores);

        // Indicadores
        for (Indicador indicador : stock.getIndicadores()) {
            String textoFormatado = formatarIndicador(indicador);
            if (textoFormatado == null) continue;

            TextView indicadorView = new TextView(this);
            indicadorView.setText(textoFormatado);
            indicadorView.setTextColor(0xFFFFFFFF);
            indicadorView.setTextSize(16);
            indicadorView.setPadding(0, 16, 0, 16);

            containerIndicadores.addView(indicadorView);
            adicionarDivisor(containerIndicadores);
        }

        buttonGoToThesis.setOnClickListener(view -> {
            new android.app.AlertDialog.Builder(this)
                    .setTitle("Informar LPA e VPA?")
                    .setMessage("Você gostaria de informar os valores de LPA e VPA manualmente?")
                    .setPositiveButton("Sim", (dialog, which) -> {
                        mostrarDialogoEntradaManual(stock);
                    })
                    .setNegativeButton("Não", (dialog, which) -> {
                        // Vai direto pra próxima tela com valores padrão
                        Intent intent = new Intent(StockDetailActivity.this, IaThesisActivity.class);
                        intent.putExtra(StockDetailActivity.EXTRA_TICKER, stock.getTicker());
                        intent.putExtra("STOCK_PRICE", stock.getPreco());
                        intent.putExtra("LPA", 0.0);
                        intent.putExtra("VPA", 0.0);
                        startActivity(intent);
                    })
                    .show();
        });
    }

    private void mostrarDialogoEntradaManual(Stock stock) {
        // Layout para os campos de entrada
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(50, 40, 50, 10);

        final EditText inputLPA = new EditText(this);
        inputLPA.setHint("Informe o LPA");
        inputLPA.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);
        layout.addView(inputLPA);

        final EditText inputVPA = new EditText(this);
        inputVPA.setHint("Informe o VPA");
        inputVPA.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);
        layout.addView(inputVPA);

        new android.app.AlertDialog.Builder(this)
                .setTitle("Informe os dados")
                .setView(layout)
                .setPositiveButton("OK", (dialog, which) -> {
                    try {
                        double lpa = Double.parseDouble(inputLPA.getText().toString());
                        double vpa = Double.parseDouble(inputVPA.getText().toString());

                        Intent intent = new Intent(StockDetailActivity.this, IaThesisActivity.class);
                        intent.putExtra(StockDetailActivity.EXTRA_TICKER, stock.getTicker());
                        intent.putExtra("STOCK_PRICE", stock.getPreco());
                        intent.putExtra("LPA", lpa);
                        intent.putExtra("VPA", vpa);
                        startActivity(intent);
                    } catch (NumberFormatException e) {
                        Toast.makeText(this, "Valores inválidos. Use apenas números.", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Cancelar", null)
                .show();
    }


    private void adicionarDivisor(LinearLayout container) {
        View divisor = new View(this);
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                1
        );
        params.setMargins(0, 0, 0, 0);
        divisor.setLayoutParams(params);
        divisor.setBackgroundColor(0x55FFFFFF); // branco translúcido
        container.addView(divisor);
    }


    // Método auxiliar para formatar os indicadores
    private String formatarIndicador(Indicador indicador) {
        // Lista de indicadores que são porcentagens
        Set<String> indicadoresPercentuais = new HashSet<>(Arrays.asList("ROE", "ROIC", "Div_Yield", "Marg_Bruta", "Marg_EBIT", "Marg_Liquida", "Cres_Rec_5a"));

        String nomeFormatado = indicador.nome.replace("_", " ");

        if (indicadoresPercentuais.contains(indicador.nome)) {
            return String.format(Locale.forLanguageTag("pt-BR"), "• %s: %.1f%%", nomeFormatado, indicador.valor / 10.0);
        } else if (indicador.nome.equalsIgnoreCase("Cotacao")) {
            // Não exibimos a cotação aqui pois ela já está no campo "Preço"
            return null;
        } else {
            // Formatação para números grandes
            if (Math.abs(indicador.valor) > 1_000_000_000) {
                return String.format(Locale.forLanguageTag("pt-BR"), "• %s: R$ %.2f Bi", nomeFormatado, indicador.valor / 1_000_000_000.0);
            } else if (Math.abs(indicador.valor) > 1_000_000) {
                return String.format(Locale.forLanguageTag("pt-BR"), "• %s: R$ %.2f Mi", nomeFormatado, indicador.valor / 1_000_000.0);
            }
            return String.format(Locale.forLanguageTag("pt-BR"), "• %s: %.2f", nomeFormatado, indicador.valor);
        }
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}