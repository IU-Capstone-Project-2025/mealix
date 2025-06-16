package ru.mealix.config;

import lombok.Getter;

@Getter
public enum Language {
    EN("en"),
    RU("ru");

    private final String code;

    Language(String code) {
        this.code = code;
    }
}
