.PHONY: build up down

build:
	sudo docker-compose build

up:
	sudo docker-compose up -d

down:
	sudo docker-compose down

run:
	sudo docker-compose exec giancolotto python ./src/main.py
