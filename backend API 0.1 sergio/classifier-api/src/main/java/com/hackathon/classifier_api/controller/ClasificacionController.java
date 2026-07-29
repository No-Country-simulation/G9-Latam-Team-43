package com.hackathon.classifier_api.controller;

import com.hackathon.classifier_api.dto.ClasificacionResponse;
import com.hackathon.classifier_api.dto.ContenidoRequest;
import com.hackathon.classifier_api.service.ModeloClienteService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1")
public class ClasificacionController {

    private final ModeloClienteService modeloClienteService;

    public ClasificacionController(ModeloClienteService modeloClienteService) {
        this.modeloClienteService = modeloClienteService;
    }

    @PostMapping("/clasificar")
    public ResponseEntity<ClasificacionResponse> clasificar(@Valid @RequestBody ContenidoRequest request) {
        ClasificacionResponse respuesta = modeloClienteService.clasificar(request);
        return ResponseEntity.ok(respuesta);
    }

    @GetMapping("/salud")
    public ResponseEntity<String> salud() {
        return ResponseEntity.ok("API operativa");
    }
}