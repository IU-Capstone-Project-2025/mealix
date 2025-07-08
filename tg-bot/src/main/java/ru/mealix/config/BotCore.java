package ru.mealix.config;

import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.commands.SetMyCommands;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.commands.BotCommand;
import org.telegram.telegrambots.meta.api.objects.commands.scope.BotCommandScopeDefault;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;
import ru.mealix.command.Command;
import ru.mealix.handler.ChainNode;

import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executor;

/**
 * Main class for bot. It's extends {@link TelegramLongPollingBot} and add some features like
 * handling updates in separate thread pool and handling commands in simple chain of responsibility pattern.
 */
@Service
@Slf4j
public class BotCore extends TelegramLongPollingBot {
    private final Executor botAsyncExecutor;
    private final ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands;
    private final ChainNode handler;

    public BotCore(String botToken, Executor botAsyncExecutor, ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands, ChainNode handler) {
        super(botToken);
        this.botAsyncExecutor = botAsyncExecutor;
        this.commands = commands;
        this.handler = handler;
    }

    /**
     * Simple init method for telegram bot. It register bot in TelegramBotsApi and set commands for bot.
     */
    @PostConstruct
    public void init() {
        try {
            TelegramBotsApi telegramBotsApi = new TelegramBotsApi(DefaultBotSession.class);
            telegramBotsApi.registerBot(this);

            execute(new SetMyCommands(
                    commands.get(Language.RU)
                            .values().stream()
                            .map(command -> (BotCommand) command)
                            .toList(),
                    new BotCommandScopeDefault(), "ru")
            );
            execute(new SetMyCommands(
                    commands.get(Language.EN)
                            .values().stream()
                            .map(command -> (BotCommand) command)
                            .toList(),
                    new BotCommandScopeDefault(), "en")
            );

        } catch (TelegramApiException e) {
            log.error("Error registering commands: {}", e.getMessage());
            throw new RuntimeException(e);
        }
    }

    @Override
    public void onUpdatesReceived(List<Update> updates) {
        updates.forEach(update ->
                botAsyncExecutor.execute(
                        () -> onUpdateReceived(update)
                )
        );
    }

    @Override
    public void onUpdateReceived(Update update) {
        try {
            handler.handle(update, this);
        } catch (TelegramApiException e) {
            log.error("Error handling update: {}", e.getMessage());
        } catch (RuntimeException e) {
            log.error("Unknown error: {}", e.getMessage());
        }
    }

    @Override
    public String getBotUsername() {
        return "Mealix Bot";
    }
}
