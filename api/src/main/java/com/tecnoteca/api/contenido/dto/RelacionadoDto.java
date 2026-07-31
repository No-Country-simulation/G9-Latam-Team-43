package com.tecnoteca.api.contenido.dto;

/** Contenido relacionado, con su similitud coseno respecto al consultado. */
public record RelacionadoDto(long id, String titulo, String categoria, double similitud) {}
