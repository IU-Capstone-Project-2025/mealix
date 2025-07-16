package ru.backend.exception;

/**
 * This exception is thrown when object is not found in repository or in service.
 */
public class NotFoundException extends RuntimeException {
    public NotFoundException(String message) {
        super(message);
    }
}
