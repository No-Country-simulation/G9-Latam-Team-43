package com.tecnoteca.api.contenido.dto;

import java.util.List;

/** Resultado de GET /buscar, ordenado por similitud descendente. */
public record ResultadoBusqueda(long id, String titulo, String categoria,
                                double similitud, List<String> informacionAdicional) {}
