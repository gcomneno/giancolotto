.PHONY: build up down

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

run:
	docker-compose exec giancolotto python main.py
