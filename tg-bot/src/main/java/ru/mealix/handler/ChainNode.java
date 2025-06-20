package ru.mealix.handler;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.config.Language;
import ru.mealix.exception.UpdateHandleException;
import ru.mealix.service.UserService;

public abstract class ChainNode {
    private ChainNode next;
    protected final UserService userService;

    public ChainNode(ChainNode next, UserService userService) {
        this.next = next;
        this.userService = userService;
    }

    public ChainNode(UserService userService) {
        this.userService = userService;
    }

    public final void handle(Update update, DefaultAbsSender client) throws TelegramApiException {
        boolean done = false;
        if (canHandle(update)) {
            done = process(update, client);
        }
        if (done) return;
        next(update, client);
    }

    protected abstract boolean canHandle(Update update);

    protected abstract boolean process(Update update, DefaultAbsSender client) throws TelegramApiException;

    private void next(Update update, DefaultAbsSender client) throws TelegramApiException {
        if (next != null) {
            next.handle(update, client);
        } else {
            if (update.hasMessage()) {
                Language language = Language.fromUpdate(update);
                client.execute(SendMessage
                        .builder()
                        .chatId(update.getMessage().getChatId())
                        .text(language.equals(Language.RU) ? "Что то пошло не так с обработкой обновления" : "Something went wrong with the update handling")
                        .build()
                );
            }
        }
    }

    public final ChainNode setNext(ChainNode next) {
        this.next = next;
        return this;
    }

}
