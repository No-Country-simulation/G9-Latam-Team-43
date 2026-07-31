package com.tecnoteca.api.errores;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;

import com.tecnoteca.api.modelo.ServicioModeloException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.multipart.support.MissingServletRequestPartException;

/** Todas las respuestas de error de la API en un JSON consistente y en español. */
@RestControllerAdvice
public class ManejadorErrores {

    private static final Logger log = LoggerFactory.getLogger(ManejadorErrores.class);

    record Detalle(String campo, String mensaje) {}

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> entradaInvalida(MethodArgumentNotValidException e) {
        List<Detalle> detalles = e.getBindingResult().getFieldErrors().stream()
                .map(err -> new Detalle(err.getField(), err.getDefaultMessage()))
                .toList();
        return respuesta(HttpStatus.BAD_REQUEST, "Entrada inválida", detalles);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<Map<String, Object>> jsonInvalido(HttpMessageNotReadableException e) {
        return respuesta(HttpStatus.BAD_REQUEST,
                "El cuerpo de la petición no es un JSON válido", null);
    }

    @ExceptionHandler({MissingServletRequestParameterException.class,
            MethodArgumentTypeMismatchException.class})
    public ResponseEntity<Map<String, Object>> parametroInvalido(Exception e) {
        return respuesta(HttpStatus.BAD_REQUEST,
                "Parámetro de la petición faltante o inválido", null);
    }

    @ExceptionHandler(MissingServletRequestPartException.class)
    public ResponseEntity<Map<String, Object>> faltaArchivo(MissingServletRequestPartException e) {
        return respuesta(HttpStatus.BAD_REQUEST,
                "Falta el archivo CSV (campo multipart 'archivo')", null);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Map<String, Object>> peticionInvalida(IllegalArgumentException e) {
        return respuesta(HttpStatus.BAD_REQUEST, e.getMessage(), null);
    }

    @ExceptionHandler(NoSuchElementException.class)
    public ResponseEntity<Map<String, Object>> noEncontrado(NoSuchElementException e) {
        return respuesta(HttpStatus.NOT_FOUND, e.getMessage(), null);
    }

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public ResponseEntity<Map<String, Object>> archivoMuyGrande(MaxUploadSizeExceededException e) {
        return respuesta(HttpStatus.PAYLOAD_TOO_LARGE,
                "El archivo supera el tamaño máximo permitido (5 MB)", null);
    }

    @ExceptionHandler(ServicioModeloException.class)
    public ResponseEntity<Map<String, Object>> modeloCaido(ServicioModeloException e) {
        log.warn("Servicio de modelo no disponible: {}", e.getMessage());
        return respuesta(HttpStatus.SERVICE_UNAVAILABLE, e.getMessage(), null);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> errorInterno(Exception e) {
        log.error("Error no controlado", e);
        return respuesta(HttpStatus.INTERNAL_SERVER_ERROR, "Error interno del servidor", null);
    }

    private ResponseEntity<Map<String, Object>> respuesta(HttpStatus estado, String error,
                                                          List<Detalle> detalles) {
        Map<String, Object> cuerpo = new LinkedHashMap<>();
        cuerpo.put("error", error);
        if (detalles != null && !detalles.isEmpty()) {
            cuerpo.put("detalles", detalles);
        }
        return ResponseEntity.status(estado).body(cuerpo);
    }
}
