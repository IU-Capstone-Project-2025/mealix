package ru.mealix.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.client.RestClientTest;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.ExpectedCount;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientResponseException;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

@RestClientTest
class UserServiceTest {

    @Autowired
    private RestClient.Builder restClientBuilder;

    private MockRestServiceServer mockServer;
    private UserService userService;

    @BeforeEach
    void setUp() {
        // Создаем мок-сервер и сервис
        mockServer = MockRestServiceServer.bindTo(restClientBuilder).build();
        RestClient restClient = restClientBuilder
                .baseUrl("http://base-url/user") // Добавляем базовый URL
                .build();
        userService = new UserService(restClient);
    }

    @Test
    void isRegistered_WhenUserRegistered_ReturnsTrue() {
        // Указываем полный URL с базовым путем
        mockServer.expect(ExpectedCount.once(),
                        requestTo("http://base-url/user/isRegistered/123"))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess("true", MediaType.APPLICATION_JSON));

        Boolean result = userService.isRegistered(123L);
        assertTrue(result);
        mockServer.verify();
    }

    @Test
    void isRegistered_WhenUserNotRegistered_ReturnsFalse() {
        mockServer.expect(requestTo("http://base-url/user/isRegistered/456"))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess("false", MediaType.APPLICATION_JSON));

        Boolean result = userService.isRegistered(456L);
        assertFalse(result);
        mockServer.verify();
    }

}