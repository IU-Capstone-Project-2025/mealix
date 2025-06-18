package ru.mealix.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Objects;

@Service
@RequiredArgsConstructor
public class UserService {
    /*
     * TODO: Implement cache for registered userIds (cache hit/miss)
     */

    private final WebClient userClient;

    public Boolean isRegistered(Long userId) {
        return Objects.requireNonNull(userClient
                .get()
                .uri("/isRegistered?user_id=" + userId)
                .retrieve()
                .toEntity(Boolean.class)
                .block()).getBody();
    }

}
