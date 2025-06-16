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
        String languageCode = update.getCallbackQuery().getFrom().getLanguageCode();
        return Language.valueOf(languageCode);
    }
}
