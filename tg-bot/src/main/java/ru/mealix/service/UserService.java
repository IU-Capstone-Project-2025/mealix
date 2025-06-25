package ru.mealix.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Objects;

@Service
@RequiredArgsConstructor
public class UserService {
    /*
     * TODO: Implement cache for registered userIds (cache hit/miss)
     */

    private final RestClient userClient;

    public Boolean isRegistered(Long userId) {
        return Objects.requireNonNull(userClient
                .get()
                .uri("/isRegistered/" + userId)
                .retrieve()
                .toEntity(Boolean.class)).getBody();
    }

}
