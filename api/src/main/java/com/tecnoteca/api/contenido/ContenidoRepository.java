package com.tecnoteca.api.contenido;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface ContenidoRepository extends JpaRepository<Contenido, Long> {

    List<Contenido> findByCategoriaIgnoreCase(String categoria, Pageable paginacion);

    interface ConteoCategoria {
        String getCategoria();
        long getCantidad();
    }

    @Query("select c.categoria as categoria, count(c) as cantidad "
            + "from Contenido c group by c.categoria")
    List<ConteoCategoria> contarPorCategoria();
}
