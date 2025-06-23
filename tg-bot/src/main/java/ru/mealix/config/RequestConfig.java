package ru.mealix.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatusCode;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Configuration
public class RequestConfig {

    @Value("${backend.host}")
    private String backendHost;

    @Bean(name = "userClient")
    public WebClient userClient() {
        return WebClient.builder()
                .baseUrl(backendHost + "/user")
                .defaultStatusHandler(HttpStatusCode::is4xxClientError, r -> Mono.error(new RuntimeException(r.statusCode().toString())))
                .build();
    }


}
