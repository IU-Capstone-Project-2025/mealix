package ru.mealix.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Objects;

/**
 * Simple service for checking if the user is registered in the backend.
 */
@Service
@RequiredArgsConstructor
public class UserService {
    /*
     * TODO: Implement cache for registered userIds (cache hit/miss)
     */

    private final RestClient userClient;


    /**
     * Checks if the user is registered in the backend.
     *
     * @param userId id of the user
     * @return true if the user is registered, false otherwise
     */
    public Boolean isRegistered(Long userId) {
        return Objects.requireNonNull(userClient
                .get()
                .uri("/isRegistered/" + userId)
                .retrieve()
                .toEntity(Boolean.class)).getBody();
    }

}
