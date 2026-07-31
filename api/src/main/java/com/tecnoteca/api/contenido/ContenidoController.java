package com.tecnoteca.api.contenido;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import com.tecnoteca.api.contenido.dto.CategoriaConteo;
import com.tecnoteca.api.contenido.dto.ContenidoDetalle;
import com.tecnoteca.api.contenido.dto.ContenidoResumen;
import com.tecnoteca.api.contenido.dto.EntradaContenido;
import com.tecnoteca.api.contenido.dto.RelacionadoDto;
import com.tecnoteca.api.contenido.dto.RespuestaContenido;
import com.tecnoteca.api.contenido.dto.RespuestaLote;
import com.tecnoteca.api.contenido.dto.ResultadoBusqueda;
import com.tecnoteca.api.modelo.ClienteModelo;
import jakarta.validation.Valid;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class ContenidoController {

    private final ContenidoService servicio;
    private final ClienteModelo clienteModelo;

    public ContenidoController(ContenidoService servicio, ClienteModelo clienteModelo) {
        this.servicio = servicio;
        this.clienteModelo = clienteModelo;
    }

    /** Endpoint principal del MVP: analiza (y por defecto guarda) un contenido. */
    @PostMapping("/contenido")
    public RespuestaContenido analizar(@Valid @RequestBody EntradaContenido entrada) {
        return servicio.analizar(entrada);
    }

    /** Procesamiento por lotes: CSV con columnas titulo y texto (máx. 200 filas). */
    @PostMapping(value = "/contenido/lote", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public RespuestaLote lote(@RequestParam("archivo") MultipartFile archivo,
                              @RequestParam(name = "guardar", defaultValue = "true") boolean guardar) {
        return servicio.lote(archivo, guardar);
    }

    @GetMapping("/contenidos")
    public List<ContenidoResumen> listar(
            @RequestParam(required = false) String categoria,
            @RequestParam(defaultValue = "20") int limite) {
        return servicio.listar(categoria, limite);
    }

    @GetMapping("/contenidos/{id}")
    public ContenidoDetalle obtener(@PathVariable long id) {
        return servicio.obtener(id);
    }

    @GetMapping("/contenidos/{id}/relacionados")
    public List<RelacionadoDto> relacionados(@PathVariable long id,
                                             @RequestParam(defaultValue = "3") int k) {
        return servicio.relacionados(id, k);
    }

    /** Búsqueda semántica sobre la base de conocimiento. */
    @GetMapping("/buscar")
    public List<ResultadoBusqueda> buscar(
            @RequestParam String q,
            @RequestParam(required = false) String categoria,
            @RequestParam(defaultValue = "5") int k) {
        if (q == null || q.trim().length() < 2) {
            throw new IllegalArgumentException(
                    "El parámetro 'q' debe tener al menos 2 caracteres");
        }
        return servicio.buscar(q.trim(), categoria, k);
    }

    @GetMapping("/categorias")
    public List<CategoriaConteo> categorias() {
        return servicio.categorias();
    }

    @GetMapping("/salud")
    public Map<String, Object> salud() {
        Map<String, Object> respuesta = new LinkedHashMap<>();
        respuesta.put("estado", "ok");
        respuesta.put("servicio", "tecnoteca-api");
        respuesta.put("contenidos", servicio.total());
        try {
            respuesta.put("modelo", clienteModelo.salud());
        } catch (Exception e) {
            respuesta.put("modelo", Map.of("estado", "inaccesible"));
        }
        return respuesta;
    }
}
