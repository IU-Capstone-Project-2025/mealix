package ru.mealix.handler;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.config.Language;
import ru.mealix.service.UserService;

/**
 * Abstract class for creating of chain of responsibility
 * for handling of update from telegram
 * The class is responsible for the correct handling of updates
 * and for the transition of the update to the next handler in the chain
 */
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

    /**
     * Checks if the update can be handled by this node
     * and processes this update if it can
     * else it sends update to the next node
     * @param update to be handled
     * @param client for sending messages
     * @throws TelegramApiException if there is a problem with sending of message
     */
    public final void handle(Update update, DefaultAbsSender client) throws TelegramApiException {
        boolean done = false;
        if (canHandle(update)) {
            done = process(update, client);
        }
        if (done) return;
        next(update, client);
    }

    /**
     * This method checks if the update can be handled by this node
     * @param update to be handled
     * @throws TelegramApiException if there is a problem with sending of message
     */
    protected abstract boolean canHandle(Update update);

    /**
     * Processes the update if it can be handled by this node
     * @param update to be handled
     * @param client for sending messages
     * @return true if the update is handled, else false
     * @throws TelegramApiException if there is a problem with sending of message
     */
    protected abstract boolean process(Update update, DefaultAbsSender client) throws TelegramApiException;

    /**
     * This method sends the update to the next node in the chain
     * if current node can't handle this update
     * @param update to be handled
     * @param client for sending messages
     * @throws TelegramApiException if there is a problem with sending of message
     */
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
