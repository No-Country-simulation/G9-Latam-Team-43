package com.tecnoteca.api.contenido.dto;

import java.util.List;
import java.util.Map;

import com.tecnoteca.api.modelo.ClienteModelo.TemaModelo;
import com.tecnoteca.api.modelo.ClienteModelo.TerminoPeso;

/**
 * Respuesta de POST /contenido. Mantiene los campos del enunciado del
 * hackathon (categoria, probabilidad, informacion_adicional) y los amplía con
 * el tema, la explicación del modelo y los contenidos relacionados.
 */
public record RespuestaContenido(
        Long id,
        String categoria,
        Double probabilidad,
        List<String> informacionAdicional,
        TemaModelo tema,
        List<TerminoPeso> explicacion,
        Map<String, Double> distribucion,
        List<RelacionadoDto> relacionados) {}
