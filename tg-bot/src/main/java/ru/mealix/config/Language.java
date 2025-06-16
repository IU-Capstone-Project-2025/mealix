package ru.mealix.config;

import lombok.Getter;
import org.telegram.telegrambots.meta.api.objects.Update;

@Getter
public enum Language {
    EN("en"),
    RU("ru");

    private final String code;

    Language(String code) {
        this.code = code;
    }

    public static Language fromUpdate(Update update) {
        String languageCode;
        if (update.hasMessage()) {
            languageCode = update.getMessage().getFrom().getLanguageCode();
        } else {
            languageCode = "en";
        }
        return switch (languageCode) {
            case "ru" -> Language.RU;
            case "en" -> Language.EN;
            default -> Language.EN;
        };
    }
}
