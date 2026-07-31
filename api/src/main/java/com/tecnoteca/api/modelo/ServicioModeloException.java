package com.tecnoteca.api.modelo;

/** El servicio de modelo (Python) no está disponible o rechazó la petición. */
public class ServicioModeloException extends RuntimeException {

    public ServicioModeloException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}
