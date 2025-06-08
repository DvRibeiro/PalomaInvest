package com.example.palomagem;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class Periodo implements Serializable {
    @SerializedName("ano")
    public double ano;

    @SerializedName("trimestre")
    public int trimestre;
}