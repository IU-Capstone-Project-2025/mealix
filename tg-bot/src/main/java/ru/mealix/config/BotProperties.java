package ru.mealix.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "bot")
@Setter
@Getter
public class BotProperties {

    private String token;

}
