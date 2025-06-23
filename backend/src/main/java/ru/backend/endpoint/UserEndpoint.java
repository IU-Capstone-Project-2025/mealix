package ru.backend.endpoint;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.backend.dto.UserDto;
import ru.backend.exception.NotFoundException;
import ru.backend.service.UserService;

@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserEndpoint {

    private final UserService userService;

    @PostMapping
    public ResponseEntity<Void> createUser(@RequestBody @Valid UserDto userDto) {
        userService.saveUser(userDto);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/{userId}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long userId) {
        UserDto userDto = userService.getUser(userId);
        return ResponseEntity.ok(userDto);
    }

    @GetMapping("/isRegistered/{userId}")
    public ResponseEntity<Boolean> isRegistered(@PathVariable Long userId) {
        try {
            userService.getUser(userId);
            return ResponseEntity.ok(true);
        } catch (NotFoundException e) {
            return ResponseEntity.ok(false);
        }
    }

}
