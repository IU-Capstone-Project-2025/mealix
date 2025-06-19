package ru.backend.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import ru.backend.dto.UserDto;
import ru.backend.exception.NotFoundException;
import ru.backend.repository.UserRepository;

@Service
@RequiredArgsConstructor
@Transactional
public class UserService {

    private final UserRepository userRepository;

    public void saveUser(UserDto userDto) {
        userRepository.save(userDto.toEntity());
    }

    public UserDto getUser(Long userId) {
        return userRepository
                .findById(userId)
                .map(UserDto::fromEntity)
                .orElseThrow(() -> new NotFoundException("User not found"));
    }

}
