FROM maven:3.8.8-eclipse-temurin-21 AS builder

WORKDIR /app

COPY pom.xml .

COPY ./src ./src
RUN mvn clean package

# Финальный образ
FROM eclipse-temurin:21-jdk-alpine-3.21

WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]

#For locla build

#FROM eclipse-temurin:21-jdk-alpine-3.21
#ARG JAR_FILE=target/*.jar
#COPY ${JAR_FILE} app.jar
#ENTRYPOINT ["java", "-jar", "/app.jar"]