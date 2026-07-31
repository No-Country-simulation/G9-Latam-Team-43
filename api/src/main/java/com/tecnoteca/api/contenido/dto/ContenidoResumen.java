package com.tecnoteca.api.contenido.dto;

import java.time.Instant;
import java.util.List;

/** Elemento de los listados (GET /contenidos). */
public record ContenidoResumen(long id, String titulo, String categoria,
                               Double probabilidad, List<String> informacionAdicional,
                               String tema, String origen, Instant creadoEn) {}
