package ru.mealix.command;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.config.Language;
import ru.mealix.util.MiniAppUtil;

public class SettingsCommand extends Command {
    private final String messageText;
    private final String buttonText;

    public SettingsCommand(Language language) {
        super("/settings", language.equals(Language.RU) ? "Настройки" : "Settings");
        this.messageText = language.equals(Language.RU) ?
                "Вы можете приступить к настройкам в мини-апп" :
                "You can start the settings in the mini-app";
        this.buttonText = language.equals(Language.RU) ? "Мини-апп" : "Mini-app";
    }

    @Override
    public void execute(Update update, DefaultAbsSender client) throws TelegramApiException {
        client.execute(SendMessage
                .builder()
                .chatId(update.getMessage().getChatId())
                .text(messageText)
                .replyMarkup(MiniAppUtil.getMiniAppButton("/settings?user_id=" + update.getMessage().getChatId(), buttonText))
                .build()
        );
    }
}
