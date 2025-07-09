package ru.backend.util;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Converter for storing and retrieving a list of strings as a single string with a
 * delimiter. The delimiter used is a semicolon (;). This allows JPA to store
 * collections of strings in a single column in the database.
 */
@Converter
public class StringListConverter implements AttributeConverter<List<String>, String> {

    private static final String SPLIT_CHAR = ";";


    /**
     * Converts a list of strings to a single string that can be stored in the
     * database. The strings in the list are joined with a semicolon (;).
     *
     * @param attribute The list of strings to be converted.
     * @return A single string that can be stored in the database.
     */
    @Override
    public String convertToDatabaseColumn(List<String> attribute) {
        return attribute == null || attribute.isEmpty()
                ? ""
                : attribute.stream().collect(Collectors.joining(SPLIT_CHAR));
    }


    /**
     * Converts a string retrieved from the database to a list of strings.
     *
     * @param dbData The string retrieved from the database.
     * @return A list of strings.
     */
    @Override
    public List<String> convertToEntityAttribute(String dbData) {
        return dbData == null || dbData.isEmpty()
                ? List.of()
                : Arrays.asList(dbData.split(SPLIT_CHAR));
    }
}