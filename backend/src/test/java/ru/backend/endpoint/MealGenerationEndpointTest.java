package ru.backend.endpoint;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.client.RestClient;
import ru.backend.dto.*;
import ru.backend.service.UserService;

import java.util.List;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
class MealGenerationEndpointTest {

    private MockMvc mockMvc;

    @Mock
    private UserService userService;

    @Mock
    private RestClient mlClient;

    @Mock
    private RestClient.RequestBodyUriSpec requestBodyUriSpec;

    @Mock
    private RestClient.RequestBodySpec requestBodySpec;

    @Mock
    private RestClient.ResponseSpec responseSpec;

    @InjectMocks
    private MealGenerationEndpoint mealGenerationEndpoint;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(mealGenerationEndpoint).build();

        when(mlClient.post()).thenReturn(requestBodyUriSpec);
        when(requestBodyUriSpec.contentType(MediaType.APPLICATION_JSON)).thenReturn(requestBodySpec);
        when(requestBodySpec.body(any(Map.class))).thenReturn(requestBodySpec);
        when(requestBodySpec.retrieve()).thenReturn(responseSpec);
    }

    @Test
    void generateMeals_validRequest_returnsDayMealDto() throws Exception {
        Long userId = 1L;
        GenerationRequestDto requestDto = new GenerationRequestDto(userId, 1, "Healthy meals", "", "");

        UserDto userDto = new UserDto(
                userId,
                "testUser",
                new PreferencesDto(
                        List.of("Lactose"),
                        List.of("Vegetarian"),
                        List.of("Italian")
                )
        );

        MealDto mealDto = new MealDto(
                "Oatmeal",
                "Healthy breakfast",
                List.of(new IngredientDto(
                        "Oats",
                        "1",
                        "100g",
                        "Oatmeal",
                        "Healthy breakfast"
                )),
                List.of()
        );

        DayMealDto dayMealDto = new DayMealDto(List.of(mealDto));

        when(userService.getUser(userId)).thenReturn(userDto);
        when(responseSpec.toEntity(DayMealDto.class))
                .thenReturn(ResponseEntity.ok(dayMealDto));

        mockMvc.perform(post("/meals")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                    {
                        "userId": 1,
                        "period": 1,
                        "text": "Healthy meals"
                    }
                    """))
                .andExpect(status().isOk());

        verify(requestBodySpec).body(eq(Map.of(
                "allergies", "Lactose, Vegetarian",
                "general_prefs", "Italian",
                "today_prefs", "Healthy meals"
        )));
    }

}