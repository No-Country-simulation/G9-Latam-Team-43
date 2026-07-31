package com.tecnoteca.api.modelo;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.client.RestClientTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withServerError;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;
import static org.springframework.http.HttpMethod.POST;

/** Verifica el contrato JSON (snake_case) con el servicio de modelo Python. */
@RestClientTest(components = ClienteModelo.class,
        properties = "tecnoteca.modelo.url=http://modelo-prueba")
class ClienteModeloTest {

    @Autowired
    private ClienteModelo cliente;

    @Autowired
    private MockRestServiceServer servidor;

    @Test
    void analizarMapeaLaRespuestaDelModelo() {
        servidor.expect(requestTo("http://modelo-prueba/analizar"))
                .andExpect(method(POST))
                .andRespond(withSuccess("""
                        {"categoria": "Backend", "probabilidad": 0.91,
                         "distribucion": {"Backend": 0.91, "Frontend": 0.02},
                         "palabras_clave": ["Java", "Spring Boot"],
                         "tema": {"id": 2, "etiqueta": "java, spring, api"},
                         "explicacion": [{"termino": "spring boot", "peso": 1.2}]}
                        """, MediaType.APPLICATION_JSON));

        ClienteModelo.AnalisisModelo analisis = cliente.analizar("t", "x");

        assertEquals("Backend", analisis.categoria());
        assertEquals(0.91, analisis.probabilidad());
        assertEquals(List.of("Java", "Spring Boot"), analisis.palabrasClave());
        assertEquals("java, spring, api", analisis.tema().etiqueta());
    }

    @Test
    void errorDelModeloSeTraduceAExcepcionPropia() {
        servidor.expect(requestTo("http://modelo-prueba/analizar"))
                .andRespond(withServerError());
        assertThrows(ServicioModeloException.class, () -> cliente.analizar("t", "x"));
    }
}
