package ru.backend.service;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import ru.backend.dto.PreferencesDto;
import ru.backend.dto.UserDto;
import ru.backend.model.User;
import ru.backend.repository.UserRepository;
import ru.backend.util.DbTestConfig;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;


class UserServiceTest extends DbTestConfig {

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository;

    @Test
    void saveUserTest() {
        UserDto userDto = new UserDto(
                1L,
                "test",
                new PreferencesDto(
                        List.of("test1", "test2"),
                        List.of("test"),
                        List.of("test")
                )
        );
        userService.saveUser(userDto);

        User user = userRepository.findById(1L).orElse(null);

        assertEquals(1L, user.getUserId());
        assertEquals("test", user.getName());
        assertEquals(List.of("test1", "test2"), user.getAllergies());
        assertEquals(List.of("test"), user.getDietaryRestrictions());
        assertEquals(List.of("test"), user.getFavoriteCuisines());
    }

    @Test
    void getUserTest() {
        UserDto userDto = new UserDto(
                2L,
                "test",
                new PreferencesDto(
                        List.of("test1", "test2"),
                        List.of("test"),
                        List.of("test")
                )
        );
        userService.saveUser(userDto);

        UserDto user = userService.getUser(2L);

        assertEquals(2L, user.userId());
        assertEquals("test", user.name());
        assertEquals(List.of("test1", "test2"), user.preferences().allergies());
        assertEquals(List.of("test"), user.preferences().dietaryRestrictions());
        assertEquals(List.of("test"), user.preferences().favoriteCuisines());
    }
}
