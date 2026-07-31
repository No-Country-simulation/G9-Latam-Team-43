# API pública (Spring Boot) en dos etapas: construcción con Maven y ejecución
# con un JRE liviano.
FROM maven:3.9-eclipse-temurin-21 AS construccion
WORKDIR /app
COPY pom.xml .
RUN mvn -q dependency:go-offline
COPY src/ src/
RUN mvn -q -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=construccion /app/target/tecnoteca-api-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
