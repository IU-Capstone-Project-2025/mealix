package ru.mealix.util;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.api.objects.webapp.WebAppInfo;

import java.util.ArrayList;
import java.util.List;

/**
 * Utility class for work with Telegram Mini Apps
 */
@Component
public class MiniAppUtil {

    @Value("${bot.miniapp.host}")
    private String miniAppHost;

    private static String miniAppHostStatic;

    @PostConstruct
    public void init() {
        miniAppHostStatic = miniAppHost;
    }

    /**
     * Generates inline keyboard markup for button with mini app url.
     *
     * @param url    mini app url
     * @param text   button text
     * @return inline keyboard markup
     */
    public static InlineKeyboardMarkup getMiniAppButton(String url, String text) {
        InlineKeyboardMarkup markupInline = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> rowsInline = new ArrayList<>();
        List<InlineKeyboardButton> rowInline = new ArrayList<>();

        InlineKeyboardButton webApp = new InlineKeyboardButton();
        webApp.setText(text);
        webApp.setUrl(miniAppHostStatic + url);

        rowInline.add(webApp);
        rowsInline.add(rowInline);
        markupInline.setKeyboard(rowsInline);

        return markupInline;
    }

}
