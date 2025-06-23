package ru.backend.dto;

import java.util.List;

public record PreferencesDto (
        List<String> allergies,
        List<String> dietaryRestrictions,
        List<String> favoriteCuisines
) {
}
