package com.example.palomagem;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Locale;

public class StockAdapter extends RecyclerView.Adapter<StockAdapter.StockViewHolder> {

    private final ArrayList<Stock> stockList;
    private final Context context;

    public StockAdapter(Context context, ArrayList<Stock> stockList) {
        this.context = context;
        this.stockList = stockList;
    }

    @NonNull
    @Override
    public StockViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_stock, parent, false);
        return new StockViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull StockViewHolder holder, int position) {
        Stock currentStock = stockList.get(position);

        holder.textViewStockName.setText(currentStock.getName());
        holder.textViewStockTicker.setText(currentStock.getTicker());

        double precoOriginal = currentStock.getPreco();
        double precoCorrigido = precoOriginal / 100.0;

        NumberFormat formatadorMoeda = NumberFormat.getCurrencyInstance(new Locale("pt", "BR"));
        String precoFormatado = formatadorMoeda.format(precoCorrigido);
        holder.textViewStockPrice.setText(precoFormatado);

        holder.itemView.setOnClickListener(v -> {
            Intent intent = new Intent(context, StockDetailActivity.class);
            intent.putExtra("STOCK_OBJECT", currentStock);
            context.startActivity(intent);
        });
    }

    @Override
    public int getItemCount() {
        return stockList.size();
    }

    public static class StockViewHolder extends RecyclerView.ViewHolder {
        TextView textViewStockName;
        TextView textViewStockTicker;
        TextView textViewStockPrice;

        public StockViewHolder(@NonNull View itemView) {
            super(itemView);
            textViewStockName = itemView.findViewById(R.id.textViewStockName);
            textViewStockTicker = itemView.findViewById(R.id.textViewStockTicker);
            textViewStockPrice = itemView.findViewById(R.id.textViewStockPrice);
        }
    }
}