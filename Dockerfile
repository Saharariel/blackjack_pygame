# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

RUN pip install pygbag

COPY . .

RUN pygbag --build main.py

# Final stage: serve using nginx
FROM nginx:alpine

COPY --from=builder /app/build/web /usr/share/nginx/html

EXPOSE 80

