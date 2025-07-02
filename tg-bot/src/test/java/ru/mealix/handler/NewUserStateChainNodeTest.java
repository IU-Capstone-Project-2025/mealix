package ru.mealix.handler;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.telegram.telegrambots.bots.DefaultAbsSender;
import org.telegram.telegrambots.meta.api.objects.Chat;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.User;
import ru.mealix.command.Command;
import ru.mealix.command.GenerationCommand;
import ru.mealix.command.SettingsCommand;
import ru.mealix.command.StartCommand;
import ru.mealix.config.Language;
import ru.mealix.service.UserService;

import java.util.concurrent.ConcurrentHashMap;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class NewUserStateChainNodeTest {

    @Mock
    private UserService userService;
    @Mock
    private DefaultAbsSender client;
    @InjectMocks
    private NewUserStateChainNode chainNode;

    private static final ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands = new ConcurrentHashMap<>();

    @BeforeAll
    static void setUp() {
        ConcurrentHashMap<String, Command> commandsRu = new ConcurrentHashMap<>();
        commandsRu.put("/start", new StartCommand(Language.RU));
        commandsRu.put("/settings", new SettingsCommand(Language.RU));
        commandsRu.put("/generate", new GenerationCommand(Language.RU));

        ConcurrentHashMap<String, Command> commandsEn = new ConcurrentHashMap<>();
        commandsEn.put("/start", new StartCommand(Language.EN));
        commandsEn.put("/settings", new SettingsCommand(Language.EN));
        commandsEn.put("/generate", new GenerationCommand(Language.EN));

        commands.put(Language.RU, commandsRu);
        commands.put(Language.EN, commandsEn);
    }

    @Test
    void canHandle_NewUserWithText_ReturnsTrue() {
        Update update = createTextUpdate("/start", 123L, "ru");
        when(userService.isRegistered(123L)).thenReturn(false);

        assertTrue(chainNode.canHandle(update));
    }

    @Test
    void process_StartCommand_CallsExecute() throws Exception {
        Update update = createTextUpdate("/start", 123L, "en");
        Command startCommand = mock(StartCommand.class);

        ConcurrentHashMap<String, Command> enCommands = new ConcurrentHashMap<>();
        enCommands.put("/start", startCommand);
        commands.put(Language.EN, enCommands);

        chainNode = new NewUserStateChainNode(userService, commands);

        boolean result = chainNode.process(update, client);

        assertTrue(result);
        verify(startCommand).execute(update, client);
    }

    private Update createTextUpdate(String text, Long chatId, String langCode) {
        User user = new User();
        user.setLanguageCode(langCode);

        Chat chat = new Chat();
        chat.setId(chatId);

        Message message = new Message();
        message.setText(text);
        message.setFrom(user);
        message.setChat(chat);

        Update update = new Update();
        update.setMessage(message);
        return update;
    }
}