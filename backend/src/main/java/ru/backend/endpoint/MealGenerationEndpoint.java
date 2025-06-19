package ru.backend.endpoint;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;

@RestController
@RequestMapping("/meals")
@RequiredArgsConstructor
public class MealGenerationEndpoint {

    private final WebClient mlClient;

    // TODO: implement method with correct data

    @PostMapping
    public void generateMeals() {
        mlClient.post().body(null).retrieve();
    }

}
