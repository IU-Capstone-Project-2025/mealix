package ru.mealix.command;

import lombok.NonNull;
import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.commands.BotCommand;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public abstract class Command extends BotCommand {

    public Command(@NonNull String command, @NonNull String description) {
        super(command, description);
    }

    public abstract void execute(Update update, DefaultAbsSender client) throws TelegramApiException;

}
