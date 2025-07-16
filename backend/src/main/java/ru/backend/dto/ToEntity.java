package ru.backend.dto;

/**
 * This interface is used to convert DTO to Entity object
 */
public interface ToEntity<T> {
    /**
     * Convert DTO object to Entity object
     * @return Entity object
     */
    T toEntity();
}
