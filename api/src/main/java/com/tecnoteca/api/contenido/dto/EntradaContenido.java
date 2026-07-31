package com.tecnoteca.api.contenido.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Cuerpo de POST /contenido. Si {@code guardar} es nulo se asume {@code true}. */
public record EntradaContenido(
        @NotBlank(message = "El título es obligatorio")
        @Size(min = 3, max = 300, message = "El título debe tener entre 3 y 300 caracteres")
        String titulo,

        @NotBlank(message = "El texto es obligatorio")
        @Size(min = 20, max = 50_000, message = "El texto debe tener entre 20 y 50000 caracteres")
        String texto,

        Boolean guardar) {

    public boolean debeGuardar() {
        return guardar == null || guardar;
    }
}
