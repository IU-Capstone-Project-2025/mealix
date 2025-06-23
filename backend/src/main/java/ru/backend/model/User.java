package ru.backend.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import ru.backend.util.StringListConverter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Access(AccessType.FIELD)
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Table(name = "users")
public class User {

        @Id
        private Long userId;

        private String name;

        @Convert(converter = StringListConverter.class)
        @Column(name = "allergies")
        private List<String> allergies = new ArrayList<>();

        @Convert(converter = StringListConverter.class)
        @Column(name = "restrictions")
        private List<String> dietaryRestrictions = new ArrayList<>();

        @Convert(converter = StringListConverter.class)
        @Column(name = "cousines")
        private List<String> favoriteCuisines = new ArrayList<>();
}

