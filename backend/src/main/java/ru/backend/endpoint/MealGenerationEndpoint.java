package ru.backend.endpoint;

import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;
import ru.backend.dto.GenerationRequestDto;
import ru.backend.dto.GenerationResponseDto;
import ru.backend.dto.UserDto;
import ru.backend.service.UserService;

import java.util.Map;
import java.util.Objects;

@RestController
@RequestMapping("/meals")
@RequiredArgsConstructor
public class MealGenerationEndpoint {

    private final UserService userService;
    private final WebClient mlClient;

    @PostMapping
    public ResponseEntity<GenerationResponseDto> generateMeals(@RequestBody GenerationRequestDto generationDto) {
        UserDto user = userService.getUser(generationDto.userId());
        GenerationResponseDto response = Objects.requireNonNull(mlClient
                .post()
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(Map.of(
                        "user", user,
                        "generation", generationDto
                ))
                .retrieve()
                .toEntity(GenerationResponseDto.class)
                .block()).getBody();
        return ResponseEntity.ok(response);
    }

}
