package ru.mealix.command;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.config.Language;
import ru.mealix.util.MiniAppUtil;

public class StartCommand extends Command {
    private final String messageText;
    private final String buttonText;

    public StartCommand(Language language) {
        super("/start", language.equals(Language.RU) ? "Запускает бота" : "Starts the bot");
        this.messageText = language.equals(Language.RU) ?
                "Привет! Я Mealix Bot! Вы можете приступить к настройкам в мини-апп" :
                "Hello! I'm Mealix Bot! You can start the settings in the mini-app";
        this.buttonText = language.equals(Language.RU) ? "Мини-апп" : "Mini-app";
    }

    @Override
    public void execute(Update update, DefaultAbsSender client) throws TelegramApiException {
        client.execute(SendMessage
                .builder()
                .chatId(update.getMessage().getChatId())
                .text(messageText)
                .replyMarkup(MiniAppUtil.getMiniAppButton("/newuser?user_id=" + update.getMessage().getChatId(), buttonText))
                .build()
        );
    }

}
