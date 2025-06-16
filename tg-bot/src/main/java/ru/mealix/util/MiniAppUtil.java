package ru.mealix.util;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.api.objects.webapp.WebAppInfo;

import java.util.ArrayList;
import java.util.List;

@Component
public class MiniAppUtil {

    @Value("${bot.miniapp.host}")
    private String miniAppHost;

    private static String miniAppHostStatic;

    @PostConstruct
    public void init() {
        miniAppHostStatic = miniAppHost;
    }


    public static InlineKeyboardMarkup getMiniAppButton(String url, String text) {
        InlineKeyboardMarkup markupInline = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rowsInline = new ArrayList<>();
        List<InlineKeyboardButton> rowInline = new ArrayList<>();

        rowInline.add(InlineKeyboardButton.builder()
                .text(text)
                .webApp(new WebAppInfo(miniAppHostStatic + url))
                .build());
        rowsInline.add(rowInline);
        markupInline.setKeyboard(rowsInline);

        return markupInline;
    }

}
