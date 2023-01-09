e=.env

up:
	docker-compose $(f) --env-file $(e) up -d $(c)