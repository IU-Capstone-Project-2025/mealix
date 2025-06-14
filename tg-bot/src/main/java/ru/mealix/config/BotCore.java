package ru.mealix.config;

import org.springframework.stereotype.Service;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.objects.Update;

import java.util.List;
import java.util.concurrent.Executor;

@Service
public class BotCore extends TelegramLongPollingBot {
    private final Executor botAsyncExecutor;

    public BotCore(String botToken, Executor botAsyncExecutor) {
        super(botToken);
        this.botAsyncExecutor = botAsyncExecutor;
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

    }

    @Override
    public String getBotUsername() {
        return "Mealix Bot";
    }
}
