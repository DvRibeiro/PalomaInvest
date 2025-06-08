package com.example.palomagem;

import com.google.gson.annotations.SerializedName;

public class Thesis {

    @SerializedName("ticker")
    private String ticker;

    @SerializedName("tese")
    private String thesisText;

    @SerializedName("vi")
    private String vi;

    // Getters
    public String getTicker() {
        return ticker;
    }

    public String getThesisText() {
        return thesisText;
    }

    public String getVi() { return vi; }
}