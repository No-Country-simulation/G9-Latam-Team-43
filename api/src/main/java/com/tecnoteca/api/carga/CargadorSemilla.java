package com.tecnoteca.api.carga;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;

import com.tecnoteca.api.contenido.ContenidoService;
import com.tecnoteca.api.modelo.ClienteModelo;
import com.tecnoteca.api.util.LectorCsv;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

/**
 * Al arrancar: espera al servicio de modelo, puebla la base de conocimiento con
 * la semilla (solo si la base está vacía) y sincroniza el índice de similitud.
 */
@Component
public class CargadorSemilla implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(CargadorSemilla.class);

    private final ClienteModelo clienteModelo;
    private final ContenidoService servicio;
    private final String rutaSemilla;

    public CargadorSemilla(ClienteModelo clienteModelo, ContenidoService servicio,
                           @Value("${tecnoteca.semilla.ruta}") String rutaSemilla) {
        this.clienteModelo = clienteModelo;
        this.servicio = servicio;
        this.rutaSemilla = rutaSemilla;
    }

    @Override
    public void run(ApplicationArguments args) {
        if (!esperarServicioModelo()) {
            log.warn("El servicio de modelo no respondió a tiempo; "
                    + "la API arranca sin semilla ni índice sincronizado.");
            return;
        }
        sembrarSiHaceFalta();
        sincronizarIndice();
    }

    private boolean esperarServicioModelo() {
        for (int intento = 1; intento <= 45; intento++) {
            try {
                if (Boolean.TRUE.equals(clienteModelo.salud().modeloCargado())) {
                    return true;
                }
                log.info("El servicio de modelo respondió pero aún no tiene modelo cargado...");
            } catch (Exception e) {
                if (intento % 10 == 0) {
                    log.info("Esperando al servicio de modelo (intento {})...", intento);
                }
            }
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
        return false;
    }

    private void sembrarSiHaceFalta() {
        if (servicio.total() > 0) {
            return;
        }
        Path ruta = Path.of(rutaSemilla);
        if (!Files.exists(ruta)) {
            log.info("Sin archivo de semilla en {}; la base de conocimiento arranca vacía.", ruta);
            return;
        }
        int cargados = 0;
        try (InputStream entrada = Files.newInputStream(ruta)) {
            for (LectorCsv.Fila fila : LectorCsv.leer(entrada, 1000)) {
                try {
                    servicio.guardar(fila.titulo(), fila.texto(),
                            clienteModelo.analizar(fila.titulo(), fila.texto()), "semilla");
                    cargados++;
                } catch (Exception e) {
                    log.warn("Fila {} de la semilla omitida: {}", fila.numero(), e.getMessage());
                }
            }
        } catch (Exception e) {
            log.warn("No fue posible leer la semilla: {}", e.getMessage());
        }
        log.info("Semilla cargada: {} contenidos clasificados y guardados.", cargados);
    }

    private void sincronizarIndice() {
        try {
            int indexados = clienteModelo.reindexar(servicio.todosParaIndice());
            log.info("Índice de similitud sincronizado: {} documentos.", indexados);
        } catch (Exception e) {
            log.warn("No fue posible sincronizar el índice: {}", e.getMessage());
        }
    }
}
