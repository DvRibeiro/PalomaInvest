package com.example.palomagem;

import com.google.gson.annotations.SerializedName;

public class TeseRequest {

    @SerializedName("lpa")
    private double lpa;

    @SerializedName("vpa")
    private double vpa;

    public TeseRequest(double lpa, double vpa) {
        this.lpa = lpa;
        this.vpa = vpa;
    }
}