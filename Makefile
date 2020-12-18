
up:
	docker-compose up flask-dev

init:
	docker-compose run --rm manage run flask db init

migrate:
	docker-compose run --rm manage run flask db migrate

upgrade:
	docker-compose run --rm manage run flask db upgrade 