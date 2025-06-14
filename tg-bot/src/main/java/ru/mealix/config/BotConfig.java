package ru.mealix.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(BotProperties.class)
public class BotConfig {

    private final BotProperties botProperties;

    public BotConfig(BotProperties botProperties) {
        this.botProperties = botProperties;
    }

    @Bean(name = "botToken")
    public String botToken() {
        String token = botProperties.getToken();

        if (token == null || token.trim().isEmpty()) {
            throw new IllegalStateException("Bot token is null or empty");
        }

        return token;
    }

}
