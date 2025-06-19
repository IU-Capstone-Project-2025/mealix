package ru.backend.dto;

import java.util.List;

public record GenerationResponseDto(
        List<String> meals
) {
}
