package com.tecnoteca.api.util;

import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

/** Lectura de archivos CSV con columnas {@code titulo} y {@code texto}. */
public final class LectorCsv {

    public record Fila(int numero, String titulo, String texto) {}

    private LectorCsv() {}

    public static List<Fila> leer(InputStream entrada, int maximo) throws IOException {
        String contenido = new String(entrada.readAllBytes(), StandardCharsets.UTF_8);
        if (contenido.startsWith("﻿")) {
            contenido = contenido.substring(1);
        }
        CSVFormat formato = CSVFormat.DEFAULT.builder()
                .setHeader()
                .setSkipHeaderRecord(true)
                .setTrim(true)
                .setIgnoreEmptyLines(true)
                .build();
        try (CSVParser analizador = CSVParser.parse(new StringReader(contenido), formato)) {
            String columnaTitulo = null;
            String columnaTexto = null;
            for (String nombre : analizador.getHeaderNames()) {
                if (nombre.trim().equalsIgnoreCase("titulo")) {
                    columnaTitulo = nombre;
                } else if (nombre.trim().equalsIgnoreCase("texto")) {
                    columnaTexto = nombre;
                }
            }
            if (columnaTitulo == null || columnaTexto == null) {
                throw new IllegalArgumentException(
                        "El CSV debe incluir las columnas 'titulo' y 'texto'");
            }
            List<Fila> filas = new ArrayList<>();
            for (CSVRecord registro : analizador) {
                String titulo = registro.get(columnaTitulo).trim();
                String texto = registro.get(columnaTexto).trim();
                if (titulo.isEmpty() && texto.isEmpty()) {
                    continue;
                }
                filas.add(new Fila((int) registro.getRecordNumber(), titulo, texto));
                if (filas.size() > maximo) {
                    throw new IllegalArgumentException(
                            "El CSV supera el máximo de " + maximo + " filas");
                }
            }
            return filas;
        }
    }
}
