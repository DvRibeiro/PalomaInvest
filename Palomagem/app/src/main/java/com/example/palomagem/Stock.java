package com.example.palomagem;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.List;

public class Stock implements Serializable {

    @SerializedName("codigo_acao")
    private String ticker;

    @SerializedName("nome_empresa")
    private String name;

    @SerializedName("setor")
    private String setor;

    @SerializedName("periodo")
    private Periodo periodo;

    @SerializedName("indicadores")
    private List<Indicador> indicadores;

    // --- GETTERS ---
    public String getTicker() {
        return ticker;
    }

    public String getName() {
        return name;
    }

    public String getSetor() {
        return setor;
    }

    public List<Indicador> getIndicadores() {
        return indicadores;
    }

    public double getPreco() {
        if (indicadores == null) {
            return 0.0;
        }
        for (Indicador i : indicadores) {
            if ("Cotacao".equalsIgnoreCase(i.nome)) {
                return i.valor;
            }
        }
        return 0.0;
    }
}