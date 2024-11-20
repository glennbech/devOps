FROM maven:3.9.0-eclipse-temurin-17 AS build

WORKDIR /app

COPY pom.xml .

RUN mvn dependency:go-offline

COPY src /app/src

RUN mvn clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

COPY --from=build /app/target/imagegenerator-0.0.1-SNAPSHOT.jar /app/imagegenerator.jar

ENV SQS_QUEUE_URL=https://sqs.eu-west-1.amazonaws.com/160885256027/image-processing-queue

ENTRYPOINT ["java", "-jar", "/app/imagegenerator.jar"]