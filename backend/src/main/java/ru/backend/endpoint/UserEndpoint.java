package ru.backend.endpoint;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.backend.dto.UserDto;
import ru.backend.exception.NotFoundException;
import ru.backend.service.UserService;

/**
 * REST endpoint for user operations.
 *
 * <p>This endpoint provides a simple REST interface for registering and retrieving users.
 * Currently, the following operations are supported:
 *
 * <ul>
 *     <li>POST /user - Registering a new user.</li>
 *     <li>GET /user/{userId} - Get user information by user id.</li>
 *     <li>GET /user/isRegistered/{userId} - Check if the user is registered.</li>
 * </ul>
 */
@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
@CrossOrigin(origins = {
        "http://localhost:5173",
        "https://mealix.vercel.app"
})
public class UserEndpoint {

    private final UserService userService;

    /**
     * Registers a new user in the system.
     *
     * @param userDto New user's data.
     * @return empty response with status 200 if user is registered successfully.
     */
    @PostMapping
    public ResponseEntity<Void> createUser(@RequestBody @Valid UserDto userDto) {
        userService.saveUser(userDto);
        return ResponseEntity.ok().build();
    }

    /**
     * Gets user information by user id.
     *
     * @param userId user id to be found.
     * @return user information if user is found.
     * @throws NotFoundException if user is not registered.
     */
    @GetMapping("/{userId}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long userId) {
        UserDto userDto = userService.getUser(userId);
        return ResponseEntity.ok(userDto);
    }

    /**
     * Checks if the user is registered.
     *
     * @param userId user id to be checked.
     * @return true if the user is registered, false otherwise.
     */
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
