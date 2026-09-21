FROM cirrusci/flutter:stable AS build
WORKDIR /app
COPY . .
RUN flutter pub get
RUN flutter build apk --release

FROM alpine:latest
COPY --from=build /app/build/app/outputs/flutter-apk/app-release.apk /app.apk
