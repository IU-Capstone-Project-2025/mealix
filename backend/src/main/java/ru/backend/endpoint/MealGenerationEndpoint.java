package ru.backend.endpoint;

import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestClient;
import ru.backend.dto.DayMealDto;
import ru.backend.dto.GenerationRequestDto;
import ru.backend.dto.GenerationResponseDto;
import ru.backend.dto.UserDto;
import ru.backend.service.UserService;

import java.util.Map;
import java.util.Objects;

@RestController
@RequestMapping("/meals")
@RequiredArgsConstructor
@CrossOrigin(origins = {
        "http://localhost:5173",
        "https://mealix.vercel.app"
})
public class MealGenerationEndpoint {

    private final UserService userService;
    private final RestClient mlClient;

    @PostMapping
    public ResponseEntity<DayMealDto> generateMeals(@RequestBody GenerationRequestDto generationDto) {
        UserDto user = userService.getUser(generationDto.userId());
        DayMealDto response = Objects.requireNonNull(mlClient
                .post()
                .contentType(MediaType.APPLICATION_JSON)
                .body(Map.of(
                    "allergies", String.join(", ", user.preferences().allergies()) + "\n" + String.join(", ", user.preferences().dietaryRestrictions()),
                    "general_prefs", String.join(", ", user.preferences().favoriteCuisines()),
                    "today_prefs", generationDto.text()
                ))
                .retrieve()
                .toEntity(DayMealDto.class)).getBody();
        return ResponseEntity.ok(response);
    }

}
