package com.hackathon.classifier_api.exception;

public class ModeloNoDisponibleException extends RuntimeException {

    public ModeloNoDisponibleException(String mensaje) {
        super(mensaje);
    }
}