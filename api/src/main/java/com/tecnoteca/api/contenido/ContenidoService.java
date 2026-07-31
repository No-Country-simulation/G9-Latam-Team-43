package com.tecnoteca.api.contenido;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.TreeSet;
import java.util.function.Function;
import java.util.stream.Collectors;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tecnoteca.api.contenido.dto.CategoriaConteo;
import com.tecnoteca.api.contenido.dto.ContenidoDetalle;
import com.tecnoteca.api.contenido.dto.ContenidoResumen;
import com.tecnoteca.api.contenido.dto.EntradaContenido;
import com.tecnoteca.api.contenido.dto.RelacionadoDto;
import com.tecnoteca.api.contenido.dto.RespuestaContenido;
import com.tecnoteca.api.contenido.dto.RespuestaLote;
import com.tecnoteca.api.contenido.dto.ResultadoBusqueda;
import com.tecnoteca.api.modelo.ClienteModelo;
import com.tecnoteca.api.modelo.ClienteModelo.AnalisisModelo;
import com.tecnoteca.api.modelo.ClienteModelo.SimilarModelo;
import com.tecnoteca.api.modelo.ServicioModeloException;
import com.tecnoteca.api.util.LectorCsv;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/** Orquesta el flujo entre la API pública, el servicio de modelo y la base de datos. */
@Service
public class ContenidoService {

    private final ContenidoRepository repositorio;
    private final ClienteModelo clienteModelo;
    private final ObjectMapper json;

    public ContenidoService(ContenidoRepository repositorio, ClienteModelo clienteModelo,
                            ObjectMapper json) {
        this.repositorio = repositorio;
        this.clienteModelo = clienteModelo;
        this.json = json;
    }

    public RespuestaContenido analizar(EntradaContenido entrada) {
        AnalisisModelo analisis = clienteModelo.analizar(entrada.titulo(), entrada.texto());
        Long id = null;
        if (entrada.debeGuardar()) {
            id = guardar(entrada.titulo(), entrada.texto(), analisis, "api").getId();
        }
        List<RelacionadoDto> relacionados =
                relacionadosDeTexto(entrada.titulo() + ". " + entrada.texto(), id, 3);
        return new RespuestaContenido(id, analisis.categoria(), analisis.probabilidad(),
                analisis.palabrasClave(), analisis.tema(), analisis.explicacion(),
                analisis.distribucion(), relacionados);
    }

    /** Guarda el contenido ya analizado y lo agrega al índice de similitud. */
    public Contenido guardar(String titulo, String texto, AnalisisModelo analisis,
                             String origen) {
        Contenido contenido = new Contenido();
        contenido.setTitulo(titulo);
        contenido.setTexto(texto);
        contenido.setCategoria(analisis.categoria());
        contenido.setProbabilidad(analisis.probabilidad());
        contenido.setPalabrasClave(aJson(analisis.palabrasClave()));
        contenido.setTema(analisis.tema() != null ? analisis.tema().etiqueta() : null);
        contenido.setOrigen(origen);
        Contenido guardado = repositorio.save(contenido);
        clienteModelo.indexar(guardado.getId(), titulo, texto, analisis.categoria());
        return guardado;
    }

    public List<ContenidoResumen> listar(String categoria, int limite) {
        Pageable paginacion = PageRequest.of(0, acotar(limite, 1, 100),
                Sort.by(Sort.Direction.DESC, "creadoEn"));
        List<Contenido> contenidos = (categoria == null || categoria.isBlank())
                ? repositorio.findAll(paginacion).getContent()
                : repositorio.findByCategoriaIgnoreCase(categoria.trim(), paginacion);
        return contenidos.stream().map(this::aResumen).toList();
    }

    public ContenidoDetalle obtener(long id) {
        Contenido c = buscarPorId(id);
        return new ContenidoDetalle(c.getId(), c.getTitulo(), c.getTexto(), c.getCategoria(),
                c.getProbabilidad(), deJson(c.getPalabrasClave()), c.getTema(),
                c.getOrigen(), c.getCreadoEn());
    }

    public List<RelacionadoDto> relacionados(long id, int k) {
        Contenido c = buscarPorId(id);
        return relacionadosDeTexto(c.getTitulo() + ". " + c.getTexto(), id, acotar(k, 1, 20));
    }

    public List<ResultadoBusqueda> buscar(String consulta, String categoria, int k) {
        String filtroCategoria = (categoria == null || categoria.isBlank())
                ? null : categoria.trim();
        List<SimilarModelo> similares =
                clienteModelo.buscar(consulta, filtroCategoria, acotar(k, 1, 50));
        Map<Long, Contenido> porId = cargarPorIds(similares);
        return similares.stream()
                .filter(s -> porId.containsKey(s.id()))
                .map(s -> {
                    Contenido c = porId.get(s.id());
                    return new ResultadoBusqueda(c.getId(), c.getTitulo(), c.getCategoria(),
                            s.similitud(), deJson(c.getPalabrasClave()));
                })
                .toList();
    }

