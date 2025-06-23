package ru.backend.dto;

import java.util.List;

public record MealDto(
        String type,
        String dish,
        List<IngredientDto> ingredients,
        List<String> steps
) {
}
