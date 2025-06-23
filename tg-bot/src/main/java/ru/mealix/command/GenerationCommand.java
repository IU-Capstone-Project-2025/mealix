package ru.mealix.command;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.config.Language;
import ru.mealix.util.MiniAppUtil;

public class GenerationCommand extends Command {
    private final String messageText;
    private final String buttonText;

    public GenerationCommand(Language language) {
        super("/generate", language.equals(Language.RU) ? "Генерация меню" : "Generation menu");
        this.messageText = language.equals(Language.RU) ?
                "Вы может сгенерировать меню в мини-апп" :
                "You can generate a menu in the mini-app";
        this.buttonText = language.equals(Language.RU) ? "Мини-апп" : "Mini-app";
    }

    @Override
    public void execute(Update update, DefaultAbsSender client) throws TelegramApiException {
        client.execute(SendMessage
                .builder()
                .chatId(update.getMessage().getChatId())
                .text(messageText)
                .replyMarkup(MiniAppUtil.getMiniAppButton("/generation?user_id=" + update.getMessage().getChatId(), buttonText))
                .build()
        );
    }
}
