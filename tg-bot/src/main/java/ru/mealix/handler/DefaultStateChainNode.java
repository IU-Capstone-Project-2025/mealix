package ru.mealix.handler;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.command.Command;

import java.util.concurrent.ConcurrentHashMap;

public class DefaultStateChainNode extends ChainNode {
    private final ConcurrentHashMap<String, Command> commands;

    public DefaultStateChainNode(ChainNode next, ConcurrentHashMap<String, Command> commands) {
        super(next);
        this.commands = commands;
    }

    public DefaultStateChainNode(ConcurrentHashMap<String, Command> commands) {
        super();
        this.commands = commands;
    }

    @Override
    protected boolean canHandle(Update update) {
        return update.hasMessage()
                && update.getMessage().hasText();
    }

    @Override
    protected boolean process(Update update, DefaultAbsSender client) throws TelegramApiException {
        String text = update.getMessage().getText();
        if (commands.containsKey(text)) {
            commands.get(text).execute(update, client);
            return true;
        }
        return false;
    }
}
