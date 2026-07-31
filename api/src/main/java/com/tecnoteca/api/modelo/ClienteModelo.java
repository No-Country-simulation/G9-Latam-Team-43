package com.tecnoteca.api.modelo;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientResponseException;

/**
 * Cliente HTTP hacia el servicio de modelo del equipo de ciencia de datos.
 * Toda la comunicación es JSON en snake_case (configurado en application.properties).
 */
@Component
public class ClienteModelo {

    private final RestClient http;

    public ClienteModelo(RestClient.Builder builder,
                         @Value("${tecnoteca.modelo.url}") String urlModelo) {
        this.http = builder.baseUrl(urlModelo).build();
    }

    // ── Contratos JSON con el servicio de modelo ──
    public record TemaModelo(Integer id, String etiqueta) {}
    public record TerminoPeso(String termino, Double peso) {}
    public record AnalisisModelo(String categoria, Double probabilidad,
                                 Map<String, Double> distribucion,
                                 List<String> palabrasClave, TemaModelo tema,
                                 List<TerminoPeso> explicacion) {}
    public record SimilarModelo(Long id, Double similitud) {}
    public record DocumentoIndice(Long id, String titulo, String texto, String categoria) {}
    public record SaludModelo(String estado, Boolean modeloCargado, String versionModelo,
                              List<String> categorias, Integer documentosIndexados,
                              Map<String, Object> oci) {}

    private record PeticionAnalisis(String titulo, String texto) {}
    private record PeticionSimilares(String texto, int k, Long excluirId, String categoria) {}
    private record PeticionBusqueda(String consulta, int k, String categoria) {}
    private record PeticionReindexar(List<DocumentoIndice> documentos) {}
    private record RespuestaSimilares(List<SimilarModelo> resultados) {}

    public AnalisisModelo analizar(String titulo, String texto) {
        return post("/analizar", new PeticionAnalisis(titulo, texto), AnalisisModelo.class);
    }

    public void indexar(long id, String titulo, String texto, String categoria) {
        post("/indexar", new DocumentoIndice(id, titulo, texto, categoria), Map.class);
    }

    public int reindexar(List<DocumentoIndice> documentos) {
        Map<?, ?> respuesta = post("/reindexar", new PeticionReindexar(documentos), Map.class);
        Object indexados = respuesta.get("indexados");
        return indexados instanceof Number n ? n.intValue() : 0;
    }

    public List<SimilarModelo> similares(String texto, Long excluirId, int k) {
        return post("/similares", new PeticionSimilares(texto, k, excluirId, null),
                RespuestaSimilares.class).resultados();
    }

    public List<SimilarModelo> buscar(String consulta, String categoria, int k) {
        return post("/buscar", new PeticionBusqueda(consulta, k, categoria),
                RespuestaSimilares.class).resultados();
    }

    public SaludModelo salud() {
        try {
            return http.get().uri("/salud").retrieve().body(SaludModelo.class);
        } catch (RestClientResponseException | ResourceAccessException e) {
            throw new ServicioModeloException("El servicio de modelo no está disponible", e);
        }
    }

    private <T> T post(String ruta, Object cuerpo, Class<T> tipoRespuesta) {
        try {
            return http.post().uri(ruta)
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(cuerpo)
                    .retrieve()
                    .body(tipoRespuesta);
        } catch (RestClientResponseException e) {
            throw new ServicioModeloException(
                    "El servicio de modelo respondió con error " + e.getStatusCode(), e);
        } catch (ResourceAccessException e) {
            throw new ServicioModeloException(
                    "No fue posible comunicarse con el servicio de modelo", e);
        }
    }
}
