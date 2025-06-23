package ru.backend.dto;

public record IngredientDto(
        String name,
        int amount,
        String unit,
        String product_name,
        String article
) {
}
