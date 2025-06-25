package ru.mealix.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatusCode;
import org.springframework.web.client.RestClient;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Configuration
@Slf4j
public class RequestConfig {

    @Value("${backend.host}")
    private String backendHost;

    @Bean(name = "userClient")
    public RestClient userClient() {
        return RestClient.create(backendHost + "/user");
    }

    private ExchangeFilterFunction logRequest() {
        return ExchangeFilterFunction.ofRequestProcessor(clientRequest -> {
            log.info("Sending request: {} {}", clientRequest.method(), clientRequest.url());
            return Mono.just(clientRequest);
        });
    }


}