    public List<CategoriaConteo> categorias() {
        Map<String, Long> conteos = new HashMap<>();
        repositorio.contarPorCategoria()
                .forEach(c -> conteos.put(c.getCategoria(), c.getCantidad()));
        TreeSet<String> todas = new TreeSet<>(conteos.keySet());
        try {
            todas.addAll(clienteModelo.salud().categorias());
        } catch (ServicioModeloException ignorada) {
            // sin servicio de modelo mostramos solo las categorías ya guardadas
        }
        return todas.stream()
                .map(cat -> new CategoriaConteo(cat, conteos.getOrDefault(cat, 0L)))
                .toList();
    }

    public RespuestaLote lote(MultipartFile archivo, boolean guardar) {
        if (archivo == null || archivo.isEmpty()) {
            throw new IllegalArgumentException("El archivo CSV está vacío");
        }
        List<LectorCsv.Fila> filas;
        try (InputStream entrada = archivo.getInputStream()) {
            filas = LectorCsv.leer(entrada, 200);
        } catch (IOException e) {
            throw new IllegalArgumentException("No fue posible leer el archivo CSV");
        }
        if (filas.isEmpty()) {
            throw new IllegalArgumentException("El CSV no contiene filas con datos");
        }
        List<RespuestaLote.FilaLote> resultados = new ArrayList<>();
        int errores = 0;
        for (LectorCsv.Fila fila : filas) {
            try {
                if (fila.titulo().length() < 3) {
                    throw new IllegalArgumentException("el título es demasiado corto");
                }
                if (fila.texto().length() < 20) {
                    throw new IllegalArgumentException(
                            "el texto es demasiado corto (mínimo 20 caracteres)");
                }
                AnalisisModelo analisis = clienteModelo.analizar(fila.titulo(), fila.texto());
                if (guardar) {
                    guardar(fila.titulo(), fila.texto(), analisis, "lote");
                }
                resultados.add(new RespuestaLote.FilaLote(fila.numero(), fila.titulo(),
                        analisis.categoria(), analisis.probabilidad(), null));
            } catch (ServicioModeloException e) {
                throw e; // sin servicio de modelo no tiene sentido continuar el lote
            } catch (Exception e) {
                errores++;
                resultados.add(new RespuestaLote.FilaLote(fila.numero(), fila.titulo(),
                        null, null, e.getMessage()));
            }
        }
        return new RespuestaLote(resultados.size() - errores, errores, guardar, resultados);
    }

    public long total() {
        return repositorio.count();
    }

    public List<ClienteModelo.DocumentoIndice> todosParaIndice() {
        return repositorio.findAll().stream()
                .map(c -> new ClienteModelo.DocumentoIndice(c.getId(), c.getTitulo(),
                        c.getTexto(), c.getCategoria()))
                .toList();
    }

    // ── auxiliares ──
    private Contenido buscarPorId(long id) {
        return repositorio.findById(id).orElseThrow(
                () -> new NoSuchElementException("No existe el contenido con id " + id));
    }

    private List<RelacionadoDto> relacionadosDeTexto(String texto, Long excluirId, int k) {
        List<SimilarModelo> similares = clienteModelo.similares(texto, excluirId, k);
        Map<Long, Contenido> porId = cargarPorIds(similares);
        return similares.stream()
                .filter(s -> porId.containsKey(s.id()))
                .map(s -> {
                    Contenido c = porId.get(s.id());
                    return new RelacionadoDto(c.getId(), c.getTitulo(), c.getCategoria(),
                            s.similitud());
                })
                .toList();
    }

    private Map<Long, Contenido> cargarPorIds(List<SimilarModelo> similares) {
        List<Long> ids = similares.stream().map(SimilarModelo::id).toList();
        return repositorio.findAllById(ids).stream()
                .collect(Collectors.toMap(Contenido::getId, Function.identity()));
    }

    private ContenidoResumen aResumen(Contenido c) {
        return new ContenidoResumen(c.getId(), c.getTitulo(), c.getCategoria(),
                c.getProbabilidad(), deJson(c.getPalabrasClave()), c.getTema(),
                c.getOrigen(), c.getCreadoEn());
    }

    private String aJson(List<String> valores) {
        try {
            return json.writeValueAsString(valores == null ? List.of() : valores);
        } catch (IOException e) {
            return "[]";
        }
    }

    private List<String> deJson(String valores) {
        if (valores == null || valores.isBlank()) {
            return List.of();
        }
        try {
            return json.readValue(valores, new TypeReference<List<String>>() {});
        } catch (IOException e) {
            return List.of();
        }
    }

    private static int acotar(int valor, int minimo, int maximo) {
        return Math.max(minimo, Math.min(maximo, valor));
    }
}
