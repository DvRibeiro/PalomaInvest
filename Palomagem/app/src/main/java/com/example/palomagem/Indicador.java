package com.example.palomagem;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class Indicador implements Serializable {
    @SerializedName("nome")
    public String nome;

    @SerializedName("valor")
    public double valor;
}