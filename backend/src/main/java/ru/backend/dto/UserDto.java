package ru.backend.dto;

import jakarta.validation.constraints.NotNull;
import ru.backend.model.User;

import java.io.Serializable;

public record UserDto (
        @NotNull
    Long userId,
    String name,
    PreferencesDto preferences
) implements ToEntity<User>, Serializable {

    public static UserDto fromEntity(User user) {
        return new UserDto(
                user.getUserId(),
                user.getName(),
                new PreferencesDto(
                        user.getAllergies(),
                        user.getDietaryRestrictions(),
                        user.getFavoriteCuisines()
                )
        );
    }

    @Override
    public User toEntity() {
        return new User(
                userId,
                name,
                preferences.allergies(),
                preferences.dietaryRestrictions(),
                preferences.favoriteCuisines()
        );
    }
}
