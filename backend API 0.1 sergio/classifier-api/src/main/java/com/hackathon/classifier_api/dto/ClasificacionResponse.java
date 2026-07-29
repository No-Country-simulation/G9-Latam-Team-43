package com.hackathon.classifier_api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class ClasificacionResponse {

    private String categoria;
    private double probabilidad;

    @JsonProperty("informacion_adicional")
    private List<String> informacionAdicional;

    public ClasificacionResponse() {
    }

    public ClasificacionResponse(String categoria, double probabilidad, List<String> informacionAdicional) {
        this.categoria = categoria;
        this.probabilidad = probabilidad;
        this.informacionAdicional = informacionAdicional;
    }

    public String getCategoria() {
        return categoria;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    public double getProbabilidad() {
        return probabilidad;
    }

    public void setProbabilidad(double probabilidad) {
        this.probabilidad = probabilidad;
    }

    public List<String> getInformacionAdicional() {
        return informacionAdicional;
    }

    public void setInformacionAdicional(List<String> informacionAdicional) {
        this.informacionAdicional = informacionAdicional;
    }
}