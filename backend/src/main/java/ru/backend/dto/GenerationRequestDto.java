package ru.backend.dto;

public record GenerationRequestDto(
        Long userId,
        int period,
        String text
) {
}
