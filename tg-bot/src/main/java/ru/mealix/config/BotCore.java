package ru.mealix.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import ru.mealix.command.Command;
import ru.mealix.handler.ChainNode;

import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executor;

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
