package ru.mealix.handler;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public abstract class ChainNode {
    private ChainNode next;

    public ChainNode(ChainNode next) {
        this.next = next;
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
        }
    }

    public final ChainNode setNext(ChainNode next) {
        this.next = next;
        return this;
    }

}
