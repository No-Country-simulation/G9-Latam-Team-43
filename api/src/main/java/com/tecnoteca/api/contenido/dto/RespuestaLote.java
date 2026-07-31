package com.tecnoteca.api.contenido.dto;

import java.util.List;

/** Resumen del procesamiento por lotes de un CSV (POST /contenido/lote). */
public record RespuestaLote(int procesados, int errores, boolean guardado,
                            List<FilaLote> resultados) {

    /** Resultado de una fila del CSV; {@code error} es nulo cuando salió bien. */
    public record FilaLote(int fila, String titulo, String categoria,
                           Double probabilidad, String error) {}
}
