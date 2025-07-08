package ru.mealix.command;

import lombok.NonNull;
import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.commands.BotCommand;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

/**
 * Base class for all commands.
 *
 * <p>It contains description of a command and abstract method for its execution.
 */
public abstract class Command extends BotCommand {

    public Command(@NonNull String command, @NonNull String description) {
        super(command, description);
    }

    /**
     * Executes the command
     *
     * @param update the update object which caused the command to be executed
     * @param client the client object which is used to send messages back to the user
     * @throws TelegramApiException on any error happening while sending the message
     */
    public abstract void execute(Update update, DefaultAbsSender client) throws TelegramApiException;

}
