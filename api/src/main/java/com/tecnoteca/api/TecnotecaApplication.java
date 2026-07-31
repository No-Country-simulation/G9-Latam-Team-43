package com.tecnoteca.api;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@OpenAPIDefinition(info = @Info(
        title = "Tecnoteca API",
        version = "1.0.0",
        description = "Organizador inteligente de contenido técnico (Hackathon ONE G9). "
                + "Recibe contenidos, los clasifica con el modelo del equipo de ciencia de "
                + "datos y permite buscarlos y relacionarlos."))
public class TecnotecaApplication {

    public static void main(String[] args) {
        SpringApplication.run(TecnotecaApplication.class, args);
    }
}
