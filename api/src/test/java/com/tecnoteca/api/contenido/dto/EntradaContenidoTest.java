package com.tecnoteca.api.contenido.dto;

import java.util.Set;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

class EntradaContenidoTest {

    private static final Validator VALIDADOR =
            Validation.buildDefaultValidatorFactory().getValidator();

    @Test
    void aceptaEntradaValida() {
        EntradaContenido entrada = new EntradaContenido("Introducción a Spring Boot",
                "En este contenido se presentan los conceptos básicos para crear APIs REST.",
                null);
        assertTrue(VALIDADOR.validate(entrada).isEmpty());
        assertTrue(entrada.debeGuardar());
    }

    @Test
    void rechazaTextoDemasiadoCorto() {
        EntradaContenido entrada = new EntradaContenido("Título válido", "corto", true);
        Set<ConstraintViolation<EntradaContenido>> violaciones = VALIDADOR.validate(entrada);
        assertTrue(violaciones.stream()
                .anyMatch(v -> v.getPropertyPath().toString().equals("texto")));
    }

    @Test
    void rechazaTituloEnBlanco() {
        EntradaContenido entrada = new EntradaContenido("   ",
                "Un texto suficientemente largo para pasar la validación de tamaño.", false);
        assertTrue(VALIDADOR.validate(entrada).stream()
                .anyMatch(v -> v.getPropertyPath().toString().equals("titulo")));
    }
}
