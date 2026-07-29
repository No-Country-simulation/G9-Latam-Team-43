package com.hackathon.classifier_api.service;

import com.hackathon.classifier_api.dto.ClasificacionResponse;
import com.hackathon.classifier_api.dto.ContenidoRequest;
import com.hackathon.classifier_api.exception.ModeloNoDisponibleException;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.time.Duration;

@Service
public class ModeloClienteService {

    private final WebClient webClient;

    public ModeloClienteService(WebClient webClient) {
        this.webClient = webClient;
    }

    public ClasificacionResponse clasificar(ContenidoRequest request) {
        try {
            return webClient.post()
                    .uri("/predict")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(ClasificacionResponse.class)
                    .timeout(Duration.ofSeconds(5))
                    .block();
        } catch (WebClientResponseException e) {
            throw new ModeloNoDisponibleException(
                    "Error del modelo: " + e.getStatusCode());
        } catch (Exception e) {
            throw new ModeloNoDisponibleException(
                    "No se pudo conectar con el servicio de modelo");
        }
    }
}