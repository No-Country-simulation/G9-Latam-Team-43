package com.tecnoteca.api.contenido.dto;

import java.time.Instant;
import java.util.List;

/** Detalle completo de un contenido (GET /contenidos/{id}). */
public record ContenidoDetalle(long id, String titulo, String texto, String categoria,
                               Double probabilidad, List<String> informacionAdicional,
                               String tema, String origen, Instant creadoEn) {}
