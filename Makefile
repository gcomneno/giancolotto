.PHONY: build up down run

build:
	docker-compose build

up:	build
	docker-compose up -d

down:
	docker-compose down

run: up
	docker-compose exec giancolotto python /app/src/main.py
