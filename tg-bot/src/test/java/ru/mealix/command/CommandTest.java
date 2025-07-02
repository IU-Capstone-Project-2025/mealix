package ru.mealix.command;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Chat;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import ru.mealix.config.Language;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class CommandTest {

    @Mock
    private DefaultAbsSender client;
    @Captor
    private ArgumentCaptor<SendMessage> messageCaptor;

    @Test
    void generationCommand_Execute_SendsCorrectMessage() throws Exception {
        GenerationCommand command = new GenerationCommand(Language.RU);
        Update update = new Update();
        Message message = new Message();
        message.setChat(new Chat(123L, "chatName"));
        update.setMessage(message);

        command.execute(update, client);

        verify(client).execute(messageCaptor.capture());
        SendMessage sentMessage = messageCaptor.getValue();

        assertEquals("Вы может сгенерировать меню в мини-апп", sentMessage.getText());
    }
}