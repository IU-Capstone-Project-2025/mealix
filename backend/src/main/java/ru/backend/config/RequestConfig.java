package ru.backend.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestClient;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;

@Configuration
public class RequestConfig {

    @Value("${ml.url}")
    private String mlUrl;

    @Bean
    public RestClient mlClient() {
        return RestClient.builder()
                .baseUrl(mlUrl)
                .requestFactory(simpleClientHttpRequestFactory())
                .build();
    }

    @Bean
    public SimpleClientHttpRequestFactory simpleClientHttpRequestFactory() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(Duration.ofMinutes(5));
        factory.setReadTimeout(Duration.ofMinutes(5));
        return factory;
    }
}
