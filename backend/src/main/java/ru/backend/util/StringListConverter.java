package ru.backend.util;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Converter
public class StringListConverter implements AttributeConverter<List<String>, String> {

    private static final String SPLIT_CHAR = ";";

    @Override
    public String convertToDatabaseColumn(List<String> attribute) {
        return attribute == null || attribute.isEmpty()
                ? ""
                : attribute.stream().collect(Collectors.joining(SPLIT_CHAR));
    }

    @Override
    public List<String> convertToEntityAttribute(String dbData) {
        return dbData == null || dbData.isEmpty()
                ? List.of()
                : Arrays.asList(dbData.split(SPLIT_CHAR));
    }
}