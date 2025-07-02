package ru.backend.endpoint;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.shaded.com.fasterxml.jackson.databind.ObjectMapper;
import ru.backend.dto.PreferencesDto;
import ru.backend.dto.UserDto;
import ru.backend.exception.NotFoundException;
import ru.backend.service.UserService;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserEndpoint.class)
class UserEndpointIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private UserService userService;

    @Test
     void createUser_validDto_returnsOk() throws Exception {
        UserDto userDto = new UserDto(1L, "testUser", new PreferencesDto(List.of(), List.of(), List.of()));

        mockMvc.perform(post("/user")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                    "userId":1,
                                    "name":"testUser",
                                    "preferences": {
                                        "allergies":[],
                                        "dietaryRestrictions":[],
                                        "favoriteCuisines":[]
                                    }
                                }
                                """)
                        )
                .andExpect(status().isOk());

        verify(userService, times(1)).saveUser(any(UserDto.class));
    }

    @Test
    void getUser_existingId_returnsUserDto() throws Exception {
        Long userId = 1L;
        UserDto userDto = new UserDto(1L, "testUser", new PreferencesDto(List.of(), List.of(), List.of()));

        when(userService.getUser(userId)).thenReturn(userDto);

        mockMvc.perform(get("/user/{userId}", userId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.userId").value(userId))
                .andExpect(jsonPath("$.name").value(userDto.name()));

        verify(userService, times(1)).getUser(userId);
    }

    @Test
    void isRegistered_existingId_returnsTrue() throws Exception {
        Long userId = 1L;

        when(userService.getUser(userId)).thenReturn(new UserDto(userId, "testUser", new PreferencesDto(List.of(), List.of(), List.of())));

        mockMvc.perform(get("/user/isRegistered/{userId}", userId))
                .andExpect(status().isOk())
                .andExpect(content().string("true"));

        verify(userService, times(1)).getUser(userId);
    }

    @Test
    void isRegistered_nonExistingId_returnsFalse() throws Exception {
        Long userId = 999L;

        when(userService.getUser(userId)).thenThrow(NotFoundException.class);

        mockMvc.perform(get("/user/isRegistered/{userId}", userId))
                .andExpect(status().isOk())
                .andExpect(content().string("false"));

        verify(userService, times(1)).getUser(userId);
    }
}