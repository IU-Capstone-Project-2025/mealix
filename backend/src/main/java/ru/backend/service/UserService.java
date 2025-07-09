package ru.backend.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import ru.backend.dto.UserDto;
import ru.backend.exception.NotFoundException;
import ru.backend.repository.UserRepository;

/**
 * Service for work with users.
 */
@Service
@RequiredArgsConstructor
@Transactional
public class UserService {

    private final UserRepository userRepository;


    /**
     * Saves user to database.
     * @param userDto Dto with user data.
     */
    public void saveUser(UserDto userDto) {
        userRepository.save(userDto.toEntity());
    }


    /**
     * Gets user by id.
     * @param userId id of user.
     * @return UserDto with user data.
     * @throws NotFoundException if user not found.
     */
    public UserDto getUser(Long userId) {
        return userRepository
                .findById(userId)
                .map(UserDto::fromEntity)
                .orElseThrow(() -> new NotFoundException("User not found"));
    }

}
