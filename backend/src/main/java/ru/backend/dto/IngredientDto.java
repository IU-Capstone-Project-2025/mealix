package ru.backend.dto;

public record IngredientDto(
        String name,
        String amount,
        String unit,
        String product_name,
        String article
) {
}
