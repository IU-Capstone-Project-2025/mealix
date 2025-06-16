package ru.mealix.handler;

import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.command.Command;
import ru.mealix.config.Language;
import ru.mealix.service.UserService;

import java.util.concurrent.ConcurrentHashMap;

public class DefaultStateChainNode extends ChainNode {

    private final ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands;

    public DefaultStateChainNode(ChainNode next, UserService userService, ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands) {
        super(next, userService);
        this.commands = commands;
    }

    public DefaultStateChainNode(UserService userService, ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands) {
        super(userService);
        this.commands = commands;
    }

    @Override
    protected boolean canHandle(Update update) {
        return update.hasMessage()
                && update.getMessage().hasText()
                && userService.isRegistered(update.getMessage().getChatId());
    }

    @Override
    protected boolean process(Update update, DefaultAbsSender client) throws TelegramApiException {
        String text = update.getMessage().getText();
        Language language = Language.fromUpdate(update);
        if (text.equals("/start")) {
            client.execute(SendMessage
                    .builder()
                    .chatId(update.getMessage().getChatId())
                    .text(language.equals(Language.RU) ?
                            "Вы уже зарегистрированы" : "You are already registered")
                    .build()
            );
        }

        ConcurrentHashMap<String, Command> command;
        if (commands.containsKey(language)) {
            command = commands.get(language);
        } else {
            command = commands.get(Language.EN);
        }

        if (command.containsKey(text)) {
            command.get(text).execute(update, client);
            return true;
        }
        return false;
    }
}
