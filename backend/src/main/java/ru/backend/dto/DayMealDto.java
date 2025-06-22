package ru.backend.dto;

import java.util.List;

public record DayMealDto(
        List<MealDto> meals
) {
}
