package ru.mealix.config;

import lombok.RequiredArgsConstructor;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import ru.mealix.command.Command;
import ru.mealix.command.SettingsCommand;
import ru.mealix.command.StartCommand;
import ru.mealix.handler.ChainNode;
import ru.mealix.handler.DefaultStateChainNode;
import ru.mealix.handler.NewUserStateChainNode;
import ru.mealix.service.UserService;

import java.util.concurrent.ConcurrentHashMap;

@Configuration
@EnableConfigurationProperties(BotProperties.class)
@RequiredArgsConstructor
public class BotConfig {

    private final BotProperties botProperties;
    private final UserService userService;


    @Bean(name = "botToken")
    public String botToken() {
        String token = botProperties.getToken();

        if (token == null || token.trim().isEmpty()) {
            throw new IllegalStateException("Bot token is null or empty");
        }

        return token;
    }

    @Bean
    public ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands() {
        ConcurrentHashMap<Language, ConcurrentHashMap<String, Command>> commands = new ConcurrentHashMap<>();
        ConcurrentHashMap<String, Command> commandsRu = new ConcurrentHashMap<>();
        commandsRu.put("/start", new StartCommand(Language.RU));
        commandsRu.put("/settings", new SettingsCommand(Language.RU));

        ConcurrentHashMap<String, Command> commandsEn = new ConcurrentHashMap<>();
        commandsEn.put("/start", new StartCommand(Language.EN));
        commandsEn.put("/settings", new SettingsCommand(Language.EN));

        commands.put(Language.RU, commandsRu);
        commands.put(Language.EN, commandsEn);
        return commands;
    }

    @Bean
    public ChainNode handler() {
        return new NewUserStateChainNode(userService, commands())
                .setNext(new DefaultStateChainNode(userService, commands()));
    }

}
