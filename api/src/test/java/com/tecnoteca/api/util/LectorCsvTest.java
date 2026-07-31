package com.tecnoteca.api.util;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class LectorCsvTest {

    private static ByteArrayInputStream entrada(String contenido) {
        return new ByteArrayInputStream(contenido.getBytes(StandardCharsets.UTF_8));
    }

    @Test
    void leeFilasValidas() throws Exception {
        String csv = "titulo,texto\n"
                + "Curso de Docker,\"Contenedores, imágenes y despliegue.\"\n"
                + "Apuntes de SQL,Consultas con JOIN y agregaciones.\n";
        List<LectorCsv.Fila> filas = LectorCsv.leer(entrada(csv), 10);
        assertEquals(2, filas.size());
        assertEquals("Curso de Docker", filas.get(0).titulo());
        assertEquals("Contenedores, imágenes y despliegue.", filas.get(0).texto());
    }

    @Test
    void toleraBomYMayusculasEnCabeceras() throws Exception {
        String csv = "﻿Titulo,Texto\nHola,Un texto cualquiera de prueba.\n";
        List<LectorCsv.Fila> filas = LectorCsv.leer(entrada(csv), 10);
        assertEquals(1, filas.size());
        assertEquals("Hola", filas.get(0).titulo());
    }

    @Test
    void rechazaCsvSinColumnasRequeridas() {
        String csv = "nombre,descripcion\na,b\n";
        assertThrows(IllegalArgumentException.class, () -> LectorCsv.leer(entrada(csv), 10));
    }

    @Test
    void rechazaCsvConDemasiadasFilas() {
        StringBuilder csv = new StringBuilder("titulo,texto\n");
        for (int i = 0; i < 5; i++) {
            csv.append("t").append(i).append(",un texto de prueba\n");
        }
        assertThrows(IllegalArgumentException.class, () -> LectorCsv.leer(entrada(csv.toString()), 3));
    }
}
